'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Icon } from './icons';
import { Button } from './ui';
import { useAuth } from './auth-provider';
import { useState } from 'react';

const main = [
  ['/app', 'Overview', Icon.grid],
  ['/app/projects', 'Projects', Icon.folder],
  ['/app/apis', 'APIs', Icon.terminal],
  ['/app/scans', 'Scans', Icon.scan],
  ['/app/findings', 'Findings', Icon.bug],
  ['/app/reports', 'Reports', Icon.file],
] as const;
const org = [
  ['/app/team', 'Team', Icon.users],
  ['/app/audit-log', 'Audit log', Icon.activity],
  ['/app/settings', 'Settings', Icon.settings],
] as const;

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const [mobile, setMobile] = useState(false);
  const { user, logout } = useAuth();
  const nav = (items: typeof main) => items.map(([href,label,IconComp]) => {
    const active = pathname === href || (href !== '/app' && pathname.startsWith(href));
    return <Link key={href} href={href} onClick={()=>setMobile(false)} className={`group flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm transition ${active ? 'bg-cyan-400/[.08] text-cyan-100' : 'text-slate-400 hover:bg-white/[.03] hover:text-white'}`}>
      <span className={active ? 'text-cyan-300' : 'text-slate-500 group-hover:text-slate-300'}>{IconComp({size:16})}</span>{label}
      {active && <span className="ml-auto size-1.5 rounded-full bg-cyan-300 shadow-[0_0_10px_rgba(73,185,255,.55)]" />}
    </Link>;
  });
  return <div className="min-h-screen bg-[var(--bg)] text-white">
    <div className="fixed inset-0 -z-10 app-grid opacity-40" />
    <div className="fixed left-[18%] top-[-10%] -z-10 size-[28rem] rounded-full bg-cyan-400/[.05] blur-3xl" />
    <header className="fixed inset-x-0 top-0 z-40 h-16 border-b border-white/[.06] bg-[#070a0f]/90 px-4 backdrop-blur-xl lg:pl-[278px]">
      <div className="flex h-full items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <button onClick={()=>setMobile(v=>!v)} className="grid size-9 place-items-center rounded-xl border border-white/10 bg-white/[.03] lg:hidden"><Icon.menu /></button>
          <div className="hidden items-center gap-2 rounded-xl border border-white/[.06] bg-white/[.025] px-3 py-2 sm:flex"><Icon.search size={15}/><span className="text-xs text-slate-500">Search projects, endpoints, findings...</span><kbd className="ml-8 rounded border border-white/10 px-1.5 py-0.5 text-[10px] text-slate-500">⌘ K</kbd></div>
        </div>
        <div className="flex items-center gap-2">
          <div className="hidden items-center gap-2 rounded-full border border-emerald-400/15 bg-emerald-400/[.05] px-3 py-1.5 text-[10px] font-semibold uppercase tracking-[.16em] text-emerald-200 md:flex"><span className="status-dot"/> System operational</div>
          <button className="grid size-9 place-items-center rounded-xl border border-white/10 bg-white/[.025] text-slate-400 hover:text-white"><Icon.bell size={16}/></button>
          <div className="flex items-center gap-2 rounded-xl border border-white/10 bg-white/[.025] px-2 py-1.5"><span className="grid size-7 place-items-center rounded-lg bg-cyan-400/[.12] text-xs font-bold text-cyan-200">{(user?.first_name?.[0] || 'N').toUpperCase()}</span><span className="hidden max-w-28 truncate text-xs text-slate-300 sm:block">{user?.email || 'demo@sentinel.local'}</span></div>
        </div>
      </div>
    </header>

    <aside className="fixed inset-y-0 left-0 z-50 hidden w-[254px] border-r border-white/[.06] bg-[#070a0f]/95 px-3 py-4 backdrop-blur-xl lg:block">
      <Brand />
      <div className="mt-8 px-2"><div className="mono text-[10px] uppercase tracking-[.18em] text-slate-600">Workspace</div><div className="mt-2 rounded-xl border border-white/[.07] bg-white/[.025] px-3 py-2.5"><div className="text-sm font-semibold">Sentinel Labs</div><div className="mt-0.5 text-[11px] text-slate-500">Security workspace</div></div></div>
      <nav className="mt-7 space-y-1">{nav(main)}</nav>
      <div className="my-6 h-px bg-white/[.06]" />
      <div className="px-2 pb-2 text-[10px] uppercase tracking-[.18em] text-slate-600">Organization</div>
      <nav className="space-y-1">{nav(org)}</nav>
      <div className="absolute inset-x-3 bottom-4 rounded-2xl border border-white/[.07] bg-white/[.025] p-3">
        <div className="flex items-center gap-2"><div className="grid size-8 place-items-center rounded-lg border border-cyan-400/10 bg-cyan-400/[.05] text-cyan-200"><Icon.shield size={15}/></div><div><div className="text-xs font-semibold">API Sentinel</div><div className="mono text-[10px] text-slate-600">v0.1.0</div></div></div>
      </div>
    </aside>

    {mobile && <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm lg:hidden" onClick={()=>setMobile(false)}><aside className="h-full w-[280px] border-r border-white/[.06] bg-[#080b11] px-3 py-4" onClick={e=>e.stopPropagation()}><Brand/>{<nav className="mt-8 space-y-1">{nav(main)}{nav(org)}</nav>}<button className="mt-6 w-full text-left text-xs text-slate-500" onClick={logout}>Sign out</button></aside></div>}

    <main className="min-h-screen pt-16 lg:pl-[254px]">
      <div className="mx-auto max-w-[1540px] p-4 sm:p-6 xl:p-8">{children}</div>
    </main>
  </div>;
}

function Brand() { return <Link href="/app" className="flex items-center gap-3 px-2"><span className="grid size-10 place-items-center rounded-xl border border-cyan-400/15 bg-cyan-400/[.06] text-cyan-200"><Icon.shield size={20}/></span><div><div className="text-sm font-semibold tracking-tight">API Sentinel</div><div className="mono text-[10px] uppercase tracking-[.16em] text-slate-600">security platform</div></div></Link>; }
