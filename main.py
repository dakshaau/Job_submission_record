from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config
import alchemy as al
from datetime import date, datetime
import json

session = None

@view_config(route_name='add', renderer='/templates/add.jinja2')
def add_record(request):
    return {'no_app':al.get_count(session),'success':'hidden','failure':'hidden'}

@view_config(route_name='add', renderer='/templates/add.jinja2', request_method='POST')
def submitted(request):
    pr = request.params
    args = {
    # 'app': date(pr['date']),
    'comp': pr['company'].strip(),
    'pos': pr['position'].strip(),
    'resp': False
    }

    # print(pr['date'])
    year, month, day = [int(dt) for dt in pr['date'].split('-')]
    dt = date(year=year, month=month, day=day)
    # print(dt)
    args['app'] = dt

    if pr['pid'] != '':
        args['p_id'] = pr['pid'].strip()

    if pr['location'] != '':
        args['loc'] = pr['location'].strip()
    
    if pr['country'] == 'Other':
        args['country'] = pr['other_country'].strip()
    else:
        args['country'] = pr['country']
    
    if pr['portals'] == 'Other':
        args['portal'] = pr['other_portals'].strip()
    else:
        args['portal'] = pr['portals']

    skills = []
    if 'skills' in pr:
        skills += pr.getall('skills')

    if pr['other_skills'] != '':
        temp = [skill.strip() for skill in pr['other_skills'].split(',')]
        skills += temp

    args['skills'] = skills

    template_args = {}
    try:
        al.insert_job(session, args)
        template_args['no_app'] = al.get_count(session)
        template_args['success'] = ''
        template_args['failure'] = 'hidden'
    except Exception as e:
        print(e)
        template_args['no_app'] = al.get_count(session)
        template_args['success'] = 'hidden'
        template_args['failure'] = ''
    finally:
        return template_args

@view_config(route_name='search', renderer='/templates/search.jinja2')
def search_record(request):
    return {'company_val':'', 'pos_cal':'', 'p_id_val': ''}

@view_config(route_name='search', renderer='/templates/search2.jinja2', request_method='POST')
def display_records(request):
    # print(request.params)
    param = {'company': request.params['company']}
    if request.params['position'] != '':
        param['position'] = request.params['position']
    if request.params['position_id'] != '':
        param['p_id'] = request.params['position_id']

    res = al.get_jobs(session, param)
    if len(res) == 0:
        return {'company_val':request.params['company'],
        'pos_val': request.params['position'],
        'p_id_val': request.params['position_id'],
        'res_count':0, 'table_hidden':'hidden'}
    else:
        return {'company_val':request.params['company'],
        'pos_val': request.params['position'],
        'p_id_val': request.params['position_id'],
        'res_count':len(res), 'table_hidden':'',
        'apps': [dict([('ID',job.ID),('comp',job.comp),('pos',job.pos),('date',str(job.app))]) for job in res]}

@view_config(route_name='update',request_method='POST', renderer='json')
def send_or_update_job(request):
    if request.params['status'] == 'view':
        job = al.get_job_by_id(session, request.params['ID'])
        return json.dumps({
            'ID': job.ID,
            'company': job.comp,
            'pos': job.pos,
            'p_id': job.p_id,
            'country': job.country,
            'loc': job.loc,
            'skills': job.skills,
            'portal': job.portal,
            'resp': job.resp,
            'status': job.status,
            'date': str(job.app)
            })
    elif request.params['status'] == 'update':
        ID = request.params['ID']
        status = request.params['stat']
        resp = request.params['resp']
        if resp == 'false':
            resp = False
        else:
            resp = True
        # print(resp, type(resp))
        if status == '':
            status = None
        ret = None
        try:
            ret = al.update_job(session, resp=resp, application_id=ID, status=status)
        except Exception as e:
            print(e)
            return json.dumps({
                    'status': 'Error'
                })
        else:
            if type(ret) is str:
                return json.dumps({
                        'status': 'Error'
                    })
            else:
                return json.dumps({
                        'status': 'Success'
                    })



if __name__ == '__main__':
    host, db, port, uname, pswd = [line.strip() for line in open('config','r').readlines()]
    c_str = 'postgresql://{}:{}@{}:{}/{}'.format(uname, pswd, host, port, db)
    session = al.connect(c_str)

    config = Configurator()
    config.include('pyramid_jinja2')
    config.add_route('add', '/')
    config.add_route('search','/search')
    config.add_route('update','/update')
    config.add_static_view(name='static',path='templates')
    # config.add_static_view(name='static',path='templates')
    config.scan()
    app = config.make_wsgi_app()
    server = make_server('127.0.0.1', 6543, app)
    try:
        print('Started server ...')
        server.serve_forever()
    except KeyboardInterrupt as e:
        session.close()
        print('Closed connection ...')