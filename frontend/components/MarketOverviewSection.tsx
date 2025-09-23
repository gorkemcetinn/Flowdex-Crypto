import Sparkline from './Sparkline';
import type { MarketAssetSnapshot } from '../lib/api';
import { formatCompactNumber, formatCurrency, formatPercent } from '../lib/format';

interface MarketOverviewSectionProps {
  assets: MarketAssetSnapshot[];
}

export default function MarketOverviewSection({ assets }: MarketOverviewSectionProps) {
  if (!assets.length) {
    return null;
  }

  return (
    <section className="rounded-3xl border border-slate-800 bg-slate-900/40 p-6 shadow-xl shadow-slate-950/30">
      <div className="flex flex-col gap-2 md:flex-row md:items-end md:justify-between">
        <div className="space-y-1">
          <h2 className="text-2xl font-semibold text-slate-50">Canlı Market Özeti</h2>
          <p className="text-sm text-slate-400">
            Piyasanın en yoğun takip edilen varlıkları için fiyat, hacim ve trendleri anlık olarak izleyin.
          </p>
        </div>
        <span className="text-xs uppercase tracking-wide text-slate-500">Veri kaynağı: Demo statik set</span>
      </div>

      <div className="mt-6 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {assets.map((asset) => {
          const positiveDay = asset.percent_change_24h >= 0;
          const positiveWeek = asset.percent_change_7d >= 0;
          return (
            <article
              key={asset.symbol}
              className="flex flex-col gap-4 rounded-2xl border border-slate-800/80 bg-slate-900/60 p-5 transition-colors hover:border-slate-700/80"
            >
              <div className="flex items-start justify-between gap-2">
                <div>
                  <p className="text-xs uppercase tracking-wide text-slate-500">{asset.symbol}</p>
                  <h3 className="text-lg font-semibold text-slate-100">{asset.name}</h3>
                </div>
                <div className="text-right">
                  <p className="text-xl font-semibold text-slate-50">{formatCurrency(asset.price)}</p>
                  <p className={`text-sm font-medium ${positiveDay ? 'text-emerald-400' : 'text-rose-400'}`}>
                    {formatPercent(asset.percent_change_24h)} <span className="text-xs text-slate-400">24s</span>
                  </p>
                </div>
              </div>

              <Sparkline values={asset.sparkline} positive={positiveDay} className="h-16" />

              <dl className="grid grid-cols-3 gap-3 text-xs text-slate-400">
                <div className="space-y-1">
                  <dt>7g değişim</dt>
                  <dd className={`font-medium ${positiveWeek ? 'text-emerald-300' : 'text-rose-300'}`}>
                    {formatPercent(asset.percent_change_7d)}
                  </dd>
                </div>
                <div className="space-y-1">
                  <dt>24s hacim</dt>
                  <dd className="font-medium text-slate-100">{formatCompactNumber(asset.volume_24h)}</dd>
                </div>
                <div className="space-y-1">
                  <dt>Market cap</dt>
                  <dd className="font-medium text-slate-100">{formatCompactNumber(asset.market_cap)}</dd>
                </div>
              </dl>
            </article>
          );
        })}
      </div>
    </section>
  );
}
