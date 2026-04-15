import dayjs from "dayjs";

const BASE = `${process.env.NEXT_PUBLIC_API_URL}/analyses`;

export class AnalysisService {
  static async recordAnalysis(data: Entity.CreateAnalysis): Promise<Entity.RecordAnalysisResponse> {
    const payload = {
      ...data,
      analysis_date: dayjs(data.analysis_date).toISOString(),
    };
    const res = await fetch(BASE, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error(`AnalysisService.recordAnalysis failed: ${res.status}`);
    return res.json();
  }

  static async fetchAnalyses(userId: string, startDate: string): Promise<Entity.AnalysisRecord[]> {
    const normalizedDate = encodeURIComponent(dayjs(startDate).toISOString());
    const url = `${BASE}/${userId}?start_date=${normalizedDate}`;
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
    const payload = {
      ...data,
      analysis_date: data.analysis_date ? dayjs(data.analysis_date).toISOString() : null,
    };
    const res = await fetch(`${BASE}/${analysisId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
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
