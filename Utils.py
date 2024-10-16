
def get_champlist_as_list():
    with open('./champlist.txt', 'r') as f:
        return [name.strip() for name in f]
