from app import app, db
from app.models import *
from gevent.pywsgi import WSGIServer

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Bought': Bought, 'Item': Item}

if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
