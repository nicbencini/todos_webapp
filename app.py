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
    get_list_index_by_id,
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
    return render_template('lists.html', lists=session['lists'])

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
    idx = get_list_index_by_id(list_id, session['lists'])

    if not idx:
        exceptions.NotFound('List not found!') 
    
    lst = session['lists'][idx]

    return render_template('list.html', lst=lst )

@app.route("/lists/<list_id>/todos", methods=["POST"])
def create_todo(list_id):
    todo_title = request.form["todo"].strip()
    idx = get_list_index_by_id(list_id, session['lists'])

    if not idx:
        exceptions.NotFound('List not found!') 
    
    lst = session['lists'][idx]

    error = error_for_todo_title(todo_title)
    if error:
        flash(error, "error")
        return render_template('list.html', lst=lst)

    
    session['lists'][idx]['todos'].append({
        'id' : str(uuid4()),
        'title' : todo_title,
        'completed' : False
    })

    flash("The todo has been created.", "success")
    session.modified = True
    return redirect(url_for('show_list', list_id=list_id))

""" WIP
@app.route("/lists/<list_id>/todos/<todo_id>/toggle")
def delete_todo(list_id, todo_id):
    idx = get_list_index_by_id(list_id, session['lists'])

    if not idx:
        exceptions.NotFound('List not found!') 
    
    lst = session['lists'][idx]

"""



if __name__ == "__main__":
    app.run(debug=True, port=5003)