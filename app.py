from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Sequence
from sqlalchemy.types import Date, CLOB
from datetime import date

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
  
@app.route('/face', methods=['GET', 'POST'])
def addFace():
  if request.method == 'POST':
    new_record = Face(
      matrix='Some large text data',
      type='A1',
      tbl_id=123,
      des='Some description',
      createdate=date.today()
    )
    db.session.add(new_record)
    db.session.commit()
    return "Add face successfully"
  else:
    return "Get all faces"