const BASE = `${process.env.NEXT_PUBLIC_API_URL}/devices`;

export class DeviceService {
  static async getByUser(userId: string): Promise<Entity.Device[]> {
    const res = await fetch(`${BASE}/${userId}`, { cache: "no-store" });
    if (!res.ok) throw new Error(`DeviceService.getByUser failed: ${res.status}`);
    return res.json();
  }

  static async add(userId: string, form: Entity.AddDeviceForm): Promise<Entity.AddDeviceResponse> {
    const res = await fetch(BASE, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: userId,
        type_device: form.type_device,
        diagnosis_mock: form.diagnosis_mock || null,
      }),
    });
    if (!res.ok) throw new Error(`DeviceService.add failed: ${res.status}`);
    return res.json();
  }

  static async remove(deviceId: string): Promise<void> {
    const res = await fetch(`${BASE}/${deviceId}`, { method: "DELETE" });
    if (!res.ok) throw new Error(`DeviceService.remove failed: ${res.status}`);
  }
}
