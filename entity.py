"""entity"""
class Entity():
    def __init__(self, uuid):
        self.id = None
        self.uuid = uuid
        self.name = None
        self.position = []

    def set_position(self, x, y, z):
        self.position = [x, y, z]

    def is_uuid(self, uuid):
        return self.uuid == uuid

    def is_name(self, name, partial=False):
        print(partial)
        if partial:
            return self.name.startswith(name)
        return self.name == name
    
    def is_inrange(self, coords, distance):
        return True in [abs(x[0] - x[1]) < distance for x in zip(coords, self.position)]
        
    def is_not_inrange(self, coords, distance):
        return True in [abs(x[0] - x[1]) > distance for x in zip(coords, self.position)]
        