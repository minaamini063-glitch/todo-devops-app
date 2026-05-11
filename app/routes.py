from flask import Blueprint, render_template, request, redirect, jsonify
from .models import Todo
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)

@main.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    description = request.form.get('description')

    if title:
        todo = Todo(title=title, description=description)
        db.session.add(todo)
        db.session.commit()

    return redirect('/')

@main.route('/complete/<int:id>')
def complete(id):
    todo = Todo.query.get_or_404(id)
    todo.completed = not todo.completed
    db.session.commit()

    return redirect('/')

@main.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()

    return redirect('/')

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    todo = Todo.query.get_or_404(id)

    if request.method == 'POST':
        todo.title = request.form['title']
        todo.description = request.form['description']

        db.session.commit()
        return redirect('/')

    return render_template('edit.html', todo=todo)

@main.route('/api/todos')
def api_todos():
    todos = Todo.query.all()
    return jsonify([todo.to_dict() for todo in todos])