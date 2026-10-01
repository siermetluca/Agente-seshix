#!/usr/bin/env python3
from pathlib import Path
import json, re, subprocess, sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / "config/development/authority.yaml"
TRACE = ROOT / "schemas/development/traceability_record.schema.json"

SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
]
FORBIDDEN_FILES = {".env", "id_rsa", "id_ed25519"}

def fail(msg):
    print("FAIL", msg)
    raise SystemExit(1)

def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True).strip()

def check_authority():
    data = yaml.safe_load(AUTH.read_text())
    actions = data["actions"]
    if actions.get("direct_write_main") != "DENY":
        fail("direct_write_main must be DENY")
    for action in ("merge_pull_request", "create_release"):
        if "HITL" not in actions.get(action, ""):
            fail(f"{action} must require HITL")
    print("PASS B04/B06 authority + HITL policy")
def check_traceability():
    schema = json.loads(TRACE.read_text())
    required = set(schema.get("required", []))
    expected = {
        "dev_task_id", "dev_context_package_id", "change_plan_id",
        "implementation_ref", "test_result_ref", "review_result_ref",
        "architecture_audit_ref", "context_audit_ref", "release_gate_ref",
    }
    if required != expected:
        fail("traceability chain incomplete")
    print("PASS B05 traceability schema")

def scan_text(text, label):
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            fail(f"secret-like content in {label}")

def check_leakage():
    names = git("diff", "--cached", "--name-only").splitlines()
    for name in names:
        path = Path(name)
        if path.name in FORBIDDEN_FILES:
            fail(f"forbidden public file: {name}")
        full = ROOT / path
        if full.is_file():
            try:
                scan_text(full.read_text(errors="ignore"), name)
            except UnicodeDecodeError:
                pass
    print("PASS B07 deterministic leakage check")

def self_test():
    for bad in [
        "-----BEGIN " + "PRIVATE KEY-----",
        "gh" + "p_" + "A" * 30,
        "AK" + "IA" + "A" * 16,
    ]:
        try:
            for pattern in SECRET_PATTERNS:
                if pattern.search(bad):
                    break
            else:
                fail("leakage detector self-test missed fixture")
        except Exception as exc:
            fail(str(exc))
    print("PASS leakage detector self-test")
def main():
    branch = git("branch", "--show-current")
    if branch == "main":
        fail("bootstrap/development write attempted on main")
    check_authority()
    check_traceability()
    self_test()
    check_leakage()
    print("PASS BOOTSTRAP GOVERNANCE LOCAL ENFORCEMENT")
    print("INFO B02 remote main protection must be verified separately")

if __name__ == "__main__":
    main()
