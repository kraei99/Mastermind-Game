import os
import time
import turtle
import random
from Marble import Marble  # Assuming custom class for representing a marble
from Point import Point    # Assuming custom class for representing a point

# Constants
SCREEN_WIDTH = 1005  # Width of the entire game screen
SCREEN_HEIGHT = 768  # Height of the entire game screen
BOARD_WIDTH = 400    # Width of the guess board
BOARD_HEIGHT = SCREEN_HEIGHT - 175
# Height of the guess board, calculated from screen height
LEADERBOARD_WIDTH = 330  # Width of the leaderboard section
# Height of the leaderboard, same as the guess board
LEADERBOARD_HEIGHT = BOARD_HEIGHT
COLOR_PALETTE_HEIGHT = 120  # Height of the color palette section
MARBLE_RADIUS = 15  # Radius of each marble
MARBLE_SPACING = MARBLE_RADIUS + 10  # Space between marbles
GUESS_MARBLE_OFFSET_X = -SCREEN_WIDTH // 3  # X-offset for placing guess marbles
GUESS_MARBLE_OFFSET_Y = SCREEN_HEIGHT // 2 - \
    MARBLE_SPACING  # Y-offset for placing guess marbles
COLORS = ["red", "green", "blue", "yellow",
          "purple", "black"]  # List of available colors

LEADER_FILE = 'leaderboard.txt'


def draw_guess_board():
    border = turtle.Turtle()
    border.penup()
    border.color("black")  # Set the pen color to black for the border
    border.pensize(5)  # Set the pensize to make the border more visible

    # Adjust the start position further to the left by subtracting from the x-coordinate
    extend_left = 100  # Amount by which to extend the border to the left
    border_start_x = GUESS_MARBLE_OFFSET_X - MARBLE_RADIUS - extend_left
    border_start_y = GUESS_MARBLE_OFFSET_Y + MARBLE_RADIUS

    border.goto(border_start_x, border_start_y)
    border.pendown()

    # Increase the total width of the board to account for the extended left border
    extended_border_width = BOARD_WIDTH + extend_left

    # Draw the rectangular border
    border.forward(extended_border_width)  # Draw the bottom border line
    border.right(90)
    border.forward(BOARD_HEIGHT)
    border.right(90)
    border.forward(extended_border_width)  # Draw the top border line
    border.right(90)
    border.forward(BOARD_HEIGHT)
    border.hideturtle()

    guess_board = turtle.Turtle()
    guess_board.hideturtle()
    guess_board.speed('fastest')
    for row in range(10):
        temp = []
        for col in range(4):

            guess_board.penup()
            x = GUESS_MARBLE_OFFSET_X + col * \
                (2 * MARBLE_SPACING) - 40  # Add a value to move right
            # Subtract a value to move down
            y = GUESS_MARBLE_OFFSET_Y - row * (2 * MARBLE_SPACING) - 50

            t = Marble(Point(x, y), 'white')
            t.draw_empty()
            temp.append(t)

        # Adjust feedback circles position and size
        # Adjust this value as needed to move the feedback circles to the right
        feedback_offset_x = 80
        # Making the feedback circles smaller
        feedback_circle_radius = MARBLE_RADIUS // 3
        # Adjust spacing between feedback circles
        feedback_circle_spacing = MARBLE_SPACING // 1.75
        tt = []
        for i in range(2):  # Two columns of feedback circles
            for j in range(2):  # Two feedback circles per column
                # Adjust feedback circle position with feedback_offset_x and feedback_circle_spacing
                feedback_x = x + (2 * MARBLE_RADIUS) + \
                    feedback_offset_x + (i * feedback_circle_spacing)
                feedback_y = y - MARBLE_RADIUS + (j * feedback_circle_spacing)
                m = Marble(Point(feedback_x, feedback_y),
                           'white', feedback_circle_radius)
                m.draw_empty()
                tt.append(m)
        temp.append(tt)
        all_guess_marbles.append(temp)


def draw_leaderboard():

    # Create a turtle for the leaderboard border
    leaderboard_border = turtle.Turtle()

    leaderboard_border.hideturtle()  # Hide the turtle
    leaderboard_border.speed('fastest')  # Set the drawing speed to fastest
    leaderboard_border.penup()  # Lift the pen
    leaderboard_border.pencolor("dark blue")  # Set the pencolor to dark blue
    # Set the pensize to make the border more visible
    leaderboard_border.pensize(5)

    # Position the turtle at the top-left corner of the leaderboard
    leaderboard_border.goto(
        GUESS_MARBLE_OFFSET_X + BOARD_WIDTH + 50, GUESS_MARBLE_OFFSET_Y + MARBLE_RADIUS)
    leaderboard_border.pendown()  # Begin drawing the border

    # Draw the dark blue rectangular border
    for _ in range(2):
        leaderboard_border.forward(LEADERBOARD_WIDTH)
        leaderboard_border.right(90)
        leaderboard_border.forward(LEADERBOARD_HEIGHT)
        leaderboard_border.right(90)
    leaderboard_border.hideturtle()  # Hide the border turtle

   # Now, add text to the leaderboard
    leaderboard_text = turtle.Turtle()
    leaderboard_text.hideturtle()
    leaderboard_text.penup()
    # Set the text color to dark blue for visibility
    leaderboard_text.color("dark blue")

    # Make sure the position is within the visible area of the leaderboard
    text_x = GUESS_MARBLE_OFFSET_X + BOARD_WIDTH + \
        60  # X coordinate within the leaderboard
    text_y = GUESS_MARBLE_OFFSET_Y + MARBLE_RADIUS - \
        40  # Y coordinate within the leaderboard

    leaderboard_text.goto(text_x, text_y)
    leaderboard_text.write("Leaders:", align="left",
                           font=("Arial", 24, "bold"))


def draw_leaderboard_players(players):
    global LEADERS_TURTLE
    if LEADERS_TURTLE is not None:
        LEADERS_TURTLE.clear()

    leaderboard_text = turtle.Turtle()
    LEADERS_TURTLE = leaderboard_text
    leaderboard_text.hideturtle()
    leaderboard_text.penup()
    # Set the text color to dark blue for visibility
    leaderboard_text.color("dark blue")

    # Make sure the position is within the visible area of the leaderboard
    text_x = GUESS_MARBLE_OFFSET_X + BOARD_WIDTH + \
        60  # X coordinate within the leaderboard
    text_y = GUESS_MARBLE_OFFSET_Y + MARBLE_RADIUS - \
        40  # Y coordinate within the leaderboard

    for i, (k, v) in enumerate(players.items(), 1):
        leaderboard_text.goto(text_x, (i*-30) + text_y)
        leaderboard_text.write(f"{k}\t{v}", align="left",
                               font=("Arial", 24, "bold"))


# Adjusted function to draw the color palette with a border
def draw_color_pallete_board():
    color_palette = turtle.Turtle()
    color_palette.hideturtle()
    color_palette.speed('fastest')
    color_palette.penup()

    # Define the starting position for the color palette border
    # This should be aligned with the left side of the color palette
    palette_x = -SCREEN_WIDTH // 2 + 50
    # This should be just below the color palette
    palette_y = -SCREEN_HEIGHT // 2 + 20

    # Set the dimensions of the color palette border
    # Adjust if necessary to span the width of the color palette area
    palette_width = SCREEN_WIDTH - 100
    # Set to the height of the color palette area
    palette_height = COLOR_PALETTE_HEIGHT

    # Draw the border for the color palette
    palette_border = turtle.Turtle()
    palette_border.hideturtle()
    palette_border.speed('fastest')
    palette_border.penup()
    palette_border.pencolor("black")  # Set the pencolor for the palette border
    palette_border.pensize(5)  # Set the pensize for visibility
    palette_border.goto(palette_x, palette_y)
    palette_border.pendown()
    for _ in range(2):
        palette_border.forward(palette_width)
        palette_border.left(90)
        palette_border.forward(palette_height)
        palette_border.left(90)
    palette_border.hideturtle()

    # Adjust these values to move the color dots
    base_x = -SCREEN_WIDTH // 2 + 75   # Increase or decrease to move left or right
    base_y = palette_y + 55  # Increase or decrease to move up or down

    # Draw the color dots
    for i, color in enumerate(COLORS):
        new_marble = Marble(
            Point(base_x + i * (2 * MARBLE_SPACING), base_y - MARBLE_RADIUS), color)
        new_marble.draw()
        color_btns.append(new_marble)

    # wn.update()  # Update the window to show the drawn elements


def on_color_button_click(x, y, color):
    print(f"Color {color} clicked at coordinates ({x}, {y})!")


def draw_buttons():
    # Define button positions independently
    check_button_y = -SCREEN_HEIGHT // 2 + 70
    x_button_y = -SCREEN_HEIGHT // 2 + 70
    quit_button_y = -SCREEN_HEIGHT // 2 + 70

    # Create and position the Check button
    check_button = turtle.Turtle()
    check_button.shape("checkbutton.gif")
    check_button.penup()
    # Adjust the x coordinate as needed
    check_button.goto(-100, check_button_y)
    check_button.onclick(on_check_button_click)

    # Create and position the X button
    x_button = turtle.Turtle()
    x_button.shape("xbutton.gif")
    x_button.penup()
    x_button.goto(0, x_button_y)  # Adjust the x coordinate as needed
    x_button.onclick(on_x_button_click)

    # Create and position the Quit button
    quit_button = turtle.Turtle()
    quit_button.shape("quit.gif")
    quit_button.penup()
    quit_button.goto(350, quit_button_y)  # Adjust the x coordinate as needed
    quit_button.onclick(on_quit_button_click)

    wn.update()


def on_check_button_click(x, y):
    global tries, col_number

    if len(current_guess_colors) != 4:
        return
    # Placeholder function for check button click
    print("Check button clicked")
    pegs = score_pegs(secret_code, current_guess_colors)

    t_col = 0
    for k, v in pegs.items():
        for _ in range(v):
            all_guess_marbles[tries][-1][t_col].set_color(k)
            all_guess_marbles[tries][-1][t_col].draw()
            t_col += 1

    tries += 1

    update_leaders_dict()
    if current_guess_colors == secret_code:
        game_won()

    col_number = 0
    current_guess_colors.clear()

    for each in color_btns:
        each.draw()

    if tries == 10:
        draw_leaderboard()
        draw_leaderboard_players(LEADERS)
        lose_btn = turtle.Turtle()
        lose_btn.penup()
        lose_btn.shape("Lose.gif")
        lose_btn.goto(SCREEN_WIDTH//20, SCREEN_HEIGHT//20)
        wn.update()


def game_won():
    global LEADERS
    draw_leaderboard()
    draw_leaderboard_players(LEADERS)
    won_btn = turtle.Turtle()
    won_btn.penup()
    won_btn.shape("winner.gif")
    won_btn.goto(SCREEN_WIDTH//20, SCREEN_HEIGHT//20)
    wn.update()

    data_save()


def update_leaders_dict():
    global LEADERS
    if player_name in LEADERS:
        if LEADERS[player_name] < 10-tries:
            LEADERS[player_name] = 10-tries
    else:
        LEADERS[player_name] = 10-tries
    LEADERS = dict(
        sorted(LEADERS.items(), key=lambda x: x[1], reverse=True)[:10])


def data_save():
    with open(LEADER_FILE, 'w') as f:
        for k, v in LEADERS.items():
            f.write(f"{k},{v}\n")


def on_x_button_click(x, y):
    global col_number
    if col_number == 0:
        return
    # Placeholder function for X button click
    print("X button clicked")

    col_number -= 1
    current_guess_colors.pop()

    for each in color_btns:
        if each.color not in current_guess_colors:
            each.draw()

    all_guess_marbles[tries][col_number].set_color('white')
    all_guess_marbles[tries][col_number].draw()


def on_quit_button_click(x, y):
    # Placeholder function for quit button click
    print("Quit button clicked")
    close_btn = turtle.Turtle()
    close_btn.penup()
    close_btn.shape("quitmsg.gif")
    close_btn.goto(SCREEN_WIDTH//20, SCREEN_HEIGHT//20)
    wn.update()

    time.sleep(5)
    turtle.bye()


def score_pegs(secret, current_guess):
    if len(secret) != len(current_guess):
        # Lists must be of the same length to compare positions and values.
        return {}

    red_pegs = 0
    black_pegs = 0

    for i in range(len(secret)):
        if secret[i] == current_guess[i]:
            black_pegs += 1
        elif current_guess[i] in secret:
            red_pegs += 1

    return {"red": red_pegs, "black": black_pegs}


def detect_area(x, y):
    global col_number

    for each in color_btns:
        if each.clicked_in_region(x, y) and each.color not in current_guess_colors and len(current_guess_colors) < 4 and col_number < 4:
            # print(each.color, 'clicked')
            current_guess_colors.append(each.color)
            each.erase()

            all_guess_marbles[tries][col_number].set_color(each.color)
            all_guess_marbles[tries][col_number].draw()

            col_number += 1

# ask the username:


if __name__ == '__main__':
    # Set up the screen
    wn = turtle.Screen()  # Create a turtle screen object
    wn.title("CS5001 MasterMind Code Game")  # Set the title of the window
    # Set up the window size
    wn.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    wn.bgcolor("white")  # Set the background color of the window
    wn.tracer(0)  # Turn off animation for instant drawing

    # Register button shapes
    wn.register_shape("checkbutton.gif")
    wn.register_shape("quit.gif")
    wn.register_shape("xbutton.gif")
    wn.register_shape("winner.gif")
    wn.register_shape("Lose.gif")
    wn.register_shape("quitmsg.gif")
    wn.register_shape("leaderboard_error.gif")

    # Main program
    player_name = wn.textinput(
        "Mastermind Game", "Enter your name:") or "Player"

    if not os.path.exists(LEADER_FILE):
        open(LEADER_FILE, 'w')
        leader_error = turtle.Turtle()
        leader_error.penup()
        leader_error.shape("leaderboard_error.gif")
        leader_error.goto(SCREEN_WIDTH//20, SCREEN_HEIGHT//20)
        wn.update()
        time.sleep(2)
        leader_error.clear()
        wn.update()

    LEADERS = {}

    with open(LEADER_FILE, 'r') as f:
        for line in f:
            line = line.strip().split(',')
            LEADERS[line[0]] = int(line[1])

    # getting only top 10 PERSONS
    LEADERS = dict(
        sorted(LEADERS.items(), key=lambda x: x[1], reverse=True)[:10])
    print("LEADERS", LEADERS)

    LEADERS_TURTLE = None

    # Initialize game variables
    # A list of 4 unique random colors
    # secret_code = [random.choice(COLORS) for _ in range(4)]
    secret_code = random.sample(COLORS, 4)
    guesses = []
    results = []
    tries = 0
    all_guess_marbles: list[list[Marble | list[Marble]]] = []
    current_guess_marbles = []
    current_guess_colors = []
    color_btns: list[Marble] = []
    # Call the drawing functions
    draw_guess_board()
    draw_leaderboard()
    draw_leaderboard_players(LEADERS)
    draw_color_pallete_board()
    draw_buttons()

    col_number = 0

    print("CORRECT CODE", secret_code)

    wn.onclick(detect_area)

    # Main loop
    wn.mainloop()