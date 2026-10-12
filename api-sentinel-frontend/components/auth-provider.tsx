'use client';

import { createContext, useContext, useEffect, useMemo, useState } from 'react';
import { api, DEMO_MODE } from '@/lib/api';
import { User } from '@/lib/types';

type AuthContextValue = { user: User | null; loading: boolean; demo: boolean; signIn: (email: string, password: string) => Promise<void>; signUp: (payload: any) => Promise<void>; logout: () => void };
const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(DEMO_MODE ? api.demo.user : null);
  const [loading, setLoading] = useState(!DEMO_MODE);
  useEffect(() => {
    if (DEMO_MODE) return;
    const access = localStorage.getItem('api_sentinel_access');
    if (!access) { setLoading(false); return; }
    api.auth.me().then(setUser).catch(()=>{ localStorage.removeItem('api_sentinel_access'); localStorage.removeItem('api_sentinel_refresh'); }).finally(()=>setLoading(false));
  }, []);
  const value = useMemo<AuthContextValue>(() => ({
    user, loading, demo: DEMO_MODE,
    async signIn(email, password) {
      if (DEMO_MODE) { setUser(api.demo.user); return; }
      const result = await api.auth.login(email, password);
      localStorage.setItem('api_sentinel_access', result.tokens.access); localStorage.setItem('api_sentinel_refresh', result.tokens.refresh); setUser(result.user);
    },
    async signUp(payload) {
      if (DEMO_MODE) { setUser({ ...api.demo.user, email: payload.email, first_name: payload.first_name, last_name: payload.last_name }); return; }
      const result = await api.auth.register(payload);
      localStorage.setItem('api_sentinel_access', result.tokens.access); localStorage.setItem('api_sentinel_refresh', result.tokens.refresh); setUser(result.user);
    },
    logout() { localStorage.removeItem('api_sentinel_access'); localStorage.removeItem('api_sentinel_refresh'); setUser(null); },
  }), [user, loading]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
export function useAuth() { const ctx = useContext(AuthContext); if (!ctx) throw new Error('useAuth must be used inside AuthProvider'); return ctx; }
