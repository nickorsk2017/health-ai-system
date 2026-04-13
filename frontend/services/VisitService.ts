const BASE = `${process.env.NEXT_PUBLIC_API_URL}/visits`;
const HISTORY_BASE = `${process.env.NEXT_PUBLIC_API_URL}/history`;

export class VisitService {
  static async recordVisit(data: Entity.CreateVisit): Promise<Entity.RecordVisitResponse> {
    const res = await fetch(BASE, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error(`VisitService.recordVisit failed: ${res.status}`);
    return res.json();
  }

  static async fetchHistory(userId: string, lastDateVisit: string): Promise<Entity.VisitRecord[]> {
    const url = `${HISTORY_BASE}/${userId}?last_date_visit=${lastDateVisit}`;
    const res = await fetch(url);
    if (!res.ok) throw new Error(`VisitService.fetchHistory failed: ${res.status}`);
    return res.json();
  }
}
