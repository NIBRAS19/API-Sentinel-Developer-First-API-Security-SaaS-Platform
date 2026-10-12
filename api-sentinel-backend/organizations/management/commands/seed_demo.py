from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from organizations.models import Organization, Membership
from projects.models import Project
from apis.models import Environment, APIService
from apis.services import import_openapi

DEMO_SPEC={
  'openapi':'3.0.3',
  'info':{'title':'Demo Customer API','version':'1.0.0'},
  'servers':[{'url':'http://host.docker.internal:9000'}],
  'paths':{
    '/api/users':{'get':{'summary':'List users','security':[{'bearerAuth':[]}]},},
    '/api/users/{id}':{'get':{'summary':'Get user','parameters':[{'name':'id','in':'path','required':True,'schema':{'type':'string'}}],'security':[{'bearerAuth':[]}]}},
    '/api/login':{'post':{'summary':'Login','security':[]}},
    '/api/admin/users':{'get':{'summary':'Admin users','security':[{'bearerAuth':[]}]}},
    '/api/callback':{'post':{'summary':'Callback handler','parameters':[{'name':'url','in':'query','schema':{'type':'string','format':'uri'}}],'security':[{'bearerAuth':[]}]}},
  },
  'components':{'securitySchemes':{'bearerAuth':{'type':'http','scheme':'bearer'}}}
}
class Command(BaseCommand):
    help='Create a demo workspace and import a sample OpenAPI inventory.'
    def handle(self,*args,**kwargs):
        User=get_user_model(); user,_=User.objects.get_or_create(username='demo@api-sentinel.local',defaults={'email':'demo@api-sentinel.local','first_name':'Demo','last_name':'User'}); user.set_password('ChangeMe123!'); user.save()
        org,_=Organization.objects.get_or_create(name='Demo Workspace',defaults={'slug':'demo-workspace','owner':user}); Membership.objects.get_or_create(organization=org,user=user,defaults={'role':Membership.Role.OWNER})
        project,_=Project.objects.get_or_create(organization=org,slug='demo-project',defaults={'name':'Demo Project','description':'API Sentinel demo project'})
        env,_=Environment.objects.get_or_create(project=project,name='Staging',defaults={'kind':'staging','base_url':'http://host.docker.internal:9000'})
        api,_=APIService.objects.get_or_create(project=project,environment=env,name='Demo Customer API',defaults={'base_url':env.base_url})
        import_openapi(api,DEMO_SPEC)
        self.stdout.write(self.style.SUCCESS('Demo seeded. Login: demo@api-sentinel.local / ChangeMe123!'))
