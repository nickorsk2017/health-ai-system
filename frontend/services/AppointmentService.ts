import dayjs from "dayjs";

const BASE = `${process.env.NEXT_PUBLIC_API_URL}/appointments`;

export class AppointmentService {
  static async getAll(userId: string): Promise<Entity.Appointment[]> {
    const url = userId ? `${BASE}?user_id=${encodeURIComponent(userId)}` : BASE;
    const res = await fetch(url, { cache: "no-store" });
    if (!res.ok) throw new Error(`AppointmentService.getAll failed: ${res.status}`);
    return res.json();
  }

  static async create(form: Entity.CreateAppointment): Promise<Entity.Appointment> {
    const payload = {
      ...form,
      appointment_date: dayjs(form.appointment_date).toISOString(),
    };
    const res = await fetch(BASE, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error(`AppointmentService.create failed: ${res.status}`);
    return res.json();
  }
}
