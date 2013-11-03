# represents a tile of the grid
class Tile:
    # nb: tile number
    # pos: position in the grid
    # ties: connected components
    # img: image representing the tile
    # x: x coordinate in the grid
    # y: y coordinate in the grid
    def __init__(self, nb, pos, ties, img=None, x=None, y=None):
        self.img = img;
        self.x = x;
        self.y = y;
        self.ties = ties;
        self.pos = pos;
        self.nb = nb;
        
    def setPos(self, pos):
        self.pos = pos;
        
    def setImg(self, img):
        self.img = img;
        
    def setX(self, x):
        self.x = x;
        
    def setY(self, y):
        self.y = y;