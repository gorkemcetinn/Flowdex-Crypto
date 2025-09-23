import Sparkline from './Sparkline';
import type { MarketAssetDetail } from '../lib/api';
import { formatCompactNumber, formatCurrency, formatPercent } from '../lib/format';

interface AssetDetailCardProps {
  asset: MarketAssetDetail;
}

export default function AssetDetailCard({ asset }: AssetDetailCardProps) {
  const positive = asset.percent_change_24h >= 0;

  return (
    <section className="flex h-full flex-col gap-4 rounded-3xl border border-slate-800 bg-slate-900/60 p-6">
      <header className="flex items-start justify-between gap-4">
        <div>
          <p className="text-xs uppercase tracking-wide text-slate-500">Odak Varlık</p>
          <h2 className="text-2xl font-semibold text-slate-50">
            {asset.name} <span className="text-sm font-normal text-slate-400">({asset.symbol})</span>
          </h2>
        </div>
        <div className="text-right">
          <p className="text-3xl font-semibold text-slate-50">{formatCurrency(asset.price)}</p>
          <p className={`text-sm font-semibold ${positive ? 'text-emerald-400' : 'text-rose-400'}`}>
            {formatPercent(asset.percent_change_24h)}
          </p>
        </div>
      </header>

      <Sparkline values={asset.sparkline} positive={positive} className="h-16" />

      <dl className="grid grid-cols-2 gap-4 text-sm text-slate-300">
        <div>
          <dt className="text-xs uppercase tracking-wide text-slate-500">24s Yüksek</dt>
          <dd className="font-medium text-slate-100">{formatCurrency(asset.high_24h)}</dd>
        </div>
        <div>
          <dt className="text-xs uppercase tracking-wide text-slate-500">24s Düşük</dt>
          <dd className="font-medium text-slate-100">{formatCurrency(asset.low_24h)}</dd>
        </div>
        <div>
          <dt className="text-xs uppercase tracking-wide text-slate-500">Market Cap</dt>
          <dd className="font-medium text-slate-100">{formatCompactNumber(asset.market_cap)}</dd>
        </div>
        <div>
          <dt className="text-xs uppercase tracking-wide text-slate-500">24s Hacim</dt>
          <dd className="font-medium text-slate-100">{formatCompactNumber(asset.volume_24h)}</dd>
        </div>
      </dl>

      <p className="text-sm leading-relaxed text-slate-300">{asset.description}</p>
    </section>
  );
}
