from flask import (Flask, request, jsonify)
from flask_cors import CORS
from sqlalchemy import MetaData, create_engine, and_, ForeignKey
from sqlalchemy.exc import OperationalError
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Aspire@localhost/Admin_panel"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
cors = CORS(app)


class Students(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    department_id = db.Column(db.Integer, ForeignKey(
        'department.department_id'), nullable=False)
    department = db.relationship('Departments', backref=db.backref('student', lazy=True))



def __init__(self, username, email, department_id):
    self.username = username
    self.email = email
    self.department_id = department_id


class Departments(db.Model):
    __tablename__ = 'department'
    department_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    department_name = db.Column(db.String(100), unique=True, nullable=False)
    HOD_of_Department = db.Column(db.String(150), nullable=False)


def __init__(self, department_name, HOD_of_Department):
    self.department_name = department_name
    self.HOD_of_Department = HOD_of_Department


with app.app_context():
    db.create_all()
#


def database_exists(db_uri):
    try:
        engine = create_engine(db_uri)
        engine.connect()
        return True
    except OperationalError:
        return False


@app.route('/', methods=['GET'])
def handle_route():
    return jsonify({'Server': 'Active and Running'})


@app.route("/create_student", methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        email = data.get('email')
        department = data.get('department_id')
        username = data.get('username')
        student_Exist = db.session.query(Students).filter_by(email=email).all()
        if student_Exist:
            db.session.close()
            return jsonify({'Message': "Student already exist"})
        student = Students(username=username, email=email,
                           department_id=department)
        db.session.add(student)
        db.session.commit()
        
        return jsonify({'Message': 'Student Created Successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)})


@app.route("/get_students", methods=['GET'])
def get_users():
    try:
        students = db.session.query(Students).all()
        students_list = []
        for student in students:
            # Convert each Student object to a dictionary
            student_data = {
                'id': student.id,
                'name': student.username,
                'email': student.email,
                'department_id': student.department_id
            }
            students_list.append(student_data)
        db.session.close()
        return jsonify(students_list)
    except Exception as e:
        return jsonify({'error': str(e)}, 500)


@app.route("/get_student/<int:id>", methods=['GET'])
def get_student(id):
    try:
        student_object = db.session.query(Students).filter_by(id=id).all()
        student = []
        for student_ in student_object:
            studen = {
                'id': student_.id,
                'name': student_.username,
                'email': student_.email,
                'department': student_.department_id
            }
            student.append(studen)
            db.session.close()
        return jsonify(student)
    except Exception as e:
        return jsonify({"MessageError": str(e)})


@app.route("/update_student/<int:id>", methods=['PUT'])
def update_student(id):
    try:
        data = request.get_json()
        email = data.get('email')
        department = data.get('department')
        username = data.get('name')
        is_student_exist_with_email = db.session.query(Students).filter(
            and_(Students.id != id, Students.email == email))
        if is_student_exist_with_email:
            db.session.close()
            return jsonify({'Message': 'Another Student Already existed with this email, Duplicate email'})
        student = db.session.query(Students).get(id)
        student.email = email
        student.username = username
        student.department = department
        db.session.commit()
        return jsonify({"Message": "Student updated successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({'messageError': str(e)})


@app.route("/delete_student/<int:id>", methods=['DELETE'])
def delete_student(id):
    try:
        student = db.session.query(Students).get(id)
        db.session.delete(student)
        db.session.commit()
        return jsonify({'Message': "Student Deleted Successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({'MessageError': str(e)})


@app.route("/delete_all_students", methods=['DELETE'])
def delete_all_students():
    try:
        all_students = db.session.query(Students).all()
        for student in all_students:
            db.session.delete(student)
        db.session.commit()
        return jsonify({'Message': "Successfully deleted"})
    except Exception as e:
        db.session.rollback()
        return jsonify({'MessageError': str(e)})

@app.route("/create_dep", methods=['POST'])
def create_dep():
    try:
        data = request.get_json()
        department_name = data.get('department_name')
        department_id = data.get('department_id')
        HOD_of_Department = data.get('HOD_of_Department')
        print(1)
        # department_existed = db.session.query(Departments).get(department_id)
        print(2)
        # if department_existed:
        #     return jsonify({'Message': 'Department already exist'}).status_code(208)
        print(3)
        department = Departments(department_id=department_id, department_name=department_name, HOD_of_Department=HOD_of_Department)
        print(4)
        db.session.add(department)
        db.session.commit()
        db.session.close()
        print(5)
        return jsonify({'Message': 'Department created Successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'MessageError': str(e)})
    
@app.route("/get_departments", methods=['GET'])
def get_departments():
    try:
        departments = db.session.query(Departments).all()
        departments_list = []
        for department in departments:
            single_department={
                'department_id': department.department_id,
                'department_name': department.department_name,
                'HOD_of_Department': department.HOD_of_Department
            }
            departments_list.append(single_department)
        db.session.close()
        return jsonify(departments_list)
    except Exception as e:
        return jsonify({'MessageError': str(e)})

@app.route("/delete_dep/<int:id>", methods=['DELETE'])
def delete_dep(id):
    try:
        department = db.session.query(Departments).get(id)
        if department:
            db.session.delete(department)
            db.session.commit()
            return "success"
        else:
            return "Not found"
    except Exception as e:
        return 'k'


if __name__ == '__main__':
    app.run(debug=True)

#
#                             To run this app use below command
#
# `flask --app hello run --debug`
#
