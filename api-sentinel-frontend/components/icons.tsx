import React from 'react';

type Props = { size?: number; stroke?: number; className?: string };
const Svg = ({ size = 18, stroke = 1.8, className, children }: Props & { children: React.ReactNode }) => <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={stroke} strokeLinecap="round" strokeLinejoin="round" className={className}>{children}</svg>;
export const Icon = {
  grid: (p?: Props) => <Svg {...p}><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></Svg>,
  folder: (p?: Props) => <Svg {...p}><path d="M3 6.5A2.5 2.5 0 0 1 5.5 4H10l2 2h6.5A2.5 2.5 0 0 1 21 8.5v9A2.5 2.5 0 0 1 18.5 20h-13A2.5 2.5 0 0 1 3 17.5z"/></Svg>,
  shield: (p?: Props) => <Svg {...p}><path d="M12 3 20 6v5c0 5.2-3.5 8.8-8 10-4.5-1.2-8-4.8-8-10V6z"/><path d="m9 12 2 2 4-4"/></Svg>,
  scan: (p?: Props) => <Svg {...p}><path d="M5 3H3v4M19 3h2v4M5 21H3v-4M19 21h2v-4"/><path d="M8 8h8v8H8z"/></Svg>,
  bug: (p?: Props) => <Svg {...p}><path d="M9 9a3 3 0 1 1 6 0v2a4 4 0 0 1-8 0V9z"/><path d="M5 11H3m18 0h-2M6 7 4.5 5.5M18 7l1.5-1.5M6 16l-1.5 1.5M18 16l1.5 1.5M9 5V3m6 2V3"/></Svg>,
  file: (p?: Props) => <Svg {...p}><path d="M6 3h8l4 4v14H6z"/><path d="M14 3v5h5M9 13h6M9 17h6"/></Svg>,
  users: (p?: Props) => <Svg {...p}><circle cx="9" cy="8" r="3"/><path d="M3 20a6 6 0 0 1 12 0M17 8a3 3 0 1 1 0 6M16 17a5 5 0 0 1 5 3"/></Svg>,
  settings: (p?: Props) => <Svg {...p}><path d="m12 2 1 3 3 1 3-1 2 3-2 2 1 3-1 3 2 2-2 3-3-1-3 1-3-1-3 1-2-3 2-2-1-3 1-3-2-2 2-3 3 1z"/><circle cx="12" cy="12" r="3"/></Svg>,
  search: (p?: Props) => <Svg {...p}><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></Svg>,
  bell: (p?: Props) => <Svg {...p}><path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9M10 21h4"/></Svg>,
  plus: (p?: Props) => <Svg {...p}><path d="M12 5v14M5 12h14"/></Svg>,
  arrow: (p?: Props) => <Svg {...p}><path d="M5 12h14M13 6l6 6-6 6"/></Svg>,
  chevron: (p?: Props) => <Svg {...p}><path d="m9 18 6-6-6-6"/></Svg>,
  check: (p?: Props) => <Svg {...p}><path d="m5 12 4 4L19 6"/></Svg>,
  x: (p?: Props) => <Svg {...p}><path d="m6 6 12 12M18 6 6 18"/></Svg>,
  menu: (p?: Props) => <Svg {...p}><path d="M4 7h16M4 12h16M4 17h16"/></Svg>,
  more: (p?: Props) => <Svg {...p}><circle cx="5" cy="12" r="1" fill="currentColor"/><circle cx="12" cy="12" r="1" fill="currentColor"/><circle cx="19" cy="12" r="1" fill="currentColor"/></Svg>,
  upload: (p?: Props) => <Svg {...p}><path d="M12 16V4M7 9l5-5 5 5M5 20h14"/></Svg>,
  download: (p?: Props) => <Svg {...p}><path d="M12 4v12m0 0-5-5m5 5 5-5M5 20h14"/></Svg>,
  activity: (p?: Props) => <Svg {...p}><path d="M3 12h4l2-5 5 10 2-5h5"/></Svg>,
  terminal: (p?: Props) => <Svg {...p}><path d="m5 7 5 5-5 5M13 17h6"/></Svg>,
  lock: (p?: Props) => <Svg {...p}><rect x="5" y="10" width="14" height="10" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></Svg>,
};
