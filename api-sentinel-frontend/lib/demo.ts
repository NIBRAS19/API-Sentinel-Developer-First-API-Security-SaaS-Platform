import { APIService, AuditLog, Endpoint, Finding, Membership, Organization, Project, Report, Scan, User } from './types';

const now = new Date();
const iso = (minutes: number) => new Date(now.getTime() - minutes * 60_000).toISOString();

export const demoUser: User = {
  id: 'user-demo', email: 'nibras@example.com', first_name: 'Nibras', last_name: 'Ahmed', is_active: true, date_joined: iso(900),
};

export const demoOrg: Organization = {
  id: 'org-demo', name: 'Sentinel Labs', slug: 'sentinel-labs', owner: demoUser.id, created_at: iso(900), updated_at: iso(2),
};

export const demoProjects: Project[] = [
  { id: 'proj-customer', organization: demoOrg.id, name: 'Customer Platform', slug: 'customer-platform', description: 'Customer-facing API estate and web application.', archived: false, created_at: iso(640), updated_at: iso(6) },
  { id: 'proj-mobile', organization: demoOrg.id, name: 'Mobile API', slug: 'mobile-api', description: 'Mobile backend and authentication services.', archived: false, created_at: iso(520), updated_at: iso(22) },
  { id: 'proj-admin', organization: demoOrg.id, name: 'Admin Control Plane', slug: 'admin-control-plane', description: 'Internal management APIs and privileged workflows.', archived: false, created_at: iso(410), updated_at: iso(45) },
];

export const demoApis: APIService[] = [
  { id: 'api-customer', project: 'proj-customer', environment: 'env-prod', name: 'Customer API', version: 'v1', base_url: 'https://api.example.test', imported_at: iso(65), created_at: iso(620), updated_at: iso(6) },
  { id: 'api-mobile', project: 'proj-mobile', environment: 'env-stage', name: 'Mobile API', version: 'v2', base_url: 'https://mobile.example.test', imported_at: iso(120), created_at: iso(500), updated_at: iso(22) },
  { id: 'api-admin', project: 'proj-admin', environment: 'env-prod', name: 'Admin API', version: 'v1', base_url: 'https://admin.example.test', imported_at: iso(180), created_at: iso(390), updated_at: iso(45) },
];

export const demoEndpoints: Endpoint[] = [
  { id: 'ep-1', api: 'api-customer', method: 'GET', path: '/api/users/{id}', operation_id: 'getUser', summary: 'Get user by ID', security_required: true, parameters: [{ name: 'id', in: 'path' }], tags: ['users'], created_at: iso(61), updated_at: iso(6) },
  { id: 'ep-2', api: 'api-customer', method: 'POST', path: '/api/auth/login', operation_id: 'login', summary: 'Authenticate account', security_required: false, parameters: [], tags: ['auth'], created_at: iso(61), updated_at: iso(6) },
  { id: 'ep-3', api: 'api-admin', method: 'GET', path: '/api/admin/users', operation_id: 'adminUsers', summary: 'List users for admin', security_required: true, parameters: [], tags: ['admin'], created_at: iso(170), updated_at: iso(45) },
  { id: 'ep-4', api: 'api-customer', method: 'GET', path: '/api/orders/{id}', operation_id: 'getOrder', summary: 'Get order', security_required: true, parameters: [{ name: 'id', in: 'path' }], tags: ['orders'], created_at: iso(61), updated_at: iso(6) },
  { id: 'ep-5', api: 'api-mobile', method: 'POST', path: '/api/uploads/presign', operation_id: 'presignUpload', summary: 'Create upload URL', security_required: true, parameters: [], tags: ['files'], created_at: iso(119), updated_at: iso(22) },
  { id: 'ep-6', api: 'api-customer', method: 'GET', path: '/api/health', operation_id: 'health', summary: 'Service health', security_required: false, parameters: [], tags: ['system'], created_at: iso(61), updated_at: iso(6) },
];

export const demoFindings: Finding[] = [
  { id: 'find-1', project: 'proj-customer', endpoint: 'ep-1', check_id: 'API1-BOLA', category: 'Authorization / Object Access', title: 'Broken Object Level Authorization', severity: 'high', status: 'open', description: 'The endpoint appears to expose an object identifier without sufficient evidence of object-level authorization.', impact: 'A user may access an object belonging to another authorization context.', remediation: 'Enforce server-side object ownership or policy checks before returning the requested object.', verification: 'Verify same-user access succeeds and cross-user access returns an authorization failure.', assignee: demoUser.id, assignee_email: demoUser.email, evidence: [{ id: 'ev-1', kind: 'authorization-check', request_data: { method: 'GET', path: '/api/users/{id}' }, response_data: { status: 200, note: 'Controlled test context' }, notes: 'Sanitized evidence from a controlled test identity pair.', created_at: iso(4) }], first_seen_at: iso(140), last_seen_at: iso(4) },
  { id: 'find-2', project: 'proj-admin', endpoint: 'ep-3', check_id: 'API5-FUNCTION-AUTH', category: 'Authorization / Function Access', title: 'Broken Function Level Authorization', severity: 'high', status: 'open', description: 'A privileged function appears reachable from a lower-privilege authorization context.', impact: 'A lower-privilege user may reach administrative operations.', remediation: 'Enforce function-level authorization at the server boundary for every privileged route.', verification: 'Test with a non-admin identity and confirm an explicit authorization denial.', assignee: null, assignee_email: null, evidence: [], first_seen_at: iso(300), last_seen_at: iso(12) },
  { id: 'find-3', project: 'proj-customer', endpoint: 'ep-2', check_id: 'API4-RATE-LIMIT', category: 'Resource Consumption', title: 'Missing or Unclear Rate-Limit Controls', severity: 'medium', status: 'triaged', description: 'The authentication endpoint does not expose clear rate-limit behavior within the configured test profile.', impact: 'Automated repeated requests may increase service and abuse risk.', remediation: 'Apply and document rate limits with suitable thresholds for authentication attempts.', verification: 'Exercise a controlled request burst in staging and verify throttling behavior.', assignee: demoUser.id, assignee_email: demoUser.email, evidence: [], first_seen_at: iso(220), last_seen_at: iso(18) },
  { id: 'find-4', project: 'proj-mobile', endpoint: 'ep-5', check_id: 'API8-MISCONFIG', category: 'Security Misconfiguration', title: 'Upload Endpoint Configuration Requires Review', severity: 'medium', status: 'in_progress', description: 'The upload workflow exposes configuration that should be explicitly reviewed for content-type and authorization controls.', impact: 'Misconfigured upload flows can increase data exposure and abuse risk.', remediation: 'Constrain content types, enforce object-scoped authorization and use short-lived upload URLs.', verification: 'Test authorized and unauthorized upload scenarios in staging.', assignee: demoUser.id, assignee_email: demoUser.email, evidence: [], first_seen_at: iso(440), last_seen_at: iso(35) },
  { id: 'find-5', project: 'proj-customer', endpoint: 'ep-4', check_id: 'API3-PROPERTY-AUTH', category: 'Authorization / Property Access', title: 'Sensitive Property Exposure Needs Review', severity: 'medium', status: 'open', description: 'The response schema contains fields that should be confirmed against the caller authorization context.', impact: 'Sensitive properties may be exposed beyond intended user or role boundaries.', remediation: 'Enforce allowlists for response properties by role and use serializer-level access control.', verification: 'Compare responses for low-privilege and privileged identities.', assignee: null, assignee_email: null, evidence: [], first_seen_at: iso(320), last_seen_at: iso(28) },
  { id: 'find-6', project: 'proj-admin', endpoint: null, check_id: 'API9-INVENTORY', category: 'Inventory', title: 'Undocumented API Version Detected', severity: 'low', status: 'fixed', description: 'An active API surface is not represented in the imported inventory.', impact: 'Untracked endpoints can bypass normal security review and lifecycle controls.', remediation: 'Keep production API inventory synchronized with deployed versions.', verification: 'Re-run inventory and confirm the undocumented version is represented.', assignee: demoUser.id, assignee_email: demoUser.email, evidence: [], first_seen_at: iso(620), last_seen_at: iso(55) },
];

export const demoScans: Scan[] = [
  { id: 'scan-1', project: 'proj-customer', api: 'api-customer', profile: 'standard', status: 'completed', safe_mode: true, authorization_confirmed: true, requested_by: demoUser.id, progress: 100, summary: { critical: 1, high: 4, medium: 11, low: 6 }, started_at: iso(52), completed_at: iso(48), created_at: iso(58) },
  { id: 'scan-2', project: 'proj-mobile', api: 'api-mobile', profile: 'quick', status: 'completed', safe_mode: true, authorization_confirmed: true, requested_by: demoUser.id, progress: 100, summary: { critical: 0, high: 2, medium: 4, low: 2 }, started_at: iso(96), completed_at: iso(88), created_at: iso(100) },
  { id: 'scan-3', project: 'proj-admin', api: 'api-admin', profile: 'deep', status: 'running', safe_mode: true, authorization_confirmed: true, requested_by: demoUser.id, progress: 68, summary: {}, started_at: iso(3), completed_at: null, created_at: iso(5) },
];

export const demoReports: Report[] = [
  { id: 'report-1', project: 'proj-customer', name: 'Customer API Security Assessment', report_format: 'html', scope: { environment: 'Production' }, content: { summary: 'Assessment completed with 22 findings.' }, created_by: demoUser.id, created_at: iso(18) },
  { id: 'report-2', project: 'proj-mobile', name: 'Mobile API Baseline', report_format: 'json', scope: { environment: 'Staging' }, content: { summary: 'Baseline scan report.' }, created_by: demoUser.id, created_at: iso(88) },
];

export const demoMembers: Membership[] = [
  { id: 'm-1', user: demoUser.id, user_email: demoUser.email, role: 'owner', created_at: iso(900) },
  { id: 'm-2', user: 'u-2', user_email: 'security@example.test', role: 'analyst', created_at: iso(800) },
  { id: 'm-3', user: 'u-3', user_email: 'developer@example.test', role: 'developer', created_at: iso(600) },
];

export const demoAuditLogs: AuditLog[] = [
  { id: 'a-1', action: 'scan.completed', resource_type: 'scan', resource_id: 'scan-1', actor_email: demoUser.email, metadata: { findings: 22 }, created_at: iso(48) },
  { id: 'a-2', action: 'finding.created', resource_type: 'finding', resource_id: 'find-1', actor_email: demoUser.email, metadata: { severity: 'high' }, created_at: iso(140) },
  { id: 'a-3', action: 'api.openapi_imported', resource_type: 'api', resource_id: 'api-customer', actor_email: demoUser.email, metadata: { endpoints: 128 }, created_at: iso(65) },
  { id: 'a-4', action: 'member.invited', resource_type: 'organization', resource_id: demoOrg.id, actor_email: demoUser.email, metadata: { role: 'developer' }, created_at: iso(70) },
];
