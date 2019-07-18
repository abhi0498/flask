from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        taskC = request.form['content']
        todo = Todo(content=taskC)

        try:
            db.session.add(todo)
            db.session.commit()
            return redirect('/')
        except:
            print("no")

    else:
        task = Todo.query.order_by(Todo.date).all()
        return render_template('index.html', tasks=task)


@app.route('/delete/<int:id>')
def delete(id):
    task_id = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_id)
        db.session.commit()
        return redirect('/')

    except:
        return("error")


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):

    task_id = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task_id.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return"no"
    else:
        return render_template('update.html', task=task_id)


if __name__ == "__main__":
    app.run()
