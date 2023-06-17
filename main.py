#Author: William Bukowski, using chatgpt to make this pong game with a gui in python 3

from kivy.app import App
from ponggame import PongGame

class PongApp(App):
    def build(self):
        game = PongGame()
        return game

if __name__ == '__main__':
    PongApp().run()
