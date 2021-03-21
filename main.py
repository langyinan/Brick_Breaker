import pygame
pygame.init()

windows_width = 800
windows_height = 800
margin = 20
win = pygame.display.set_mode((windows_width, windows_height))
pygame.display.set_caption("Yinan Lang's game")
pause_text = pygame.font.SysFont('Consolas', 32).render('Pause', True, pygame.color.Color('White'))


class Player(object):
    def __init__(self, x, y, width, height, velocity):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = velocity

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 0), (self.x, self.y, self.width, self.height))


class Brick(object):
    def __init__(self, x, y, width, height, color, armor):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.armor = armor

    def hit(self):
        pass

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x + 3, self.y + 3, self.width - 6, self.height - 6))
        pygame.draw.rect(win, (100, 120, 130), (self.x, self.y, 3, self.height))
        pygame.draw.rect(win, (100, 120, 130), (self.x + self.width - 3, self.y, 3, self.height))
        pygame.draw.rect(win, (100, 120, 130), (self.x, self.y, self.width, 3))
        pygame.draw.rect(win, (100, 120, 130), (self.x, self.y + self.height - 3, self.width, 3))


class Ball(object):
    def __init__(self, x, y, radius, color, power, velocity):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.power = power
        self.velocity = velocity
        self.direction = 1.5, 2

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


player = Player(400, 750, 200, 20, 5)
ball = Ball(400, 400, 10, (255, 0, 100), 1, 2)
blocks = []


def ballMove():
    dx, dy = ball.direction
    ball.x += ball.velocity * dx
    ball.y += ball.velocity * dy
    ifCollision()


def ifCollision():
    dx, dy = ball.direction
    if ball.x - ball.radius <= margin or ball.x + ball.radius >= windows_width - margin:
        ball.direction = -dx, dy
    if ball.y - ball.radius <= 0:
        ball.direction = dx, -dy

    if ball.x < player.x < ball.x + ball.radius and player.y < ball.y < player.y + player.height:
        ball.direction = -dx, dy

    if ball.x - ball.radius < player.x + player.width < ball.x and player.y < ball.y < player.y + player.height:
        ball.direction = -dx, dy

    if ball.y < player.y < ball.y + ball.radius and player.x < ball.x < player.x + player.width:
        ball.direction = dx, -dy

    if ball.y - ball.radius < player.y + player.height < ball.y and player.x < ball.x < player.x + player.width:
        ball.direction = dx, -dy

    for block in blocks:
        if ball.x < block.x < ball.x + ball.radius and block.y < ball.y < block.y + block.height:
            ball.direction = -dx, dy
            blocks.pop(blocks.index(block))
            break

        if ball.x - ball.radius < block.x + block.width < ball.x and block.y < ball.y < block.y + block.height:
            ball.direction = -dx, dy
            blocks.pop(blocks.index(block))
            break

        if ball.y < block.y < ball.y + ball.radius and block.x < ball.x < block.x + block.width:
            ball.direction = dx, -dy
            blocks.pop(blocks.index(block))
            break

        if ball.y - ball.radius < block.y + block.height < ball.y and block.x < ball.x < block.x + block.width:
            ball.direction = dx, -dy
            blocks.pop(blocks.index(block))
            break


def redrawGameWindow():
    win.fill((0, 0, 0))
    ball.draw(win)
    for block in blocks:
        block.draw(win)
    player.draw(win)
    ballMove()

    pygame.draw.rect(win, (255, 255, 255), (0, 0, margin, windows_height))
    pygame.draw.rect(win, (255, 255, 255), (windows_width - margin, 0, margin, windows_height))
    pygame.display.update()


def initializeBlocks():
    for x in range(11):
        blocks.append(Brick(70 + 60 * x, 50, 60, 30, (130, 255, 130), 1))
    for x in range(10):
        blocks.append(Brick(100 + 60 * x, 80, 60, 30, (130, 255, 130), 1))
    for x in range(11):
        blocks.append(Brick(70 + 60 * x, 110, 60, 30, (130, 255, 130), 1))
    for x in range(10):
        blocks.append(Brick(100 + 60 * x, 140, 60, 30, (130, 255, 130), 1))
    for x in range(11):
        blocks.append(Brick(70 + 60 * x, 170, 60, 30, (130, 255, 130), 1))
    for x in range(10):
        blocks.append(Brick(100 + 60 * x, 200, 60, 30, (130, 255, 130), 1))


initializeBlocks()
run = True
pause = False

while run:

    pygame.time.delay(10)

    if len(blocks) == 0:
        run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if ball.y + ball.radius >= windows_height:
        run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        pause = not pause
        if pause:
            win.blit(pause_text, (100, 100))

    if keys[pygame.K_LEFT]:
        if player.x > margin:
            player.x -= player.velocity

    if keys[pygame.K_RIGHT]:
        if player.x < windows_width - player.width - margin:
            player.x += player.velocity

    redrawGameWindow()

pygame.quit()