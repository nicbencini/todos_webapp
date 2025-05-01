from uuid import uuid4

from werkzeug import exceptions

from flask import (
    flash,
    Flask,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from todos.utils import (
    error_for_list_title,
    error_for_todo_title, 
    get_list_by_id, 
    get_todo_by_id,
    todos_remaining,
    is_list_completed,
    is_todo_completed,
    sort_items    
    )

app = Flask(__name__)
app.secret_key = 'secret1'

@app.before_request
def intialize_session():
    if 'lists' not in session:
        session['lists'] = []

@app.route("/")
def index():
    return redirect(url_for('get_lists'))

@app.route("/lists/new")
def add_todo_list():
    return render_template("new_list.html")

# Render the list of todo lists
@app.route("/lists")
def get_lists():
    lists = sort_items(session['lists'], is_list_completed)
    return render_template('lists.html',
                           lists=lists,
                           todos_remaining=todos_remaining)

@app.route("/lists", methods=["POST"])
def create_list():
    title = request.form["list_title"].strip()
    
    error = error_for_list_title(title, session['lists'])
    if error:
        flash(error, "error")
        return render_template('new_list.html', title=title)
        
    session['lists'].append({
        'id': str(uuid4()),
        'title': title,
        'todos': [],
    })

    flash("The list has been created.", "success")
    session.modified = True
    return redirect(url_for('get_lists'))
  
@app.route("/lists/<list_id>")
def show_list(list_id):
    lst = get_list_by_id(list_id, session['lists'])

    if not lst:
        exceptions.NotFound('List not found!') 
    
    lst['todos'] = sort_items(lst['todos'], is_todo_completed)
    return render_template('list.html', lst=lst)

@app.route("/lists/<list_id>/todos", methods=["POST"])
def create_todo(list_id):
    todo_title = request.form["todo"].strip()
    lst = get_list_by_id(list_id, session['lists'])

    if not lst:
        exceptions.NotFound('List not found!') 
    
    error = error_for_todo_title(todo_title)
    if error:
        flash(error, "error")
        return render_template('list.html', lst=lst)

    
    lst['todos'].append({
        'id' : str(uuid4()),
        'title' : todo_title,
        'completed' : False
    })

    flash("The todo has been created.", "success")
    session.modified = True
    return redirect(url_for('show_list', list_id=list_id))


@app.route("/lists/<list_id>/todos/<todo_id>/toggle", methods=["POST"])
def update_todo(list_id, todo_id):
    lst = get_list_by_id(list_id, session['lists'])

    if not lst:
        exceptions.NotFound('List not found!') 
    
    todo_lst = lst['todos']

    todo = get_todo_by_id(todo_id, todo_lst)

    if not todo:
        exceptions.NotFound('Todo not found!') 

    if todo['completed'] == True:
        todo['completed'] = False
    else:
        todo['completed'] = True  

    flash("The todo has been completed.", "success")
    session.modified = True

    return redirect(url_for('show_list', list_id=list_id))


@app.route("/lists/<list_id>/todos/<todo_id>/delete", methods=["POST"])
def delete_todo(list_id, todo_id):
    lst = get_list_by_id(list_id, session['lists'])

    if not lst:
        exceptions.NotFound('List not found!') 
    
    todo_lst = lst['todos']

    todo = get_todo_by_id(todo_id, todo_lst)

    if not todo:
        exceptions.NotFound('Todo not found!') 

    todo_lst.remove(todo)

    flash("The todo has been deleted.", "success")
    session.modified = True

    return redirect(url_for('show_list', list_id=list_id))

@app.route("/lists/<list_id>/complete_all", methods=["POST"])
def complete_all_todo(list_id):
    lst = get_list_by_id(list_id, session['lists'])

    if not lst:
        exceptions.NotFound('List not found!') 
    
    todo_lst = lst['todos']

    for todo in todo_lst:
        todo['completed'] = True

    flash("All todos have been completed!", "success")
    session.modified = True

    return redirect(url_for('show_list', list_id=list_id))

@app.route("/lists/<list_id>/edit")
def edit_list(list_id):

    lst = get_list_by_id(list_id, session['lists'])

    if not lst:
        exceptions.NotFound('List not found!') 
    
    return render_template('edit_list.html', lst=lst )

@app.route("/lists/<list_id>/delete", methods=["POST"])
def delete_list(list_id):
    lst = get_list_by_id(list_id, session['lists'])

    if not lst:
        exceptions.NotFound('List not found!')
    
    session['lists'].remove(lst)
    flash("List has been deleted!", "success")
    session.modified = True

    return redirect(url_for('get_lists'))

@app.route("/lists/<list_id>/edit_title", methods=["POST"])
def edit_list_title(list_id):
    lst = get_list_by_id(list_id, session['lists'])

    if not lst:
        exceptions.NotFound('List not found!')
    
    title = request.form["list_title"].strip()
    
    error = error_for_list_title(title, session['lists'])
    if error:
        flash(error, "error")
        return render_template('edit_list.html', lst=lst)
    
    lst['title'] = title
    flash("List title has been updated!", "success")
    session.modified = True

    return redirect(url_for('show_list', list_id=list_id))

@app.context_processor
def list_utilities_processor():
    return dict(
        is_list_completed=is_list_completed,
    )




if __name__ == "__main__":
    app.run(debug=True, port=5003)