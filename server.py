from flask import Flask
import uuid
from domain_lookup import run_on_suffix
app = Flask(__name__)


@app.route('/')
def welcome():
    run_on_suffix("paypal","com")
    return "welcome page here"



@app.route('/login', methods = ['POST'])
def login():
    return "login stuff here"


@app.route('/register', methods = ['POST'])
def register():
    return "register stuff here"


@app.route('/acc_info', methods = ['GET'])
def get_info():
    return "Account info here"


@app.route('/scan', methods = ['GET'])
def start_scan():
    return "this will start the scan in domain_lookup.py"

@app.route('/add_domain', methods = ['POST'])
def add_domain():
    return "this will add the domain to the database"

if __name__ == '__main__':
    app.run()