import base64
from io import BytesIO
from PIL import Image
import face_recognition
from flask import Flask, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import ast
from sqlalchemy import Sequence
import cx_Oracle
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@127.0.0.1/face_id'
# lib_dir=r"C:\oracle\instantclient_21_13"
# cx_Oracle.init_oracle_client(lib_dir=lib_dir)
app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle+cx_oracle://FACE_OWNER:ftp2023@192.168.1.251:1521/?service_name=orcl'
db = SQLAlchemy(app)

passed = False
user_id = 0
success = False
face_id = []
#create database
class User(db.Model):
    id = db.Column(db.Integer, Sequence('user_id_seq'), primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    face_id = db.Column(db.String(2500), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

# with app.app_context():
#     db.create_all()

def load_image_from_base64(base64_string):
    image_data = base64.b64decode(base64_string)
    
    image = Image.open(BytesIO(image_data))
    
    image_np = np.array(image)
    
    return image_np

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Check if the POST request has the file part
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        
        if file:
            try:
                # Read the image file and encode it to base64
                image = Image.open(file)
                image = image.convert('RGB')
                buffered = BytesIO()
                image.save(buffered, format="JPEG")
                base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

                image = load_image_from_base64(base64_image)
               
                face_id = face_recognition.face_encodings(image)[0]
                face_id = str(face_id)
                # print(face_id)
                
                name = request.form.get('name')
                password = request.form.get('password')
                if not name:
                    return jsonify({'error': 'Name is required'}), 400

                new_user = User(username=name, face_id=face_id, password=password)
                db.session.add(new_user)
                db.session.commit()

                return jsonify({"success": "Đăng ký thành công"})
            except Exception as e:
                return jsonify({'error': str(e)})
    
    return '''
    <!doctype html>
    <title>Face id</title>
    <h1>Điền thông tin của bạn!</h1>
    <style>
        * {
            margin: 5px;
        }
    </style>
    <form method="POST" enctype="multipart/form-data">
        <label for="name">username:</label>
        <input type="text" name="name" required><br>
        <label for="password">password:</label>
        <input type="text" name="password" required><br>
        <input type="file" name="file" required><br>
        <input type="submit" value="Upload">
    </form>
    '''

@app.route('/', methods=['GET', 'POST'])
def home():
    if success:
        return "Đã đăng nhập thành công"

    return '''
    <a href="/signin">Sign in</a>
    <a href="/signup">Sign up</a>
    '''

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    global passed, id, face_id

    if request.method == 'POST':  
        try:
            name = request.form.get('name')
            password = request.form.get('password')
            face_from_sql = User.query.filter_by(username=name, password=password).first()
            
            if face_from_sql:
                passed = True
                id = face_from_sql.id
                face_id = face_from_sql.face_id
                return redirect(url_for('signin_image'))
                
            else:
                return jsonify({"error": "sai mật khẩu hoặc username"})

        except Exception as e:
            return jsonify({'error': str(e)})
    return '''
    <style>
        * {
            margin: 5px;
        }
    </style>
    <form method="POST" enctype="multipart/form-data">
        <label for="name">username:</label>
        <input type="text" name="name" required><br>
        <label for="password">password:</label>
        <input type="text" name="password" required><br>
        <input type="submit" value="Đăng nhập">
    </form>
    '''

@app.route('/signin/image', methods=['GET', 'POST'])
def signin_image():
    if passed:
        global face_id, success
        if request.method == 'POST':
            if 'file' not in request.files:
                return jsonify({'error': 'No file part'})
            
            file = request.files['file']
            
            if file.filename == '':
                return jsonify({'error': 'No selected file'})
        
            if file:
                # Read the image file and encode it to base64
                image = Image.open(file)
                image = image.convert('RGB')
                buffered = BytesIO()
                image.save(buffered, format="JPEG")
                base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

                image = load_image_from_base64(base64_image)
                face_check_id = face_recognition.face_encodings(image)[0]

                face = face_id.strip('[]')
                array_elements = face.split()

                array_elements = [np.float64(element) for element in array_elements]

                face_id_sql = np.array(array_elements)
                # print(type(face_id))
                match = face_recognition.compare_faces([face_id_sql], face_check_id)

                if match[0]:
                    success = True
                    return redirect(url_for('home'))

                else: return "Ảnh không khớp"
                
    else: return "Bạn chưa đăng nhập"
    
    return '''
    <style>
    * {
        margin: 5px;
    }
    </style>
    <form method="POST" enctype="multipart/form-data">
        <input id="avatar" type="file" name="file" required><br>
        <input type="submit" value="Xác minh avatar">
    </form>
    '''
