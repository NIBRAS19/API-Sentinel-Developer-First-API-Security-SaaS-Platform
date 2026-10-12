'use client';
import { FormEvent, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { api } from '@/lib/api';
import { Button, PageHeader } from '@/components/ui';

const sample = JSON.stringify({openapi:'3.0.3',info:{title:'Customer API',version:'v1'},servers:[{url:'https://api.example.test'}],paths:{'/api/health':{get:{summary:'Health check',responses:{200:{description:'OK'}}}}}},null,2);

export default function ImportOpenAPI(){
 const {apiId}=useParams<{apiId:string}>(); const r=useRouter(); const [spec,setSpec]=useState(sample); const [error,setError]=useState(''); const [busy,setBusy]=useState(false); const [result,setResult]=useState<any>(null);
 async function submit(e:FormEvent){e.preventDefault();setError('');setBusy(true);try{const parsed=JSON.parse(spec);if(api.demo){setResult({endpoints:1,schemas:0,message:'Demo import completed'});return}const out=await api.importOpenAPI(apiId,parsed);setResult(out)}catch(err){setError(err instanceof Error?err.message:'Invalid OpenAPI JSON')}finally{setBusy(false)}}
 return <div className="mx-auto max-w-4xl"><PageHeader eyebrow="api inventory / import" title="Import OpenAPI" description="Upload a JSON OpenAPI document to populate the endpoint inventory."/><form onSubmit={submit} className="card p-6"><label className="block"><span className="mb-2 block text-xs font-medium text-slate-300">OpenAPI JSON</span><textarea value={spec} onChange={e=>setSpec(e.target.value)} className="mono min-h-[430px] w-full rounded-2xl border border-white/10 bg-black/20 p-4 text-xs leading-6 text-slate-300 outline-none focus:border-cyan-400/30" spellCheck={false}/></label>{error&&<div className="mt-4 rounded-xl border border-red-400/15 bg-red-400/[.05] p-3 text-xs text-red-200">{error}</div>}{result&&<div className="mt-4 rounded-xl border border-emerald-400/15 bg-emerald-400/[.05] p-4 text-sm text-emerald-200">Import complete. <span className="text-emerald-100/70">{JSON.stringify(result)}</span></div>}<div className="mt-6 flex justify-end gap-2"><Button variant="secondary" onClick={()=>r.back()}>Cancel</Button><Button type="submit" disabled={busy}>{busy?'Importing…':'Import OpenAPI'}</Button></div></form></div>
}
