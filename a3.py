"""
CSSE1001 Assignment 3
Semester 2, 2017
"""

# There are a number of jesting comments in the support code
# They should not be taken seriously. Keep it fun folks :D
# Students are welcome to add their own source code humour, provided it remains civil

import tkinter as tk
from tkinter import messagebox
from tkinter.messagebox import showinfo, askquestion
import random

from view import GridView, ObjectivesView
from game import DotGame, ObjectiveManager, CompanionGame, CoreDotGame
from dot import BasicDot, WildcardDot
from util import create_animation, ImageManager, load_image
from companion import UselessCompanion
from cell import VoidCell

# Fill these in with your details
__author__ = "Jia Hao Wu (s4403711)"
__email__ = ""
__date__ = ""

__version__ = "1.1.2"

DEFAULT_ANIMATION_DELAY = 0  # (ms)
ANIMATION_DELAYS = {
    # step_name => delay (ms)
    'ACTIVATE_ALL': 50,
    'ACTIVATE': 100,
    'ANIMATION_BEGIN': 300,
    'ANIMATION_DONE': 0,
    'ANIMATION_STEP': 200
}


# Define your classes here
class InfoPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.remaining_moves_label = tk.Label(self, font=('Times New Roman', 20, 'italic'))
        self.remaining_moves_label.pack(side=tk.LEFT, anchor=tk.NW)

        self.score_label = tk.Label(self)
        self.score_label.pack(side=tk.LEFT, anchor=tk.S)

        self.icon_button = tk.Button(self)
        self.icon_button.pack(side=tk.LEFT)

        self.objectives = None

    def set_default_icon(self, icon):
        self.icon_button.config(image=icon)

    def set_objectives(self, image_manager, objectives):
        self.objectives = ObjectivesView(self, image_manager=image_manager)
        self.objectives.pack(side=tk.RIGHT)
        self.objectives.draw(objectives)

    def refresh_objectives(self, objectives):
        self.objectives.draw(objectives)

    def decrease_remaining_moves_and_increase_score(self, moves, score):
        self.remaining_moves_label.config(text=moves)
        self.score_label.config(text=score)


class IntervalBar(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent, bg='white', width=48 * 6, height=24)

    def draw_step(self, count):
        self.delete(tk.ALL)
        blank_step = "self.create_rectangle(1.5 + 48 * {}, 1.5, 0.5 + 48 * {}, 24.5, outline='light grey', width=1.1)"
        filled_step = "self.create_rectangle(1.5 + 48 * {}, 1.5, 0.5 + 48 * {}, 24.5, fill='#5CACEE', outline='light grey', width=1.1)"
        i = 0
        for i in range(count):
            eval(filled_step.format(i, i + 1))
        for j in range(6 - count):
            eval(blank_step.format(j + i + 1, j + i + 2))


class CompanionDot(BasicDot):
    DOT_NAME = 'companion'

    def activate(self, position, game, activated, has_loop=False):
        super().activate(position, game, activated, has_loop)
        game.companion.charge()
        print(game.companion.get_charge())


class BuffaloCompanion(UselessCompanion):
    def activate(self, game):
        super().activate(game)
        loop = True
        while loop:
            temp = random.choice(list(game.grid.items()))
            position = temp[0]
            if type(temp[1]) is type(VoidCell()):
                continue
            name = temp[1].get_dot().get_name()
            if name != WildcardDot().get_name():
                loop = False
        print(position, name)
        game._connected = [position, position, (3, 3), (3, 4), (4, 4), (4, 3), (-3, 3)]
        game.connect((-3, 3))
        game._score -= 1


# You may edit as much of DotsApp as you wish
class DotsApp:
    """Top level GUI class for simple Dots & Co game"""
    DEFAULT_TITLE = 'Dots & Co'
    FIRST = True

    def __init__(self, master, icon=None, switch=False):
        """Constructor

        Parameters:
            master (tk.Tk|tk.Frame): The parent widget
        """
        self._master = master
        master.title(self.DEFAULT_TITLE)

        self.flag = False

        self.default_icon = tk.PhotoImage(file='images/companions/useless.gif')

        self.extra_icon = tk.PhotoImage(file='images/companions/penguin.gif')

        self.icon = icon if icon else self.default_icon

        self.default_step = 1

        self.score = 0

        self._playing = True

        self._image_manager = ImageManager('images/dots/', loader=load_image)

        menu_bar = tk.Menu(master)
        master.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar)
        menu_bar.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='New Game', command=self.reset)
        file_menu.add_command(label='Exit Game', command=self.close)

        master.protocol('WM_DELETE_WINDOW', self.close)

        # Game
        counts = [10, 15, 25, 25]
        random.shuffle(counts)
        # randomly pair counts with each kind of dot
        objectives = zip([BasicDot(1), BasicDot(2), BasicDot(4), BasicDot(3)], counts)

        self._objectives = ObjectiveManager(objectives)

        dead_cells = {(2, 2), (2, 3), (2, 4),
                      (3, 2), (3, 3), (3, 4),
                      (4, 2), (4, 3), (4, 4),
                      (0, 7), (1, 7), (6, 7), (7, 7)}
        self.dot_game = DotGame({BasicDot: 1}, objectives=self._objectives, kinds=(1, 2, 3, 4), size=(8, 8),
                                dead_cells=dead_cells)
        self.companion_game = CompanionGame({BasicDot: 43, CompanionDot: 9, WildcardDot: 6}, BuffaloCompanion(),
                                            objectives=self._objectives,
                                            kinds=(1, 2, 3, 4),
                                            size=(8, 8), dead_cells=dead_cells)

        # Game
        self._game = self.companion_game if switch else self.dot_game
        if self.FIRST:
            reply = askquestion(type=messagebox.YESNO, title='Select Model',
                                message='Would you like to start a new game with "Companion Dot"?')
            if reply == messagebox.YES:
                showinfo('"Companion Dot" Model', 'Enjoy the game with "Companion Dot"!')
                self.icon = self.extra_icon
                self._game = self.companion_game
                self._master.title('Dots & Co - "Companion Dot"')
            else:
                showinfo('New Game', 'Enjoy the basic game!')
                self._game = self.dot_game
            self.FIRST = False

        # The following code may be useful when you are implementing task 2:
        # for i in range(0, 4):
        #     for j in range(0, 2):
        #         position = i, j
        #         self._game.grid[position].set_dot(BasicDot(3))
        # self._game.grid[(7, 3)].set_dot(BasicDot(1))

        # InfoPanel
        self.info_panel = InfoPanel(master)
        self.info_panel.set_default_icon(self.icon)
        self.info_panel.decrease_remaining_moves_and_increase_score(self._game.get_moves(), self._game.get_score())
        self.info_panel.set_objectives(self._image_manager, self._objectives.get_status())
        self.info_panel.pack()

        # IntervalBar
        self.interval_bar = IntervalBar(master)
        self.interval_bar.draw_step(self.default_step)
        self.interval_bar.pack()

        # Grid View
        self._grid_view = GridView(master, size=self._game.grid.size(), image_manager=self._image_manager)
        self._grid_view.pack()
        self._grid_view.draw(self._game.grid)
        self.draw_grid_borders()

        # Events
        self.bind_events()

        # Set initial score again to trigger view update automatically
        self._refresh_status()

    def close(self):
        if self.can_close():
            self._master.destroy()

    def can_close(self):
        reply = askquestion(type=messagebox.YESNO, title='Confirm Exit', message='Are you sure you want to quit?')
        if reply == messagebox.YES:
            return True
        else:
            return False

    def draw_grid_borders(self):
        """Draws borders around the game grid"""

        borders = list(self._game.grid.get_borders())

        # this is a hack that won't work well for multiple separate clusters
        outside = max(borders, key=lambda border: len(set(border)))

        for border in borders:
            self._grid_view.draw_border(border, fill=border != outside)

    def bind_events(self):
        """Binds relevant events"""
        self._grid_view.on('start_connection', self._drag)
        self._grid_view.on('move_connection', self._drag)
        self._grid_view.on('end_connection', self._drop)

        self._game.on('reset', self._refresh_status)
        self._game.on('complete', self._drop_complete)

        self._game.on('connect', self._connect)
        self._game.on('undo', self._undo)

    def _animation_step(self, step_name):
        """Runs for each step of an animation

        Parameters:
            step_name (str): The name (type) of the step
        """
        print(step_name)
        self._refresh_status()
        self.draw_grid()

    def animate(self, steps, callback=lambda: None):
        """Animates some steps (i.e. from selecting some dots, activating companion, etc.

        Parameters:
            steps (generator): Generator which yields step_name (str) for each step in the animation
        """

        if steps is None:
            steps = (None for _ in range(1))

        animation = create_animation(self._master, steps,
                                     delays=ANIMATION_DELAYS, delay=DEFAULT_ANIMATION_DELAY,
                                     step=self._animation_step, callback=callback)
        animation()

    def _drop(self, position):  # pylint: disable=unused-argument
        """Handles the dropping of the dragged connection

        Parameters:
            position (tuple<int, int>): The position where the connection was
                                        dropped
        """
        if not self._playing:
            return

        if self._game.is_resolving():
            return

        self._grid_view.clear_dragged_connections()
        self._grid_view.clear_connections()

        self.animate(self._game.drop())

    def _connect(self, start, end):
        """Draws a connection from the start point to the end point

        Parameters:
            start (tuple<int, int>): The position of the starting dot
            end (tuple<int, int>): The position of the ending dot
        """

        if self._game.is_resolving():
            return
        if not self._playing:
            return
        self._grid_view.draw_connection(start, end,
                                        self._game.grid[start].get_dot().get_kind())

    def _undo(self, positions):
        """Removes all the given dot connections from the grid view

        Parameters:
            positions (list<tuple<int, int>>): The dot connects to remove
        """
        for _ in positions:
            self._grid_view.undo_connection()

    def _drag(self, position):
        """Attempts to connect to the given position, otherwise draws a dragged
        line from the start

        Parameters:
            position (tuple<int, int>): The position to drag to
        """

        if self._game.is_resolving():
            return
        if not self._playing:
            return

        tile_position = self._grid_view.xy_to_rc(position)

        if tile_position is not None:
            cell = self._game.grid[tile_position]
            dot = cell.get_dot()

            if dot and self._game.connect(tile_position):
                self._grid_view.clear_dragged_connections()
                return

        kind = self._game.get_connection_kind()

        if not len(self._game.get_connection_path()):
            return

        start = self._game.get_connection_path()[-1]

        if start:
            self._grid_view.draw_dragged_connection(start, position, kind)

    @staticmethod
    def remove(*_):
        """Deprecated in 1.1.0"""
        raise DeprecationWarning("Deprecated in 1.1.0")

    def draw_grid(self):
        """Draws the grid"""
        self._grid_view.draw(self._game.grid)

    def reset(self):
        """Resets the game"""
        # raise NotImplementedError()
        if self._playing:
            reply = askquestion(type=messagebox.YESNO, title='Now Playing', message='Are you sure you want to restart?')
            if reply == messagebox.YES:
                self.select_model()
            else:
                pass
        else:
            self.select_model()

    def select_model(self):
        reply = askquestion(type=messagebox.YESNOCANCEL, title='Select Model',
                            message='Would you like to start a new game with "Companion Dot"?')
        if reply == messagebox.YES:
            showinfo('"Companion Dot" Model', 'Enjoy the game with "Companion Dot"!')
            self.restart(True)
            # self.restart_o()
            self._master.title('Dots & Co - "Companion Dot"')
        elif reply == messagebox.NO:
            showinfo('New Game', 'Enjoy the basic game!')
            self.restart()
        else:
            pass

    def restart(self, flag=False):
        self.info_panel.destroy()
        self.interval_bar.destroy()
        self._grid_view.destroy()
        if flag:
            self.__init__(self._master, self.extra_icon, True)
        else:
            self.__init__(self._master)

    def check_game_over(self):
        """Checks whether the game is over and shows an appropriate message box if so"""
        state = self._game.get_game_state()

        if state == self._game.GameState.WON:
            showinfo("Game Over!", "You won!!!")
            self._playing = False
        elif state == self._game.GameState.LOST:
            showinfo("Game Over!",
                     f"You didn't reach the objective(s) in time. You connected {self._game.get_score()} points")
            self._playing = False

    def _drop_complete(self):
        """Handles the end of a drop animation"""

        # Useful for when implementing a companion
        # if self._game.companion.is_fully_charged():
        #     self._game.companion.reset()
        #     steps = self._game.companion.activate(self._game)
        #     self._refresh_status()
        #
        #     return self.animate(steps)

        # Need to check whether the game is over
        # raise NotImplementedError()  # no mercy for stooges
        print(self._game.get_game_state())
        if self.flag:
            if self._game.companion.is_fully_charged():
                self._game.companion.reset()
                showinfo('Ultimate Skill!!!!', 'BOOM SHAKALAKA!!!!!!!')
                self._game.companion.activate(self._game)
            self.interval_bar.draw_step(self._game.companion.get_charge() + 1)
            self.flag = False
        self.check_game_over()
        if not self._playing:
            print('ok')

    def _refresh_status(self):
        """Handles change in game status"""

        # Normally, this should raise the following error:
        # raise NotImplementedError()
        # But so that the game can work prior to this method being implemented,
        # we'll just print some information
        # Sometimes I believe Python ignores all my comments :(
        score = self._game.get_score()
        print("Score is now {}.".format(score))
        if self.score < score:
            if type(self._game) is type(self.dot_game):
                self.basic_progress()
            else:
                self.companion_progress()
            self.score = score
            self.info_panel.decrease_remaining_moves_and_increase_score(self._game.get_moves(), score)
            self.info_panel.refresh_objectives(self._objectives.get_status())

    def basic_progress(self):
        self.default_step += 1
        if self.default_step > 6:
            self.default_step = 1
        self.interval_bar.draw_step(self.default_step)

    def companion_progress(self):
        if self._game.companion.get_charge() < 6:
            self.interval_bar.draw_step(self._game.companion.get_charge() + 1)
        else:
            self.interval_bar.draw_step(self._game.companion.get_charge())
            self.flag = True


def main():
    """Sets-up the GUI for Dots & Co"""
    # Write your GUI instantiation code here
    root = tk.Tk()
    DotsApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
