from ANN import Brain
import sys, pygame, time, numpy, random
import threading

class Player:
    def __init__(self, x:int, y:int, w:int, h:int, speed:float, brain:Brain):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.speed = speed
        self.brain = brain
        self.points = 0
    
    def think (self, bolX:int, deltatime:float):
        entry = self.brain.think(numpy.array([self.x, bolX]))[0]

        if entry > 0.0 and self.x < 300:
            self.x += self.speed * deltatime
        elif entry < -0.0 and self.x > 0:
            self.x -= self.speed * deltatime



class Avaliation:
    def __init__(self, brains:list, lenTest: int):
        self.players = [Player(100, 200, 50, 10, 50*20, brain) for brain in brains]
        self.lenTest = lenTest
    
    def start (self):
        pygame.init()
        size = width, height = 320, 240
        black = 0, 0, 0
        red = 255, 0, 0
        blue = 0, 0, 255

        screen = pygame.display.set_mode(size)

        bolX = 50
        bolY = 50
        bolR = 10
        bolSpeed = 500
        contBols = self.lenTest

        deltatime = 1/60
        close = False
        while contBols != 0 and not close:
            init = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close = True

            [player.think(bolX, deltatime) for player in self.players]

            bolY += bolSpeed * deltatime

            if bolY > 200:
                for player in self.players:
                    if ((player.x - player.w / 2) < bolX < (player.x + player.w / 2)):
                        player.points += 1
                bolX = random.randint(5, 300)
                bolY = 0

                contBols -= 1
            
            screen.fill(black)

            pygame.draw.circle(screen, blue, (bolX, int(bolY)), bolR)

            for player in self.players:
                pygame.draw.line(screen, red, (player.x - player.w / 2, player.y), (player.x + player.w / 2, player.y), player.h)

            pygame.display.flip()

            deltatime = time.time() - init
        
        points = [player.points for player in self.players]
        pygame.quit()
        return points

if __name__ == "__main__":
    print(Avaliation([Brain(2, [20], 1, False) for i in range(5)], 10).start())