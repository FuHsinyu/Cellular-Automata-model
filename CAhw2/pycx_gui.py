# "pycx_gui.py"
# Realtime Simulation GUI (originally from PyCX)

# Developed by:
# Chun Wong
# email@chunwong.net
#
# Revised by:
# Hiroki Sayama
# sayama@binghamton.edu
#
# Copyright 2012 Chun Wong & Hiroki Sayama
#
# Simulation control & GUI extensions
# Copyright 2013 Przemyslaw Szufel & Bogumil Kaminski
# {pszufe, bkamins}@sgh.waw.pl
#
# Revised by:
# Koen Koning, K.Koning@uva.nl
# Modifications to make the code compatible with the framework of the UvA
# course `Introduction Computational Science', 2014/2015
#      Python 3 support, GUI refinements, improved parameter support
#
# Minor revision by
# Dick van Albada, G.D.vanAlbada@uva.nl
# Added plt.show() to draw_model() to force actual display of the plot
#
# The matplotlib backend will be automatically selected based on your OS when
# this file is first imported. It is therefore important that matplotlib.pyplot
# imported *after* this file. A clean way do to this is to import pyplot
# locally in the draw function of your model only.

import sys
import matplotlib.pyplot as plt
import matplotlib
from numpy.ma import arange
from pylab import *

if sys.platform == 'darwin':
    # On OSX, Both TkAgg and the builtin backend ('MacOSX') usually work.
    # However, the macosx backend seems to have slightly less issues when
    # setting up your Python, so we prefer that one for OSX.
    matplotlib.use('MacOSX')
else:
    matplotlib.use('TkAgg')

try:
    # Python2
    from Tkinter import (Tk, StringVar, Frame, Label, Button, Scale, Entry,
                         Canvas, Scrollbar, Text, YES, NO, LEFT, RIGHT, BOTH, TOP, SUNKEN, X,
                         Y, W, WORD, NORMAL, DISABLED, HORIZONTAL, END)
except ImportError:
    # Python3
    from tkinter import (Tk, StringVar, Frame, Label, Button, Scale, Entry,
                         Canvas, Scrollbar, Text, YES, NO, LEFT, RIGHT, BOTH, TOP, SUNKEN, X,
                         Y, W, WORD, NORMAL, DISABLED, HORIZONTAL, END)


class GUI:
    def __init__(self, model, title='PyCX Simulator', interval=0, step_size=1, param_gui_names=None):
        self.model = model
        self.titleText = title
        self.timeInterval = interval
        self.stepSize = step_size
        self.param_gui_names = param_gui_names
        if param_gui_names is None:
            self.param_gui_names = {}
        self.param_entries = {}
        self.statusStr = ""
        self.running = False
        self.modelFigure = None
        self.currentStep = 0

        self.init_gui()

    def init_gui(self):
        # create root window
        self.rootWindow = Tk()
        self.statusText = StringVar(value=self.statusStr)
        self.set_status_str("Simulation not yet started")

        self.rootWindow.wm_title(self.titleText)
        self.rootWindow.protocol('WM_DELETE_WINDOW', self.quit_gui)
        self.rootWindow.geometry('550x700')
        self.rootWindow.columnconfigure(0, weight=1)
        self.rootWindow.rowconfigure(0, weight=1)

        self.frameSim = Frame(self.rootWindow)

        self.frameSim.pack(expand=YES, fill=BOTH, padx=5, pady=5, side=TOP)
        self.status = Label(self.rootWindow, width=40, height=3, relief=SUNKEN,
                            bd=1, textvariable=self.statusText)
        self.status.pack(side=TOP, fill=X, padx=1, pady=1, expand=NO)

        self.runPauseString = StringVar()
        self.runPauseString.set("Run")
        self.buttonRun = Button(self.frameSim, width=30, height=2,
                                textvariable=self.runPauseString,
                                command=self.run_event)
        self.buttonRun.pack(side=TOP, padx=5, pady=5)

        self.show_help(self.buttonRun,
                       "Runs the simulation (or pauses the running simulation)")
        self.buttonStep = Button(self.frameSim, width=30, height=2,
                                 text="Step Once", command=self.step_once)
        self.buttonStep.pack(side=TOP, padx=5, pady=5)
        self.show_help(self.buttonStep, "Steps the simulation only once")
        self.buttonReset = Button(self.frameSim, width=30, height=2,
                                  text="Reset", command=self.reset_model)
        self.buttonReset.pack(side=TOP, padx=5, pady=5)
        self.show_help(self.buttonReset, "Resets the simulation")

        for param in self.model.params:
            var_text = self.param_gui_names.get(param, param)
            can = Canvas(self.frameSim)
            lab = Label(can, width=25, height=1 + var_text.count('\n'),
                        text=var_text, anchor=W, takefocus=0)
            lab.pack(side='left')
            ent = Entry(can, width=11)
            val = getattr(self.model, param)
            if isinstance(val, bool):
                val = int(val)  # Show 0/1 which can convert back to bool
            ent.insert(0, str(val))
            ent.pack(side='left')
            can.pack(side='top')
            self.param_entries[param] = ent
        if self.param_entries:
            self.buttonSaveParameters = Button(self.frameSim, width=50,
                                               height=1, command=self.save_parameters_cmd,
                                               text="Save parameters to the running model", state=DISABLED)
            self.show_help(self.buttonSaveParameters, "Saves the parameter values.\n Not all values may take effect "
                                                      "on a running model\n A model reset might be required.")
            self.buttonSaveParameters.pack(side='top', padx=5, pady=5)
            self.buttonSaveParametersAndReset = Button(self.frameSim, width=50,
                                                       height=1, command=self.save_parameters_and_reset_cmd,
                                                       text="Save parameters to the model and reset the model")
            self.show_help(self.buttonSaveParametersAndReset, "Saves the given parameter values and resets the model")
            self.buttonSaveParametersAndReset.pack(side='top', padx=5, pady=5)

        can = Canvas(self.frameSim)
        lab = Label(can, width=25, height=1, text="Step size ", justify=LEFT,
                    anchor=W, takefocus=0)
        lab.pack(side='left')
        self.stepScale = Scale(can, from_=1, to=500, resolution=1,
                               command=self.change_step_size, orient=HORIZONTAL,
                               width=25, length=150)
        self.stepScale.set(self.stepSize)
        self.show_help(self.stepScale, "Skips model redraw during every [n] simulation steps\n" +
                       " Results in a faster model run.")
        self.stepScale.pack(side='left')
        can.pack(side='top')

        can = Canvas(self.frameSim)
        lab = Label(can, width=25, height=1,
                    text="Step visualization delay in ms ", justify=LEFT,
                    anchor=W, takefocus=0)
        lab.pack(side='left')
        self.stepDelay = Scale(can, from_=0, to=max(2000, self.timeInterval),
                               resolution=10, command=self.change_step_delay,
                               orient=HORIZONTAL, width=25, length=150)
        self.stepDelay.set(self.timeInterval)
        self.show_help(self.stepDelay, "The visualization of each step is " +
                       "delays by the given number of " +
                       "milliseconds.")
        self.stepDelay.pack(side='left')
        can.pack(side='top')

    def set_status_str(self, new_status):
        self.statusStr = new_status
        self.statusText.set(self.statusStr)

    # model control functions
    def change_step_size(self, val):
        self.stepSize = int(val)

    def change_step_delay(self, val):
        self.timeInterval = int(val)

    def save_parameters_cmd(self):
        for param, entry in self.param_entries.items():
            val = entry.get()
            if isinstance(getattr(self.model, param), bool):
                val = bool(int(val))
            setattr(self.model, param, val)
            # See if the model changed the value (e.g. clipping)
            new_val = getattr(self.model, param)
            if isinstance(new_val, bool):
                new_val = int(new_val)
            entry.delete(0, END)
            entry.insert(0, str(new_val))
        self.set_status_str("New parameter values have been set")

    def save_parameters_and_reset_cmd(self):
        self.save_parameters_cmd()
        self.reset_model()

    def run_event(self):
        if not self.running:
            self.running = True
            self.rootWindow.after(self.timeInterval, self.step_model)
            self.runPauseString.set("Pause")
            self.buttonStep.configure(state=DISABLED)
            if self.param_entries:
                self.buttonSaveParameters.configure(state=NORMAL)
                self.buttonSaveParametersAndReset.configure(state=DISABLED)
        else:
            self.stop_running()

    def stop_running(self):
        self.running = False
        self.runPauseString.set("Continue Run")
        self.buttonStep.configure(state=NORMAL)
        self.draw_model()
        if self.param_entries:
            self.buttonSaveParameters.configure(state=NORMAL)
            self.buttonSaveParametersAndReset.configure(state=NORMAL)

    def step_model(self):
        if self.running:
            if self.model.step() is True:
                self.stop_running()
            self.currentStep += 1
            self.set_status_str("Step " + str(self.currentStep))
            self.status.configure(foreground='black')
            if self.currentStep % self.stepSize == 0:
                self.draw_model()
            self.rootWindow.after(int(self.timeInterval * 1.0 / self.stepSize),
                                  self.step_model)

    def step_once(self):
        self.running = False
        self.runPauseString.set("Continue Run")
        self.model.step()
        self.currentStep += 1
        self.set_status_str("Step " + str(self.currentStep))
        self.draw_model()
        if self.param_entries:
            self.buttonSaveParameters.configure(state=NORMAL)
        self.currentStep += 1

    def reset_model(self):
        self.running = False
        self.runPauseString.set("Run")
        self.model.reset()
        self.currentStep = 0
        self.set_status_str("Model has been reset")
        self.draw_model()

    def get_point_color(self, data):
        point_colors = []
        for i in data:
            point_colors.append([0, 0, 0, i / self.model.k])
        return point_colors

    def draw_model(self):

        if self.modelFigure is None:
            self.modelFigure = plt.figure()

            ax = self.modelFigure.add_subplot(111)
            xax = ax.xaxis
            xax.tick_top()

            points = self.init_values()

            ax.axis([0, len(points[0]) + 1, 0, 100])
            ax.invert_yaxis()

            plt.scatter(points[0], points[1], c=self.get_point_color(points[2]), s=5, marker='s')
            plt.gray()
            plt.ion()
            dpi = self.modelFigure.get_dpi()
            self.modelFigure.set_size_inches(550.0 / float(dpi), 550.0 / float(dpi))
            self.modelFigure.canvas.manager.window.resizable("false", "false")
            plt.show()

        if sys.platform == 'darwin':
            self.modelFigure.canvas.manager.show()
        else:
            points = self.init_values()
            plt.scatter(points[0], points[1], c=self.get_point_color(points[2]), s=5, marker='s')
            self.modelFigure.canvas.manager.window.update()

    def init_values(self):
        data = self.model.draw()
        x = []
        point_value = 1
        for _ in data:
            x.append(point_value)
            point_value += 1

        t = np.empty(len(x))
        t.fill(self.currentStep)
        return [x, t, data]

    def start(self):
        if self.model.step.__doc__:
            self.show_help(self.buttonStep, self.model.step.__doc__.strip())

        self.model.reset()
        self.draw_model()
        self.rootWindow.mainloop()

    def quit_gui(self):
        plt.close('all')
        self.rootWindow.quit()
        self.rootWindow.destroy()

    def show_help(self, widget, text):
        def set_text(self):
            self.statusText.set(text)
            self.status.configure(foreground='blue')

        def show_help_leave(self):
            self.statusText.set(self.statusStr)
            self.status.configure(foreground='black')

        widget.bind("<Enter>", lambda e: set_text(self))
        widget.bind("<Leave>", lambda e: show_help_leave(self))
