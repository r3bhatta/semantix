from flask import render_template
from app import app

@app.route('/')
def index():
    json = { 'title': 'Semantix' } # fake user
    return render_template(
        "index.html",
        title = 'Home',
        description = 'Semantix business crawler that trawls sites for information.')

