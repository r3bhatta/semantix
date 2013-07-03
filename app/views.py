from flask import render_template
from app import app
import Main

@app.route('/')
def index():
    data = { 
        'name'		: 'California Pizza Kitchen',
        'business'	: 'Restaurant',
        'location'	: '123 Pizza Drive, San Francisco, US, 12345',
        'hours'		: '8:00 AM to 10:00 PM'
    }
    return render_template('index.html', data = data)

@app.route('/locations')
def locations():
    return Main.locations()

@app.route('/menu')
def menu():
    return Main.menu()

