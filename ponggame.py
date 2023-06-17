from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Ellipse
from kivy.core.window import Window
from kivy.clock import Clock
from random import choice


class Paddle(Widget):
    def move_up(self):
        self.y += 10

    def move_down(self):
        self.y -= 10


class Ball(Widget):
    def __init__(self, paddle, opponent, **kwargs):
        super(Ball, self).__init__(**kwargs)
        self.vel = [choice([-1, 1]), choice([-1, 1])]
        self.paddle = paddle
        self.opponent = opponent

    def move(self):
        self.x += self.vel[0] * 4
        self.y += self.vel[1] * 4

        if self.y < 0 or self.y > Window.height - 10:
            self.vel[1] *= -1

        if self.collide_widget(self.paddle) or self.collide_widget(self.opponent):
            if self.vel[0] > 0:
                self.vel[0] *= -1
                self.x = self.paddle.x - self.width
            else:
                self.vel[0] *= -1
                self.x = self.paddle.x + self.paddle.width


class PongGame(Widget):
    def __init__(self, **kwargs):
        super(PongGame, self).__init__(**kwargs)
        self.paddle = Paddle(pos=[20, Window.height/2-40])
        self.opponent = Paddle(pos=[Window.width-40, Window.height/2-40])
        self.ball = Ball(paddle=self.paddle, opponent=self.opponent, pos=[Window.width/2, Window.height/2])

        self.paddle_rect = Rectangle(pos=self.paddle.pos, size=(10, 80))
        self.opponent_rect = Rectangle(pos=self.opponent.pos, size=(10, 80))
        self.canvas.add(self.paddle_rect)
        self.canvas.add(self.opponent_rect)

        self.ball_ellipse = Ellipse(pos=self.ball.pos, size=(20, 20))
        self.canvas.add(self.ball_ellipse)

        Clock.schedule_interval(self.update, 1/60.)

    def update(self, dt):
        self.ball.move()

        if self.ball.x > self.width - 50:
            self.opponent.move_up()
        if self.ball.x < 50:
            self.opponent.move_down()

        self.paddle_rect.pos = self.paddle.pos
        self.opponent_rect.pos = self.opponent.pos
        self.ball_ellipse.pos = self.ball.pos

        self.check_win()

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
