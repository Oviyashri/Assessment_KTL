from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///employees.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer)
    email = db.Column(db.String(20), unique=True)
    designation = db.Column(db.String(20))
    salary = db.Column(db.Float, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_name = db.Column(db.String(50), nullable=False)
    department_name = db.Column(db.String(30))
    employees = db.relationship('Employee', backref='department')

# 1 API for employee table
@app.route('/employees', methods=['GET'])
def get_employee():
    employees = Employee.query.all()
    get_result = [
        {
            'id': employee.id,
            'employee_name': employee.employee_name,
            'age': employee.age,
            'email': employee.email,
            'designation': employee.designation,
            'salary': employee.salary,
            'department_id': employee.department_id
        } for employee in employees
    ]
    return {'employees': get_result}

@app.route('/employees', methods=['POST'])
def create_employee():
    data = request.json
    employee = Employee(
        employee_name = data.get('employee_name'),
        age = data.get('age'),
        email = data.get('email'),
        designation = data.get('designation'),
        salary = data.get('salary'),
        department_id = data.get('department_id'))
    db.session.add(employee)
    db.session.commit()
    return {'message': 'Employee created successfully'}

@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    employee = Employee.query.get(id)
    if not employee:
        return {'message': 'Employee not found'}, 404

    data = request.json
    employee.employee_name = data.get('employee_name', employee.employee_name)
    employee.age = data.get('age', employee.age)
    employee.email = data.get('email', employee.email)
    employee.designation = data.get('designation', employee.designation)
    employee.salary = data.get('salary', employee.salary)
    employee.department_id = data.get('department_id', employee.department_id)
    db.session.commit()
    return {'message': 'Updated successfully'}

@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
        employee = Employee.query.get(id)
        if not employee:
            return {"message": "Employee not found"}, 404

        db.session.delete(employee)
        db.session.commit()
        return {'message': 'Deleted successfully'}

# 2 API for department table 
@app.route('/departments', methods=['GET'])
def get_departments():
    departments = Department.query.all()
    result = [
        {
            "id": department.id,
            "employee_name": department.employee_name,
            "department_name": department.department_name,
            "employees": [
                {"id": employee.id,
                "employee_name": employee.employee_name,
                "age": employee.age,
                "email": employee.email,
                "designation": employee.designation,
                "salary": employee.salary} for employee in department.employees]
        } for department in departments
        ]
    return {"departments": result}

@app.route('/departments', methods=['POST'])
def create_department():
    data = request.json
    department = Department(
        employee_name=data.get('employee_name'),
        department_name=data.get('department_name'))
    db.session.add(department)
    db.session.commit()
    return {'message': 'Department created successfully'}

@app.route('/departments/<int:id>', methods=['PUT'])
def update_department(id):
    department = Department.query.get(id)
    if not department:
        return {'message': 'Department not found'}, 404

    data = request.json
    department.employee_name = data.get('employee_name', department.employee_name)
    department.department_name = data.get('department_name', department.department_name)
    db.session.commit()
    return {'message': 'Updated successfully'}

# 3 Created new endpoint which takes both in one api and saves in two tables
@app.route('/employee-department', methods=['POST'])
def create_employee_and_department():
    try:
        data = request.json
        department = Department(
            employee_name=data.get('employee_name'),
            department_name=data.get('department_name'))
        db.session.add(department)
        db.session.commit()

        employee = Employee(
            employee_name = data.get('employee_name'),
            age = data.get('age'),
            email = data.get('email'),
            designation = data.get('designation'),
            salary = data.get('salary'),
            department_id = department.id)
        db.session.add(employee)
        db.session.commit()
        return {'message': 'Employee and department both created successfully'}

    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    app.run(debug=True)
