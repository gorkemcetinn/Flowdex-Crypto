'use client';

import { useEffect, useMemo, useState } from 'react';

import type { StreamEvent, WatchlistAsset } from '../lib/api';
import { getApiBaseUrl } from '../lib/config';
import { formatCurrency, formatPercent } from '../lib/format';
import Sparkline from './Sparkline';

interface WatchlistStreamProps {
  initialQuotes: WatchlistAsset[];
  symbols: string[];
}

export default function WatchlistStream({ initialQuotes, symbols }: WatchlistStreamProps) {
  const [quotes, setQuotes] = useState(initialQuotes);
  const [isStreaming, setIsStreaming] = useState(false);

  const normalizedSymbols = useMemo(
    () => symbols.map((symbol) => symbol.toUpperCase()),
    [symbols]
  );

  useEffect(() => {
    setQuotes(initialQuotes);
  }, [initialQuotes]);

  useEffect(() => {
    if (!normalizedSymbols.length) {
      setIsStreaming(false);
      return;
    }

    const params = new URLSearchParams({
      symbols: normalizedSymbols.join(','),
      max_events: '30',
      delay: '0.2'
    });
    const url = `${getApiBaseUrl()}/markets/stream?${params.toString()}`;
    const source = new EventSource(url);
    setIsStreaming(true);

    source.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data) as StreamEvent;
        if (!payload.quotes?.length) {
          return;
        }

        const updates = new Map(payload.quotes.map((quote) => [quote.symbol, quote]));
        setQuotes((current) => {
          if (!current.length) {
            return current;
          }
          return current.map((entry) => {
            const update = updates.get(entry.symbol);
            if (!update) {
              return entry;
            }
            return {
              ...entry,
              price: update.price,
              percent_change_24h: update.percent_change_24h
            };
          });
        });
      } catch (error) {
        console.error('Failed to parse watchlist stream payload', error);
      }
    };

    source.onerror = () => {
      setIsStreaming(false);
      source.close();
    };

    return () => {
      setIsStreaming(false);
      source.close();
    };
  }, [normalizedSymbols]);

  if (!quotes.length) {
    return (
      <div className="rounded-2xl border border-dashed border-slate-800 p-6 text-sm text-slate-400">
        Watchlist boş. API üzerinden sembol ekleyerek canlı yayını başlatabilirsiniz.
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between text-xs uppercase tracking-wide text-slate-500">
        <span>Gerçek zamanlı SSE</span>
        <span className={`flex items-center gap-2 font-semibold ${isStreaming ? 'text-emerald-400' : 'text-slate-500'}`}>
          <span className={`h-2 w-2 rounded-full ${isStreaming ? 'bg-emerald-400 animate-pulse' : 'bg-slate-600'}`} />
          {isStreaming ? 'canlı' : 'beklemede'}
        </span>
      </div>

      <ul className="space-y-4">
        {quotes.map((quote) => {
          const positive = quote.percent_change_24h >= 0;
          return (
            <li
              key={quote.symbol}
              className="rounded-2xl border border-slate-800/70 bg-slate-950/40 p-4 shadow-sm shadow-slate-950/20"
            >
              <div className="flex items-start justify-between gap-4">
                <div>
                  <p className="text-xs uppercase tracking-wide text-slate-500">{quote.symbol}</p>
                  <p className="text-sm font-medium text-slate-200">{quote.name}</p>
                </div>
                <div className="text-right">
                  <p className="text-lg font-semibold text-slate-50">{formatCurrency(quote.price)}</p>
                  <p className={`text-sm font-semibold ${positive ? 'text-emerald-400' : 'text-rose-400'}`}>
                    {formatPercent(quote.percent_change_24h)}
                  </p>
                </div>
              </div>
              <Sparkline values={quote.sparkline} positive={positive} className="mt-3 h-12" />
            </li>
          );
        })}
      </ul>
    </div>
  );
}
