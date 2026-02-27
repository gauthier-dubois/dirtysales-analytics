import { fetchEnergyTelemetry } from "@/lib/api";
import type { EnergyTelemetryDto } from "@/lib/types";
import { useEffect, useState } from "react";

export default function EnergyPage() {
  const [loading, setLoading] = useState<boolean>(false);
  const [data, setData] = useState<EnergyTelemetryDto[]>([]);
  const [data2, setData2] = useState<EnergyTelemetryDto[]>([]);
  const [days, setDays] = useState<number>(7);
  const [intervalMinutes, setIntervalMinutes] = useState<number>(15);
  const [sites, setSites] = useState<number>(4);
  const [metersPerSite, setMeterPerSite] = useState<number>(6);
  const [seed, setSeed] = useState<number>(42);

  const load = () => {
    setLoading(true);
    fetchEnergyTelemetry({
      days,
      intervalMinutes,
      sites,
      metersPerSite,
      seed,
    })
      .then((rows) => {
        console.log(rows);
        setData2(rows);
      })
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    load();
  }, []);

  console.log(data);

  return <div>Energie page</div>;
}
