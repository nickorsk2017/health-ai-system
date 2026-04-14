SYSTEM_PROMPT = """Role: Synthetic Apple Watch/HealthKit generator (Series 9+).
Sleep (5–9.5h total): Deep (8–20%), Core (45–60%), REM (20–30%), Awake (0.1–0.8h). Efficiency: 78–96%.
Movement: Steps (2.5k–22k). Active kcal: Steps × 0.045–0.065. Resting kcal: 1.4k–2.2k. Exercise: 0–120m. Stand: 6–16h.
Vitals: HRV (SDNN: 15–110ms), Resting HR (44–80 BPM), Resp Rate (12–20 br/min).
Recovery: Score (30–98), VO2 Max (28–58), Body Battery (20–100%).
Logic: VO2 Max/Resting Energy are stable (±0.3/±30). HRV/Recovery inversely correlate with RHR. Exercise scales with Active kcal. Weekend variance applied. No physiological overflows.
"""


def diagnosis_system_prompt(diagnosis: str) -> str:
    return f"""Role: Synthetic Apple Watch/HealthKit generator (Series 9+) for a patient with {diagnosis}.

Generate data that reflects the physiological impact of {diagnosis} on Apple Health metrics.
Override healthy baselines with the condition-specific patterns below:

GENERAL BOUNDS
Sleep (3–9.5h): Deep (5–20%), Core (30–60%), REM (5–30%), Awake (0.1–3h). Efficiency: 45–96%.
Movement: Steps (500–15k). Active kcal: steps × 0.045–0.065. Resting kcal: 1.2k–2.4k. Exercise: 0–90m. Stand: 4–16h.
Vitals: HRV (SDNN: 8–110ms), Resting HR (44–160 BPM), Resp Rate (10–28 br/min).
Recovery: Score (10–98), VO2 Max (20–58), Body Battery (5–100%).

CONDITION-SPECIFIC OVERRIDES FOR {diagnosis.upper()}
Apply the known physiological markers of {diagnosis}:
- Pheochromocytoma → episodic Resting HR spikes (120–160 BPM), HRV 8–25ms,
  sleep efficiency 45–70%, elevated resp rate (18–28), low recovery score (10–40),
  body battery < 30 on crisis days.
- Include 1–2 paroxysmal/crisis days per week with dramatically abnormal values.
- Maintain inter-day continuity except during simulated episodes.
- No physiological overflows (REM cannot exceed total sleep, etc.).
"""


def user_prompt(user_id: str, dates: list[str], diagnosis_mock: str | None = None) -> str:
    condition_note = f" The patient has {diagnosis_mock}." if diagnosis_mock else ""
    return (
        f"Generate synthetic Apple HealthKit daily metrics for user '{user_id}'{condition_note} "
        f"for the following dates: {dates}.\n"
        "Return a JSON object with a single key 'records' containing an array of daily entries. "
        "Each entry must match the DailyHealthMetrics schema exactly."
    )
