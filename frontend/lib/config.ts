const DEFAULT_API_BASE_URL = 'http://localhost:8000/api';

function normalizeBaseUrl(value: string): string {
  return value.replace(/\/$/, '');
}

export function getApiBaseUrl(): string {
  const envValue = process.env.NEXT_PUBLIC_API_BASE_URL?.trim();
  if (envValue) {
    return normalizeBaseUrl(envValue);
  }

  return DEFAULT_API_BASE_URL;
}
