from flask import Flask, render_template, redirect,session, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, RadioField, SelectField, TextAreaField,IntegerField, validators
from wtforms.validators import DataRequired, Length
import os
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__,template_folder="./")
app.config['SECRET_KEY'] = 'gradekey'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

datab = SQLAlchemy(app)

class Student(datab.Model):
    __tablename__ = "students"
    id = datab.Column(datab.Integer, primary_key = True)
    name = datab.Column(datab.Text)
    grade = datab.Column(datab.Text)
    def  __init__(self,name,grade):
        self.name = name
        self.grade = grade
    def __repr__(self):
        return f"{self.id} {self.name} {self.grade}"

class MyForm(FlaskForm):
    St_name = StringField ('Student Name:')
    St_grade = StringField ('Grade:')
    St_id = StringField ('Delete ID:')
#
@app.route('/', methods=['GET','POST'])
def index():
     error = None
     form = MyForm()
     if request.method == 'POST':
        if request.form['submit_btn'] == 'Submit':
            if form.St_name.data == ' ' or form.St_grade.data == ' ':
                error = 'yes'
                return render_template ('home.html',form = form,error = error)
            session['St_name'] = form.St_name.data
            session['St_grade'] = form.St_grade.data
            new_student = Student(session['St_name'],session['St_grade'])
            datab.create_all()
            datab.session.add_all([new_student])
            datab.session.commit()
            form.St_name.data = ' '
            form.St_grade.data = ' '
            return render_template ('home.html', form = form, error =error)
        if request.form['submit_btn'] == 'btn1':
            global btn
            btn = 'btn1'
            return redirect(url_for('studentlist',btn = btn))
        elif request.form['submit_btn'] == 'btn2':
            btn = 'btn2'
            return redirect(url_for('studentlist',btn = btn))
        elif request.form['submit_btn'] == 'Delete':
            id = form.St_id.data
            delete_student = Student.query.get(id)
            datab.session.delete(delete_student)
            datab.session.commit()
            form.St_id.data = None
            return render_template ('home.html', form = form, error =error)
     return render_template ('home.html', form = form)
#
@app.route('/studentlist')
def studentlist():
#
    if (btn == 'btn1'):
        all_students = Student.query.all()
        return render_template ('studentlist.html', studentlist = all_students,type = 'all')
		
    if (btn == 'btn2'):
        print('btn2')
        pass_students = Student.query.filter(Student.grade > 85)
        return render_template ('studentlist.html', studentlist = pass_students.all(),type = 'pass')
#
if __name__ == '__main__':
    app.run(debug=True)
