export type Severity = 'critical' | 'high' | 'medium' | 'low' | 'info';
export type FindingStatus = 'open' | 'triaged' | 'in_progress' | 'fixed' | 'verified' | 'closed' | 'false_positive';
export type ScanStatus = 'queued' | 'running' | 'completed' | 'failed' | 'canceled';

export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  is_active: boolean;
  date_joined: string;
}

export interface Organization {
  id: string;
  name: string;
  slug: string;
  owner: string;
  created_at: string;
  updated_at: string;
}

export interface Membership {
  id: string;
  user: string;
  user_email: string;
  role: 'owner' | 'admin' | 'analyst' | 'developer' | 'viewer';
  created_at: string;
}

export interface Project {
  id: string;
  organization: string;
  name: string;
  slug: string;
  description: string;
  archived: boolean;
  created_at: string;
  updated_at: string;
}

export interface Environment {
  id: string;
  project: string;
  name: string;
  kind: 'development' | 'staging' | 'production' | 'other';
  base_url: string;
  created_at: string;
  updated_at: string;
}

export interface APIService {
  id: string;
  project: string;
  environment: string;
  name: string;
  version: string;
  base_url: string;
  imported_at?: string | null;
  created_at: string;
  updated_at: string;
}

export interface Endpoint {
  id: string;
  api: string;
  method: string;
  path: string;
  operation_id: string;
  summary: string;
  security_required: boolean;
  parameters: unknown[];
  tags: string[];
  created_at: string;
  updated_at: string;
}

export interface Evidence {
  id: string;
  kind: string;
  request_data: Record<string, unknown>;
  response_data: Record<string, unknown>;
  notes: string;
  created_at: string;
}

export interface Finding {
  id: string;
  project: string;
  endpoint?: string | null;
  check_id: string;
  category: string;
  title: string;
  severity: Severity;
  status: FindingStatus;
  description: string;
  impact: string;
  remediation: string;
  verification: string;
  assignee?: string | null;
  assignee_email?: string | null;
  evidence: Evidence[];
  first_seen_at: string;
  last_seen_at: string;
}

export interface Scan {
  id: string;
  project: string;
  api: string;
  profile: 'quick' | 'standard' | 'deep';
  status: ScanStatus;
  safe_mode: boolean;
  authorization_confirmed: boolean;
  requested_by: string;
  progress: number;
  summary: Record<string, number>;
  started_at?: string | null;
  completed_at?: string | null;
  created_at: string;
}

export interface Report {
  id: string;
  project: string;
  name: string;
  report_format: 'json' | 'html';
  scope: Record<string, unknown>;
  content: Record<string, unknown>;
  created_by: string;
  created_at: string;
}

export interface AuditLog {
  id: string;
  action: string;
  resource_type: string;
  resource_id: string;
  actor_email?: string;
  metadata: Record<string, unknown>;
  created_at: string;
}
