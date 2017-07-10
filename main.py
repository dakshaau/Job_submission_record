from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config
import alchemy as al

@view_config(route_name='add', renderer='/templates/add.jinja2')
def add_record(request):
    return {'success':'hidden','failure':'hidden'}

@view_config(route_name='add', renderer='/templates/add.jinja2', request_method='POST')
def submitted(request):
    print(request.params)
    return {'success':'','failure':'hidden'}

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