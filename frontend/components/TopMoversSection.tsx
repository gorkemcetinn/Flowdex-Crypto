import type { MarketMove, TopMoversPayload } from '../lib/api';
import { formatCompactNumber, formatCurrency, formatPercent } from '../lib/format';

interface MoversListProps {
  title: string;
  items: MarketMove[];
  positive: boolean;
}

function MoversList({ title, items, positive }: MoversListProps) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/50 p-5">
      <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-400">{title}</h3>
      <ul className="mt-4 space-y-4">
        {items.map((item) => (
          <li key={item.symbol} className="flex items-center justify-between gap-4">
            <div>
              <p className="text-xs uppercase tracking-wide text-slate-500">{item.symbol}</p>
              <p className="text-base font-medium text-slate-100">{item.name}</p>
            </div>
            <div className="text-right">
              <p className="text-sm text-slate-300">{formatCurrency(item.price)}</p>
              <p className={`text-sm font-semibold ${positive ? 'text-emerald-400' : 'text-rose-400'}`}>
                {formatPercent(item.percent_change_24h)}
              </p>
              <p className="text-xs text-slate-500">Vol: {formatCompactNumber(item.volume_24h)}</p>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default function TopMoversSection({ gainers, losers }: TopMoversPayload) {
  if (!gainers.length && !losers.length) {
    return null;
  }

  return (
    <section className="rounded-3xl border border-slate-800 bg-slate-950/40 p-6">
      <div className="flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
        <div>
          <h2 className="text-2xl font-semibold text-slate-50">Top Movers</h2>
          <p className="text-sm text-slate-400">24 saatlik performansta öne çıkan varlıklar.</p>
        </div>
      </div>

      <div className="mt-6 grid gap-4 md:grid-cols-2">
        <MoversList title="Gainers" items={gainers} positive />
        <MoversList title="Losers" items={losers} positive={false} />
      </div>
    </section>
  );
}
