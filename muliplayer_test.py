import curses
import time
import os
import random
import networking as net

def stop(message=''):
    try:
        network.server.stop()
        curses.endwin()
    except:
        pass
    time.sleep(0.1)
    if message: print(message)
    os._exit(1)

def randPos(maxy, maxx):
    y = (int((random.randint(1, maxy-1)-1)/2)+1)*2 
    x = (int((random.randint(1, maxx-1)-1)/2)+1)*2
    return y, x
	
def main(stdscr, network):
    curses.curs_set(0)
    stdscr.nodelay(1)

    # Reset file.
    network.putData([])
    score = 0
    network.putKey('score', score)
    oscore = 0

    # Get players and their positions set up.
    maxy, maxx = stdscr.getmaxyx()
    network.putKey('maxy', maxy)
    network.putKey('maxx', maxx)

    othery = int(network.client.get('maxy'))
    otherx = int(network.client.get('maxx'))

    maxy = min((maxy, othery))
    maxx = min((maxx, otherx))

    y, x = randPos(maxy, maxx)
    network.putKey('y', y)
    network.putKey('x', x)

    py, px = 1, 1

    # Decide dot position
    doty = network.client.get('doty')
    dotx = network.client.get('dotx')
    if doty == 'False':
        doty, dotx = randPos(maxy, maxx)
        network.putKey('doty', doty)
        network.putKey('dotx', dotx)
    else:
        network.putKey('doty', doty)
        network.putKey('dotx', dotx)

    try:
        while True:
            # Position our player.
            xold, yold = x, y
            
            c = stdscr.getch()
            curses.flushinp()
            if c == curses.KEY_LEFT and x > 2:
                x -= 2
            elif c == curses.KEY_RIGHT and x < maxx-2:
                x += 2
            elif c == curses.KEY_UP and y > 1:
                y -= 1
            elif c == curses.KEY_DOWN and y < maxy-2:
                y += 1
            
            if not xold == x:
                network.putKey('x', x)
            if not yold == y:
                network.putKey('y', y)
            
            # Position other player.
            pxold, pyold = px, py
            try:
                py = int(network.client.get('y'))
                px = int(network.client.get('x'))
            except:
                pass
            
            if px > maxx-1:
                px = maxx-1
            if py > maxy-2:
                py = maxy-2

            # Postion the dot.
            dotyold, dotxold = doty, dotx
            doty = int(network.client.get('doty'))
            dotx = int(network.client.get('dotx'))

            # Detect collisions with dot
            scoreold = score
            if doty == y and dotx == x:
                score += 1
                network.putKey('score', score)
            oscoreold = oscore
            oscore = network.client.get('score')
            
            # Write to screen.
            if not (pyold == py and
                    pxold == px and
                    yold == y and
                    xold == x and
                    dotyold == doty and
                    dotxold == dotx and 
                    scoreold == score and
                    oscoreold == oscore):
                stdscr.clear()
                stdscr.addstr(0, 0, 'You: ' + str(score))
                stdscr.addstr(1, 0, 'Other: ' + str(oscore))

                stdscr.addstr(doty, dotx, '*')
                stdscr.addstr(py, px, '@')
                stdscr.addstr(y, x, '#')
                stdscr.refresh()
            time.sleep(0.01)

    except KeyboardInterrupt:
        stop()

network = net.Net(stop)
curses.wrapper(main, network)
