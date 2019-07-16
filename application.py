import os
import connexion
from flask_cors import CORS

from flask import redirect

from py.db.endpoint import DatabaseEndpoint

conn_app = connexion.App(__name__, specification_dir=os.getenv('SPEC_DIR'))
conn_app.add_api(os.getenv('SPEC_FILENAME'))

app = conn_app.app
app.config.from_object('config.{}Config'.format(os.getenv('FLASK_ENV')))

cors = CORS(app, resources={r'/api/*': {"origins": "*"}})

with app.app_context():
    DatabaseEndpoint.init_app(app)


@app.route('/')
def home():
    return redirect('/api/ui')
