import { getApiBaseUrl } from './config';

export interface MarketAssetSnapshot {
  symbol: string;
  name: string;
  price: number;
  percent_change_24h: number;
  percent_change_7d: number;
  volume_24h: number;
  market_cap: number;
  sparkline: number[];
}

export interface MarketAssetDetail extends MarketAssetSnapshot {
  high_24h: number;
  low_24h: number;
  description: string;
}

export interface MarketMove {
  symbol: string;
  name: string;
  price: number;
  percent_change_24h: number;
  volume_24h: number;
}

export interface TopMoversPayload {
  gainers: MarketMove[];
  losers: MarketMove[];
}

export interface WatchlistAsset extends MarketAssetSnapshot {}

export interface StreamQuote {
  symbol: string;
  price: number;
  percent_change_24h: number;
}

export interface StreamEvent {
  type: string;
  quotes: StreamQuote[];
}

export interface UserPayload {
  id: string;
  email: string;
}

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const response = await fetch(`${getApiBaseUrl()}${path}`, {
    cache: 'no-store',
    ...init,
    headers: {
      Accept: 'application/json',
      ...(init.headers ?? {})
    }
  });

  if (!response.ok) {
    throw new Error(`API request to ${path} failed with ${response.status}`);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return (await response.json()) as T;
}

export async function ensureDemoUser(email = 'demo@flowdex.app'): Promise<UserPayload> {
  return request<UserPayload>('/users', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ email })
  });
}

export async function seedDemoWatchlist(userId: string, symbols: readonly string[]): Promise<void> {
  await Promise.all(
    symbols.map(async (symbol) => {
      const response = await fetch(`${getApiBaseUrl()}/watchlist/${userId}`, {
        method: 'POST',
        cache: 'no-store',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ symbol })
      });

      if (!response.ok) {
        throw new Error(`Failed to seed watchlist with ${symbol}`);
      }
    })
  );
}

export async function fetchMarketOverview(limit = 8): Promise<MarketAssetSnapshot[]> {
  return request<MarketAssetSnapshot[]>(`/markets/overview?limit=${limit}`);
}

export async function fetchTopMovers(limit = 4): Promise<TopMoversPayload> {
  return request<TopMoversPayload>(`/markets/top-movers?limit=${limit}`);
}

export async function fetchWatchlist(userId: string): Promise<WatchlistAsset[]> {
  return request<WatchlistAsset[]>(`/markets/watchlist/${userId}`);
}

export async function fetchAssetDetail(symbol: string): Promise<MarketAssetDetail> {
  return request<MarketAssetDetail>(`/markets/${encodeURIComponent(symbol)}`);
}
