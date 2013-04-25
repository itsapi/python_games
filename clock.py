import math
import time
import console
import sys
import colorsText
import circle

class Clock(object):
    def __init__(self, time, size):
        self.time = int(time)
        self.size = size
        self.seconds = Hand(1, self.time, colorsText.WHITE)
        self.minutes = Hand(60, self.time, colorsText.WHITE)
        self.hours = Hand(720, self.time, colorsText.WHITE)

    def update(self, time):
        self.time = int(time)
        self.seconds.set(self.time)
        self.minutes.set(self.time)
        self.hours.set(self.time)

    def digital(self):
        return self.hours.digital(self.time) + ':' + self.minutes.digital(self.time) + ':' + self.seconds.digital(self.time)

    def analogue(self, data):
        screen = Screen(self.size, self.size, self)
        screen.vector((int(self.size/2), int(self.size/2)), self.seconds.calcAng(), self.size*.4, self.seconds.color)
        screen.vector((int(self.size/2), int(self.size/2)), self.minutes.calcAng(), self.size*.35, self.minutes.color)
        screen.vector((int(self.size/2), int(self.size/2)), self.hours.calcAng(), self.size*.3, self.hours.color)
        screen.display[self.size/2][self.size/2] = colorsText.printout('O', colorsText.WHITE)
	screen.border()
        return screen.update(data)
        
class Hand(object):
    def __init__(self, interval, time, color):
	self.color = color
        self.interval = interval
        self.pos = ((time / self.interval) % 60)

    def digital(self, time):
        temp = '{:2d}'
        if self.interval == 720:
            return colorsText.printout(temp.format(((time / 3600) % 60) % 24), self.color)
        else:
            return colorsText.printout(temp.format((time / self.interval) % 60), self.color)

    def set(self, time):
        if time % self.interval == 0:
            self.pos = (time / self.interval) % 60

    def calcAng(self):
        if self.interval == 720:
	        return (self.pos+6)*6
	else:
	        return self.pos*6

class Screen(object):
    def __init__(self, x, y, clock):
        self.clock = clock
        self.size = y
        self.display = [[' ' for j in range(x)] for i in range(y)]

    def vector(self, start, angle, length, color):
        xLength = length * math.sin(math.radians(angle))
        yLength = length * math.cos(math.radians(angle))
        if (angle-45) % 180 < 90:
            if xLength <= 0:
                for xOff in range(0, int(xLength), -1):
                    self.display[int(start[1] + ((xLength-xOff)/math.tan(math.radians(angle))))][int(start[0]+xLength-xOff)] = colorsText.printout('#', color)
            else:
                for xOff in range(int(xLength)):
                    self.display[int(start[1] + ((xLength-xOff)/math.tan(math.radians(angle))))][int(start[0]+xLength-xOff)] = colorsText.printout('#', color)
        else:
            if yLength <= 0:
                for yOff in range(0, int(yLength), -1):
                    self.display[int(start[1]+yLength-yOff)][int(start[0] + ((yLength-yOff)*math.tan(math.radians(angle))))] = colorsText.printout('#', color)
            else:
                for yOff in range(int(yLength)):
                    self.display[int(start[1]+yLength-yOff)][int(start[0] + ((yLength-yOff)*math.tan(math.radians(angle))))] = colorsText.printout('#', color)

    def border(self):
	self.display = circle.circle(self.display, (self.size/2,self.size/2), (self.size/2)-1, colorsText.WHITE)

    def update(self, data):
        y = len(self.display)
        x = len(self.display[0])
        reversedClock = [[' ' for i in range(x)] for j in range(y)]
        a = 0
        for row in range(y-1, 0, -1):
            x = len(self.display[row])
            b = 0
            for pixel in range(0, x-1, 1):
                reversedClock[row][pixel] = self.display[a][b]
                b += 1
            a += 1

        result = '\n' * ((console.HEIGHT - self.size)/2)
        for row in reversedClock:
            result += ' ' * ((console.WIDTH - self.size*2)/2)
            for pixel in row:
                result += pixel + ' '
            result += '\n'
        result += '\n' * ((console.HEIGHT - self.size)/2)
       # result += '\n' + (' '*((console.WIDTH - 8)/2) + self.clock.digital() + '\n' + data
        return result

class Fps(object):
    def __init__(self):
        self.oldTime = time.time()
        self.frames = 0
        self.fps = '0 FPS'

    def __str__(self):
        self.frames += 1
        if time.time() >= self.oldTime +1 :
            self.oldTime = time.time()
            self.fps = str(self.frames) + ' FPS'
            self.frames = 0
        return self.fps

if console.WIDTH > console.HEIGHT:
    size = console.HEIGHT * .9
else:
    size = console.WIDTH * .9
clock = Clock(time.time(), int(size))
fps = Fps()
while True:
    try:
        time.sleep(.9)
        clock.update(time.time())
        sys.stdout.write(clock.analogue(''))#str(fps)) + '\n')
    except KeyboardInterrupt:
        print '\n' * console.HEIGHT
        sys.exit()