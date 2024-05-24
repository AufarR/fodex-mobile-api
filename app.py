from flask import Flask,jsonify,request,Response
import sqlite3
import os
import hashlib
  
app =   Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./upload"

def connect_db():
    conn = None
    try:
        conn = sqlite3.connect("./fodex.db")
    except Exception as e:
        print(e)
    return conn
  
@app.route('/upload', methods = ['POST'])
def upload():
    try:
        if 'file' not in request.files:
            raise Exception("Data not provided")
        file = request.files['file']
        filename = hashlib.md5(file.read()).hexdigest() + ".png"
        file.seek(0)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return filename, 201
    except Exception as e:
        print(e)
    return "",400
        
@app.route('/akun', methods = ['GET','POST','PATCH'])
def akun():
    return "akun"

@app.route('/kurir', methods = ['GET','POST','PATCH'])
def kurir():
    return "kurir"

@app.route('/paket', methods = ['GET','POST','PATCH'])
def paket():
    return "paket"

@app.route('/bunga', methods = ['GET','POST','PATCH'])
def bunga():
    return "bunga"
  
if __name__=='__main__': 
    app.run(debug=True)