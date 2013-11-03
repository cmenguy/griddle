import random
import pygame

# represents a grid as a set of tiles
class Grid:
    # horizontal: width of the grid in number of tiles
    # vertical: height of the grid in number of tiles
    # distance: distance between each tile in the grid
    def __init__(self, horizontal, vertical, distance=5):
        self.horizontal = horizontal;
        self.vertical = vertical;
        self.tiles = [];
        # objective function - what we need to optimize
        self.objective = 0;
        self.distance = distance
        
    # generate connections between tiles
    def genConn(self):
        states = [];
        numbers = [];
        
        for i in range(1, self.horizontal*self.vertical+1):
            numbers.append(i);
            states.append([]);
            if i > self.horizontal:
                states[i-1].append(i-self.horizontal);
            if i <= (self.vertical-1)*self.horizontal:
                states[i-1].append(i+self.horizontal);
            if i % self.horizontal != 1:
                states[i-1].append(i-1);
            if i % self.horizontal != 0:
                states[i-1].append(i+1);
                
        return numbers, states
        
    # read a file to import saved grid if needed
    def importer(self, filename):
        numbers, states = self.genConn();
        
        input = open(filename, 'r');
        lines = input.readlines()[0:];
        for l in range(len(lines)):
            tokens = lines[l].strip().split(',');
            gc = Tile(int(tokens[0]), int(tokens[1]), states[l])
            self.tiles.append(gc)
                        
        self.connLength();
    
    # move 1 tile defined by its start positions to its end position
    # also updates objective function
    def move(self, start, end):
        for comp in self.tiles:
            if comp.pos == start:
                for tie in comp.ties:
                    self.objective -= self.manhattan([(comp.pos-1) % self.horizontal, (comp.pos-1) / self.vertical], [(self.tiles[tie-1].pos-1) % self.horizontal, (self.tiles[tie-1].pos-1) / self.vertical]) * self.distance;
                comp.pos = end;
                for tie in comp.ties:
                    self.objective += self.manhattan([(comp.pos-1) % self.horizontal, (comp.pos-1) / self.vertical], [(self.tiles[tie-1].pos-1) % self.horizontal, (self.tiles[tie-1].pos-1) / self.vertical]) * self.distance;
                
            else:
                if comp.pos == end:
                    for tie in comp.ties:
                        self.objective -= self.manhattan([(comp.pos-1) % self.horizontal, (comp.pos-1) / self.vertical], [(self.tiles[tie-1].pos-1) % self.horizontal, (self.tiles[tie-1].pos-1) / self.vertical]) * self.distance;
                    comp.pos = start;
                    for tie in comp.ties:
                        self.objective += self.manhattan([(comp.pos-1) % self.horizontal, (comp.pos-1) / self.vertical], [(self.tiles[tie-1].pos-1) % self.horizontal, (self.tiles[tie-1].pos-1) / self.vertical]) * self.distance;            
    
    def genList(self):
        res = [];
        for i in range(0, self.horizontal*self.vertical):
            res.append(i);
            
        return res;
        
    # initialize grid by placing tiles at random and calculating objective function
    def initGrid(self):
        numbers, states = self.genConn();
        
        gen = self.genList();
        
        for i in range(0, self.vertical*self.horizontal):
            rd = random.randint(0, len(gen)-1);
            gc = Tile(numbers[i], gen[rd]+1, states[i])
            gen.remove(gen[rd]);
            self.tiles.append(gc);
            
        self.connLength();
    
    # manhattan distance
    def manhattan(self, a, b):
        res = 0
        for i in range(0, len(a)):
            res += abs(a[i] - b[i])
        return res
    
    # generate objective function by going through every tile of the grid
    def connLength(self):
        for i in range(len(self.tiles)):
            for tie in self.tiles[i].ties:
                self.objective += self.manhattan([(self.tiles[i].pos-1) % self.horizontal, (self.tiles[i].pos-1) / self.vertical], [(self.tiles[tie-1].pos-1) % self.horizontal, (self.tiles[tie-1].pos-1) / self.vertical]) * self.distance;
                
        self.objective = self.objective / 2;
    
    # Affichage de la grille et des composants ainsi que de leurs connexions.
    # display the grid, its tiles and connections
    def displayGrid(self, temp=0, palier=0, tau=0.8, cptA=0, cptT=0):
        pygame.init();
        
        # may need to change these or make configurable
        spritesizeW = 96;
        spritesizeH = 96;
        maxscreenW = 1600;
        maxscreenH = 800;
        menusize = 500;

        width = spritesizeW*self.horizontal + (maxscreenW-spritesizeW*self.horizontal);
        height = spritesizeH*self.vertical + (maxscreenH-spritesizeH*self.vertical);
        
        correctionW = width*3/100;
        correctionH = height*3/100;
        
        # general display properties
        screen = pygame.display.set_mode((width, height));
        pygame.display.set_caption('Simulated annealing for grid optimization - github.com/cmenguy/grid-optimizer')
        
        # fonts
        font = pygame.font.Font('../data/scribble.TTF', 42)
        font2 = pygame.font.Font('../data/KLEPTOMA.TTF', 42)
        font2.set_underline(True);
        font3 = pygame.font.Font('../data/scribble.TTF', 21)
        
        running = 1;
        
        # get coordinates of tiles based on position and order
        for i in range(len(self.tiles)):
            self.tiles[i].setImg(pygame.image.load('../data/component.png').convert());
            posx = (self.tiles[i].pos -1) % self.horizontal;
            posy = (self.tiles[i].pos -1) / self.vertical;
            self.tiles[i].setX(posx*spritesizeW + posx*(maxscreenW-spritesizeW*self.horizontal-menusize)/(self.horizontal-1));
            self.tiles[i].setY(posy*spritesizeH + posy*(maxscreenH-spritesizeH*self.vertical)/(self.vertical-1));            
                
        # main loop to display all tiles
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = 0;
                        
            screen.fill((255, 255, 255));
            
            for i in range(len(self.tiles)):
                
                text = font.render(str(i+1), 1, (255, 255, 255))
                textpos = text.get_rect()
                textpos.centerx = self.tiles[i].x+correctionW;
                textpos.centery = self.tiles[i].y+correctionH;
                
                screen.blit(self.tiles[i].img, (self.tiles[i].x, self.tiles[i].y));
                screen.blit(text, textpos)
                
                for tie in self.tiles[i].ties:
                    pygame.draw.line(screen, (255,0,0), (self.tiles[i].x+correctionW, self.tiles[i].y+correctionH), (self.tiles[tie-1].x+correctionW, self.tiles[tie-1].y+correctionH))
                    
            menu = pygame.Surface((menusize, height))
            menu = menu.convert()
            menu.fill((255, 255, 255))
            
            title = font2.render('Results', 1, (1, 1, 1))
            energie = font3.render('Total energy : ' + str(self.objective), 1, (1, 1, 1))
            temperature = font3.render('Temperature : ' + str(temp), 1, (1, 1, 1))
            palierS = font3.render('Iteration # : ' + str(palier), 1, (1, 1, 1))
            tauS = font3.render('Initial perturbation coefficient : ' + str(tau), 1, (1, 1, 1))
            cptAS = font3.render('# of accepted perturbations : ' + str(cptA), 1, (1, 1, 1))
            cptTS = font3.render('# of attempted perturbations : ' + str(cptT), 1, (1, 1, 1))
            
            menu.blit(title, (50, 50))
            menu.blit(energie, (50, 400))
            menu.blit(temperature, (50, 450))
            menu.blit(palierS, (50, 500))
            menu.blit(tauS, (50, 550))
            menu.blit(cptAS, (50, 600))
            menu.blit(cptTS, (50, 650))
            screen.blit(menu, (width - menusize, 0))
            
            pygame.display.flip();

# represents a tile of the grid
class Tile:
    # nb: tile number
    # pos: position in the grid
    # ties: connected tiles
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