def is_new(new_database_len, database_len):
    if (type(new_database_len) == int) and (type(database_len) == int):
        if (new_database_len > database_len) and (new_database_len > 0) and (database_len >= 0):
            return True
        return False
    return False
print(is_new(1, 0))


