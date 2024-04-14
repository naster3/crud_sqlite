from flask import Flask, render_template, request, url_for, redirect, flash, Markup
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from data import TaskForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'

db = SQLAlchemy(app)

#tabla
class Task(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    done = db.Column(db.Boolean)
    fecha_creacion= db.Column(db.DateTime, default=datetime.utcnow)
# muestra la app por default
@app.route('/')
def home():
    tasks= Task.query.all()
    return render_template('crud.html', tasks=tasks)
#buscador
@app.route('/get', methods=['GET'])
def get_task():
    search_query = request.args.get('query')
    if search_query:
            try:
                date_query = datetime.strptime(search_query, '%Y-%m-%d').date()
                tasks = Task.query.filter(Task.fecha_creacion.contains(date_query)).all()
            except ValueError:
                tasks = Task.query.filter(Task.content.contains(search_query)).all()
    else:
        tasks = Task.query.all()
    return render_template('crud.html', tasks=tasks)
    
#agregamos tareas
@app.route('/create-task', methods=['POST'])
def create():
    form = TaskForm(request.form)
    if form.validate():
        new_task = Task(content=form.content.data, done=form.done.data, fecha_creacion=form.fecha_creacion.data)
        db.session.add(new_task)
        db.session.commit()
        flash('Tarea creada exitosamente', 'success')
    else:
        flash('Error en la validación de los datos', 'error')
    return redirect(url_for('home'))
# actualizar
@app.route('/done/<id>')
def done(id):
    task = Task.query.filter_by(id=int(id)).first()
    task.done = not (task.done)
    db.session.commit()
    return redirect(url_for('home'))



@app.route('/delete/<id>')
def delete(id):
    Task.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    # Crear todas las tablas definidas en los modelos
    with app.app_context():
        db.create_all()

# Cerrar la aplicación Flask
    db.session.close_all()
    app.app_context().push()
    app.run(debug=True)
