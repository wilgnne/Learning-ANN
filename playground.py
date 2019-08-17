from ANN import Brain
import sys, pygame, time, numpy, random
import threading

pygame.init()

def main ():
    size = width, height = 320, 240
    black = 0, 0, 0
    red = 255, 0, 0
    blue = 0, 0, 255

    screen = pygame.display.set_mode(size)

    playerX = 100
    playerW = 50
    playerH = 10
    playerSpeed = 1000

    bolX = 50
    bolY = 50
    bolR = 10
    bolSpeed = 500

    brain = Brain(2, [20], 1, ones=False)

    framerate = 1/60
    while 1:
        init = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        entry = brain.think(numpy.array([playerX, bolX]))[0]

        if entry > 0.0 and playerX < 300:
            playerX += playerSpeed * framerate
        elif entry < -0.0 and playerX > 0:
            playerX -= playerSpeed * framerate

        bolY += bolSpeed * framerate

        if bolY > 200:
            if ((playerX - playerW / 2) < bolX < (playerX + playerW / 2)) == False:
                brain = Brain(2, [20], 1, ones=False)
            bolX = random.randint(5, 300)
            bolY = 0
        screen.fill(black)

        pygame.draw.circle(screen, blue, (bolX, int(bolY)), 10)
        pygame.draw.line(screen, red, (playerX - playerW / 2, 200), (playerX + playerW / 2, 200), playerH)

        pygame.display.flip()

        framerate = time.time() - init

main()