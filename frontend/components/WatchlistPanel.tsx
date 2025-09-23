import WatchlistStream from './WatchlistStream';
import type { WatchlistAsset } from '../lib/api';

interface WatchlistPanelProps {
  initialQuotes: WatchlistAsset[];
  symbols: string[];
}

export default function WatchlistPanel({ initialQuotes, symbols }: WatchlistPanelProps) {
  return (
    <section className="rounded-3xl border border-slate-800 bg-slate-900/50 p-6">
      <header className="flex flex-col gap-2">
        <h2 className="text-2xl font-semibold text-slate-50">Watchlist</h2>
        <p className="text-sm text-slate-400">
          Kullanıcı watchlist&apos;i için SSE üzerinden akan anlık fiyat güncellemeleri.
        </p>
      </header>

      <div className="mt-6">
        <WatchlistStream initialQuotes={initialQuotes} symbols={symbols} />
      </div>
    </section>
  );
}
