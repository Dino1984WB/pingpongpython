#Author: William Bukowski, using chatgpt to make this pong game with a gui in python 3
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Ellipse
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.core.window import Window
from random import choice

# Set up the game window size
Window.size = (800, 400)


class Paddle(Widget):
    def move_up(self):
        self.y += 10  # Move the paddle up by changing the y-coordinate

    def move_down(self):
        self.y -= 10  # Move the paddle down by changing the y-coordinate


class Ball(Widget):
    def __init__(self, paddle, opponent, **kwargs):
        super(Ball, self).__init__(**kwargs)
        self.vel = [choice([-1, 1]), choice([-1, 1])]  # Random initial velocity
        self.paddle = paddle
        self.opponent = opponent

    def move(self):
        self.x += self.vel[0] * 4  # Move the ball horizontally based on velocity
        self.y += self.vel[1] * 4  # Move the ball vertically based on velocity

        # Bounce off walls
        if self.y < 0 or self.y > Window.height - 10:
            self.vel[1] *= -1  # Reverse the vertical velocity upon hitting the top or bottom wall

        # Bounce off paddles
        if self.collide_widget(self.paddle) or self.collide_widget(self.opponent):
            if self.vel[0] > 0:  # Ball moving to the right
                self.vel[0] *= -1  # Reverse the horizontal velocity
                self.x = self.paddle.x - self.width  # Adjust the effective collision area by moving the ball to the left of the paddle
            else:  # Ball moving to the left
                self.vel[0] *= -1  # Reverse the horizontal velocity
                self.x = self.paddle.x + self.paddle.width  # Adjust the effective collision area by moving the ball to the right of the paddle


class PongGame(Widget):
    def __init__(self, **kwargs):
        super(PongGame, self).__init__(**kwargs)
        self.paddle = Paddle(pos=[20, Window.height/2-40])  # Create the player's paddle
        self.opponent = Paddle(pos=[Window.width-40, Window.height/2-40])  # Create the opponent's paddle
        self.ball = Ball(paddle=self.paddle, opponent=self.opponent, pos=[Window.width/2, Window.height/2])  # Create the ball

        # Add graphics for paddles
        self.paddle_rect = Rectangle(pos=self.paddle.pos, size=(10, 80))  # Modify the paddle size here
        self.opponent_rect = Rectangle(pos=self.opponent.pos, size=(10, 80))  # Modify the paddle size here
        self.canvas.add(self.paddle_rect)  # Add the player's paddle graphics to the canvas
        self.canvas.add(self.opponent_rect)  # Add the opponent's paddle graphics to the canvas

        # Add graphics for ball
        self.ball_ellipse = Ellipse(pos=self.ball.pos, size=(20, 20))  # Modify the ball size here
        self.canvas.add(self.ball_ellipse)  # Add the ball graphics to the canvas

        self.keys_pressed = set()  # Use a set to store the currently pressed keys

        Clock.schedule_interval(self.update, 1/60.)

    def update(self, dt):
        self.ball.move()

        # Move the player's paddle using mouse touch
        for touch in self.touches:
            if touch.x < self.width / 2:
                self.paddle.center_y = touch.y

        if self.ball.x > self.width - 50:
            self.opponent.move_up()
        if self.ball.x < 50:
            self.opponent.move_down()

        # Update the positions of the graphics elements
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
