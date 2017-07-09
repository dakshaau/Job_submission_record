from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config
import alchemy as al

conn = None

@view_config(route_name='hello', renderer='/templates/trial.jinja2')
def hello_world(request):
    return {'lines':[{'name':'Daksh','dob':'25-Nov-1993'},
    {'name':'Charul','dob':'8-Aug-1993'},
    {'name':'Ajir','dob':'21-Nov-1990'}]}

if __name__ == '__main__':
	host, db, port, uname, pswd = [line.strip() for line in open('config','r').readlines()]
    c_str = 'postgresql://{}:{}@{}:{}/{}'.format(uname, pswd, host, port, db)
    session = al.connect(c_str)

    config = Configurator()
    config.include('pyramid_jinja2')
    config.add_route('hello', '/')
    config.add_static_view(name='static',path='templates')
    # config.add_static_view(name='static',path='templates')
    config.scan()
    app = config.make_wsgi_app()
    server = make_server('127.0.0.1', 6543, app)
    server.serve_forever()