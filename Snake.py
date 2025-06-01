import random
import turtle

# Define program constants
WIDTH = 800
HEIGHT = 600
DELAY = 100  # Milliseconds
FOOD_SIZE: int = 32
SNAKE_SIZE = 20

offsets = {
    "up": (0, SNAKE_SIZE),
    "down": (0, -SNAKE_SIZE),
    "left": (-SNAKE_SIZE, 0),
    "right": (SNAKE_SIZE, 0)
            }


# High score
high_score = 0

# Load the high score if it exist
try:
    with open("snake_highscore.txt", "r") as file:
        high_score = int(file.read())
except FileNotFoundError:
    pass


def update_high_score():
    global high_score
    if score > high_score:
        high_score = score
        with open("snake_highscore.txt", "w") as file:
            file.write(str(high_score))


def bind_direction_keys():
    screen.onkey(lambda: set_snake_direction("up"), "Up")
    screen.onkey(lambda: set_snake_direction("down"), "Down")
    screen.onkey(lambda: set_snake_direction("right"), "Right")
    screen.onkey(lambda: set_snake_direction("left"), "Left")


def set_snake_direction(direction):
    global snake_direction
    if direction == "up":
        if snake_direction != "down":  # No self-collision
            snake_direction = "up"

    elif direction == "down":
        if snake_direction != "up":  # No self-collision
            snake_direction = "down"

    elif direction == "left":
        if snake_direction != "right":  # No self-collision
            snake_direction = "left"

    elif direction == "right":
        if snake_direction != "left":  # No self-collision
            snake_direction = "right"


def game_loop():
    stamper.clearstamps()  # Remove existing stamps made by stamper

    new_head = snake[-1].copy()
    new_head[0] += offsets[snake_direction][0]
    new_head[1] += offsets[snake_direction][1]

    # Check collissions
    if new_head in snake or new_head[0] < -WIDTH / 2 or new_head[0] > WIDTH / 2 or new_head[1] < -HEIGHT / 2 or \
            new_head[1] > HEIGHT / 2:
        reset()

    else:
        # Add new head to snake body.
        snake.append(new_head)

        # Check food collision
        if not food_collision():
            snake.pop(0)  # Keep the snake the same length unless fed

        # Draw snake
        stamper.shape("Imagini/snake-head-20x20.gif")
        stamper.goto(snake[-1][0], snake[-1][1])
        stamper.stamp()
        stamper.shape("circle")
        for segment in snake[:-1]:
            stamper.goto(segment[0], segment[1])
            stamper.stamp()

        # Refresh screen
        screen.title(f"Snake Game. Score:{score} High Score:{high_score}")
        screen.update()

        # Rinse and repeat
        turtle.ontimer(game_loop, DELAY)


def food_collision():
    global food_pos, score
    if get_distance(snake[-1], food_pos) < 20:
        score += 1
        update_high_score()
        food_pos = get_random_food_pos()
        food.goto(food_pos)
        return True
    return False


def get_random_food_pos():
    x = random.randint(-WIDTH // 2 + FOOD_SIZE, WIDTH // 2 - FOOD_SIZE)
    y = random.randint(-HEIGHT // 2 + FOOD_SIZE, HEIGHT // 2 - FOOD_SIZE)
    return x, y


def get_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    distance = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5  # Pythagora's Theorem
    return distance


def reset():
    global score, snake, snake_direction, food_pos
    score = 0
    snake = [[0, 0], [SNAKE_SIZE, 0], [SNAKE_SIZE * 2, 0], [SNAKE_SIZE * 3, 0]]
    snake_direction = "up"
    food_pos = get_random_food_pos()
    food.goto(food_pos)
    game_loop()


# create a window where we will do our drawing
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.title("Snake")
screen.bgpic("Imagini/bg2.gif")
screen.register_shape("Imagini/snake-food-32x32.gif")
screen.register_shape("Imagini/snake-head-20x20.gif")
screen.tracer(0)  # Turn off automatic animations

# Event handlers
screen.listen()
bind_direction_keys()

# Create a turtle to do your binding
stamper = turtle.Turtle()
stamper.shape("circle")
stamper.color("#009ef1")
stamper.penup()

# Create snake as  a list of coordinate pairs.
snake = [[0, 0], [20, 0], [40, 0], [60, 0]]
snake_direction = "up"
score = 0

# Food
food = turtle.Turtle()
food.shape("Imagini/snake-food-32x32.gif")
food.shapesize(FOOD_SIZE / 20)
food.penup()
food_pos = get_random_food_pos()
food.goto(food_pos)

# Set animation in motion
reset()

# Finish nicely
turtle.done()
