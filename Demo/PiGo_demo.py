import Tkinter as tk
from itertools import product
import ttk
import sys
import threading
import time

from PiGoLib import *

#TODO Onemogoci resize in maximize
#TODO Spodaj naj bo logo
#TODO Arduino

TITLE_FONT = ("Tahoma", 36)
BTN_FONT = ("Tahoma", 24)
LABEL_FONT = ("Tahoma", 24)

class App(tk.Frame):

    def __init__(self, root):
        try:
            rev = 1
            for arg in sys.argv:
              if arg == "rev1":
                rev = 1
              elif arg == "rev2":
                rev = 2
            
            self.board = PiGoBoard(TestMode=0, RPi_Rev=rev)
        except OSError, e:
            print e
            sys.exit(1)
        except EnvironmentError, e:
            print e
            sys.exit(2)

        tk.Frame.__init__(self, root)
        self.parent = root
        self.root = root

        self.main = main = tk.Frame(self)
        main.grid(row=1, column=1, columnspan=2, sticky="N")
        self.rowconfigure(1, minsize=400)

        self.home = home = tk.Frame(main)
        home.pack()
        self.active_frame = home

        tk.Label(home, text="PiGo DEMO", font=TITLE_FONT).grid(row=1, column=1, columnspan=2)

        for text, new_frame, (r, c) in zip(["A/D & D/A", "Motor Control", "Arduino", "Buffered I/O"],
                                           [ADDA_Frame(main, self), MotorFrame(main, self),
                                            None, ExtIOFrame(main, self)],
                                           product([2, 3], [1, 2])):
            tk.Button(home, text=text, font = BTN_FONT, width=20, height=5,
                command=self.replace_frame(new_frame)).grid(row=r, column=c)

        bottom = tk.Frame(self, background="grey", height=100, width=750)
        bottom.grid(row=2, column=1, columnspan=2)
        
        self.PiGo_IMAGE = tk.PhotoImage(file="PiGo_Logo_2.gif")
        logo = tk.Label(bottom, image=self.PiGo_IMAGE).pack()

    def replace_frame(self, new_frame):
        def home(_):
            if hasattr(new_frame, "home"):
                new_frame.home()
        def callback():
            self.home.pack_forget()
            new_frame.show()
            self.active_frame = new_frame
            self.root.bind("<Escape>", home)
            self.update()

        return callback

    def terminate(self):
        if hasattr(self.active_frame, "terminate"):
            self.active_frame.terminate()


class ContentFrame(tk.Frame):
    def __init__(self, parent, app, title, module_select=False):
        self.app = app
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.title = title
        title_frame = tk.Frame(self)
        title_frame.grid(row=0, column=1, columnspan=3)
        title_frame.columnconfigure(1, minsize= 75)
        title_frame.columnconfigure(2, minsize=600)
        title_frame.columnconfigure(3, minsize= 75)
        tk.Label(title_frame, text=title, font=TITLE_FONT).grid(row=1, column=2)
        self.thread = None
        self.selected_module = 0
        self.module_select = module_select

        if module_select:
            mod_select_frame = tk.Frame(title_frame)
            self.mod_select_buttons = [tk.Button(mod_select_frame, text=t, command=self._select_module(i))
                                       for i, t in enumerate(["A", "B", "C", "D"])]
            for i, btn in enumerate(self.mod_select_buttons):
                btn.grid(row=i%2, column=i/2)

            mod_select_frame.grid(row=1, column=3, sticky="W")

        self.HOME_IMAGE = tk.PhotoImage(file="Home.gif")
        tk.Button(title_frame, image=self.HOME_IMAGE, command=self.home).grid(row=1, column=1)

    def _select_module(self, ix):
        def callback():
            self.selected_module = ix
            for i, btn in enumerate(self.mod_select_buttons):
                btn.config(relief = "sunken" if i==ix else "raised")
            if hasattr(self, "select_module"):
                self.select_module(ix)
        return callback

    def show(self):
        if hasattr(self, "RefreshThread"):
            self.thread = self.RefreshThread(self.app.board, self)

        if self.module_select:
            self._select_module(0)()

        if self.thread:
            self.thread.start()

        self.pack()

    def home(self):
        self.pack_forget()
        if self.thread:
            self.thread.terminate()
            self.thread.join()
            self.thread = None
        self.app.home.pack()
        self.update()

    def terminate(self):
        if self.thread:
            self.thread.terminate()
            self.thread.join()
        self.thread = None


class ADDA_Frame(ContentFrame):
    ELEMENT_WIDTH = 400

    class RefreshThread(threading.Thread):
        def __init__(self, board, ui):
            threading.Thread.__init__(self)
            self.ui = ui
            self.terminated = False

            self.ad_values = [None, None]
            self.ad_changed = False

            self.da_values = [0, 0]
            self.da_changed = [True, True]

            self.board = board

        def select_module(self, ix):
            self.module = ModuleADDA(self.board, ['A', 'B', 'C', 'D'][ix])

        def set_da(self, ix, value):
            if self.da_values[ix] != value:
                self.da_values[ix] = value
                self.da_changed[ix] = True

        def _fetch_ad(self, ix):
            value = self.module.getAD(ix)
            if self.ad_values[ix] != value:
                self.ad_values[ix] = value
                self.ad_changed = True

        def _commit_da(self, ix):
            if not self.da_changed[ix]:
                return
            self.module.setDA(ix, self.da_values[ix])

        def terminate(self):
            self.terminated = True

        def run(self):
            while not self.terminated:
                self._fetch_ad(0)
                self._fetch_ad(1)
                self._commit_da(0)
                self._commit_da(1)
                time.sleep(0.05)

    def __init__(self, parent, app):
        ContentFrame.__init__(self, parent, app, "A/D & D/A", module_select=True)
        PAD = 8

        tk.Label(self, text="A/D", font=LABEL_FONT).grid(row=1, column=1, columnspan=3, pady=20)
        tk.Label(self, text="D/A", font=LABEL_FONT).grid(row=5, column=1, columnspan=3, pady=20)
        tk.Label(self, text="0", font=LABEL_FONT).grid(row=2, column=1, padx=20, pady=PAD)
        tk.Label(self, text="1", font=LABEL_FONT).grid(row=3, column=1, padx=20, pady=PAD)
        tk.Label(self, text="A", font=LABEL_FONT).grid(row=6, column=1, padx=20, pady=PAD)
        tk.Label(self, text="B", font=LABEL_FONT).grid(row=7, column=1, padx=20, pady=PAD)

        ad1_text = tk.StringVar()
        ad1 = ttk.Progressbar(self, length=self.ELEMENT_WIDTH, maximum=1023)
        ad1.grid(row=2, column=2)
        ad1_label = tk.Label(self, textvariable=ad1_text)
        ad1_label.grid(row=2, column=3)

        ad2_text = tk.StringVar()
        ad2 = ttk.Progressbar(self, length=self.ELEMENT_WIDTH, maximum=1023)
        ad2.grid(row=3, column=2)
        ad2_label = tk.Label(self, textvariable=ad2_text)
        ad2_label.grid(row=3, column=3)

        self.rowconfigure(4, minsize=10)

        da1_text = tk.StringVar()
        da1 = tk.Scale(self, orient=tk.HORIZONTAL, length=self.ELEMENT_WIDTH, from_=0, to=1023, showvalue=False,
            command=self.update_da)
        da1.grid(row=6, column=2)
        da1_label = tk.Label(self, textvariable=da1_text)
        da1_label.grid(row=6, column=3)

        da2_text = tk.StringVar()
        da2 = tk.Scale(self, orient=tk.HORIZONTAL, length=self.ELEMENT_WIDTH, from_=0, to=1023, showvalue=False,
            command=self.update_da)
        da2.grid(row=7, column=2)
        da2_label = tk.Label(self, textvariable=da2_text)
        da2_label.grid(row=7, column=3)

        self.ad_controls = [(ad1, ad1_text), (ad2, ad2_text)]
        self.da_controls = [(da1, da1_text), (da2, da2_text)]

    def select_module(self, ix):
        self.thread.select_module(ix)

    def update_ad(self):
        if not self.thread:
            return
        if self.thread.ad_changed:
            for i, (bar, text) in enumerate(self.ad_controls):
                value = self.thread.ad_values[i]
                bar["value"] = 0 if value is None else value
                text.set("N/A" if value is None else ("%1.03f V" % (value*3.3/1024)))
        self.after(100, self.update_ad)

    def update_da(self, _):
        if not self.thread:
            return
        for i, (scale, text) in enumerate(self.da_controls):
            value = scale.get()
            self.thread.set_da(i, value)
            text.set("N/A" if value is None else ("%1.03f V" % (value/500.0)))

    def show(self):
        ContentFrame.show(self)
        self.update_ad()


class MotorFrame(ContentFrame):
    ELEMENT_WIDTH = 400

    MODE_DIGITAL = 0
    MODE_PWM = 1

    class RefreshThread(threading.Thread):
        def __init__(self, board, ui):
            self.mode = MotorFrame.MODE_DIGITAL

            threading.Thread.__init__(self)
            self.ui = ui
            self.terminated = False

            self.value = 0.0

            self.board = board

        def _renew_object(self):
            self.motor = ModuleMotor(self.board, ['A', 'B', 'C', 'D'][self.selected_module], self.mode)
            self.value_changed = True

        def set_output(self, value):
            self.value = value
            self.value_changed = True

        def select_module(self, ix):
            self.selected_module = ix
            self._renew_object()

        def set_mode(self, mode):
            self.mode = mode
            self._renew_object()

        def terminate(self):
            self.terminated = True

        def run(self):
            while not self.terminated:
                if self.value_changed:
                    self.value_changed = False
                    self.motor.setOutput(self.value)
                time.sleep(0.05)

    def __init__(self, parent, app):
        ContentFrame.__init__(self, parent, app, "Motor Control", module_select=True)

        self.rowconfigure(1, minsize=50)

        btn_frame = tk.Frame(self)
        btn_frame.grid(row=2, column=2, pady=30)
        self.mode_buttons = [tk.Button(btn_frame, text="DIGITAL", command=self.select_mode(self.MODE_DIGITAL)),
                             tk.Button(btn_frame, text="PWM", command=self.select_mode(self.MODE_PWM))]
        for i, btn in enumerate(self.mode_buttons):
            btn.pack(side=tk.LEFT)

        self.scale = tk.Scale(self, orient=tk.HORIZONTAL, length=self.ELEMENT_WIDTH, from_=-1, to=1, showvalue=True,
            command=self.update_output)
        self.scale.grid(row=3, column=1, columnspan=3, pady=30)

    def update_buttons(self, mode):
        for i, btn in enumerate(self.mode_buttons):
            btn.config(relief = "sunken" if i==mode else "raised")

    def select_mode(self, mode):
        def callback():
            self.update_buttons(mode)
            self.thread.set_mode(mode)
            self.scale.config(resolution=1 if mode==self.MODE_DIGITAL else 0.001)
        return callback

    def update_output(self, _):
        self.thread.set_output(self.scale.get())

    def select_module(self, ix):
        self.thread.select_module(ix)

    def show(self):
        self.update_buttons(self.MODE_DIGITAL)
        ContentFrame.show(self)


class ExtIOFrame(ContentFrame):
    ELEMENT_WIDTH = 400

    class RefreshThread(threading.Thread):
        def __init__(self, board, ui):
            threading.Thread.__init__(self)
            self.ui = ui
            self.terminated = False

            self.output = [False] * 8
            self.output_changed = [True] * 8

            self.value = [False] * 8
            self.value_changed = [True] * 8

            self.board = board

        def flip_direction(self, ix):
            self.output[ix] = not self.output[ix]
            self.output_changed[ix] = True
            if self.output[ix]:
                self.value[ix] = False
            self.value_changed[ix] = True

        def flip_value(self, ix):
            if self.output[ix]:
                self.value[ix] = not self.value[ix]
                self.value_changed[ix] = True

        def terminate(self):
            self.terminated = True

        def run(self):
            while not self.terminated:
                for ix in range(8):
                    if self.output_changed[ix]:
                        self.board.setIOdir(ix, not self.output[ix])
                        self.output_changed[ix] = False

                    if self.output[ix]:
                        if self.value_changed[ix]:
                            self.board.setIO(ix, self.value[ix])
                            self.value_changed[ix] = False
                    else:
                        val = self.board.getIO(ix)
                        self.value_changed[ix] |= (self.value[ix] != val)
                        self.value[ix] = val
                time.sleep(0.05)

    def __init__(self, parent, app):
        ContentFrame.__init__(self, parent, app, "Buffered I/O", module_select=False)

        self.rowconfigure(1, minsize=20)
        frame = tk.Frame(self)
        frame.grid(row=2, column=2)

        PADY=5
        PADX=20

        tk.Label(frame, text="IO").grid(row=2, column=1, padx=PADX, pady=PADY)
        tk.Label(frame, text="Direction").grid(row=2, column=2, padx=PADX, pady=PADY)
        tk.Label(frame, text="Value").grid(row=2, column=3, padx=PADX, pady=PADY)

        self.IMG_DIRECTION = [tk.PhotoImage(file="IN.gif"), tk.PhotoImage(file="OUT.gif")]
        self.IMG_VALUE = [tk.PhotoImage(file="0.gif"), tk.PhotoImage(file="1.gif")]

        btn_direction, btn_value = [], []
        self.btn_direction, self.btn_value = btn_direction, btn_value
        for ix in range(8):
            tk.Label(frame, text=str(ix+1)).grid(row=3+ix, column=1, padx=PADX, pady=PADY)
            btn_direction.append(tk.Label(frame, image=self.IMG_DIRECTION[0]))
            btn_direction[-1].grid(row=3+ix, column=2, padx=PADX, pady=PADY)
            btn_direction[-1].bind("<Button-1>", self.flip_direction(ix))
            btn_value.append(tk.Label(frame, image=self.IMG_VALUE[0]))
            btn_value[-1].grid(row=3+ix, column=3, padx=PADX, pady=PADY)
            btn_value[-1].bind("<Button-1>", self.flip_value(ix))

    def flip_direction(self, ix):
        def callback(_):
            self.thread.flip_direction(ix)
            self.btn_direction[ix].config(image=self.IMG_DIRECTION[self.thread.output[ix]])
            self.btn_value[ix].config(image=self.IMG_VALUE[self.thread.value[ix]])
        return callback

    def flip_value(self, ix):
        def callback(_):
            self.thread.flip_value(ix)
            self.btn_value[ix].config(image=self.IMG_VALUE[self.thread.value[ix]])
        return callback

    def update_inputs(self):
        if not self.thread:
            return
        for ix in range(8):
            if not self.thread.output[ix] and self.thread.value_changed[ix]:
                self.thread.value_changed[ix] = False
                self.btn_value[ix].config(image=self.IMG_VALUE[self.thread.value[ix]])
                self.update()
        self.after(100, self.update_inputs)

    def show(self):
        ContentFrame.show(self)
        self.update_inputs()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("750x500")
    root.title("PiGO DEMO")
    app = App(root)
    app.pack()
    try:
        root.mainloop()
    finally:
        app.terminate()
