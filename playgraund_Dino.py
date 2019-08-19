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

    framerate = 1/60
    while True:
        init = time.time()
        screen.fill(black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        
        key=pygame.key.get_pressed()  #checking pressed keys
        if key[pygame.K_a] and isJumping == False:
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
        if contFrame > 1:
            if random.random() > 0.5:
                obstatuco.append(GameObject(320, 200))
            contFrame = 0

        for obj in obstatuco:
            if obj.x > 0:
                obj.x -= velocity * framerate
                pygame.draw.line(screen, red, (obj.x, obj.y - 10), (obj.x, obj.y + 10), 5)
            else:
                obstatuco.remove(obj)
        
        if isJumping:
            pygame.draw.line(screen, blue, (player.x, player.jumpY - 10), (player.x, player.jumpY + 10), 5)
        else:
            pygame.draw.line(screen, blue, (player.x, player.y - 10), (player.x, player.y + 10), 5)
        
        print(obstatuco)
        
        pygame.display.flip()
        framerate = time.time() - init

if __name__ == "__main__":
    main()