# API Sentinel Frontend

Production-style Next.js App Router frontend for the API Sentinel API security platform.

## Stack

- Next.js 16.3.3 (App Router)
- React 19.2
- TypeScript
- Tailwind CSS 4.3+
- Django REST backend integration
- Demo mode with realistic local security data

Next.js 16.x is Active LTS as of September 2026. The app uses the App Router and Tailwind CSS v4's PostCSS integration. See the official Next.js support policy and Tailwind Next.js installation guide.

## Run

```bash
npm install
cp .env.example .env.local
npm run dev
```

Open http://localhost:3000.

## Demo mode

`NEXT_PUBLIC_DEMO_MODE=true` renders the complete UI with local demo data and does not require the backend.

## Backend mode

Set:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_DEMO_MODE=false
```

Then run the Django backend from the API Sentinel backend package.

## Main routes

- `/` marketing / product landing
- `/login`
- `/register`
- `/app` dashboard
- `/app/projects`
- `/app/projects/[projectId]`
- `/app/apis`
- `/app/apis/[apiId]`
- `/app/endpoints/[endpointId]`
- `/app/scans`
- `/app/scans/new`
- `/app/scans/[scanId]`
- `/app/findings`
- `/app/findings/[findingId]`
- `/app/reports`
- `/app/reports/new`
- `/app/reports/[reportId]`
- `/app/team`
- `/app/audit-log`
- `/app/settings`

## Design

Dark infrastructure-console UI, cyan/green status accents, restrained glow, monospace technical metadata, dense but readable tables, progressive disclosure for security evidence, and explicit authorized-testing workflow.
