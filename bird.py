import math

FORWARD = "forward"
SPEED_UP = "speed_up"
SLOW_DOWN = "slow_down"
LEFT = "left"
RIGHT = "right"
MOVES = [FORWARD, SPEED_UP, SLOW_DOWN, LEFT, RIGHT]

DEFAULT_SPEED = 10
DELTA_SPEED = 2
ROTATION = math.pi * 15 / 180
COLLISION_RADIUS = 1


class Bird:
    def __init__(self, x, y, direction):
        self.location = Loc(x, y, direction, DEFAULT_SPEED)

    def setLocation(self, loc):
        self.location = loc

    def toString(self):
        loc = self.location
        return "x: " + str(loc.x) + ", y: " + str(loc.y) + ", direction: " + str(loc.direction)

    def format(self):
        loc = self.location
        return str(loc.x) + " " + str(loc.y) + " " + str(loc.direction) + " " + str(loc.speed)

    def foreseeMove(self, move, loc):
        v = loc.speed
        dir = loc.direction

        if move == SPEED_UP:
            v += DELTA_SPEED

        if move == SLOW_DOWN:
            v -= DELTA_SPEED

        if move == LEFT:
            dir += ROTATION

        if move == RIGHT:
            dir -= ROTATION

        return Loc(loc.x + v * math.cos(dir), loc.y + v * math.sin(dir), dir, v)

    def collides(self, loc, depth):
        collides = False
        futureLoc = self.forward(depth)

        if futureLoc.distance(loc) < 2 * COLLISION_RADIUS:
            collides = True

        return collides

    def forward(self, depth):
        dir = self.location.direction
        v = depth * self.location.speed
        return Loc(self.location.x + v * math.cos(dir),
                   self.location.y + v * math.sin(dir), dir, v)


class Loc:
    def __init__(self, x, y, direction, speed):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed

    def distance(self, loc):
        return math.sqrt(math.pow(self.x - loc.x, 2) + math.pow(self.y - loc.y, 2))
