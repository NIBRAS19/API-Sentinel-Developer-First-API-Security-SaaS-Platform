'use client';

import React from 'react';
import { Icon } from './icons';
import { Severity, FindingStatus, ScanStatus } from '@/lib/types';

export function Button({ children, variant = 'primary', className = '', type = 'button', onClick, disabled = false }: { children: React.ReactNode; variant?: 'primary'|'secondary'|'ghost'|'danger'; className?: string; type?: 'button'|'submit'; onClick?: () => void; disabled?: boolean }) {
  const base = 'inline-flex items-center justify-center gap-2 rounded-xl px-4 py-2.5 text-sm font-semibold transition disabled:cursor-not-allowed disabled:opacity-50';
  const variants = {
    primary: 'bg-cyan-400 text-slate-950 shadow-[0_0_25px_rgba(73,185,255,.16)] hover:bg-white',
    secondary: 'border border-white/10 bg-white/[.035] text-slate-200 hover:border-cyan-400/30 hover:bg-cyan-400/[.06]',
    ghost: 'text-slate-400 hover:bg-white/[.035] hover:text-white',
    danger: 'border border-red-400/20 bg-red-400/[.08] text-red-200 hover:bg-red-400/[.13]',
  };
  return <button type={type} onClick={onClick} disabled={disabled} className={`${base} ${variants[variant]} ${className}`}>{children}</button>;
}

export function Badge({ children, tone='neutral' }: { children: React.ReactNode; tone?: 'neutral'|'cyan'|'green'|'amber'|'red'|'critical' }) {
  const cls = { neutral:'border-white/10 bg-white/[.03] text-slate-300', cyan:'border-cyan-400/20 bg-cyan-400/[.07] text-cyan-200', green:'border-emerald-400/20 bg-emerald-400/[.07] text-emerald-200', amber:'border-amber-400/20 bg-amber-400/[.08] text-amber-200', red:'border-red-400/20 bg-red-400/[.08] text-red-200', critical:'border-rose-400/20 bg-rose-400/[.08] text-rose-200' };
  return <span className={`inline-flex items-center rounded-full border px-2.5 py-1 text-[11px] font-semibold ${cls[tone]}`}>{children}</span>;
}

export function severityTone(s: Severity) { return s === 'critical' ? 'critical' : s === 'high' ? 'red' : s === 'medium' ? 'amber' : s === 'low' ? 'cyan' : 'neutral'; }
export function statusTone(s: FindingStatus | ScanStatus) { return ['fixed','verified','closed','completed'].includes(s) ? 'green' : ['in_progress','running'].includes(s) ? 'cyan' : ['failed','false_positive'].includes(s) ? 'red' : ['triaged','queued'].includes(s) ? 'amber' : 'neutral'; }

export function KpiCard({ label, value, detail, icon = Icon.activity, tone='cyan' }: { label:string; value:string|number; detail?:string; icon?: (p?: any) => React.ReactNode; tone?:'cyan'|'green'|'amber'|'red' }) {
  const colors = { cyan:'text-cyan-200 bg-cyan-400/[.08] border-cyan-400/15', green:'text-emerald-200 bg-emerald-400/[.08] border-emerald-400/15', amber:'text-amber-200 bg-amber-400/[.08] border-amber-400/15', red:'text-rose-200 bg-rose-400/[.08] border-rose-400/15' };
  return <div className="card card-hover p-5">
    <div className="flex items-center justify-between"><span className={`grid size-10 place-items-center rounded-xl border ${colors[tone]}`}>{icon({size:17})}</span><span className="text-xs text-slate-500">{detail}</span></div>
    <div className="mt-5 text-3xl font-semibold tracking-tight">{value}</div>
    <div className="mt-1 text-sm text-slate-500">{label}</div>
  </div>;
}

export function PageHeader({ eyebrow, title, description, actions }: { eyebrow?: string; title: string; description?: string; actions?: React.ReactNode }) {
  return <div className="mb-8 flex flex-col justify-between gap-5 lg:flex-row lg:items-end">
    <div>
      {eyebrow && <div className="mono mb-2 text-[11px] uppercase tracking-[.24em] text-cyan-300/70">{eyebrow}</div>}
      <h1 className="text-3xl font-semibold tracking-tight text-white sm:text-4xl">{title}</h1>
      {description && <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-400">{description}</p>}
    </div>
    {actions && <div className="flex flex-wrap gap-2">{actions}</div>}
  </div>;
}

export function EmptyState({ title, description, action }: { title: string; description: string; action?: React.ReactNode }) {
  return <div className="card p-12 text-center"><div className="mx-auto grid size-12 place-items-center rounded-2xl border border-cyan-400/15 bg-cyan-400/[.06] text-cyan-200"><Icon.shield /></div><h3 className="mt-5 text-lg font-semibold text-white">{title}</h3><p className="mx-auto mt-2 max-w-md text-sm leading-6 text-slate-500">{description}</p>{action && <div className="mt-6 flex justify-center">{action}</div>}</div>;
}

export function LoadingBlock({ lines = 5 }: { lines?: number }) { return <div className="card shimmer space-y-4 p-6">{Array.from({length: lines}).map((_,i)=><div key={i} className="h-4 rounded-lg bg-white/[.04]" style={{width:`${70 - (i%3)*12}%`}} />)}</div>; }

export function SectionTitle({ title, href, action }: { title: string; href?: string; action?: React.ReactNode }) {
  return <div className="mb-4 flex items-center justify-between"><h2 className="text-base font-semibold text-white">{title}</h2>{action || (href ? <a href={href} className="text-xs font-semibold text-cyan-300 hover:text-white">View all →</a> : null)}</div>;
}
