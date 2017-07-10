from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config
import alchemy as al
from datetime import date, datetime

session = None

@view_config(route_name='add', renderer='/templates/add.jinja2')
def add_record(request):
    return {'success':'hidden','failure':'hidden'}

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
        template_args['success'] = ''
        template_args['failure'] = 'hidden'
    except Exception as e:
        print(e)
        template_args['success'] = 'hidden'
        template_args['failure'] = ''
    finally:
        return template_args

@view_config(route_name='search', renderer='/templates/search.jinja2')
def search_record(request):
    return {'lines':[{'name':'Daksh','dob':'25-Nov-1993'},
    {'name':'Charul','dob':'8-Aug-1993'},
    {'name':'Ajir','dob':'21-Nov-1990'}]}

@view_config(route_name='update', renderer='/templates/update.jinja2')
def update_record(request):
    return {}

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