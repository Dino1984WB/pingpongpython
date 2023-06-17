#unit testing for the pong game

import unittest
from ponggame import PongGame


class PongGameTests(unittest.TestCase):
    def setUp(self):
        self.game = PongGame()

    def test_game_start(self):
        # Check if the game starts and the ball is in the middle of the screen
        self.assertEqual(self.game.ball.pos, [self.game.width / 2, self.game.height / 2])

    def test_ball_movement(self):
        # Check if the ball moves after updating the game
        initial_pos = self.game.ball.pos
        self.game.update(1)  # Update the game
        new_pos = self.game.ball.pos
        self.assertNotEqual(initial_pos, new_pos)

    def test_paddle_movement(self):
        # Check if the paddle moves up and down
        initial_y = self.game.paddle.y
        self.game.paddle.move_up()
        self.assertEqual(self.game.paddle.y, initial_y + 10)
        self.game.paddle.move_down()
        self.assertEqual(self.game.paddle.y, initial_y)

    def test_collision_detection(self):
        # Check if the collision detection between the ball and paddle/opponent works
        self.game.ball.x = self.game.paddle.x - self.game.ball.width - 1  # Set the ball to the left of the paddle
        initial_vel = self.game.ball.vel[0]
        self.game.update(1)  # Update the game
        self.assertNotEqual(initial_vel, self.game.ball.vel[0])  # Velocity should change after collision

    def test_game_over(self):
        # Check if the game ends when the ball goes out of bounds
        self.game.ball.x = -60  # Set the ball to the left of the screen
        self.game.update(1)  # Update the game
        self.assertEqual(self.game.ball.vel, [0, 0])  # Ball velocity should be zero
        self.assertEqual(self.game.ball.x, -60)  # Ball x position should remain the same

        self.game.ball.x = self.game.width + 60  # Set the ball to the right of the screen
        self.game.update(1)  # Update the game
        self.assertEqual(self.game.ball.vel, [0, 0])  # Ball velocity should be zero
        self.assertEqual(self.game.ball.x, self.game.width + 60)  # Ball x position should remain the same


if __name__ == '__main__':
    unittest.main()
