import ApiStatus from '../components/ApiStatus';
import AssetDetailCard from '../components/AssetDetailCard';
import MarketOverviewSection from '../components/MarketOverviewSection';
import TopMoversSection from '../components/TopMoversSection';
import WatchlistPanel from '../components/WatchlistPanel';
import {
  ensureDemoUser,
  fetchAssetDetail,
  fetchMarketOverview,
  fetchTopMovers,
  fetchWatchlist,
  seedDemoWatchlist
} from '../lib/api';
import { getApiBaseUrl } from '../lib/config';

const DEMO_EMAIL = 'phase1-demo@flowdex.app';
const DEMO_WATCHLIST = ['BTC', 'ETH', 'SOL'] as const;

const phaseOneHighlights = [
  {
    title: 'Gerçek zamanlı watchlist',
    description:
      'Server Sent Events ile BTC, ETH ve SOL gibi favori semboller saniyeler içinde güncellenir. Faz 2’de gerçek borsa verisiyle beslemek için hazır.'
  },
  {
    title: 'Market panoraması',
    description:
      'Sparkline grafikler, 24 saat ve 7 gün performansı ile hacim/market cap özetleri tek gridde toplanır.'
  },
  {
    title: 'Top movers & odak varlık',
    description:
      'Gainers/losers listeleri ve detay kartı; uyarı sistemi ve bildirim kanallarına giden akış için temel KPI’ları sağlar.'
  }
];

export default async function HomePage() {
  const apiBaseUrl = getApiBaseUrl();
  const demoUser = await ensureDemoUser(DEMO_EMAIL);
  await seedDemoWatchlist(demoUser.id, DEMO_WATCHLIST);

  const [overview, topMovers, watchlist, btcDetail] = await Promise.all([
    fetchMarketOverview(),
    fetchTopMovers(),
    fetchWatchlist(demoUser.id),
    fetchAssetDetail('BTC')
  ]);

  const watchlistSymbols = watchlist.map((item) => item.symbol);

  return (
    <div className="flex flex-col gap-10">
      <section className="flex flex-col gap-6">
        <ApiStatus />
        <div className="space-y-4">
          <h1 className="text-4xl font-semibold tracking-tight sm:text-5xl">Faz 1 – Canlı Market Deneyimi</h1>
          <p className="max-w-3xl text-lg text-slate-300">
            Faz 0’daki altyapıyı artık kullanıcıya değer katan ekranlarla zenginleştiriyoruz. Statik demo veri seti
            üzerinden gerçek zamanlı watchlist akışı, market panoraması ve Top Movers bileşenleri sağlandı. Bu yapı,
            Faz 2’de Kafka ve gerçek borsa stream’lerine bağlanmak üzere tasarlandı.
          </p>
        </div>
        <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 text-sm text-slate-300">
          <span className="font-semibold text-slate-100">API Base URL:</span>{' '}
          <code className="rounded bg-slate-800 px-2 py-1 text-slate-200">{apiBaseUrl}</code>
        </div>
      </section>

      <section className="grid gap-6 md:grid-cols-3">
        {phaseOneHighlights.map((item) => (
          <article
            key={item.title}
            className="flex flex-col gap-3 rounded-2xl border border-slate-800 bg-slate-900/40 p-5"
          >
            <h2 className="text-xl font-semibold text-slate-100">{item.title}</h2>
            <p className="text-sm leading-relaxed text-slate-300">{item.description}</p>
          </article>
        ))}
      </section>

      <MarketOverviewSection assets={overview} />

      <div className="grid gap-6 lg:grid-cols-[1.4fr_1fr]">
        <WatchlistPanel initialQuotes={watchlist} symbols={watchlistSymbols} />
        <AssetDetailCard asset={btcDetail} />
      </div>

      <TopMoversSection gainers={topMovers.gainers} losers={topMovers.losers} />
    </div>
  );
}
