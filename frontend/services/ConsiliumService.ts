const BASE = `${process.env.NEXT_PUBLIC_API_URL}/consilium`;

export class ConsiliumService {
  static async fetchConsilium(
    userId: string,
    startDate: string,
  ): Promise<Entity.SpecialistFinding[]> {
    const url = `${BASE}/${userId}?start_date=${startDate}`;
    const res = await fetch(url);
    if (!res.ok) throw new Error(`ConsiliumService.fetchConsilium failed: ${res.status}`);
    return res.json();
  }
}
