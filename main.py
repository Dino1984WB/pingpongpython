import PySimpleGUI as sg
import random

# Set up the game window
width, height = 800, 400
layout = [
    [sg.Canvas(size=(width, height), key="-CANVAS-")],
    [sg.Text("Player: 0", key="-PLAYER-SCORE-"), sg.Text("Opponent: 0", key="-OPPONENT-SCORE-")],
    [sg.Button("Exit")]
]

window = sg.Window("Pong", layout, finalize=True)
canvas = window["-CANVAS-"]

# Define the ball properties
ball_radius = 10
ball_pos = [width // 2, height // 2]
ball_vel = [random.choice([-1, 1]), random.choice([-1, 1])]

# Define the paddle properties
paddle_width = 10
paddle_height = 60
paddle_speed = 5
paddle_pos = [0, height // 2 - paddle_height // 2]

# Define the opponent paddle properties
opponent_pos = [width - paddle_width, height // 2 - paddle_height // 2]

# Define the score variables
player_score = 0
opponent_score = 0

# Game loop
while True:
    event, values = window.read(timeout=20)

    if event == "Exit" or event == sg.WINDOW_CLOSED:
        break

    # Update ball position
    ball_pos[0] += ball_vel[0] * 2
    ball_pos[1] += ball_vel[1] * 2

    # Ball collision with walls
    if ball_pos[1] >= height - ball_radius or ball_pos[1] <= ball_radius:
        ball_vel[1] *= -1

    # Ball collision with paddles
    if ball_pos[0] <= paddle_width and paddle_pos[1] - ball_radius <= ball_pos[1] <= paddle_pos[1] + paddle_height:
        ball_vel[0] *= -1
        player_score += 1
        window["-PLAYER-SCORE-"].update("Player: {}".format(player_score))
    elif ball_pos[0] >= width - paddle_width - ball_radius and opponent_pos[1] - ball_radius <= ball_pos[1] <= opponent_pos[1] + paddle_height:
        ball_vel[0] *= -1
        opponent_score += 1
        window["-OPPONENT-SCORE-"].update("Opponent: {}".format(opponent_score))

    # Update opponent paddle position
    if opponent_pos[1] + paddle_height // 2 < ball_pos[1]:
        opponent_pos[1] += paddle_speed
    else:
        opponent_pos[1] -= paddle_speed

    # Clear the canvas
    canvas.erase()

    # Draw the game elements
    canvas.draw_line((width // 2, 0), (width // 2, height), color="white")
    canvas.draw_circle(ball_pos, ball_radius, fill_color="white", line_color="white")
    canvas.draw_rectangle(paddle_pos, (paddle_pos[0] + paddle_width, paddle_pos[1] + paddle_height), fill_color="white", line_color="white")
    canvas.draw_rectangle(opponent_pos, (opponent_pos[0] + paddle_width, opponent_pos[1] + paddle_height), fill_color="white", line_color="white")

window.close()
