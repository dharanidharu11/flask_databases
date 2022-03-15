from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class StudentModel(db.Model):
    __tablename__ = "student"

    student_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    marks = db.Column(db.Integer())
    major = db.Column(db.String(80))

    def __repr__(self):
        return f"{self.name}:{self.student_id}"


from flask import Flask, render_template, request, redirect
from model import db, StudentModel

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()


@app.route('/data/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')

    if request.method == 'POST':
        name = request.form['name']
        marks = request.form['marks']
        major = request.form['major']
        student = StudentModel(name=name, marks=marks, major=major)
        db.session.add(student)
        db.session.commit()
        return redirect('/data')


@app.route('/data')
def RetrieveList():
    students = StudentModel.query.all()
    return render_template('datalist.html', students=students)


@app.route('/data/<int:id>')
def RetrieveStudent(id):
    student = StudentModel.query.filter_by(student_id=id).first()
    if student:
        return render_template('data.html', student=student)
    return f"Student with id ={id} Doenst exist"


@app.route('/data/<int:id>/update', methods=['GET', 'POST'])
def update(id):
    student = StudentModel.query.filter_by(student_id=id).first()
    if request.method == 'POST':
        if student:
            db.session.delete(student)
            db.session.commit()
            name = request.form['name']
            marks = request.form['marks']
            major = request.form['major']
            student = StudentModel(student_id=id, name=name, marks=marks, major=major)
            db.session.add(student)
            db.session.commit()
            return redirect(f'/data/{id}')
        return f"Student with id = {id} Does not exist"

    return render_template('update.html', student=student)


@app.route('/data/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    student = StudentModel.query.filter_by(student_id=id).first()
    if request.method == 'POST':
        if student:
            db.session.delete(student)
            db.session.commit()
            return redirect('/data')
        abort(404)

    return render_template('delete.html')

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True )
