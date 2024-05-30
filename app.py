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
  
def base64_to_mat(base64_string):
  image_data = base64.b64decode(base64_string)
  image = Image.open(BytesIO(image_data))
  image_np = np.array(image)
  return image_np
  
@app.route('/face', methods=['POST'])
def addFace():
  file = request.files.get('file')
  if not file:
    return jsonify({"error": "No file selected"}), 400
  
  if file:
    try:
      file_content = file.read()
      base64_file = base64.b64encode(file_content).decode('utf-8')

      image = base64_to_mat(base64_file)
      face_id = face_recognition.face_encodings(image)[0]
      face_id = str(face_id)

      new_record = Face(
        matrix=face_id,
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

@app.route('/face_match', methods=['POST'])
def addFace():
  file = request.files.get('file')
  file_type = request.form.get('type')
 
  if not file:
    return jsonify({"error": "No file part"}), 400
  if not file_type:
    return jsonify({"error": "No 'type' field"}), 400

  return jsonify({"message": "Request success"}), 200