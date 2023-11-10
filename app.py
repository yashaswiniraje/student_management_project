
from flask import Flask, render_template, request, redirect, url_for, session

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "yashaswini24"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Yashaswiniraje@localhost:3306/students'
db = SQLAlchemy(app)

class Students(db.Model):
    First_Name = db.Column(db.String(20), unique=False)
    Last_Name = db.Column(db.String(20), unique=False)
    DEPARTMENT = db.Column(db.String(20), unique=False)
    EVENT = db.Column(db.String(20), unique=False)
    Email_id = db.Column(db.String(40), unique=False)
    tele = db.Column(db.Integer(), primary_key=True)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/datalist")
def datalist():
    # query all students from the database
    students = Students.query.all()

    # pass the list of students to the template
    return render_template('datalist.html', students=students)



@app.route("/form", methods=['GET', 'POST'])
def StuInfo():
    if request.method == 'POST':
        'add entry to DB'

        First_Name = request.form.get('First_Name')
        Last_Name = request.form.get('Last_Name')
        DEPARTMENT = request.form.get('DEPARTMENT')
        EVENT = request.form.get('EVENT')
        Email_id = request.form.get('Email_id')
        tele = request.form.get("tele")

        entry = Students(First_Name=First_Name, Last_Name=Last_Name, DEPARTMENT=DEPARTMENT, EVENT=EVENT,
                         Email_id=Email_id, tele=tele)
        db.create_all()
        db.session.add(entry)
        db.session.commit()
    return render_template('form.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'yashaswini' and password == 'Pass@2002':
            session["email"] = username
            return redirect(url_for('datalist'))
        else:
            msg = "Invalid username"
            return render_template('login.html', msg=msg)

    return render_template('login.html')


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))
@app.route ('/datalist/update/<int:tele>', methods=['GET', 'POST'])
def update(tele):
    entry = Students.query.get(tele)
    if request.method == 'POST':
        entry.First_Name = request.form.get('First_Name')
        entry.Last_Name = request.form.get('Last_Name')
        entry.DEPARTMENT = request.form.get('DEPARTMENT')
        entry.EVENT = request.form.get('EVENT')
        entry.Email_id = request.form.get('Email_id')
        entry.tele = request.form.get('tele')
        db.session.commit()
        return redirect(url_for('datalist'))
    return render_template('update.html',entry=entry)

@app.route("/datalist/delete/<int:tele>", methods=["POST"])
def delete(tele):
    entry = Students.query.get(tele)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('datalist'))




if __name__ == "__main__":
    app.run(debug=True)


