import tkinter as tk
from tkinter import messagebox
from tkinter.messagebox import askyesno, showinfo, askquestion

import sys
import time

# Fill these in with your details
__author__ = ''
__email__ = ''
__date__ = ''


def add_student_quick():
    # TODO: code
    print(1)


def add_student_long():
    # TODO: code
    print(2)


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
                  command=add_student_quick).pack(ipadx=15, ipady=5, pady=5)
        self._hr = tk.Frame(self, bg='#c0c0c0')
        self._hr.pack(ipadx=227, pady=10)


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
                  command=add_student_long).pack(ipadx=15, ipady=5, pady=5)
        self._hr = tk.Frame(self, bg='#c0c0c0')
        self._hr.pack(ipadx=227, pady=10)


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


def main():
    """Sets-up the GUI for CSSE1001 Queue"""
    root = tk.Tk()
    QueueApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
