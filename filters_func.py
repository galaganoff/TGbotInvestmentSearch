def project_name(text):
    arr_text = text.split(' ')
    if ("Название проекта" in text) and (len(arr_text) > 2):
        return True
    return False

def poject_cat(text):
    arr_text = text.split(' ')
    if "Категория проекта" in text and (len(arr_text) > 2):
        return True
    return False

def summ_under(text):
    arr_text = text.split(' ')
    if "Сумма меньше" in text and (len(arr_text) > 2):
        return True
    return False

def summ_up(text):
    arr_text = text.split(' ')
    if "Сумма больше" in text and (len(arr_text) > 2):
        return True
    return False
