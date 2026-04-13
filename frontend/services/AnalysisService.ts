const BASE = `${process.env.NEXT_PUBLIC_API_URL}/analyses`;

export class AnalysisService {
  static async recordAnalysis(data: Entity.CreateAnalysis): Promise<Entity.RecordAnalysisResponse> {
    const res = await fetch(BASE, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error(`AnalysisService.recordAnalysis failed: ${res.status}`);
    return res.json();
  }

  static async fetchAnalyses(userId: string, startDate: string): Promise<Entity.AnalysisRecord[]> {
    const url = `${BASE}/${userId}?start_date=${startDate}`;
    const res = await fetch(url);
    if (!res.ok) throw new Error(`AnalysisService.fetchAnalyses failed: ${res.status}`);
    return res.json();
  }
}
