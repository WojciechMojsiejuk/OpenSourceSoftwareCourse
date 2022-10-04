import turtle
import glob
import time
import warnings

# global scope variables
WORLD_SIZE = 600
TILE_SIZE = 32
ROTATION_ANGLE = 90
TURN_TIME = 5


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class RunawayGame(metaclass=Singleton):
    runner = None
    chaser = None
    walls = []
    human_steps = []
    minotaur_steps = []
    exits = []
    timer_msec = 1000
    score_drawer = None
    drawer = None
    canvas = None
    levels = []
    runner_score = 0
    chaser_score = 0
    level_finished = False
    @classmethod
    def __init__(cls, canvas):
        cls.canvas = canvas
        cls.levels = glob.glob('*.csv')
        # Instantiate turtle for drawing
        cls.drawer = turtle.RawTurtle(cls.canvas)
        cls.drawer.hideturtle()
        cls.drawer.penup()
        cls.drawer.setpos(470, 500)

        cls.score_drawer = turtle.RawTurtle(cls.canvas)
        cls.score_drawer.hideturtle()
        cls.score_drawer.penup()
        cls.score_drawer.setpos(470, 550)
        cls.read_map(cls.levels.pop(0))

    @classmethod
    def start(cls):
        cls.runner.turn = True
        cls.level_finished = False
        cls.canvas.ontimer(cls.step, cls.timer_msec)

    @classmethod
    def step(cls):
        cls.score_drawer.clear()
        cls.drawer.clear()
        cls.score_drawer.write(f'Runner: {cls.runner_score} Chaser: {cls.chaser_score}', font=('Arial', 10, 'bold'))
        if cls.runner is not None and cls.chaser is not None:
            try:
                if cls.runner.turn:
                    cls.drawer.write(f'Runners turn. Remaining time: {cls.runner.timer} s', font=('Arial', 8, 'normal'))
                    cls.runner.timer -= 1

                    if cls.runner.timer <= 0.0:
                        cls.chaser.on_win()
                elif cls.chaser.turn:
                    cls.drawer.write(f'Chaser turn. Remaining time: {cls.runner.timer} s', font=('Arial', 8, 'normal'))
                    cls.chaser.timer -= 1

                    if cls.chaser.timer <= 0.0:
                        cls.runner.on_win()
                if not cls.level_finished:
                    cls.canvas.ontimer(cls.step, cls.timer_msec)
            except AttributeError as ae:
                warnings.warn(ae, RuntimeWarning)
                if not cls.levels:
                    cls.canvas.exitonclick()
                else:
                    cls.next_level()


    @classmethod
    def next_level(cls):
        cls.level_finished = True
        cls.runner.turn = False
        cls.chaser.turn = False
        cls.canvas.clear()
        cls.canvas.bgcolor('#F8F400')
        cls.on_destroy()
        if cls.levels:
            cls.read_map(cls.levels.pop(0))
            cls.start()
        else:
            cls.drawer.setpos(250, 300)
            cls.drawer.write(f'THE END. \n THANKS FOR PLAYING', align='center', font=('Arial', 18, 'normal'))
            cls.canvas.exitonclick()

    @classmethod
    def on_destroy(cls):
        cls.walls = []
        for idx, _ in enumerate(cls.human_steps):
            cls.human_steps[idx] = None
        cls.human_steps = []
        for idx, _ in enumerate(cls.minotaur_steps):
            cls.minotaur_steps[idx] = None
        cls.minotaur_steps = []
        time.sleep(1) # We need to wait 1 s because of the timer racing condition !
        cls.runner = None
        cls.chaser = None

    @classmethod
    def read_map(cls, filename):
        with open(filename, 'r') as f:
            for x_pos, line in enumerate(f.readlines()):
                line = line.strip()
                line = line.split(',')
                for y_pos, map_obj in enumerate(line):
                    try:
                        map_obj = int(map_obj)
                    except ValueError:
                        raise ValueError("Invalid map object, must be a number")

                    match map_obj:
                        case 1:
                            wall = Wall(cls.canvas, (
                                x_pos * TILE_SIZE + TILE_SIZE / 2, WORLD_SIZE - y_pos * TILE_SIZE - TILE_SIZE / 2))
                            cls.walls.append(wall)
                        case 2:
                            cls.exits.append(Exit(cls.canvas,
                                                  (x_pos * TILE_SIZE + TILE_SIZE / 2,
                                                   WORLD_SIZE - y_pos * TILE_SIZE - TILE_SIZE / 2)))
                        case 3:
                            cls.runner = Runner(canvas=cls.canvas,
                                                position=(x_pos * TILE_SIZE + TILE_SIZE / 2,
                                                          WORLD_SIZE - y_pos * TILE_SIZE - TILE_SIZE / 2),
                                                moveset={
                                                    'Up': 'Up',
                                                    'Down': 'Down',
                                                    'Left': 'Left',
                                                    'Right': 'Right',

                                                }
                                                )
                        case 4:
                            cls.chaser = Chaser(canvas=cls.canvas,
                                                position=(x_pos * TILE_SIZE + TILE_SIZE / 2,
                                                          WORLD_SIZE - y_pos * TILE_SIZE - TILE_SIZE / 2),
                                                moveset={
                                                    'Up': 'w',
                                                    'Down': 's',
                                                    'Left': 'a',
                                                    'Right': 'd',

                                                },
                                                )


class ManualMover(turtle.RawTurtle):

    def __init__(self, canvas, position, moveset):
        super().__init__(canvas)
        self.step_move = TILE_SIZE
        self.step_turn = ROTATION_ANGLE
        self.penup()
        self.setpos(position)
        self.turn = False
        self.timer = TURN_TIME

        # Register event handlers
        canvas.onkeypress(lambda: self.check_collision(moveset['Up']), moveset['Up'])
        canvas.onkeypress(lambda: self.check_collision(moveset['Down']), moveset['Down'])
        canvas.onkeypress(lambda: self.check_collision(moveset['Left']), moveset['Left'])
        canvas.onkeypress(lambda: self.check_collision(moveset['Right']), moveset['Right'])
        canvas.listen()

    def check_collision(self, move_set):
        if self.turn:
            old_position = self.pos()
            new_position = old_position
            match move_set:
                case 'Up' | 'w':
                    new_position = (old_position[0], old_position[1] + TILE_SIZE)
                case 'Down' | 's':
                    new_position = (old_position[0], old_position[1] - TILE_SIZE)
                case 'Left' | 'a':
                    new_position = (old_position[0] - TILE_SIZE, old_position[1])
                case 'Right' | 'd':
                    new_position = (old_position[0] + TILE_SIZE, old_position[1])
            self.setpos(new_position)
            for wall in RunawayGame.walls:
                p = wall.pos()
                q = self.pos()
                dx, dy = p[0] - q[0], p[1] - q[1]
                if dx ** 2 + dy ** 2 < TILE_SIZE:
                    self.setpos(old_position)
                    return

            if isinstance(self, Chaser):
                self.turn = False
                RunawayGame.chaser.timer = TURN_TIME
                RunawayGame.minotaur_steps.append(MinotaurStep(RunawayGame.canvas, old_position))
                if self.distance(RunawayGame.runner) < TILE_SIZE:
                    self.on_win()
                for step in RunawayGame.minotaur_steps:
                    if self.distance(step) < TILE_SIZE:
                        RunawayGame.runner.on_win()
                RunawayGame.runner.turn = True

            if isinstance(self, Runner):
                self.turn = False
                RunawayGame.runner.timer = TURN_TIME
                RunawayGame.human_steps.append(HumanStep(RunawayGame.canvas, old_position))
                for exit in RunawayGame.exits:
                    try:
                        if self.distance(exit) < TILE_SIZE:
                            self.on_win()
                    except UnboundLocalError as ule:
                        warnings.warn(ule, RuntimeWarning)
                for step in RunawayGame.human_steps:
                    try:
                        if self.distance(step) < TILE_SIZE:
                            RunawayGame.chaser.on_win()
                    except UnboundLocalError as ule:
                        warnings.warn(ule, RuntimeWarning)
                RunawayGame.chaser.turn = True

            return

    def on_win(self):
        if isinstance(self, Runner):
            RunawayGame.runner_score += 1
        elif isinstance(self, Chaser):
            RunawayGame.chaser_score += 1
        RunawayGame.next_level()

class Runner(ManualMover):

    def __init__(self, canvas, position, moveset):
        super().__init__(canvas, position, moveset)
        self.shape('theseus_32.gif')
        self.pendown()
        self.pen(pencolor="blue")


class Chaser(ManualMover):
    def __init__(self, canvas, position, moveset):
        super().__init__(canvas, position, moveset)
        self.shape('minotaur_32.gif')


class InActiveObject(turtle.RawTurtle):
    def __init__(self, canvas, position):
        super().__init__(canvas)
        self.speed('fastest')
        self.penup()
        self.setpos(position)


class Wall(InActiveObject):
    def __init__(self, canvas, position):
        super().__init__(canvas, position)
        self.shape('wall_32.gif')


class Exit(InActiveObject):
    def __init__(self, canvas, position):
        super().__init__(canvas, position)
        self.shape('exit_32.gif')


class HumanStep(InActiveObject):
    def __init__(self, canvas, position):
        super().__init__(canvas, position)
        self.shape('human_step.gif')
        RunawayGame.human_steps.append(self)


class MinotaurStep(InActiveObject):
    def __init__(self, canvas, position):
        super().__init__(canvas, position)
        self.shape('minotaur_step.gif')


if __name__ == '__main__':
    canvas = turtle.Screen()
    canvas.reset()
    canvas.screensize(WORLD_SIZE, WORLD_SIZE)
    canvas.setworldcoordinates(0, 0, WORLD_SIZE, WORLD_SIZE)
    canvas.bgcolor('#F8F400')
    canvas.addshape("wall_32.gif")
    canvas.addshape("exit_32.gif")
    canvas.addshape("theseus_32.gif")
    canvas.addshape("minotaur_32.gif")
    canvas.addshape("human_step.gif")
    canvas.addshape("minotaur_step.gif")

    game = RunawayGame(canvas)
    game.start()
    canvas.mainloop()
