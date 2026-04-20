import dayjs from "dayjs";

const BASE = `${process.env.NEXT_PUBLIC_API_URL}/complaints`;

export class ComplaintService {
  static async getAll(userId: string): Promise<Entity.Complaint[]> {
    const res = await fetch(`${BASE}?user_id=${encodeURIComponent(userId)}`, { cache: "no-store" });
    if (!res.ok) throw new Error(`ComplaintService.getAll failed: ${res.status}`);
    return res.json();
  }

  static async create(userId: string, form: Entity.CreateComplaint): Promise<Entity.Complaint> {
    const payload = {
      user_id: userId,
      ...form,
      date_public: dayjs(form.date_public).toISOString(),
    };
    const res = await fetch(BASE, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error(`ComplaintService.create failed: ${res.status}`);
    return res.json();
  }

  static async createByPrompt(data: Entity.ComplaintByPromptRequest): Promise<Entity.Complaint[]> {
    const res = await fetch(`${BASE}/by-prompt`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error(`ComplaintService.createByPrompt failed: ${res.status}`);
    return res.json();
  }

  static async update(
    complaintId: string,
    userId: string,
    form: Entity.UpdateComplaint,
  ): Promise<Entity.Complaint> {
    const payload = {
      user_id: userId,
      ...form,
      date_public: dayjs(form.date_public).toISOString(),
    };
    const res = await fetch(`${BASE}/${complaintId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error(`ComplaintService.update failed: ${res.status}`);
    return res.json();
  }

  static async markRead(complaintId: string): Promise<void> {
    const res = await fetch(`${BASE}/${complaintId}/read`, { method: "PATCH" });
    if (!res.ok) throw new Error(`ComplaintService.markRead failed: ${res.status}`);
  }

  static async remove(complaintId: string): Promise<void> {
    const res = await fetch(`${BASE}/${complaintId}`, { method: "DELETE" });
    if (!res.ok) throw new Error(`ComplaintService.remove failed: ${res.status}`);
  }
}
