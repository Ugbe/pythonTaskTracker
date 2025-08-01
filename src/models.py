from datetime import date

class Task:
    def __init__(self, id:int, description:str, details:str, priority:str, due_date:date=None, status:str="Pending", archived:bool=False):
        self.id = id
        self.description = description
        self.details = details
        self.due_date = due_date
        self.status = status
        self.archived = archived
        self.priority = priority
    
>>>>>>> e961c852c9765956ac44b914212cd55b5d7f0598
