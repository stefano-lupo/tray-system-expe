

class Image:

    def __init__(self,
                 id: int,
                 path: str):
        self.id = id
        self.path = path

    def get_as_json(self):
        return vars(self)
