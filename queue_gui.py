import tkinter as tk
from tkinter import messagebox
from tkinter.messagebox import showinfo, showwarning, showerror, askquestion

import time
import random
import threading

# Fill these in with your details
__author__ = ''
__email__ = ''
__date__ = ''

G = []  # self defined list for storing variable

QUICK_STUDENT_DICT = {}  # the asked quick questions students' data dict
LONG_STUDENT_DICT = {}  # the asked long questions students' data dict


def play():
    """
    Called when the hidden button be clicked
    this method will display the game window of the Finger-Guessing Game
    """

    def combat(gesture):
        """
        the method calculates the result of game
        Meanwhile, modifies the widgets and show some info to interact with player according to the game result
        it's up to the gestures given by player and bot(purely random choice)
        the way calculating result under 3 cases below
        1. scissors to cloth, scissors won
        2. hammer to scissors, hammer won
        3. cloth to hammer, cloth won
        :param gesture: the gesture given by player
        """
        order_list = list(command_dict.keys())  # ['scissors', 'hammer', 'cloth']
        idiot_gesture = random.choice(order_list)  # bot's choice
        for key in command_dict.keys():
            if key == idiot_gesture:
                command_dict.get(key)[0].config(state=tk.NORMAL)  # show the bot's choice
            if key != gesture:
                command_dict.get(key)[1].config(state=tk.DISABLED)  # disable the remaining gestures
        result = order_list.index(gesture) - order_list.index(idiot_gesture)
        if gesture == idiot_gesture:
            bar.config(text='DRAW')
            showinfo('Draw', "You sure you have a same idea as noob?")
            time.sleep(1)
        elif result is 1 or result is -2:
            reply = askquestion(type=messagebox.YESNO, title='You Slayer Man', message='Retry it?')
            if reply == messagebox.NO:
                root.destroy()
                return
        else:
            reply = askquestion(type=messagebox.YESNO, title="It Serves You Right", message='Retry it?')
            if reply == messagebox.NO:
                root.destroy()
                return
        bar.config(text='VS')
        for key in command_dict.keys():
            command_dict.get(key)[0].config(state=tk.DISABLED)
            command_dict.get(key)[1].config(state=tk.NORMAL)

    showinfo('', "Let's get it!")
    root = tk.Toplevel()
    root.title('Finger-Guessing Game')
    idiot = tk.Frame(root)
    scissors_img, hammer_img, cloth_img = G[0].get_images()
    scissors = tk.Button(idiot, image=scissors_img, state=tk.DISABLED)
    scissors.pack(side=tk.LEFT, padx=44, pady=4)
    hammer = tk.Button(idiot, image=hammer_img, state=tk.DISABLED)
    hammer.pack(side=tk.LEFT, padx=44, pady=4)
    cloth = tk.Button(idiot, image=cloth_img, state=tk.DISABLED)
    cloth.pack(side=tk.LEFT, padx=44, pady=4)
    idiot.pack()
    tk.Label(root, text='↑ NOOB ↑').pack()
    bar = tk.Label(root, text='VS', bg='red', fg='white', font='Arial 16 bold')
    bar.pack(ipadx=227, pady=10)
    tk.Label(root, text='↓ UGUY ↓').pack()
    player_scissors = tk.Button(root, image=scissors_img, command=lambda: combat('scissors'))
    player_scissors.pack(side=tk.LEFT, padx=44, pady=4)
    player_hammer = tk.Button(root, image=hammer_img, command=lambda: combat('hammer'))
    player_hammer.pack(side=tk.LEFT, padx=44, pady=4)
    player_cloth = tk.Button(root, image=cloth_img, command=lambda: combat('cloth'))
    player_cloth.pack(side=tk.LEFT, padx=44, pady=4)
    command_dict = {'scissors': (scissors, player_scissors), 'hammer': (hammer, player_hammer),
                    'cloth': (cloth, player_cloth)}
    root.mainloop()


def get_quick_student_dict():
    """
    get the asked quick questions students' data dict
    :return: the asked quick questions students' data dict
    """
    return QUICK_STUDENT_DICT


def get_long_student_dict():
    """
    get the asked long questions students' data dict
    :return: the asked long questions students' data dict
    """
    return LONG_STUDENT_DICT


def add_quick_student_dict():
    """
    Called when the Request Quick Help button be clicked
    """
    display_entry_widget(get_quick_student_dict())


def add_long_student_dict():
    """
    Called when the Request Long Help button be clicked
    """
    display_entry_widget(get_long_student_dict())


def display_entry_widget(student_dict):
    """
    display a entry widget for the students to type their name
    add the student to the queue after they typed a correct name
    :param student_dict: QUICK_STUDENT_DICT or LONG_STUDENT_DICT
    """

    def add_student_dict():
        """
        validate the name if it's proper
        add this student to the queue
        """
        name = entry.get()  # get what student typed
        if name and not name.strip():
            showerror('Not Just Typed Spaces', 'Please give the proper name!')
            return
        name = name.strip()
        if name:
            if name not in student_dict:  # a student never asking a question of a type(long or quick)
                student_dict[name] = [True, 0, time.time()]
            elif student_dict[name][0]:
                showwarning('Invalid Participation', "You're in line already!")
                return
            else:
                record_list = [True, student_dict[name][1], time.time()]
                del (student_dict[name])
                student_dict[name] = record_list
            G[0].refresh()
            root.destroy()
        else:
            showerror('Not Be Empty', 'Please give the proper name!')

    root = tk.Toplevel()
    root.title('')
    root.wm_attributes('-topmost', 1)
    label = tk.Label(root, text='Type Your Name:')
    label.pack(side=tk.LEFT)
    entry = tk.Entry(root, width=20)
    entry.pack(side=tk.LEFT, padx=5)
    join = tk.Button(root, text='Join', command=add_student_dict)
    join.pack(side=tk.RIGHT)
    root.mainloop()


def get_display(record, now):
    """
    count the delta and return the str according to this delta
    :param record: the student's time stamp when joined the queue
    :param now: the time stamp when the sub method called
    :return: the display str for showing the wait time of the student
    """
    delta = int(now - record)
    if delta < 60:
        return 'a few seconds ago', delta
    if delta < 120:
        return 'a minute ago', delta
    if delta < 3600:
        return '{} minutes ago'.format(delta // 60), delta
    if delta < 7200:
        return '1 hour ago', delta
    return '{} hours age'.format(delta // 3600), delta


def get_notice(average):
    """
    same like get_display but this method return for displaying average
    :param average: the average wait time given by sub method
    :return: the display str for showing the average wait time
    """
    if average < 60:
        return 'a few seconds'
    if average < 120:
        return 'about a minute'
    if average < 3600:
        return 'about {} minutes'.format(average // 60)
    if average < 7200:
        return 'about 1 hour'
    return 'about {} hours'.format(average // 3600)


def get_waiting_list(student_dict):
    """
    for the student dict and get the student who is waiting
    :param student_dict: QUICK_STUDENT_DICT or LONG_STUDENT_DICT
    :return: found one, yield one
    """
    for key, value in student_dict.items():
        if value[0]:  # the first element is a flag representing whether this student is in line
            yield (key, value[1], value[2])


class TitlePanel(tk.Frame):
    """
    the widget for displaying headline
    """

    def __init__(self, parent):
        super().__init__(parent, bg='#fefbed', relief=tk.GROOVE, bd=2)

        self.mystery = tk.Button(self, text='\nImportant', bg='#fefbed', width=955, anchor=tk.W, fg='#c09853',
                                 font='Arial 16 bold', relief=tk.FLAT, command=play, padx=24)
        self.mystery.bind('<Enter>', self.enter)
        self.mystery.bind('<Leave>', self.leave)
        self.mystery.pack(side=tk.TOP)
        tk.Label(self, text='Individual assessment items must be solely your own work. While students are '
                            'encouraged to have height-level conversations about the problems they are '
                            "trying to solve, you must not look at another student's code or copy from it. "
                            'The university uses sophisticated anti-collision measures to automatically '
                            'detect similarity between assignment submissions.\n', bg='#fefbed', anchor=tk.W,
                 justify=tk.LEFT, wraplength=914, pady=4).pack(side=tk.TOP)

    def enter(self, event):
        self.mystery.config(text='\nSuch a Fuss????')

    def leave(self, event):
        self.mystery.config(text='\nImportant')


class ChoicePanel(tk.Frame):
    """
    sub frame contains QuickQuestion panel and LongQuestion panel
    """

    def __init__(self, parent):
        super().__init__(parent)


class QuickQuestion(tk.Frame):
    """
    the widget for displaying QuickQuestion panel
    """

    def __init__(self, parent):
        super().__init__(parent, bg='white')

        self._panel = tk.Frame(self, bg='#dff0d8', relief=tk.GROOVE, bd=2)
        tk.Label(self._panel, bg='#dff0d8', text='Quick Questions', fg='#3c763d', font='Arial 20 bold').pack(
            side=tk.TOP, ipady=20)
        tk.Label(self._panel, bg='#dff0d8', text='< 2 mins with a tutor').pack(side=tk.TOP)
        self._panel.pack(side=tk.TOP, padx=10, pady=10, fill=tk.BOTH, ipady=10)
        tk.Label(self, text='Some examples of quick questions:\n'
                            '\n     ● Syntax errors'
                            '\n     ● Interpreting error output'
                            '\n     ● Assignment/MyPyTutor interpretation'
                            '\n     ● MyPyTutor submission issues\n', bg='white', justify=tk.LEFT).pack(side=tk.TOP,
                                                                                                        anchor=tk.W,
                                                                                                        ipadx=20,
                                                                                                        ipady=5)
        tk.Button(self, text='Request Quick Help', bg='#5cb85c', fg='#ffffff', relief=tk.RIDGE,
                  command=add_quick_student_dict).pack(ipadx=15, ipady=5, pady=5)
        tk.Frame(self, bg='#c0c0c0').pack(ipadx=227, pady=10)
        self._notice = tk.Label(self, text='No students in queue.', bg='white', justify=tk.LEFT)
        self._notice.pack(anchor=tk.W, ipadx=20, ipady=5)
        self._bar = tk.Frame(self, bg='white')
        self._bar.pack()

    def refresh(self, now):
        """
        the method called by timer roughly once every ten seconds for refreshing the state of quick question queue
        Meanwhile, draw the queue
        :param now: the time stamp when the sub method called
        """
        children = list(self._bar.children.values())
        for i in range(len(children)):
            children[i].destroy()
        waiting_list = list(get_waiting_list(get_quick_student_dict()))
        if not waiting_list:
            self._notice.config(text='No students in queue.')
            return
        tk.Frame(self._bar, bg='#c0c0c0').grid(row=0, columnspan=5, ipadx=227, pady=10)
        tk.Label(self._bar, bg='white', text='#', font='Arial 10 bold').grid(row=1, column=0, sticky=tk.W)
        tk.Label(self._bar, bg='white', text='Name', font='Arial 10 bold').grid(row=1, column=1, sticky=tk.W)
        tk.Label(self._bar, bg='white', text='Questions Asked', font='Arial 10 bold').grid(row=1, column=2, sticky=tk.W)
        tk.Label(self._bar, bg='white', text='Time', font='Arial 10 bold').grid(row=1, column=3, sticky=tk.W)
        tk.Frame(self._bar, bg='#c0c0c0').grid(row=2, columnspan=5, ipadx=227, pady=4)
        total_time = 0
        for i in range(len(waiting_list)):
            def cancel(name=waiting_list[i][0]):
                get_quick_student_dict()[name][0] = False
                self.refresh(time.time())

            def accept(name=waiting_list[i][0]):
                get_quick_student_dict()[name][1] += 1
                get_quick_student_dict()[name][0] = False
                self.refresh(time.time())

            row = i + 3
            display, delta = get_display(waiting_list[i][2], now)
            total_time += delta
            tk.Label(self._bar, bg='white', text=i + 1).grid(row=row, column=0, sticky=tk.W)
            tk.Label(self._bar, bg='white', text=waiting_list[i][0]).grid(row=row, column=1, sticky=tk.W)
            tk.Label(self._bar, bg='white', text=waiting_list[i][1]).grid(row=row, column=2, sticky=tk.W)
            tk.Label(self._bar, bg='white', text=display).grid(row=row, column=3, sticky=tk.W)
            button_field = tk.Frame(self._bar, bg='white', relief=tk.GROOVE)
            tk.Button(button_field, bg='#f6a5a3', relief=tk.GROOVE, command=cancel).pack(side=tk.LEFT, ipadx=9)
            tk.Button(button_field, bg='#a0e0aa', relief=tk.GROOVE, command=accept).pack(side=tk.LEFT, ipadx=9)
            button_field.grid(row=row, column=4, sticky=tk.W)
        self._notice.config(
            text='An average wait time of {} for {}.'.format(get_notice(total_time // len(waiting_list)),
                                                             '1 student' if len(
                                                                 waiting_list) is 1 else '{} students'.format(
                                                                 len(waiting_list))))


class LongQuestion(tk.Frame):
    """
    the widget for displaying LongQuestion panel
    """

    def __init__(self, parent):
        super().__init__(parent, bg='white')

        self._panel = tk.Frame(self, bg='#d9edf7', relief=tk.GROOVE, bd=2)
        tk.Label(self._panel, bg='#d9edf7', text='Long Questions', fg='#31708f', font='Arial 20 bold').pack(side=tk.TOP,
                                                                                                            ipady=20)
        tk.Label(self._panel, bg='#d9edf7', text='> 2 min with a tutor').pack(side=tk.TOP)
        self._panel.pack(side=tk.TOP, padx=10, pady=10, fill=tk.BOTH, ipady=10)
        tk.Label(self, text='Some examples of long questions:\n'
                            '\n     ● Open ended questions'
                            '\n     ● How to start a problem'
                            '\n     ● How to improve code'
                            '\n     ● Debugging'
                            '\n     ● Assignment help\n', bg='white', justify=tk.LEFT).pack(side=tk.TOP, anchor=tk.W,
                                                                                            ipadx=20, ipady=5)
        tk.Button(self, text='Request Long Help', bg='#5bc0de', fg='#ffffff', relief=tk.RIDGE,
                  command=add_long_student_dict).pack(ipadx=15, ipady=5, pady=5)
        self._hr = tk.Frame(self, bg='#c0c0c0')
        self._hr.pack(ipadx=227, pady=10)
        self._notice = tk.Label(self, text='No students in queue.', bg='white', justify=tk.LEFT)
        self._notice.pack(anchor=tk.W, ipadx=20, ipady=5)
        self._bar = tk.Frame(self, bg='white')
        self._bar.pack()

    def refresh(self, now):
        """
        the method called by timer roughly once every ten seconds for refreshing the state of long question queue
        Meanwhile, draw the queue
        :param now: the time stamp when the sub method called
        """
        children = list(self._bar.children.values())
        for i in range(len(children)):
            children[i].destroy()
        waiting_list = list(get_waiting_list(get_long_student_dict()))
        if not waiting_list:
            self._notice.config(text='No students in queue.')
            return
        tk.Frame(self._bar, bg='#c0c0c0').grid(row=0, columnspan=5, ipadx=227, pady=10)
        tk.Label(self._bar, bg='white', text='#', font='Arial 10 bold').grid(row=1, column=0, sticky=tk.W)
        tk.Label(self._bar, bg='white', text='Name', font='Arial 10 bold').grid(row=1, column=1, sticky=tk.W)
        tk.Label(self._bar, bg='white', text='Questions Asked', font='Arial 10 bold').grid(row=1, column=2, sticky=tk.W)
        tk.Label(self._bar, bg='white', text='Time', font='Arial 10 bold').grid(row=1, column=3, sticky=tk.W)
        tk.Frame(self._bar, bg='#c0c0c0').grid(row=2, columnspan=5, ipadx=227, pady=4)
        total_time = 0
        for i in range(len(waiting_list)):
            def cancel(name=waiting_list[i][0]):
                get_long_student_dict()[name][0] = False
                self.refresh(time.time())

            def accept(name=waiting_list[i][0]):
                get_long_student_dict()[name][1] += 1
                get_long_student_dict()[name][0] = False
                self.refresh(time.time())

            row = i + 3
            display, delta = get_display(waiting_list[i][2], now)
            total_time += delta
            tk.Label(self._bar, bg='white', text=i + 1).grid(row=row, column=0, sticky=tk.W)
            tk.Label(self._bar, bg='white', text=waiting_list[i][0]).grid(row=row, column=1, sticky=tk.W)
            tk.Label(self._bar, bg='white', text=waiting_list[i][1]).grid(row=row, column=2, sticky=tk.W)
            tk.Label(self._bar, bg='white', text=display).grid(row=row, column=3, sticky=tk.W)
            button_field = tk.Frame(self._bar, bg='white', relief=tk.GROOVE)
            tk.Button(button_field, bg='#f6a5a3', relief=tk.GROOVE, command=cancel).pack(side=tk.LEFT, ipadx=9)
            tk.Button(button_field, bg='#a0e0aa', relief=tk.GROOVE, command=accept).pack(side=tk.LEFT, ipadx=9)
            button_field.grid(row=row, column=4, sticky=tk.W)
        self._notice.config(
            text='An average wait time of {} for {}.'.format(get_notice(total_time // len(waiting_list)),
                                                             '1 student' if len(
                                                                 waiting_list) is 1 else '{} students'.format(
                                                                 len(waiting_list))))


class QueueApp:
    """
    QueueApp
    """
    DEFAULT_TITLE = 'CSSE1001 Queue'
    DEFAULT_MODE = '955x700'

    def __init__(self, master):
        self._master = master
        master.title(self.DEFAULT_TITLE)
        master.geometry(self.DEFAULT_MODE)
        master.protocol('WM_DELETE_WINDOW', self.close)

        # TitlePanel
        self._title_panel = TitlePanel(master)
        self._title_panel.pack(side=tk.TOP, fill=tk.BOTH)

        # ChoicePanel
        self._choice_panel = ChoicePanel(master)

        # QuickQuestion
        self._quick_question = QuickQuestion(self._choice_panel)
        self._quick_question.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # LongQuestion
        self._long_question = LongQuestion(self._choice_panel)
        self._long_question.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self._choice_panel.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Timer
        self._timer = threading.Thread(target=self.timer_run)
        self._timer.setDaemon(True)
        self._timer.start()

        # Finger-Guessing Game
        # store the image resources
        self.scissors_img = tk.PhotoImage(file='images/scissors.gif')
        self.hammer_img = tk.PhotoImage(file='images/hammer.gif')
        self.cloth_img = tk.PhotoImage(file='images/cloth.gif')

    def get_images(self):
        return self.scissors_img, self.hammer_img, self.cloth_img

    def close(self):
        if self.can_close():
            self._master.destroy()

    def can_close(self):
        reply = askquestion(type=messagebox.YESNO, title='Confirm Exit', message='Are you sure you want to quit?')
        if reply == messagebox.YES:
            return True
        else:
            return False

    def timer_run(self):
        self.refresh()
        time.sleep(10)
        self.timer_run()

    def refresh(self):
        now = time.time()
        self._quick_question.refresh(now)
        self._long_question.refresh(now)


def main():
    """Sets-up the GUI for CSSE1001 Queue"""
    root = tk.Tk()
    G.append(QueueApp(root))  # append QueueApp instance into global list G in order to use it in other methods' region
    root.mainloop()


if __name__ == "__main__":
    main()
