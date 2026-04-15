import uuid
from datetime import datetime, timezone

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from loguru import logger
from pydantic import BaseModel, Field
from sqlalchemy import insert

from config import settings
from db.engine import SessionLocal
from db.models import PatientAnalysis as PatientAnalysisRow
from schemas.http import CreateAnalysesFromPromptRequest, CreateAnalysesFromPromptResponse

_SYSTEM_PROMPT = (
    "Today is {today}. Parse the following text into individual laboratory analysis entries.\n"
    "For each distinct lab test event extract:\n"
    "  - analysis_text: the full lab result content (biomarkers, values, units, reference ranges).\n"
    "  - analysis_date: ISO 8601 UTC datetime when the test was performed.\n"
    "Rules:\n"
    "  - If the date cannot be determined, set analysis_date to an empty string.\n"
    "  - If meaningful lab text cannot be extracted, set analysis_text to an empty string.\n"
    "  - One entry per distinct test date. Multiple tests on the same date belong to one entry.\n"
    "  - Do not invent or guess values — only extract what is explicitly stated.\n"
)


class _ParsedAnalysis(BaseModel):
    analysis_text: str = Field(
        default="",
        description="Full text of lab results for this entry. Empty string if not present.",
    )
    analysis_date: str = Field(
        default="",
        description="ISO 8601 UTC datetime when the test was performed. Empty string if unknown.",
    )


class _ParsedAnalysisList(BaseModel):
    analyses: list[_ParsedAnalysis] = Field(
        description="All extracted lab result entries from the text."
    )


def _parse_date(raw: str) -> datetime | None:
    raw = raw.strip()
    if not raw:
        return None
    try:
        parsed = datetime.fromisoformat(raw)
    except ValueError:
        try:
            parsed = datetime.fromisoformat(f"{raw}T00:00:00")
        except ValueError:
            return None
    try:
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        else:
            parsed = parsed.astimezone(timezone.utc)
        return min(parsed, datetime.now(timezone.utc))
    except ValueError:
        return None


async def create_analyses_from_prompt(
    data: CreateAnalysesFromPromptRequest,
) -> CreateAnalysesFromPromptResponse:
    logger.info(f"Parsing lab prompt for user={data.user_id}, chars={len(data.prompt)}")

    llm = ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        temperature=0.0,
    )
    structured_llm = llm.with_structured_output(_ParsedAnalysisList)
    parsed: _ParsedAnalysisList = await structured_llm.ainvoke(
        [
            SystemMessage(content=_SYSTEM_PROMPT.format(today=datetime.now(timezone.utc).isoformat())),
            HumanMessage(content=data.prompt),
        ]
    )

    if not parsed.analyses:
        logger.warning(f"LLM returned no analyses for user={data.user_id}")
        return CreateAnalysesFromPromptResponse(success=True, list_missing_analysis=[])

    logger.info(f"LLM extracted {len(parsed.analyses)} analysis entry/entries")

    missing: list[str] = []

    async with SessionLocal() as session:
        for item in parsed.analyses:
            analysis_text = item.analysis_text.strip() or None
            analysis_date = _parse_date(item.analysis_date)

            if analysis_text is None or analysis_date is None:
                label = (item.analysis_text or item.analysis_date or "unknown entry").strip()
                missing.append(label[:80])

            await session.execute(
                insert(PatientAnalysisRow).values(
                    id=uuid.uuid4(),
                    user_id=data.user_id,
                    analysis_text=analysis_text,
                    analysis_date=analysis_date,
                )
            )
        await session.commit()

    logger.info(
        f"Saved {len(parsed.analyses)} analysis record(s) for user={data.user_id}, "
        f"{len(missing)} incomplete"
    )
    return CreateAnalysesFromPromptResponse(
        success=True,
        list_missing_analysis=missing,
    )
