'''Flask app views.'''
from . import app

@app.route('/')
def index():
    return 'RESPONSE'
