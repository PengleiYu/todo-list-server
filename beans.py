class Task(object):
    def __init__(self, id: int, name: str, content: str):
        self.id = id
        self.name = name
        self.content = content

    def __repr__(self):
        return f'Task [ id:{self.id}, name:{self.name}, content:{self.content} ]'
