import { demoApis, demoAuditLogs, demoEndpoints, demoFindings, demoMembers, demoOrg, demoProjects, demoReports, demoScans, demoUser } from './demo';
import { APIService, AuditLog, Endpoint, Finding, Membership, Organization, Project, Report, Scan, User } from './types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
export const DEMO_MODE = process.env.NEXT_PUBLIC_DEMO_MODE !== 'false';

export class APIError extends Error {
  status: number;
  constructor(message: string, status = 500) { super(message); this.status = status; }
}

function token() {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('api_sentinel_access');
}

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers);
  headers.set('Content-Type', 'application/json');
  const access = token();
  if (access) headers.set('Authorization', `Bearer ${access}`);
  const response = await fetch(`${API_URL}${path}`, { ...init, headers, cache: 'no-store' });
  const body = await response.text();
  let data: unknown = null;
  try { data = body ? JSON.parse(body) : null; } catch { data = body; }
  if (!response.ok) {
    const message = typeof data === 'string' ? data : JSON.stringify(data);
    throw new APIError(message || 'Request failed', response.status);
  }
  return data as T;
}

export const api = {
  auth: {
    async login(email: string, password: string) {
      return request<{ tokens: { access: string; refresh: string }; user: User }>('/auth/login/', { method: 'POST', body: JSON.stringify({ email, password }) });
    },
    async register(payload: { email: string; password: string; first_name: string; last_name: string; organization_name: string; authorized_testing_acknowledgement: boolean }) {
      return request<{ tokens: { access: string; refresh: string }; user: User }>('/auth/register/', { method: 'POST', body: JSON.stringify(payload) });
    },
    async me() { return request<User>('/auth/me/'); },
  },
  demo: {
    user: demoUser,
    org: demoOrg,
    projects: demoProjects,
    apis: demoApis,
    endpoints: demoEndpoints,
    findings: demoFindings,
    scans: demoScans,
    reports: demoReports,
    members: demoMembers,
    audit: demoAuditLogs,
  },
  async organizations() { return request<Organization[]>('/organizations/'); },
  async createOrganization(name: string) { return request<Organization>('/organizations/', { method: 'POST', body: JSON.stringify({ name }) }); },
  async projects() { return request<Project[]>('/projects/'); },
  async createProject(payload: { organization: string; name: string; description?: string }) { return request<Project>('/projects/', { method: 'POST', body: JSON.stringify(payload) }); },
  async getProject(id: string) { return request<Project>(`/projects/${id}/`); },
  async updateProject(id: string, payload: Partial<Project>) { return request<Project>(`/projects/${id}/`, { method: 'PATCH', body: JSON.stringify(payload) }); },
  async members(organizationId: string) { return request<Membership[]>(`/organizations/${organizationId}/members/`); },
  async audit(organizationId: string) { return request<AuditLog[]>(`/organizations/${organizationId}/audit-logs/`); },
  async environments(projectId: string) { return request<any[]>(`/projects/${projectId}/environments/`); },
  async createEnvironment(projectId: string, payload: { name: string; kind: string; base_url: string }) { return request<any>(`/projects/${projectId}/environments/`, { method: 'POST', body: JSON.stringify(payload) }); },
  async apis(projectId: string) { return request<APIService[]>(`/projects/${projectId}/apis/`); },
  async createApi(projectId: string, payload: { environment: string; name: string; version?: string; base_url: string }) { return request<APIService>(`/projects/${projectId}/apis/`, { method: 'POST', body: JSON.stringify(payload) }); },
  async api(id: string) { return request<APIService>(`/apis/${id}/`); },
  async endpoints(apiId: string) { return request<Endpoint[]>(`/apis/${apiId}/endpoints/`); },
  async endpoint(id: string) { return request<Endpoint>(`/endpoints/${id}/`); },
  async importOpenAPI(apiId: string, spec: unknown) { return request<any>(`/apis/${apiId}/openapi/import/`, { method: 'POST', body: JSON.stringify({ spec }) }); },
  async authProfiles(apiId: string) { return request<any[]>(`/apis/${apiId}/auth-profiles/`); },
  async scans() { return request<Scan[]>('/scans/'); },
  async runScan(payload: { api_id: string; profile: string; safe_mode: boolean; authorization_confirmed: boolean }) { return request<Scan>('/scans/run/', { method: 'POST', body: JSON.stringify(payload) }); },
  async scan(id: string) { return request<Scan>(`/scans/${id}/`); },
  async scanLogs(id: string) { return request<any[]>(`/scans/${id}/logs/`); },
  async findings() { return request<Finding[]>('/findings/'); },
  async finding(id: string) { return request<Finding>(`/findings/${id}/`); },
  async updateFinding(id: string, payload: Partial<Finding>) { return request<Finding>(`/findings/${id}/`, { method: 'PATCH', body: JSON.stringify(payload) }); },
  async addComment(id: string, body: string) { return request<any>(`/findings/${id}/comments/`, { method: 'POST', body: JSON.stringify({ body }) }); },
  async assignFinding(id: string, assignee: string | null) { return request<any>(`/findings/${id}/assign/`, { method: 'POST', body: JSON.stringify({ assignee }) }); },
  async reports() { return request<Report[]>('/reports/'); },
  async generateReport(payload: { project_id: string; name: string; report_format: string; scope?: Record<string, unknown> }) { return request<Report>('/reports/generate/', { method: 'POST', body: JSON.stringify(payload) }); },
  async report(id: string) { return request<Report>(`/reports/${id}/`); },
};
