from datetime import date, timedelta

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from loguru import logger

from config import settings
from prompts.biometrics_generation import SYSTEM_PROMPT, diagnosis_system_prompt, user_prompt
from schemas.biometrics import DailyBiometrics
from schemas.http import GetDailyBiometricsResponse


def _date_range(start: date, end: date) -> list[str]:
    total_days = (end - start).days + 1
    return [(start + timedelta(days=i)).isoformat() for i in range(total_days)]


async def get_daily_oura_biometrics(
    date_str: str, user_id: str, diagnosis_mock: str | None = None
) -> list[DailyBiometrics]:
    try:
        start_date = date.fromisoformat(date_str)
        today = date.today()

        if start_date > today:
            raise ValueError(f"start date {date_str} is in the future")

        dates = _date_range(start_date, today)
        system_prompt = diagnosis_system_prompt(diagnosis_mock) if diagnosis_mock else SYSTEM_PROMPT

        llm = ChatOpenAI(model=settings.openai_model, api_key=settings.openai_api_key)
        structured_llm = llm.with_structured_output(GetDailyBiometricsResponse)

        response: GetDailyBiometricsResponse = await structured_llm.ainvoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt(user_id, dates, diagnosis_mock)),
        ])

        return response.records
    except Exception as e:
        logger.exception(f"Error in get_daily_oura_biometrics: {e}")
        raise
