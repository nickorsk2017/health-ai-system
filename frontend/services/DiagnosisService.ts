const BASE = `${process.env.NEXT_PUBLIC_API_URL}/diagnosis`;

export class DiagnosisService {
  static async fetchDiagnosis(
    userId: string,
    startDate: string,
  ): Promise<Entity.GPConsultation> {
    const url = `${BASE}/${userId}?start_date=${startDate}`;
    const res = await fetch(url);
    if (!res.ok) throw new Error(`DiagnosisService.fetchDiagnosis failed: ${res.status}`);
    return res.json();
  }
}
