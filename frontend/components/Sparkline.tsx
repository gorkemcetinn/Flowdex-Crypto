'use client';

interface SparklineProps {
  values: number[];
  positive?: boolean;
  className?: string;
}

function buildPaths(values: number[], width: number, height: number): { line: string; area: string } {
  const min = Math.min(...values);
  const max = Math.max(...values);
  const range = max - min || 1;
  const points = values.map((value, index) => {
    const x = (index / (values.length - 1)) * width;
    const y = height - ((value - min) / range) * height;
    return [x, y] as const;
  });

  const line = points
    .map(([x, y], index) => `${index === 0 ? 'M' : 'L'}${x.toFixed(2)},${y.toFixed(2)}`)
    .join(' ');
  const [lastX] = points[points.length - 1];
  const area = `${line} L${lastX.toFixed(2)},${height} L0,${height} Z`;
  return { line, area };
}

export default function Sparkline({ values, positive = true, className }: SparklineProps) {
  if (!values || values.length < 2) {
    return null;
  }

  const width = 140;
  const height = 44;
  const { line, area } = buildPaths(values, width, height);
  const stroke = positive ? '#34d399' : '#f87171';
  const fill = positive ? 'rgba(52, 211, 153, 0.16)' : 'rgba(248, 113, 113, 0.16)';
  const classes = ['w-full'];
  if (className) {
    classes.push(className);
  }

  return (
    <svg
      viewBox={`0 0 ${width} ${height}`}
      className={classes.join(' ')}
      aria-hidden="true"
      role="presentation"
    >
      <path d={area} fill={fill} />
      <path d={line} fill="none" stroke={stroke} strokeWidth={2} />
    </svg>
  );
}
