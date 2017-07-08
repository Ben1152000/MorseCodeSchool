from Tkinter import *
from tone import MusicBox
from time import sleep
from random import choice
from words import *
import datetime

class Morse:

    def __init__(self, master):
        self.master = master
        master.title("Morse")
        master.minsize(width=640, height=520)
        master.resizable(width=False, height=False)
        bg = "lightgrey"
        master.configure(bg=bg)
        self.musicbox = MusicBox()

        self.generated = ""
        self.muted = IntVar()
        self.hidden_conv = IntVar()
        self.hidden_text = IntVar()
        self.v1 = IntVar()
        self.v2 = IntVar()
        self.v3 = IntVar()
        self.v4 = IntVar()
        self.v5 = IntVar()
        
        self.title = Label(master, text="Morse Code School", font=("Verdana", 30), bg=bg)
        self.rmargin = Label(master, text="", width=5, bg=bg)
        self.rcmargin = Label(master, text="", width=3, bg=bg)
        self.lcmargin = Label(master, text="", width=2, bg=bg)
        self.umargin = Label(master, text="", height=1, bg=bg)
        self.ucmargin = Label(master, text="", height=1, bg=bg)
        self.cmargin = Label(master, text="", height=1, bg=bg)
        self.bcmargin = Label(master, text="", height=1, bg=bg)
        self.bmargin = Label(master, text="", height=1, bg=bg)
        self.text = Text(master, height=10, width=24)
        self.text.insert(1.0, "Insert text here.")
        relief = "solid"
        
        self.alphabet = [
            ["t", "a", "e", "n", "i", "m"],
            ["s", "o", "r", "h", "u", "d"],
            ["k", "c", "w", "l", "g", "p"],
            ["f", "y", "b", "v", "j", "z"],
            ["q", "x", ".", "?"],
        ]
        self.vars = [[],[],[],[],[]]
        for i in range(len(self.alphabet)):
            for j in range(len(self.alphabet[i])):
                self.vars[i].append(StringVar())
        self.keyboard = [[],[],[],[],[]]
        for i in range(len(self.alphabet)):
            for j in range(len(self.alphabet[i])):
                self.vars[i][j].set(self.alphabet[i][j])
                self.keyboard[i].append(Label(master, textvariable=self.vars[i][j], width=4, pady=4, bg=bg))
        self.switch = Button(text="./-", width=2, command=self.toggle, highlightbackground=bg)

        self.group1 = Checkbutton(master, text="Group 1", bg=bg, variable=self.v1, command=self.c1)
        self.group2 = Checkbutton(master, text="Group 2", bg=bg, variable=self.v2, command=self.c2)
        self.group3 = Checkbutton(master, text="Group 3", bg=bg, variable=self.v3, command=self.c3)
        self.group4 = Checkbutton(master, text="Group 4", bg=bg, variable=self.v4, command=self.c4)
        self.group5 = Checkbutton(master, text="Group 5", bg=bg, variable=self.v5, command=self.c5)

        self.conv_button = Button(master, text="Play Morse", highlightbackground=bg, command=self.convert)
        self.mute = Checkbutton(master, text="Mute", bg=bg, variable=self.muted)
        self.freq = Scale(master, from_=2, to=4, orient=HORIZONTAL, length=100, label="Frequency (Oct.):", showvalue=0, tickinterval=1, resolution=0.1, font=("Helvetica", 10), sliderlength=20, bg=bg)
        self.rate = Scale(master, from_=3, to=18, orient=HORIZONTAL, length=110, label="F. Speed (WpM):", showvalue=0, tickinterval=3, font=("Helvetica", 10), sliderlength=20, bg=bg)
        self.freq.set(3)
        self.rate.set(9)
        self.genr_button = Button(master, text="Play Gen.", highlightbackground=bg, command=self.play_gen)

        self.converted = Text(master, height=7, width=24)
        self.notes = Text(master, height=3, width=47)
        self.tmargin = Label(master, text="", height=1, bg=bg)
        self.translate = Text(master, height=3, width=47)

        self.hide_conv = Checkbutton(master, text="Hide", bg=bg, variable=self.hidden_conv, command=self.hide)
        self.regen = Button(master, text="Generate", highlightbackground=bg, command=self.generate)
        self.hide_text = Checkbutton(master, text="Hide", bg=bg, variable=self.hidden_text, command=self.hide2)

        # Create layout
        self.umargin.grid(row=0, column=0, columnspan=15)
        self.title.grid(row=1, column=1, columnspan=15)
        self.ucmargin.grid(row=2, column=0, columnspan=15)
        self.rmargin.grid(row=0, column=0, rowspan=10)
        self.text.grid(row=3, column=1, columnspan=5, rowspan=5, sticky="ns")
        self.rcmargin.grid(row=0, column=6, rowspan=10)
        for i in range(len(self.keyboard)):
            for j in range(len(self.keyboard[i])):
                self.keyboard[i][j].grid(row=3+i, column=7+j, sticky="ew")
        self.switch.grid(row=7, column=11, columnspan=2, sticky="e")
        self.lcmargin.grid(row=0, column=13, rowspan=10)
        self.group1.grid(row=3, column=14)
        self.group2.grid(row=4, column=14)
        self.group3.grid(row=5, column=14)
        self.group4.grid(row=6, column=14)
        self.group5.grid(row=7, column=14)

        self.cmargin.grid(row=8, column=0, columnspan=15)
        self.conv_button.grid(row=9, column=1, columnspan=3)
        self.mute.grid(row=9, column=5, sticky="e")
        self.freq.grid(row=9, column=7, columnspan=3)
        self.rate.grid(row=9, column=10, columnspan=3)
        self.genr_button.grid(row=9, column=13, columnspan=3, sticky="e")

        self.bcmargin.grid(row=10, column=0, columnspan=15)
        self.converted.grid(row=11, column=1, columnspan=5, rowspan=5, sticky="ns")
        self.translate.grid(row=11, column=7, columnspan=8, rowspan=5, sticky="ns")

        self.bmargin.grid(row=16, column=0, columnspan=15)
        self.hide_conv.grid(row=17, column=1, columnspan=2)
        self.regen.grid(row=17, column=11, columnspan=3)
        self.hide_text.grid(row=17, column=13, columnspan=2, sticky="e")

    def c1(self):
        if (not self.v1.get()):
            self.v2.set(0)
            self.v3.set(0)
            self.v4.set(0)
            self.v5.set(0)
        self.generate()

    def c2(self):
        if (self.v2.get()):
            self.v1.set(1)
        else:
            self.v3.set(0)
            self.v4.set(0)
            self.v5.set(0)
        self.generate()

    def c3(self):
        if (self.v3.get()):
            self.v1.set(1)
            self.v2.set(1)
        else:
            self.v4.set(0)
            self.v5.set(0)
        self.generate()

    def c4(self):
        if (self.v4.get()):
            self.v1.set(1)
            self.v2.set(1)
            self.v3.set(1)
        else:
            self.v5.set(0)
        self.generate()

    def c5(self):
        if (self.v5.get()):
            self.v1.set(1)
            self.v2.set(1)
            self.v3.set(1)
            self.v4.set(1)
        self.generate()
    
    def hide(self):
        if (self.hidden_conv.get()):
            self.converted.delete(1.0, 'end')
        else:
            self.converted.insert(1.0, self.words2morse(self.text.get("1.0", 'end')))
        
    def hide2(self):
        if (self.hidden_text.get()):
            self.translate.delete(1.0, 'end')
        else:
            self.translate.insert("1.0", self.generated)
        
    def convert(self):
        text = self.text.get("1.0", 'end')
        self.play(text)
    
    def generate(self):
        if self.v5.get():
            text = choice(final) + " " + choice(final) + " " + choice(final) + choice([".", ".", ".", "?"])
        elif self.v4.get():
            text = choice(noxorq) + " " + choice(noxorq) + " " + choice(noxorq)
        elif self.v3.get():
            text = choice(cuwil) + " " + choice(cuwil) + " " + choice(cuwil)
        elif self.v2.get():
            text = choice(sorhud) + " " + choice(sorhud) + " " + choice(sorhud)
        elif self.v1.get():
            text = choice(taenim) + " " + choice(taenim) + " " + choice(taenim)
        else:
            text = ""
        self.generated = text
        self.translate.delete(1.0, 'end')
        if (not self.hidden_text.get()):
            self.translate.insert(1.0, text)
    
    def play_gen(self):
        self.play(self.generated)

    def play(self, text):
        freq = (2 ** float(self.freq.get())) * 55
        speed = float(self.rate.get())
        morse = self.words2morse(text)
        if (not self.muted.get()):
            self.musicbox.play(morse, freq, speed)

    def toggle(self):
        if self.switch.config('text')[-1] == './-':
            self.switch.config(text='Abc')
            for i in range(len(self.alphabet)):
                for j in range(len(self.alphabet[i])):
                    self.vars[i][j].set(self.words2morse(self.alphabet[i][j]))
        else:
            self.switch.config(text='./-')
            for i in range(len(self.alphabet)):
                for j in range(len(self.alphabet[i])):
                    self.vars[i][j].set(self.alphabet[i][j])

    def words2morse(self, string):
        alphabet = {"a" : ".-", "b" : "-...", "c" : "-.-.", "d" : "-..",
                "e" : ".", "f" : "..-.", "g" : "--.", "h" : "....",
                "i" : "..", "j" : ".---", "k" : "-.-", "l" : ".-..",
                "m" : "--", "n" : "-.", "o" : "---", "p" : ".--.",
                "q" : "--.-", "r" : ".-.", "s" : "...", "t" : "-",
                "u" : "..-", "v" : "...-", "w" : ".--", "x" : "-..-",
                "y" : "-.--", "z" : "--..", ".": ".....", "?": "----",
                " " : "/"}
        code = ""
        for char in string:
            if char in alphabet.keys():
                code += alphabet[char.lower()] + " "
        return code

root = Tk()
window = Morse(root)

def clock():
    window.converted.delete(1.0, 'end')
    if (not window.hidden_conv.get()):
        window.converted.insert(1.0, window.words2morse(window.text.get("1.0", 'end')))
    window.translate.delete(1.0, 'end')
    if (not window.hidden_text.get()):
        window.translate.insert(1.0, window.generated)
    root.after(300, clock) # run itself again after 1000 ms

clock()
root.mainloop()