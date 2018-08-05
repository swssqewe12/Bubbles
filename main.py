import pyglet
from Game import *

def main():
	game = Game()
	game.run()
	pyglet.app.run()

if __name__ == "__main__":
	main()