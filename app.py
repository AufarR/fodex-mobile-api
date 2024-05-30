from flask import Flask,jsonify,request,Response, send_file
import sqlite3
import os
import hashlib
import random
  
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
    return "Upload failed",400

@app.route('/download/<filename>', methods = ['GET'])
def download(filename):
    try:
        if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
            return send_file(
                os.path.join(app.config['UPLOAD_FOLDER'], filename),
                download_name=filename,
                as_attachment=True
            )
        else:
            raise Exception("Path invalid")
    except Exception as e:
        print(e)
    return "Not found",404

        
@app.route('/akun', methods = ['POST','PUT','PATCH'])
def akun():
    try:
        if request.method == 'POST': # Handle login + get profile
            db = connect_db()
            query = db.execute("select * from akun where nama = \"" + request.form["nama"] + "\" and password = \"" + hashlib.md5(request.form["password"].encode()).hexdigest() + "\";")
            data = query.fetchall()
            if len(data) == 1:
                data = data[0]
                db.close()
                return {
                    'id': data[0],
                    'nama': data[1],
                    'nama_toko': data[2],
                    'alamat': data[3],
                    'no_telp': data[4],
                    'foto': data[5]
                }
            
        elif request.method == 'PUT': # Handle registrations
            db = connect_db()
            query = db.execute(f"insert into akun (nama, nama_toko, alamat, no_telp, foto, password) values ('{request.form['nama']}', '{request.form['nama_toko']}', '{request.form['alamat']}', '{request.form['no_telp']}', '{request.form['foto']}', '{hashlib.md5(request.form['password'].encode()).hexdigest()}')")
            db.commit()
            db.close()
            return "Success", 201
        
        elif request.method == 'PATCH': # Handle account updates
            db = connect_db()
            if 'id' not in request.form:
                raise Exception("No ID supplied")
            if 'nama' in request.form:
                db.execute(
                    "update akun " +
                    f"set nama = \"{request.form['nama']}\"" +
                    f" where id = {request.form['id']};"
                )
            if 'nama_toko' in request.form:
                db.execute(
                    "update akun " +
                    f"set nama_toko = \"{request.form['nama_toko']}\"" +
                    f" where id = {request.form['id']};"
                )
            if 'alamat' in request.form:
                db.execute(
                    "update akun " +
                    f"set alamat = \"{request.form['alamat']}\"" +
                    f" where id = {request.form['id']};"
                )
            if 'no_telp' in request.form:
                db.execute(
                    "update akun " +
                    f"set no_telp = \"{request.form['no_telp']}\"" +
                    f" where id = {request.form['id']};"
                )
            if 'foto' in request.form:
                db.execute(
                    "update akun " +
                    f"set foto = \"{request.form['foto']}\"" +
                    f" where id = {request.form['id']};"
                )
            if 'password' in request.form:
                db.execute(
                    "update akun " +
                    f"set password = \"{hashlib.md5(request.form['password'].encode()).hexdigest()}\"" +
                    f" where id = {request.form['id']};"
                )
            db.commit()
            db.close()
            return "Success"
        
    except Exception as e:
        print(e)

    db.close()
    return "Error", 400

@app.route('/kurir', methods = ['GET','POST','PATCH'])
def kurir():
    try:
        if request.method == 'GET': # Handle get info
            db = connect_db()
            if 'id' in request.values:
                query = db.execute(
                    f"select * from kurir where id = {request.values['id']};"
                )
            elif 'akun' in request.values:
                query = db.execute(
                    f"select * from kurir where akun = {request.values['akun']};"
                )
            else:
                raise Exception('No ID')
            data = query.fetchall()
            db.close()
            if 'id' in request.values:
                if len(data) < 1:
                    return "Not found", 404
                data = data[0]
                return {
                    'id': data[0],
                    'akun': data[1],
                    'nama': data[2],
                    'nopol': data[3],
                    'no_telp': data[4],
                    'status': data[5],
                    'foto': data[6],
                    'jk': data[7]
                }
            else:
                dataList = []
                for k in data:
                    dataList.append(
                        {
                            'id': k[0],
                            'akun': k[1],
                            'nama': k[2],
                            'nopol': k[3],
                            'no_telp': k[4],
                            'status': k[5],
                            'foto': k[6],
                            'jk': k[7]
                        }
                    )
                return dataList
            
        elif request.method == 'POST': # Handle new kurir
            db = connect_db()
            query = db.execute(f"insert into kurir (akun, nama, nopol, no_telp, status, foto, jk) values ('{request.form['akun']}', '{request.form['nama']}', '{request.form['nopol']}', '{request.form['no_telp']}', '{request.form['status']}', '{request.form['foto']}', '{request.form['jk']}')")
            db.commit()
            db.close()
            return "Success", 201
        
        elif request.method == 'PATCH': # Handle kurir updates
            db = connect_db()
            if 'id' not in request.form:
                raise Exception("No ID supplied")
            if 'nama' in request.form:
                db.execute(
                    "update kurir " +
                    f"set nama = \"{request.form['nama']}\"" +
                    f" where id = {request.form['id']};"
                )
            if 'nopol' in request.form:
                db.execute(
                    "update kurir " +
                    f"set nopol = \"{request.form['nopol']}\"" +
                    f" where id = {request.form['id']};"
                )
            if 'status' in request.form:
                db.execute(
                    "update kurir " +
                    f"set status = {request.form['status']}" +
                    f" where id = {request.form['id']};"
                )
            if 'no_telp' in request.form:
                db.execute(
                    "update kurir " +
                    f"set no_telp = \"{request.form['no_telp']}\"" +
                    f" where id = {request.form['id']};"
                )
            if 'foto' in request.form:
                db.execute(
                    "update kurir " +
                    f"set foto = \"{request.form['foto']}\"" +
                    f" where id = {request.form['id']};"
                )
            if 'jk' in request.form:
                db.execute(
                    "update kurir " +
                    f"set jk = {request.form['jk']}" +
                    f" where id = {request.form['id']};"
                )
            db.commit()
            db.close()
            return "Success"
        
    except Exception as e:
        print(e)

    db.close()
    return "Error kurir", 400

@app.route('/paket', methods = ['GET','POST','PATCH'])
def paket():
    try:
        if request.method == 'GET': # Handle get info
            db = connect_db()
            if 'id' in request.values: # Get one
                query = db.execute(
                    f"select * from paket where id = {request.values['id']};"
                )
            elif 'akun' in request.values: # Get all
                query = db.execute(
                    f"select * from paket where akun = {request.values['akun']};"
                )
            else:
                raise Exception('No ID')
            data = query.fetchall()
            db.close()
            if 'id' in request.values:
                if len(data) < 1:
                    return "Not found", 404
                data = data[0]
                return {
                    'id': data[0],
                    'akun': data[5],
                    'nama': data[1],
                    'bunga': data[6],
                    'alamat': data[2],
                    'no_telp': data[3],
                    'kurir': data[7],
                    'status': data[4]
                }
            else:
                dataList = []
                for k in data:
                    dataList.append(
                        {
                            'id': k[0],
                            'akun': k[5],
                            'nama': k[1],
                            'bunga': k[6],
                            'alamat': k[2],
                            'no_telp': k[3],
                            'kurir': k[7],
                            'status': k[4]
                        }
                    )
                return dataList
            
        elif request.method == 'POST': # Handle new paket
            db = connect_db()
            # get kurir for paket
            query = db.execute(f"select id from kurir where akun = '{request.form['akun']}';")
            data = query.fetchall()
            if len(data) < 1:
                raise Exception("No kurir")
            k = random.choice(data)[0]

            query = db.execute(f"insert into paket (akun, nama, bunga, alamat, no_telp, kurir) values ('{request.form['akun']}', '{request.form['nama']}', '{request.form['bunga']}', '{request.form['alamat']}', '{request.form['no_telp']}', '{k}');")
            db.commit()
            db.close()
            return "Success", 201
        
        elif request.method == 'PATCH': # Handle paket updates
            db = connect_db()
            if 'id' not in request.form:
                raise Exception("No ID supplied")
            if 'status' in request.form:
                db.execute(
                    "update paket " +
                    f"set status = {request.form['status']}" +
                    f" where id = {request.form['id']};"
                )
            db.commit()
            db.close()
            return "Success"
        
    except Exception as e:
        print(e)

    db.close()
    return "Error paket", 400

@app.route('/bunga', methods = ['GET','POST','PATCH'])
def bunga():
    try:
        if request.method == 'GET': # Handle get info
            db = connect_db()
            if 'id' in request.values:
                query = db.execute(
                    f"select * from bunga where id = {request.values['id']};"
                )
            elif 'akun' in request.values:
                query = db.execute(
                    f"select * from bunga where akun = {request.values['akun']};"
                )
            else:
                raise Exception('No ID')
            data = query.fetchall()
            db.close()
            if 'id' in request.values:
                if len(data) < 1:
                    return "Not found", 404
                data = data[0]
                return {
                    'id': data[0],
                    'akun': data[1],
                    'nama': data[2],
                    'jenis': data[3],
                    'harga': data[4],
                    'komposisi': data[5],
                    'deskripsi': data[6],
                    'foto': data[7]
                }
            else:
                dataList = []
                for k in data:
                    dataList.append(
                        {
                            'id': k[0],
                            'akun': k[1],
                            'nama': k[2],
                            'jenis': k[3],
                            'harga': k[4],
                            'deskripsi': k[5],
                            'komposisi': k[6],
                            'foto': k[7]
                        }
                    )
                return dataList
            
        elif request.method == 'POST': # Handle new bunga
            db = connect_db()
            query = db.execute(f"insert into bunga (akun, nama, jenis, harga, deskripsi, komposisi, foto) values ('{request.form['akun']}', '{request.form['nama']}', '{request.form['jenis']}', {request.form['harga']}, '{request.form['deskripsi']}', '{request.form['komposisi']}', '{request.form['foto']}');")
            db.commit()
            db.close()
            return "Success", 201
        
        elif request.method == 'PATCH': # Handle kurir updates
            db = connect_db()
            if 'id' not in request.form:
                raise Exception("No ID supplied")
            if 'nama' in request.form:
                db.execute(
                    "update bunga " +
                    f"set nama = \"{request.form['nama']}\"" +
                    f" where id = {request.form['id']};"
                )
            if 'jenis' in request.form:
                db.execute(
                    "update bunga " +
                    f"set jenis= \"{request.form['jenis']}\"" +
                    f" where id = {request.form['id']};"
                )
            if 'harga' in request.form:
                db.execute(
                    "update bunga " +
                    f"set harga = {request.form['harga']}" +
                    f" where id = {request.form['id']};"
                )
            if 'komposisi' in request.form:
                db.execute(
                    "update bunga " +
                    f"set komposisi = \"{request.form['komposisi']}\"" +
                    f" where id = {request.form['id']};"
                )
            if 'deskripsi' in request.form:
                db.execute(
                    "update bunga " +
                    f"set deskripsi = \"{request.form['deskripsi']}\"" +
                    f" where id = {request.form['id']};"
                )
            if 'foto' in request.form:
                db.execute(
                    "update bunga " +
                    f"set foto = \"{request.form['foto']}\"" +
                    f" where id = {request.form['id']};"
                )
            db.commit()
            db.close()
            return "Success"
        
    except Exception as e:
        print(e)

    db.close()
    return "Error bunga", 400
  
if __name__=='__main__': 
    app.run(debug=True)