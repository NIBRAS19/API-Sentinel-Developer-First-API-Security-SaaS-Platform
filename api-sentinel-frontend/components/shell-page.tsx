'use client';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from './auth-provider';
import { AppShell } from './app-shell';
export function ShellPage({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();
  const router = useRouter();
  useEffect(()=>{ if(!loading && !user) router.replace('/login'); }, [loading,user,router]);
  if (loading || !user) return <div className="grid min-h-screen place-items-center bg-[var(--bg)]"><div className="mono text-xs text-slate-500">initializing security workspace…</div></div>;
  return <AppShell>{children}</AppShell>;
}
