import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Flowdex Crypto',
  description: 'Realtime crypto watchlists and alerts.'
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-slate-950 text-slate-100">
        <main className="mx-auto flex min-h-screen max-w-5xl flex-col gap-8 px-6 py-10">
          {children}
        </main>
      </body>
    </html>
  );
}
