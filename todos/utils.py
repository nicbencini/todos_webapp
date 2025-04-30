

def error_for_list_title(title, lists):
    if any(lst['title'] == title for lst in lists):
        return "The title must be unique."
    elif not 1 <= len(title) <= 100:
        return "The title must be between 1 and 100 characters"
    else:
        return None

def error_for_todo_title(title):
    if not 1 <= len(title) <= 100:
        return "The title must be between 1 and 100 characters"
    else:
        return None
    
def get_list_by_id(list_id, lists):
    for lst in lists:
        if lst['id'] == list_id:
            return lst
    
    return None


def get_todo_by_id(todo_id, todo_lst):
    for todo in todo_lst:
        if todo['id'] == todo_id:
            return todo
    
    return None


def get_list_index_by_id(list_id, lists):

    for i,todo_list in enumerate(lists):

        if todo_list['id'] == list_id:
            return i
    
    return None