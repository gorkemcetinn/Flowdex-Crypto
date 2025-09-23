'use client';

import { useEffect, useState } from 'react';

import { getApiBaseUrl } from '../lib/config';

type Status = 'loading' | 'online' | 'offline';

const statusStyles: Record<Status, { container: string; dot: string; label: string }> = {
  loading: {
    container: 'bg-slate-800/70 text-slate-200',
    dot: 'bg-slate-400',
    label: 'Checking API'
  },
  online: {
    container: 'bg-emerald-500/15 text-emerald-300',
    dot: 'bg-emerald-400',
    label: 'API Online'
  },
  offline: {
    container: 'bg-rose-500/15 text-rose-300',
    dot: 'bg-rose-400',
    label: 'API Offline'
  }
};

export default function ApiStatus() {
  const [status, setStatus] = useState<Status>('loading');
  const [message, setMessage] = useState('');

  useEffect(() => {
    const controller = new AbortController();
    async function pingApi() {
      try {
        const response = await fetch(`${getApiBaseUrl()}/health`, {
          cache: 'no-store',
          signal: controller.signal
        });
        if (!response.ok) {
          throw new Error('Health check failed');
        }
        const data = (await response.json()) as { status?: string };
        setStatus('online');
        setMessage(data.status ?? 'ok');
      } catch (error) {
        if ((error as Error).name === 'AbortError') {
          return;
        }
        setStatus('offline');
        setMessage('unreachable');
      }
    }

    void pingApi();
    return () => controller.abort();
  }, []);

  const styles = statusStyles[status];

  return (
    <div
      className={`inline-flex items-center gap-2 rounded-full px-3 py-1 text-sm font-medium transition-colors ${styles.container}`}
    >
      <span className={`h-2.5 w-2.5 rounded-full ${styles.dot}`} aria-hidden />
      <span>{styles.label}</span>
      {message && status !== 'loading' ? (
        <span className="text-xs uppercase tracking-wide text-slate-400">{message}</span>
      ) : null}
    </div>
  );
}
