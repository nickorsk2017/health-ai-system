import asyncio
from pathlib import Path

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from loguru import logger

from config import settings
from schemas.consilium import SpecialistAnalysis, SpecialistFinding

SPECIALTIES = [
    "oncology",
    "gastroenterology",
    "cardiology",
    "hematology",
    "nephrology",
    "nutrition",
    "endocrinology",
    "mental_health",
    "pulmonology",
]

_PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def _load_prompt(specialty: str) -> str:
    return (_PROMPTS_DIR / f"{specialty}.md").read_text(encoding="utf-8")


def _format_history(records: list[dict]) -> str:
    if not records:
        return "No patient history available."

    lines: list[str] = ["## Patient SOAP History\n"]
    for record in records:
        visit_date = record.get("history_date", "unknown date")
        lines.append(f"### Visit — {visit_date} | Specialty: {record.get('doctor_type', 'unknown')}")
        lines.append(f"**Subjective:** {record.get('subjective', '')}")
        lines.append(f"**Objective:** {record.get('objective', '')}")
        lines.append(f"**Assessment:** {record.get('assessment', '')}")
        if record.get("plan"):
            lines.append(f"**Plan:** {record['plan']}")
        lines.append("")
    return "\n".join(lines)


def _format_labs(records: list[dict]) -> str:
    if not records:
        return "No laboratory data available."

    lines: list[str] = ["## Laboratory Results\n"]
    for record in records:
        lab_date = record.get("analysis_date", "unknown date")
        lines.append(f"### Lab Result — {lab_date}")
        lines.append(record.get("analysis_text", ""))
        lines.append("")
    return "\n".join(lines)


class ConsiliumService:
    def __init__(self) -> None:
        self._llm = ChatOpenAI(
            model=settings.openai_model,
            api_key=settings.openai_api_key,
            temperature=0.3,
        )

    async def _analyze_specialty(
        self, specialty: str, patient_context: str
    ) -> SpecialistFinding | None:
        logger.info(f"[{specialty}] Sending patient context to LLM...")
        structured_llm = self._llm.with_structured_output(SpecialistAnalysis)

        analysis: SpecialistAnalysis = await structured_llm.ainvoke(
            [
                SystemMessage(content=_load_prompt(specialty)),
                HumanMessage(content=patient_context),
            ]
        )

        if not analysis.is_relevant:
            logger.info(f"[{specialty}] No relevant findings — excluded from consilium.")
            return None

        logger.info(f"[{specialty}] Findings recorded.")
        return SpecialistFinding(
            specialty=specialty,
            risks=analysis.risks,
            treatment=analysis.treatment,
            prognosis=analysis.prognosis,
            probable_diagnosis=analysis.probable_diagnosis,
        )

    async def run(
        self, history_records: list[dict], lab_records: list[dict]
    ) -> list[SpecialistFinding]:
        if not history_records and not lab_records:
            raise ValueError("No patient data provided for consilium.")

        patient_context = _format_history(history_records) + "\n\n" + _format_labs(lab_records)
        logger.info(f"Launching parallel consilium across {len(SPECIALTIES)} specialties...")

        tasks = [self._analyze_specialty(s, patient_context) for s in SPECIALTIES]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        findings: list[SpecialistFinding] = []
        for specialty, result in zip(SPECIALTIES, results):
            if isinstance(result, Exception):
                logger.error(f"[{specialty}] LLM call failed: {result}")
            elif result is not None:
                findings.append(result)

        logger.info(
            f"Consilium complete: {len(findings)}/{len(SPECIALTIES)} specialties provided findings."
        )
        return findings
