import builtins
import pickle

class MapManager():
    def __init__(self) -> None:
        self.model = "block.egg"
        self.texture = "block.png"
        self.color = (0.2, 0.2, 0.35, 1)
        self.colors = [
            (0.2, 0.2, 0.35, 1),
            (0.3, 0.4, 0.5, 1),
            (0.7, 0.5, 0.2, 1),
            (0.9, 0.8, 0.7, 1),
        ]

        self.textures = [
            "block.png",
            "block.png",
            "stone.png",
            "brick.png",
            "brick.png",
            "wood.png",
        ]

        self.startNew()
        self.addBlock((0,10,0))


    def startNew(self):
        self.land = builtins.render.attachNewNode("Land")

    def getColor(self, z):
        if z >= len(self.colors) - 1:
            return self.colors[-1]
        return self.colors[z]
    
    def getColor(self, z):
        if z >= len(self.textures) - 1:
            return self.textures[-1]
        return self.textures[z]
    

    def addBlock(self, position):
        self.block = builtins.loader.loadModel(self.model)
        texture = builtins.loader.loadTexture(self.texture)
        self.block.setTexture(texture)
        new_color = self.getColor(position[2])
        self.block.setColor(self.color)
        self.block.setPos(position)
        self.block.reparentTo(self.land)

        self.block.setTag("at", str(position))

    def clear(self):
        self.land.removeNode()
        self.startNew()

    def loadLand(self, filename):
        self.clear()
        with open(filename, 'r') as file:
            y = 0
            for line in file:
                x = 0
                line = line.split(" ")
                for z in line:
                    for z0 in range(int(z)+1):
                        self.addBlock((x, y,z0))
                    x += 1
                y += 1
    

    def isEmpty(self, pos):
        blocks = self.findBlock(pos)
        return not bool(blocks)
    
    def findHighestEmpty(self,pos):
        x,y,z = pos
        z = 1
        while not self.isEmpty((x,y,z)):
            z += 1
        return (x,y,z)

    def findBlock(self, pos):
        return self.land.findAllMatches("=at="+str(pos))

    def deleteBlock(self, pos):
        blocks = self.findBlock(pos)
        for b in blocks:
            b.removeNode()


    def saveToBin(self):
        blocks = self.land.getChildren()
        with open("land_bin.dat", "wb") as file :
            pickle.dump(len(blocks), file)
            for b in blocks:
                x,y,z = b.getPos()
                pos = int(x), int(y), int(z)

                pos = b.getPos()
                pos = tuple(map(int, pos))

                pickle.dump(pos, file)

    def loadBin(self):
        self.clear()
        with open("land_bin", "rb") as file:
            lenght = pickle.load(file)
            for _ in range(lenght):
                pos = pickle.load(file)
                self.addBlock(pos)