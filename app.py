from flask import Flask, render_template , request , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo1.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer , primary_key=True)
    title = db.Column(db.String(200) , nullable=False)
    desc = db.Column(db.String(500) , nullable=False)
    created_date = db.Column(db.DateTime , default=datetime.utcnow )
    mark = db.Column(db.Boolean , nullable = False)

    def __repr__(self) -> str:
        return f"{self.title} : {self.desc}"
    
with app.app_context():
    db.create_all()    

@app.route('/' , methods = ['POST' , 'GET'])
def hello():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['Description']
        mark = False
        todo = Todo(title = title , desc = desc , mark = False)
        db.session.add(todo)
        db.session.commit()

    alltodo = Todo.query.all()
    return render_template('index.html' , alltodo=alltodo)

@app.route('/dele/<int:sno>' , methods = ['GET'] )
def dele(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/update_todo/<int:sno>' , methods = ['GET','POST'])
def upd(sno):
    if request.method == 'POST':
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = request.form['title']
        todo.desc = request.form['description']
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('upd.html' , todo=todo)

@app.route('/insert_todo' , methods = ['POST' , 'GET'])
def insert():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['description']
        mark = False
        todo = Todo(title = title , desc = desc , mark = mark)
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    return render_template('insert.html')

@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == '__main__':
    app.run(debug = True , port = 8000)