

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
    todo_list = [list_dict for 
                 list_dict in lists 
                 if list_dict['id'] == list_id
                 ]
    
    if len(todo_list) < 1:
        return None

    return todo_list[0]

def get_list_index_by_id(list_id, lists):

    for i,todo_list in enumerate(lists):

        if todo_list['id'] == list_id:
            return i
    
    return None