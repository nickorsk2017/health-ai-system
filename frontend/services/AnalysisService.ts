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

  static async importFromPrompt(data: Entity.AnalysisByPromptRequest): Promise<Entity.AnalysisByPromptResponse> {
    const res = await fetch(`${BASE}/by-prompt`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error(`AnalysisService.importFromPrompt failed: ${res.status}`);
    return res.json();
  }

  static async updateAnalysis(analysisId: string, data: Entity.UpdateAnalysis): Promise<Entity.MutateAnalysisResponse> {
    const res = await fetch(`${BASE}/${analysisId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error(`AnalysisService.updateAnalysis failed: ${res.status}`);
    return res.json();
  }

  static async deleteAnalysis(analysisId: string): Promise<Entity.MutateAnalysisResponse> {
    const res = await fetch(`${BASE}/${analysisId}`, { method: "DELETE" });
    if (!res.ok) throw new Error(`AnalysisService.deleteAnalysis failed: ${res.status}`);
    return res.json();
  }
}
