import tkinter as tk
from tkinter import messagebox
from tkinter.messagebox import showinfo, showwarning, showerror, askquestion
from tkinter import ttk

import sys
import time
import threading

# Fill these in with your details
__author__ = ''
__email__ = ''
__date__ = ''

QUICK_STUDENT_DICT = {}
LONG_STUDENT_DICT = {}


def get_quick_student_dict():
    return QUICK_STUDENT_DICT


def get_long_student_dict():
    return LONG_STUDENT_DICT


def add_quick_student_dict():
    display_entry_widget(get_quick_student_dict())


def add_long_student_dict():
    display_entry_widget(get_long_student_dict())


def display_entry_widget(student_dict):
    def add_student_dict():
        name = entry.get()
        if name and not name.strip():
            showerror('Not Just Typed Spaces', 'Please give the proper name!')
            return
        name = name.strip()
        if name:
            if name not in student_dict:
                student_dict[name] = [True, 0, time.time()]
            elif student_dict[name][0]:
                showwarning('Invalid Participation', "You're in line already!")
                return
            else:
                student_dict[name] = [True, student_dict[name][1] + 1, time.time()]
            root.destroy()
        else:
            showerror('Not Be Empty', 'Please give the proper name!')

    root = tk.Tk()
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
    delta = int(now - record)
    if delta < 60:
        return 'a few seconds ago'
    if delta < 120:
        return 'a minute ago'
    if delta < 3600:
        return '{} minutes ago'.format(delta // 60)
    if delta < 7200:
        return '1 hour ago'
    return '{} hours age'.format(delta // 3600)


def get_waiting_list(student_dict, now):
    for key, value in student_dict.items():
        if value[0]:
            yield (key, value[1], get_display(value[2], now))


class TitlePanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='#fefbed', relief=tk.GROOVE, bd=2)

        tk.Label(self, text='\nImportant', bg='#fefbed', width=955, anchor=tk.W, fg='#c09853', font='Arial 16 bold',
                 padx=24).pack(side=tk.TOP)
        tk.Label(self, text='Individual assessment items must be solely your own work. While students are '
                            'encouraged to have height-level conversations about the problems they are '
                            "trying to solve, you must not look at another student's code or copy from it. "
                            'The university uses sophisticated anti-collision measures to automatically '
                            'detect similarity between assignment submissions.\n', bg='#fefbed', anchor=tk.W,
                 justify=tk.LEFT, wraplength=914, pady=4).pack(side=tk.TOP)


class ChoicePanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)


class QuickQuestion(tk.Frame):
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
        children = list(self._bar.children.values())
        for i in range(len(children)):
            children[i].destroy()
        waiting_list = list(get_waiting_list(get_quick_student_dict(), now))
        if not waiting_list:
            return
        tk.Frame(self._bar, bg='#c0c0c0').grid(row=0, columnspan=5, ipadx=227, pady=10)
        tk.Label(self._bar, bg='white', text='#', font='Arial 10 bold').grid(row=1, column=0, sticky=tk.W)
        tk.Label(self._bar, bg='white', text='Name', font='Arial 10 bold').grid(row=1, column=1, sticky=tk.W)
        tk.Label(self._bar, bg='white', text='Questions Asked', font='Arial 10 bold').grid(row=1, column=2, sticky=tk.W)
        tk.Label(self._bar, bg='white', text='Time', font='Arial 10 bold').grid(row=1, column=3, sticky=tk.W)


class LongQuestion(tk.Frame):
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
        children = list(self._bar.children.values())
        for i in range(len(children)):
            children[i].destroy()
        waiting_list = list(get_waiting_list(get_long_student_dict(), now))
        if not waiting_list:
            return
        tk.Frame(self._bar, bg='#c0c0c0').pack(ipadx=227, pady=10)


class QueueApp:
    DEFAULT_TITLE = 'CSSE1001 Queue'
    DEFAULT_MODE = '955x600'

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
        a = ['111', ]
        self._timer = threading.Thread(target=self.timer_run, args=a)
        self._timer.setDaemon(True)
        self._timer.start()

        # Finger-Guessing Game
        pass

    def close(self):
        if self.can_close():
            self._master.destroy()

    def can_close(self):
        reply = askquestion(type=messagebox.YESNO, title='Confirm Exit', message='Are you sure you want to quit?')
        if reply == messagebox.YES:
            return True
        else:
            return False

    def timer_run(self, arg):
        # TODO: code
        now = time.time()
        self._quick_question.refresh(now)
        self._long_question.refresh(now)

        self.timer_run(arg)


def main():
    """Sets-up the GUI for CSSE1001 Queue"""
    root = tk.Tk()
    QueueApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
