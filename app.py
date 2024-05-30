import base64
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Sequence
from sqlalchemy.types import Date, CLOB
from datetime import date
import face_recognition
from PIL import Image
from io import BytesIO
import numpy as np
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle+cx_oracle://FACE_OWNER:ftp2023@192.168.1.251:1521/?service_name=orcl'
db = SQLAlchemy(app)

class Face(db.Model):
  __tablename__ = 'TBL_FACE'
  id = db.Column(db.Integer, Sequence('tbl_face_id_seq'), primary_key=True)
  matrix = db.Column(CLOB, nullable=False)
  type = db.Column(db.String(2), nullable=False)
  tbl_id = db.Column(db.Integer, nullable=False)
  des = db.Column(db.String(500), nullable=True)
  createdate = db.Column(Date, nullable=False)

  def __repr__(self):
    return f'<Face {self.id}>'
  
def get_face_from_img (file):
  image_data = file.read()
  if not image_data:
    raise ValueError("Image reading failed.") 

  # Sử dụng BytesIO để tạo một đối tượng IO từ dữ liệu ảnh
  image = Image.open(BytesIO(image_data))
  image = image.convert('RGB')

  image_np = np.array(image)
  face_arr = face_recognition.face_encodings(image_np)[0]
  return face_arr

def get_face_json (file):
  face_arr = get_face_from_img(file) 
  face_list = face_arr.tolist()
  face_json = json.dumps(face_list)
  return face_json

@app.route('/face', methods=['POST'])
def addFace():
  file = request.files.get('file')
  if not file:
    return jsonify({"error": "No file selected"}), 400
  
  if file:
    try:
      new_record = Face(
        matrix=get_face_json(file),
        type='0',
        tbl_id=123,
        des=file.filename,
        createdate=date.today()
      )
      db.session.add(new_record)
      db.session.commit()
      return jsonify({"message": "Add face successfully"}), 201
    except Exception as e:
      return f"An error occurred: {str(e)}", 500

@app.route('/check-face', methods=['POST'])
def checkFace():
  """
  Truyền vào type và một ảnh (file)
  Kiểm tra xem ảnh đó có khớp với dữ liệu trong DB không
  """
  file = request.files.get('file')
  file_type = request.form.get('type')
 
  if not file:
    return jsonify({"error": "No file part"}), 400
  if not file_type:
    return jsonify({"error": "No 'type' field"}), 400
  
  faces_by_type = Face.query.filter_by(type=file_type).all()
  known_face_encodings = []

  try:
    for face in faces_by_type:
      face_list = json.loads(face.matrix)
      face_arr = np.array(face_list)
      known_face_encodings.append(face_arr)

    match = face_recognition.compare_faces(known_face_encodings, get_face_from_img(file))
    message = "Ảnh khớp" if match[0] else "Ảnh không khớp"
    return jsonify({"message": message}), 200
  
  except Exception as e:
    return jsonify({'error': str(e)})