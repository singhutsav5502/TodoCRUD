from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
app.app_context().push()


class todos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Make sure they can't leave the content of the task empty
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        taskContent = request.form['content']
        newTask = todos(content=taskContent)

        try:
            db.session.add(newTask)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error faced while adding your Task'
    else:
        tasks = todos.query.order_by(todos.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    taskToDelete = todos.query.get_or_404(id)

    try:
        db.session.delete(taskToDelete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = todos.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an Error updating your task'
    else:
        return render_template('update.html', task=task)

@app.route('/get' , methods=['GET'])
def get():
    id = int(request.args.get('queryID'))
    
    if request.method=="GET":
        task = todos.query.get_or_404(id)
        return render_template('get.html', task = task)
    else:
        redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
