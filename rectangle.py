
class Rectangle:
    def __init__(self, x, y, width, height):
        self.x : int = x
        self.y : int = y
        self.width : int = width
        self.height : int = height
    
    def __repr__(self) -> str:
        return f"x:{self.x}, y:{self.y}, width:{self.width}, height:{self.height}"