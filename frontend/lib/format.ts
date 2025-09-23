const compactFormatter = new Intl.NumberFormat('en-US', {
  notation: 'compact',
  maximumFractionDigits: 1
});

export function formatCurrency(value: number): string {
  const abs = Math.abs(value);
  const maximumFractionDigits = abs >= 100 ? 2 : abs >= 1 ? 3 : 4;
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: abs >= 1 ? 2 : 2,
    maximumFractionDigits
  }).format(value);
}

export function formatPercent(value: number): string {
  const maximumFractionDigits = Math.abs(value) >= 10 ? 1 : 2;
  const formatted = value.toFixed(maximumFractionDigits);
  return `${value >= 0 ? '+' : ''}${formatted}%`;
}

export function formatCompactNumber(value: number): string {
  return compactFormatter.format(value);
}
