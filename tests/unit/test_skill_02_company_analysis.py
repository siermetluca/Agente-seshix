import unittest

from agente_seshix.application.skill_02_company_analysis import (
    AnalysisCategory,
    CompanyAnalysisPort,
    CompanyAnalysisStatus,
    CompanyAnalysisValidationError,
    RawAnalysisFinding,
    RawCompanyAnalysisOutput,
    RawContextChangeCandidate,
    Skill02CompanyAnalysisRuntime,
)
from agente_seshix.domain.context_evidence import (
    ContextValue,
    EvidenceClassification,
    Provenance,
)
from agente_seshix.domain.primary_context import (
    PrimaryContextRecord,
    PrimaryContextVersion,
)


class FakeAnalysisProvider:
    def __init__(self, output):
        self.output = output
        self.requests = []

    def analyze(self, request):
        self.requests.append(request)
        return self.output


def fact(value, version="1"):
    return ContextValue(
        value=value,
        classification=EvidenceClassification.FATTO,
        provenance=(Provenance("human://owner", "EV-1"),),
        version=version,
    )


def hypothesis(value, version="1"):
    return ContextValue(
        value=value,
        classification=EvidenceClassification.IPOTESI,
        provenance=(Provenance("analysis://prior"),),
        version=version,
    )


def unknown(version="1"):
    return ContextValue(
        value=None,
        classification=EvidenceClassification.UNKNOWN,
        provenance=(),
        version=version,
    )


def context(*records):
    return PrimaryContextVersion(
        version_id="PCV-1",
        records=tuple(records),
        previous_version_id="PCV-0",
    )


class Skill02CompanyAnalysisTests(unittest.TestCase):
    def test_fake_provider_satisfies_port(self):
        provider = FakeAnalysisProvider(RawCompanyAnalysisOutput(findings=()))
        self.assertIsInstance(provider, CompanyAnalysisPort)

    def test_grounded_findings_create_analysis_baseline(self):
        primary = context(
            PrimaryContextRecord("R1", "company.activities", fact(["impianti elettrici"])),
            PrimaryContextRecord("R2", "company.employees", fact(6)),
        )
        provider = FakeAnalysisProvider(
            RawCompanyAnalysisOutput(
                findings=(
                    RawAnalysisFinding(
                        "F-1",
                        "CAPABILITY",
                        "L'azienda opera negli impianti elettrici.",
                        ("company.activities",),
                    ),
                )
            )
        )

        result = Skill02CompanyAnalysisRuntime(provider).analyze(
            analysis_id="A-1",
            primary_context=primary,
        )

        self.assertEqual(result.baseline.status, CompanyAnalysisStatus.ANALYZED)
        self.assertEqual(len(result.baseline.findings), 1)
        self.assertEqual(
            result.baseline.findings[0].category,
            AnalysisCategory.CAPABILITY,
        )
        self.assertEqual(result.baseline.primary_context_version_id, "PCV-1")
        self.assertEqual(
            result.derived_state.dependencies[0].version_ref,
            "PCV-1",
        )
    def test_unsupported_basis_key_is_rejected(self):
        primary = context(
            PrimaryContextRecord("R1", "company.activities", fact(["impianti elettrici"]))
        )
        provider = FakeAnalysisProvider(
            RawCompanyAnalysisOutput(
                findings=(
                    RawAnalysisFinding(
                        "F-1",
                        "CRITICITA",
                        "Problema inventato.",
                        ("company.revenue",),
                    ),
                )
            )
        )

        with self.assertRaises(CompanyAnalysisValidationError):
            Skill02CompanyAnalysisRuntime(provider).analyze(
                analysis_id="A-2",
                primary_context=primary,
            )

    def test_unknown_context_cannot_support_finding(self):
        primary = context(
            PrimaryContextRecord("R1", "company.revenue", unknown())
        )
        provider = FakeAnalysisProvider(
            RawCompanyAnalysisOutput(
                findings=(
                    RawAnalysisFinding(
                        "F-1",
                        "RISK",
                        "Il fatturato è insufficiente.",
                        ("company.revenue",),
                    ),
                )
            )
        )

        with self.assertRaises(CompanyAnalysisValidationError):
            Skill02CompanyAnalysisRuntime(provider).analyze(
                analysis_id="A-3",
                primary_context=primary,
            )

    def test_hypothesis_context_can_only_support_hypothesis_finding(self):
        primary = context(
            PrimaryContextRecord(
                "R1",
                "company.staffing_need",
                hypothesis("potrebbe servire personale"),
            )
        )
        invalid_provider = FakeAnalysisProvider(
            RawCompanyAnalysisOutput(
                findings=(
                    RawAnalysisFinding(
                        "F-1",
                        "GAP",
                        "Manca personale.",
                        ("company.staffing_need",),
                    ),
                )
            )
        )
        with self.assertRaises(CompanyAnalysisValidationError):
            Skill02CompanyAnalysisRuntime(invalid_provider).analyze(
                analysis_id="A-4",
                primary_context=primary,
            )

        valid_provider = FakeAnalysisProvider(
            RawCompanyAnalysisOutput(
                findings=(
                    RawAnalysisFinding(
                        "F-2",
                        "HYPOTHESIS",
                        "Potrebbe esistere un fabbisogno di personale da verificare.",
                        ("company.staffing_need",),
                    ),
                )
            )
        )
        result = Skill02CompanyAnalysisRuntime(valid_provider).analyze(
            analysis_id="A-5",
            primary_context=primary,
        )
        self.assertEqual(
            result.baseline.findings[0].category,
            AnalysisCategory.HYPOTHESIS,
        )
    def test_neutral_fact_cannot_support_direct_negative_finding(self):
        primary = context(
            PrimaryContextRecord("R1", "company.employees", fact(6))
        )
        provider = FakeAnalysisProvider(
            RawCompanyAnalysisOutput(
                findings=(
                    RawAnalysisFinding(
                        "F-NEG",
                        "CRITICITA",
                        "Sei dipendenti sono insufficienti.",
                        ("company.employees",),
                    ),
                )
            )
        )
        with self.assertRaises(CompanyAnalysisValidationError):
            Skill02CompanyAnalysisRuntime(provider).analyze(
                analysis_id="A-NEG",
                primary_context=primary,
            )

    def test_neutral_fact_may_support_hypothesis_not_direct_problem(self):
        primary = context(
            PrimaryContextRecord("R1", "company.employees", fact(6))
        )
        provider = FakeAnalysisProvider(
            RawCompanyAnalysisOutput(
                findings=(
                    RawAnalysisFinding(
                        "F-HYP",
                        "HYPOTHESIS",
                        "La capacità della squadra potrebbe richiedere verifica rispetto al carico.",
                        ("company.employees",),
                        ("C-WORKLOAD",),
                    ),
                ),
                context_change_candidates=(
                    RawContextChangeCandidate(
                        "C-WORKLOAD",
                        "carico operativo e numero di commesse simultanee",
                        "Serve per verificare la relazione tra organico e carico.",
                        None,
                    ),
                ),
            )
        )
        result = Skill02CompanyAnalysisRuntime(provider).analyze(
            analysis_id="A-HYP",
            primary_context=primary,
        )
        self.assertEqual(
            result.baseline.findings[0].category,
            AnalysisCategory.HYPOTHESIS,
        )
        self.assertEqual(
            result.baseline.status,
            CompanyAnalysisStatus.PARTIAL_NEEDS_CONTEXT,
        )
        self.assertEqual(
            result.baseline.findings[0].verification_candidate_ids,
            ("C-WORKLOAD",),
        )

    def test_explicit_negative_signal_key_can_support_direct_risk(self):
        primary = context(
            PrimaryContextRecord(
                "R1",
                "company.constraints.capacity_risk",
                fact("capacità dichiarata insufficiente nei picchi"),
            )
        )
        provider = FakeAnalysisProvider(
            RawCompanyAnalysisOutput(
                findings=(
                    RawAnalysisFinding(
                        "F-RISK",
                        "RISK",
                        "Esiste un rischio di capacità nei picchi.",
                        ("company.constraints.capacity_risk",),
                    ),
                )
            )
        )
        result = Skill02CompanyAnalysisRuntime(provider).analyze(
            analysis_id="A-RISK",
            primary_context=primary,
        )
        self.assertEqual(result.baseline.findings[0].category, AnalysisCategory.RISK)

    def test_admin_staff_fact_cannot_be_promoted_to_asset(self):
        primary = context(
            PrimaryContextRecord("R1", "company.admin_staff", fact(1))
        )
        provider = FakeAnalysisProvider(
            RawCompanyAnalysisOutput(
                findings=(
                    RawAnalysisFinding(
                        "F-ASSET",
                        "ASSET",
                        "Una persona amministrativa rende la gestione efficiente.",
                        ("company.admin_staff",),
                    ),
                )
            )
        )
        with self.assertRaises(CompanyAnalysisValidationError):
            Skill02CompanyAnalysisRuntime(provider).analyze(
                analysis_id="A-ASSET",
                primary_context=primary,
            )

    def test_direct_capability_statement_is_rebound_to_context_value(self):
        primary = context(
            PrimaryContextRecord(
                "R1",
                "company.activities",
                fact(["impianti elettrici e tecnologici"]),
            )
        )
        provider = FakeAnalysisProvider(
            RawCompanyAnalysisOutput(
                findings=(
                    RawAnalysisFinding(
                        "F-CAP",
                        "CAPABILITY",
                        "Testo espanso dal provider.",
                        ("company.activities",),
                    ),
                )
            )
        )
        result = Skill02CompanyAnalysisRuntime(provider).analyze(
            analysis_id="A-CAP",
            primary_context=primary,
        )
        self.assertEqual(
            result.baseline.findings[0].statement,
            "Capacità interna dichiarata: "
            "company.activities=['impianti elettrici e tecnologici']",
        )

    def test_missing_information_becomes_context_change_candidate(self):
        primary = context(
            PrimaryContextRecord("R1", "company.activities", fact(["impianti elettrici"]))
        )
        provider = FakeAnalysisProvider(
            RawCompanyAnalysisOutput(
                findings=(
                    RawAnalysisFinding(
                        "F-1",
                        "CAPABILITY",
                        "L'attività tecnica dichiarata è una capability operativa.",
                        ("company.activities",),
                    ),
                ),
                context_change_candidates=(
                    RawContextChangeCandidate(
                        "C-1",
                        "numero e ruoli delle persone operative",
                        "Serve per valutare capacità e carico operativo.",
                        "company.employees",
                    ),
                ),
            )
        )

        result = Skill02CompanyAnalysisRuntime(provider).analyze(
            analysis_id="A-6",
            primary_context=primary,
        )

        self.assertEqual(
            result.baseline.status,
            CompanyAnalysisStatus.PARTIAL_NEEDS_CONTEXT,
        )
        candidate = result.baseline.context_change_candidates[0]
        self.assertEqual(candidate.source_skill, "SKILL_02")
        self.assertEqual(candidate.requested_key, "company.employees")
        self.assertEqual(primary.records[0].key, "company.activities")

    def test_context_candidate_cannot_request_already_known_fact(self):
        primary = context(
            PrimaryContextRecord("R1", "company.employees", fact(6))
        )
        provider = FakeAnalysisProvider(
            RawCompanyAnalysisOutput(
                findings=(),
                context_change_candidates=(
                    RawContextChangeCandidate(
                        "C-1",
                        "numero dipendenti",
                        "Serve per l'analisi.",
                        "company.employees",
                    ),
                ),
            )
        )

        with self.assertRaises(CompanyAnalysisValidationError):
            Skill02CompanyAnalysisRuntime(provider).analyze(
                analysis_id="A-7",
                primary_context=primary,
            )

    def test_context_candidate_can_target_existing_unknown(self):
        primary = context(
            PrimaryContextRecord("R1", "company.revenue", unknown())
        )
        provider = FakeAnalysisProvider(
            RawCompanyAnalysisOutput(
                findings=(),
                context_change_candidates=(
                    RawContextChangeCandidate(
                        "C-1",
                        "fatturato aziendale",
                        "Serve per valutare la sostenibilità economica.",
                        "company.revenue",
                    ),
                ),
            )
        )
        result = Skill02CompanyAnalysisRuntime(provider).analyze(
            analysis_id="A-8",
            primary_context=primary,
        )
        self.assertEqual(result.baseline.status, CompanyAnalysisStatus.NEEDS_CONTEXT)
    def test_empty_primary_context_needs_context_without_calling_provider(self):
        primary = PrimaryContextVersion("PCV-EMPTY", ())
        provider = FakeAnalysisProvider(
            RawCompanyAnalysisOutput(
                findings=(
                    RawAnalysisFinding(
                        "SHOULD-NOT-RUN",
                        "ASSET",
                        "Invented.",
                        ("x",),
                    ),
                )
            )
        )

        result = Skill02CompanyAnalysisRuntime(provider).analyze(
            analysis_id="A-EMPTY",
            primary_context=primary,
        )

        self.assertEqual(result.baseline.status, CompanyAnalysisStatus.NEEDS_CONTEXT)
        self.assertEqual(provider.requests, [])
        self.assertEqual(result.baseline.findings, ())
        self.assertEqual(
            result.derived_state.dependencies[0].version_ref,
            "PCV-EMPTY",
        )

    def test_duplicate_finding_ids_are_rejected(self):
        primary = context(
            PrimaryContextRecord("R1", "company.activities", fact(["impianti elettrici"]))
        )
        provider = FakeAnalysisProvider(
            RawCompanyAnalysisOutput(
                findings=(
                    RawAnalysisFinding("F-1", "CAPABILITY", "A", ("company.activities",)),
                    RawAnalysisFinding("F-1", "CAPABILITY", "B", ("company.activities",)),
                )
            )
        )
        with self.assertRaises(CompanyAnalysisValidationError):
            Skill02CompanyAnalysisRuntime(provider).analyze(
                analysis_id="A-DUP",
                primary_context=primary,
            )

    def test_hypothesis_from_fact_without_verification_candidate_is_rejected(self):
        primary = context(
            PrimaryContextRecord("R1", "company.employees", fact(6))
        )
        provider = FakeAnalysisProvider(
            RawCompanyAnalysisOutput(
                findings=(
                    RawAnalysisFinding(
                        "F-HYP-NO-CANDIDATE",
                        "HYPOTHESIS",
                        "Potrebbe esserci un limite di capacità.",
                        ("company.employees",),
                    ),
                )
            )
        )
        with self.assertRaises(CompanyAnalysisValidationError):
            Skill02CompanyAnalysisRuntime(provider).analyze(
                analysis_id="A-HYP-NO-CANDIDATE",
                primary_context=primary,
            )

    def test_runtime_has_no_primary_context_repository_write_dependency(self):
        provider = FakeAnalysisProvider(RawCompanyAnalysisOutput(findings=()))
        runtime = Skill02CompanyAnalysisRuntime(provider)
        self.assertFalse(hasattr(runtime, "save"))
        self.assertFalse(hasattr(runtime, "_context_repository"))


if __name__ == "__main__":
    unittest.main()
