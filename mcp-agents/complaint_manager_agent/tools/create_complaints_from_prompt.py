import uuid
from datetime import datetime, timedelta, timezone

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from loguru import logger
from pydantic import BaseModel, Field
from sqlalchemy import insert, select

from config import settings
from db.engine import SessionLocal
from db.models import Complaint, COMPLAINT_STATUS_UNREAD
from schemas.complaint import ComplaintRecord, CreateComplaintsByPromptRequest

_SYSTEM_PROMPT = """\
Today is {today_iso} ({today_weekday}).

Parse the following patient-submitted text into individual health complaint entries.

Rules:
1. Extract each distinct health concern as a separate entry.
2. Resolve ALL relative date references using today's date:
   - "today" / "this morning" → {today_date}
   - "yesterday" → {yesterday}
   - "last <weekday>" → the most recent occurrence of that weekday before today
   - "X days/weeks ago" → subtract accordingly from today
3. If no date is mentioned for a complaint, default date_public to today: {today_date}T00:00:00Z
4. Multiple symptoms on the same date must be separate entries — do not merge them.
5. Format date_public as ISO 8601 UTC datetime (e.g. "2026-04-20T00:00:00+00:00").
6. Only extract what is explicitly stated. Do not invent or embellish.
"""


class _ParsedComplaint(BaseModel):
    problem_health: str = Field(description="Clear description of the health concern.")
    date_public: str = Field(description="ISO 8601 UTC datetime when patient noticed/reported it.")


class _ParsedComplaintList(BaseModel):
    complaints: list[_ParsedComplaint] = Field(
        description="All extracted complaint entries from the text."
    )


def _parse_date(raw: str) -> datetime:
    raw = raw.strip()
    if not raw:
        return datetime.now(timezone.utc)
    for fmt in (raw, f"{raw}T00:00:00"):
        try:
            parsed = datetime.fromisoformat(fmt)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            else:
                parsed = parsed.astimezone(timezone.utc)
            return min(parsed, datetime.now(timezone.utc))
        except ValueError:
            continue
    return datetime.now(timezone.utc)


def _build_system_prompt() -> str:
    now = datetime.now(timezone.utc)
    return _SYSTEM_PROMPT.format(
        today_iso=now.isoformat(),
        today_weekday=now.strftime("%A"),
        today_date=now.date().isoformat(),
        yesterday=(now - timedelta(days=1)).date().isoformat(),
    )


def _to_record(row: Complaint) -> ComplaintRecord:
    return ComplaintRecord(
        complaint_id=str(row.id),
        user_id=row.user_id,
        problem_health=row.problem_health,
        date_public=row.date_public.isoformat(),
        status=row.status,
        created_at=row.created_at.isoformat(),
    )


async def create_complaints_by_prompt(
    data: CreateComplaintsByPromptRequest,
) -> list[ComplaintRecord]:
    logger.info(f"Parsing complaint prompt for user={data.user_id}, chars={len(data.prompt)}")

    llm = ChatOpenAI(model=settings.openai_model, api_key=settings.openai_api_key, temperature=0.0)
    parsed: _ParsedComplaintList = await llm.with_structured_output(_ParsedComplaintList).ainvoke(
        [
            SystemMessage(content=_build_system_prompt()),
            HumanMessage(content=data.prompt),
        ]
    )

    if not parsed.complaints:
        logger.warning(f"LLM returned no complaints for user={data.user_id}")
        return []

    logger.info(f"LLM extracted {len(parsed.complaints)} complaint(s)")

    created: list[ComplaintRecord] = []
    async with SessionLocal() as session:
        for item in parsed.complaints:
            complaint_id = uuid.uuid4()
            date_public = _parse_date(item.date_public)
            await session.execute(
                insert(Complaint).values(
                    id=complaint_id,
                    user_id=data.user_id,
                    problem_health=item.problem_health.strip(),
                    date_public=date_public,
                    status=COMPLAINT_STATUS_UNREAD,
                )
            )
            result = await session.execute(
                select(Complaint).where(Complaint.id == complaint_id)
            )
            created.append(_to_record(result.scalar_one()))
        await session.commit()

    logger.info(f"Created {len(created)} complaint(s) for user={data.user_id}")
    return created
