import json
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
from flask_sqlalchemy import SQLAlchemy
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"
 
db = SQLAlchemy(app)
 
# model
class Students(db.Model):
    id = db.Column('student_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
 
    def __init__(self, name, city):
        self.name = name
        self.city = city
# model

@app.route('/students/', methods = ['GET', 'POST','DELETE'])
@app.route('/students/<id>', methods = ['GET', 'POST','DELETE','PUT'])
def crude_students(id=-1):
    if request.method == 'POST':
        request_data = request.get_json()
        # print(request_data['city'])
        city = request_data['city']
        name= request_data["name"]
        newStudent= Students(name,city)
        db.session.add (newStudent)
        db.session.commit()
        return "a new rcord was create"
    if request.method == 'GET':
        res=[]
        for student in Students.query.all():
            res.append({"city":student.city,"id":student.id,"name":student.name})
        return  (json.dumps(res))
    if request.method == 'DELETE': 
        # print(Students.query.filter_by(id=id))
        me=Students.query.get(id)
        db.session.delete(me)
        db.session.commit()
        return {"msg":"row deleted"}
    if request.method == 'PUT': 
        me=Students.query.get(id)
        request_data = request.get_json()
        # print(request_data['city'])
        me.city = request_data['city']
        me.name= request_data["name"]
        db.session.commit()
        return {"msg":"row updated - TADA"}

@app.route('/')
def hello():
    return 'Hello, World!'
 
if __name__ == '__main__':
    with app.app_context():db.create_all()
    app.run(debug = True)
