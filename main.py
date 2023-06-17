#Author: William Bukowski, using chatgpt to make this pong game with a gui in python 3

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Ellipse
from kivy.core.window import Window
from kivy.clock import Clock
from random import choice

# Set up the game window size
Window.size = (800, 400)


class Paddle(Widget):
    def move_up(self):
        self.pos[1] += 10

    def move_down(self):
        self.pos[1] -= 10


class Ball(Widget):
    def __init__(self, paddle, opponent, **kwargs):
        super(Ball, self).__init__(**kwargs)
        self.vel = [choice([-1, 1]), choice([-1, 1])]  # Random initial velocity
        self.paddle = paddle
        self.opponent = opponent

    def move(self):
        self.pos[0] += self.vel[0] * 3
        self.pos[1] += self.vel[1] * 3

        # Bounce off walls
        if self.y < 0 or self.y > Window.height - 20:
            self.vel[1] *= -1

        # Bounce off paddles
        if self.collide_widget(self.paddle) or self.collide_widget(self.opponent):
            self.vel[0] *= -1


class PongGame(Widget):
    def __init__(self, **kwargs):
        super(PongGame, self).__init__(**kwargs)
        self.paddle = Paddle(pos=[20, Window.height/2-40])
        self.opponent = Paddle(pos=[Window.width-40, Window.height/2-40])
        self.ball = Ball(paddle=self.paddle, opponent=self.opponent, pos=[Window.width/2, Window.height/2])

        # Add graphics for paddles
        self.paddle_rect = Rectangle(pos=self.paddle.pos, size=(10, 80))
        self.opponent_rect = Rectangle(pos=self.opponent.pos, size=(10, 80))
        self.canvas.add(self.paddle_rect)
        self.canvas.add(self.opponent_rect)

        # Add graphics for ball
        self.ball_ellipse = Ellipse(pos=self.ball.pos, size=(20, 20))
        self.canvas.add(self.ball_ellipse)

        self.keys_pressed = []

        Clock.schedule_interval(self.update, 1/60.)

    def update(self, dt):
        self.ball.move()

        if "w" in self.keys_pressed:
            self.paddle.move_up()
        if "s" in self.keys_pressed:
            self.paddle.move_down()

        if self.ball.x > self.width - 50:
            self.opponent.move_up()
        if self.ball.x < 50:
            self.opponent.move_down()

        # Update the positions of the graphics elements
        self.paddle_rect.pos = self.paddle.pos
        self.opponent_rect.pos = self.opponent.pos
        self.ball_ellipse.pos = self.ball.pos

        self.check_win()

    def on_touch_move(self, touch):
        if touch.x < self.width / 2:
            self.paddle.center_y = touch.y

    def check_win(self):
        if self.ball.x < -50:
            print("You win!")
            self.ball.vel = [0, 0]
        if self.ball.x > self.width + 50:
            print("You lose!")
            self.ball.vel = [0, 0]


class PongApp(App):
    def build(self):
        game = PongGame()
        return game


if __name__ == '__main__':
    PongApp().run()
