from graphics import *

def main():
    win = GraphWin("My Circle", 500, 500)
    c = Circle(Point(250,250), 100)
    c.draw(win)
    win.getMouse() # Pause to view result
    win.close()    # Close window when done

main()