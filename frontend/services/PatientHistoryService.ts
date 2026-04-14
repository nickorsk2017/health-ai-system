const BASE = `${process.env.NEXT_PUBLIC_API_URL}/patient-history`;

export class PatientHistoryService {
  static async recordHistory(data: Entity.CreatePatientHistory): Promise<Entity.RecordPatientHistoryResponse> {
    const res = await fetch(BASE, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error(`PatientHistoryService.recordHistory failed: ${res.status}`);
    return res.json();
  }

  static async fetchHistory(userId: string, lastHistoryDate: string): Promise<Entity.PatientHistoryRecord[]> {
    const url = `${BASE}/${userId}?last_history_date=${lastHistoryDate}`;
    const res = await fetch(url);
    if (!res.ok) throw new Error(`PatientHistoryService.fetchHistory failed: ${res.status}`);
    return res.json();
  }

  static async createByPrompt(data: Entity.HistoryFromPromptRequest): Promise<Entity.HistoryFromPromptResponse> {
    const res = await fetch(`${BASE}/by-prompt`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error(`PatientHistoryService.createByPrompt failed: ${res.status}`);
    return res.json();
  }

  static async updateHistory(historyId: string, data: Entity.UpdatePatientHistory): Promise<Entity.MutatePatientHistoryResponse> {
    const res = await fetch(`${BASE}/${historyId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error(`PatientHistoryService.updateHistory failed: ${res.status}`);
    return res.json();
  }

  static async deleteHistory(historyId: string): Promise<Entity.MutatePatientHistoryResponse> {
    const res = await fetch(`${BASE}/${historyId}`, { method: "DELETE" });
    if (!res.ok) throw new Error(`PatientHistoryService.deleteHistory failed: ${res.status}`);
    return res.json();
  }
}
