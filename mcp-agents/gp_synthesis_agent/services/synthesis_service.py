from pathlib import Path

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from loguru import logger

from config import settings
from schemas.consultation import GPConsultation

_PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "gp_synthesis.md"


def _load_system_prompt() -> str:
    return _PROMPT_PATH.read_text(encoding="utf-8")


def _format_consilium_findings(findings: list[dict]) -> str:
    lines: list[str] = [f"## Consilium Report — {len(findings)} Specialist Finding(s)\n"]
    for i, finding in enumerate(findings, start=1):
        specialty = finding.get("specialty", "unknown").replace("_", " ").title()
        lines.append(f"### [{i}] {specialty}")
        lines.append(f"**Probable Diagnosis:** {finding.get('probable_diagnosis', 'N/A')}")
        lines.append(f"**Risks:** {finding.get('risks', 'N/A')}")
        lines.append(f"**Recommended Treatment:** {finding.get('treatment', 'N/A')}")
        lines.append(f"**Prognosis:** {finding.get('prognosis', 'N/A')}")
        lines.append("")
    return "\n".join(lines)


def _format_history(records: list[dict]) -> str:
    if not records:
        return "## Patient SOAP History\nNot Provided\n"
    lines: list[str] = [f"## Patient SOAP History — {len(records)} Record(s)\n"]
    for i, r in enumerate(records, start=1):
        lines.append(
            f"### [{i}] {r.get('doctor_type', 'Unknown')} — {r.get('history_date', 'N/A')}"
        )
        lines.append(f"**Chief Complaint:** {r.get('chief_complaint', 'N/A')}")
        lines.append(f"**Subjective:** {r.get('subjective', 'N/A')}")
        lines.append(f"**Objective:** {r.get('objective', 'N/A')}")
        lines.append(f"**Assessment:** {r.get('assessment', 'N/A')}")
        lines.append(f"**Plan:** {r.get('plan', 'N/A')}")
        lines.append("")
    return "\n".join(lines)


def _format_labs(records: list[dict]) -> str:
    if not records:
        return "## Laboratory Results\nNot Provided\n"
    lines: list[str] = [f"## Laboratory Results — {len(records)} Record(s)\n"]
    for i, r in enumerate(records, start=1):
        lines.append(f"### [{i}] {r.get('test_name', 'Lab Test')} — {r.get('date', 'N/A')}")
        lines.append(r.get("analysis", str(r)))
        lines.append("")
    return "\n".join(lines)


def _format_devices(records: list[dict]) -> str:
    if not records:
        return "## Device & Wearable Data\nNot Provided\n"
    lines: list[str] = [f"## Device & Wearable Data — {len(records)} Device(s)\n"]
    for i, r in enumerate(records, start=1):
        lines.append(
            f"### [{i}] {r.get('device_name', 'Device')} (Type: {r.get('device_type', 'N/A')})"
        )
        lines.append(f"**Last Sync:** {r.get('last_sync', 'N/A')}")
        lines.append("")
    return "\n".join(lines)


def _format_complaints(records: list[dict]) -> str:
    if not records:
        return "## Patient Complaints\nNot Provided\n"
    lines: list[str] = [f"## Patient Complaints — {len(records)} Entry(ies)\n"]
    for i, r in enumerate(records, start=1):
        lines.append(f"### [{i}] {r.get('created_at', 'N/A')}")
        lines.append(r.get("complaint", str(r)))
        lines.append("")
    return "\n".join(lines)


class SynthesisService:
    def __init__(self) -> None:
        self._llm = ChatOpenAI(
            model=settings.openai_model,
            api_key=settings.openai_api_key,
            temperature=0.2,
        )

    async def synthesize(
        self,
        history_records: list[dict],
        lab_records: list[dict],
        device_records: list[dict],
        complaint_records: list[dict],
        consilium_findings: list[dict],
    ) -> GPConsultation:
        human_content = "\n\n".join([
            _format_consilium_findings(consilium_findings),
            _format_history(history_records),
            _format_labs(lab_records),
            _format_devices(device_records),
            _format_complaints(complaint_records),
        ])

        logger.info(
            f"Sending to GP synthesis LLM: {len(consilium_findings)} finding(s), "
            f"{len(history_records)} history record(s), {len(lab_records)} lab record(s), "
            f"{len(device_records)} device record(s), {len(complaint_records)} complaint(s)"
        )

        structured_llm = self._llm.with_structured_output(GPConsultation)
        consultation: GPConsultation = await structured_llm.ainvoke(
            [
                SystemMessage(content=_load_system_prompt()),
                HumanMessage(content=human_content),
            ]
        )

        logger.info("GP synthesis complete.")
        return consultation
