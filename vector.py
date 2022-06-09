
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __eq__(self, vector: 'Vector') -> bool:
        return self.x == vector.x and self.y == vector.y
    
    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"