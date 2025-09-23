import ApiStatus from '../components/ApiStatus';
import { getApiBaseUrl } from '../lib/config';

const phaseZeroFocus = [
  {
    title: 'FastAPI çekirdeği',
    description:
      'Kimliksiz temel API sözleşmeleri, watchlist ve kullanıcı tercihleri için CRUD uç noktaları.'
  },
  {
    title: 'PostgreSQL şeması',
    description:
      'Kullanıcılar, favoriler ve ayarlar için temel tablolar; Docker Compose ile hızlı başlatma.'
  },
  {
    title: 'Next.js iskeleti',
    description:
      'Gelecek dashboard ekranları için Tailwind destekli frontend başlangıç noktası.'
  }
];

export default function HomePage() {
  const apiBaseUrl = getApiBaseUrl();

  return (
    <div className="flex flex-col gap-12">
      <section className="flex flex-col gap-6">
        <ApiStatus />
        <div className="space-y-4">
          <h1 className="text-4xl font-semibold tracking-tight sm:text-5xl">Flowdex Crypto</h1>
          <p className="max-w-3xl text-lg text-slate-300">
            Faz 0 kapsamında backend ve frontend için temel altyapıyı kuruyoruz. Bu iskelet üzerinde
            gerçek zamanlı veri katmanlarını ve gelişmiş özellikleri hızlıca geliştirebileceğiz.
          </p>
        </div>
        <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 text-sm text-slate-300">
          <span className="font-semibold text-slate-100">API Base URL:</span>{' '}
          <code className="rounded bg-slate-800 px-2 py-1 text-slate-200">{apiBaseUrl}</code>
        </div>
      </section>

      <section className="grid gap-6 md:grid-cols-3">
        {phaseZeroFocus.map((item) => (
          <article
            key={item.title}
            className="flex flex-col gap-3 rounded-2xl border border-slate-800 bg-slate-900/40 p-5"
          >
            <h2 className="text-xl font-semibold text-slate-100">{item.title}</h2>
            <p className="text-sm leading-relaxed text-slate-300">{item.description}</p>
          </article>
        ))}
      </section>

      <section className="rounded-2xl border border-slate-800 bg-slate-900/40 p-6">
        <h3 className="text-lg font-semibold text-slate-100">Sonraki Adımlar</h3>
        <p className="mt-3 max-w-3xl text-sm leading-relaxed text-slate-300">
          Kafka tabanlı canlı fiyat akışı, Top Movers batch jobları ve kullanıcı tanımlı uyarı servisleri
          bir sonraki fazlarda bu iskeletin üzerine inşa edilecek. Bu repo, veri mühendisliği ve modern
          web geliştirme pratiklerini tek bir monorepo altında toplamak için hazır.
        </p>
      </section>
    </div>
  );
}
