from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 
from flask_restful import Resource, Api 

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Student(db.Model):
	student_id = db.Column(db.Integer, primary_key = True)
	first_name = db.Column(db.String(32))
	last_name = db.Column(db.String(32))
	dob = db.Column(db.String(32))
	amount_due = db.Column(db.Integer)

	def __init__(self, student_id, first_name, last_name, dob, amount_due):
		self.student_id = student_id
		self.first_name = first_name
		self.last_name = last_name
		self.dob = dob
		self.amount_due = amount_due

class StudentSchema(ma.Schema):
	class Meta:
		fields = ('student_id', 'first_name', 'last_name', 'dob', 'amount_due')

student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

class StudentManager(Resource):

	# Show student records in the database
	@staticmethod
	def get():
		# Show a specific record by providing a student_id
		try:
			id = request.args['student_id']
		except Exception as _: id = None
		# If no student_id is provided, show all records
		if not id:
			students = Student.query.all()
			return jsonify(students_schema.dump(students))
		# Show student record by student_id
		student = Student.query.get(id)
		return jsonify(student_schema.dump(student))

	# Create a student record in the database
	@staticmethod
	def post():
		student_id = request.json['student_id']
		first_name = request.json['first_name']
		last_name = request.json['last_name']
		dob = request.json['dob']
		amount_due = request.json['amount_due']

		student = Student(student_id, first_name, last_name, dob, amount_due)
		db.session.add(student)
		db.session.commit()

		return jsonify({'Message': f'Student {first_name} {last_name} created.'})

	# Update a student record
	@staticmethod
	def put():
		try:
			id = request.args['student_id']
		except Exception as _: id = None 
		# If no student_id is provided, return an error
		if not id:
			return jsonify({'Message': 'Must provide the student ID you wish to update.'})

		student = Student.query.get(id)
		first_name = request.json['first_name']
		last_name = request.json['last_name']
		dob = request.json['dob']
		amount_due = request.json['amount_due']

		student.first_name = first_name
		student.last_name = last_name
		student.dob = dob
		student.amount_due = amount_due

		db.session.commit()
		return jsonify({'Message': f'Student {first_name} {last_name} updated.'})

	# Delete a student record
	@staticmethod
	def delete():
		try:
			id = request.args['student_id']
		except Exception as _: id = None

		if not id:
			return jsonify({'Message': 'Must provide the student ID you wish to delete.'})

		student = Student.query.get(id)
		db.session.delete(student)
		db.session.commit()
		return jsonify({'Message': f'Student {str(id)} deleted.'})

api.add_resource(StudentManager, '/api/students')

if __name__ == '__main__':
	app.run(debug=True)