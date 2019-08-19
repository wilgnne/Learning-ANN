from ANN import Brain
import sys, pygame, time, numpy, random, math

pygame.init()

class GameObject:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        self.jumpY = y

def main ():
    size = width, height = 320, 240
    black = 0, 0, 0
    red = 255, 0, 0
    blue = 0, 0, 255

    screen = pygame.display.set_mode(size)

    obstatuco = []
    velocity = 100
    contFrame = 0

    player = GameObject(50, 200)
    isJumping = False
    jumpForce = 50
    jumpTime = 0.5
    jumpCont = 0

    font = pygame.font.Font('freesansbold.ttf', 16) 
    text = font.render('GeeksForGeeks', True, black)

    times = 0
    
    brain = Brain(1, [5, 8, 4], 1, ones=False)

    framerate = 1/60
    while True:
        init = time.time()
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        
        velocity += 10 * framerate
        times += framerate

        distance = min([d.x-player.x if d.x-player.x > 0 else 1000 for d in obstatuco]) if len(obstatuco) > 0 else 1000

        saida = brain.think(numpy.array([distance]))
        
        key=pygame.key.get_pressed()  #checking pressed keys
        if saida > 0 and isJumping == False:
            isJumping = True
        
        if isJumping:
            jumpCont += math.pi / jumpTime * framerate
            if jumpCont > math.pi:
                jumpCont = 0
                isJumping = False
                player.jumpY = player.y
            else:
                player.jumpY = player.y + jumpForce * -math.sin(jumpCont)

        contFrame += 1 * framerate
        if contFrame > 2*random.random()+0.7:
            if random.random() > 0.5:
                obstatuco.append(GameObject(320, 200))
            contFrame = 0

        for obj in obstatuco:
            if obj.x > 0:
                obj.x -= velocity * framerate
                pygame.draw.line(screen, red, (obj.x, obj.y - 10), (obj.x, obj.y + 10), 5)

                if obj.x - 5 < player.x < obj.x + 5 and obj.y - 5 < player.jumpY < obj.y + 5:
                    print("Morreu")
                    brain = Brain(1, [5, 8, 4], 1, ones=False)
                    times = 0
                    velocity = 100
                    obstatuco = []

            else:
                obstatuco.remove(obj)
        
        if isJumping:
            pygame.draw.line(screen, blue, (player.x, player.jumpY - 10), (player.x, player.jumpY + 10), 5)
        else:
            pygame.draw.line(screen, blue, (player.x, player.y - 10), (player.x, player.y + 10), 5)

        pygame.draw.line(screen, black, (0, 210), (320, 210), 1)

        text = font.render(str(times), True, black)
        screen.blit(text, (10, 20))

        pygame.display.flip()
        framerate = time.time() - init

if __name__ == "__main__":
    main()