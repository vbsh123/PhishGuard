from flask import Flask
from flask import request
from flask import jsonify
import uuid
from domain_lookup import scan
import psycopg2
from flask_cors import CORS, cross_origin
app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def welcome():
    #run_on_suffix("paypal","com")
    return "welcome page here"



@app.route('/login', methods = ['POST'])
@cross_origin()
def login():
    data = request.get_json()
    user_email = data["email"]
    user_psw = data["password"] 

    #connect to the db 
    con = psycopg2.connect(
    host = "ec2-54-211-169-227.compute-1.amazonaws.com",
    database="db9re09i5sa815",
    user = "ovnalxutzipgpq",
    password = "05477ca8a578982333f07a681c05a64c68fb62514965d60cf8d69fe628dbc927")

    cur = con.cursor()

    email_and_psw = (user_email,user_psw,)
  
    cur.execute("SELECT * FROM clients WHERE email=%s AND psw=%s", email_and_psw)
    rows = cur.fetchall()
    if not rows:
        return "ERROR",500
    user_token = rows[0][2]
    response = jsonify({"token":user_token})
    return response



@app.route('/register', methods = ['POST'])
@cross_origin()
def register():

    data = request.get_json()
    user_email = data["email"]
    user_psw = data["password"]
    user_full_name = data["full_name"]
    user_token = str(uuid.uuid4())


    #connect to the db
    con = psycopg2.connect(
    host = "ec2-54-211-169-227.compute-1.amazonaws.com",
    database="db9re09i5sa815",
    user = "ovnalxutzipgpq",
    password = "05477ca8a578982333f07a681c05a64c68fb62514965d60cf8d69fe628dbc927")


    cur = con.cursor()
    
    cur.execute("INSERT INTO clients (email, psw, full_name, token) VALUES ('" + user_email + "','" + user_psw + "','" + user_full_name + "' ,'" + user_token +"')" )
    cur.execute("INSERT INTO domains (token) VALUES ('" + user_token + "')" )
        #commit the transcation
    con.commit()


    #return "ERROR", 500
    #close the cursor
    cur.close()

    #close the connection
    con.close()
    response = jsonify({"token":user_token})
    return response


@app.route('/acc_info', methods = ['GET'])
@cross_origin()
def get_info():
    token = request.headers.get("token")
    con = psycopg2.connect(
    host = "ec2-54-211-169-227.compute-1.amazonaws.com",
    database="db9re09i5sa815",
    user = "ovnalxutzipgpq",
    password = "05477ca8a578982333f07a681c05a64c68fb62514965d60cf8d69fe628dbc927")

    cur = con.cursor()
    token = (token,)
    cur.execute("SELECT * FROM clients WHERE token=%s", token)
    rows = cur.fetchall()
    if not rows:
        return "ERROR"
    print(rows)
    response = jsonify({"email":rows[0][0], "password":rows[0][1],"full_name":rows[0][3]})
    return response


@app.route('/fetch_domain', methods = ['GET'])
@cross_origin()
def fetch_domain():
    token = request.headers.get("token")
    con = psycopg2.connect(
    host = "ec2-54-211-169-227.compute-1.amazonaws.com",
    database="db9re09i5sa815",
    user = "ovnalxutzipgpq",
    password = "05477ca8a578982333f07a681c05a64c68fb62514965d60cf8d69fe628dbc927")

    cur = con.cursor()
    token = (token,)
    cur.execute("SELECT * FROM domains WHERE token=%s", token)
    rows = cur.fetchall()
    if not rows:
        return "ERROR"
    
    response = jsonify({"domain":rows[0][1]})
    return response

@app.route('/scan', methods = ['POST'])
@cross_origin()
def scan_send():
    data = request.get_json()
    user_token = data["token"]
    user_domain = data["domain_name"]

    print(user_domain)
    splitted = user_domain['label'].split(" ")
    domain = splitted[0]
    level = splitted[1]
    con = psycopg2.connect(
    host = "ec2-54-211-169-227.compute-1.amazonaws.com",
    database="db9re09i5sa815",
    user = "ovnalxutzipgpq",
    password = "05477ca8a578982333f07a681c05a64c68fb62514965d60cf8d69fe628dbc927")

    cur = con.cursor()
    token = (user_token,)
    cur.execute("SELECT * FROM domains WHERE token=%s", token)
    rows = cur.fetchall()

    scan(domain,"yoelvb5801@gmail.com",level)

    response = jsonify({"status":"SUCCESS"})
    return response

@app.route('/add_domain', methods = ['POST'])
@cross_origin()
def add_domain():
    data = request.get_json()
    user_token = data["token"]
    user_domain = data["domain_name"]

    con = psycopg2.connect(
    host = "ec2-54-211-169-227.compute-1.amazonaws.com",
    database="db9re09i5sa815",
    user = "ovnalxutzipgpq",
    password = "05477ca8a578982333f07a681c05a64c68fb62514965d60cf8d69fe628dbc927")

    cur = con.cursor()

    token_and_domain = (user_domain, user_token,)
    cur.execute("UPDATE domains SET name=%s WHERE token=%s", token_and_domain)
    con.commit()
    #close the cursor
    cur.close()

    #close the connection
    con.close()
    response = jsonify({"token":user_token})
    return response




@app.route('/delete_domain', methods = ['POST'])
@cross_origin()
def delete_domain():
    data = request.get_json()
    user_token = data["token"]
    user_domain = data["domain_name"]


    con = psycopg2.connect(
    host = "ec2-54-211-169-227.compute-1.amazonaws.com",
    database="db9re09i5sa815",
    user = "ovnalxutzipgpq",
    password = "05477ca8a578982333f07a681c05a64c68fb62514965d60cf8d69fe628dbc927")

    cur = con.cursor()

    token_and_domain = (None, user_token,)
    cur.execute("UPDATE domains SET name=%s WHERE token=%s", token_and_domain)
    con.commit()
    #close the cursor
    cur.close()

    #close the connection
    con.close()
    response = jsonify({"token":user_token})
    return response

if __name__ == '__main__':
    app.run()