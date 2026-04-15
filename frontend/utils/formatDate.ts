import dayjs from "dayjs";

import utc from "dayjs/plugin/utc";
import timezone from "dayjs/plugin/timezone";

dayjs.extend(utc);
dayjs.extend(timezone);

export default function formatDate(iso: string, format = "YYYY-MM-DD HH:mm"): string {
  if (!iso) return "";
  const parsed = dayjs(iso);
  if (!parsed.isValid()) return "";
  return parsed.local().format(format);
}
