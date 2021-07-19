import tkinter as tk

class UI:
    window = None
    key_label = None    
    key_buttons = {}
    prog_buttons = {}
    degree_labels = []
    progression_frame = None
    notes = None
    chord_labels = []

    def set_key_label(self, text):
        self.key_label.config(text=f"Key: {text}")

    def set_scale(self, scale):
        suffixes = ["", "m", "m", "", "", "m", "o"]
        for i in range(7):
            self.degree_labels[i].config(text=f"{scale[i]}{suffixes[i]}")

    def set_progression(self, template, chords):
        for widget in self.progression_frame.winfo_children():
            widget.destroy()
        self.chord_labels.clear()

        # put stuff in the prog display
        self.progression_frame.rowconfigure([0,1], weight=1)
        for i in range(len(template)):
            self.progression_frame.columnconfigure(i, weight=1)

        for j, (tem, cho) in enumerate(zip(template, chords)):
            lbl_prog = tk.Label(master=self.progression_frame, text=tem, font="Helvetica 18", height=1, bg="red")
            lbl_prog.grid(row=0, column=j, sticky="sew", padx=10, pady=10)
            lbl_chord = tk.Label(master=self.progression_frame, text=cho, font="Helvetica 18", height=1, bg="red")
            self.chord_labels.append(lbl_chord)
            lbl_chord.grid(row=1, column=j, sticky="new", padx=10, pady=10)        

    def set_notes(self, notes):
        self.notes = notes
        print(notes)

    @staticmethod
    def create_app(app):
        window = tk.Tk()
        app.window = window

        APP_WIDTH       = 800
        KEY_FRM_HEIGHT  = 300
        PROG_FRM_HEIGHT = 250

        # window has two frames, key and prog
        window.columnconfigure(0, minsize=APP_WIDTH)
        frm_key = tk.Frame(master=window, height=KEY_FRM_HEIGHT)
        window.rowconfigure(0, minsize=KEY_FRM_HEIGHT)
        frm_key.grid(row=0, sticky="nsew")
        frm_prog = tk.Frame(master=window, height=PROG_FRM_HEIGHT)
        window.rowconfigure(1, minsize=PROG_FRM_HEIGHT)
        frm_prog.grid(row=1, sticky="nsew")

        KEY_SELECTOR_HEIGHT = 100
        KEY_DISPLAY_HEIGHT  = KEY_FRM_HEIGHT - KEY_SELECTOR_HEIGHT

        # frm_key has two frames, selector and display
        frm_key.columnconfigure(0, minsize=APP_WIDTH)
        frm_key_selector = tk.Frame(master=frm_key, height=KEY_SELECTOR_HEIGHT, bg="green")
        frm_key.rowconfigure(0, minsize=KEY_SELECTOR_HEIGHT)
        frm_key_selector.grid(row=0, sticky="nsew")
        frm_key_display  = tk.Frame(master=frm_key, height=KEY_DISPLAY_HEIGHT, bg="blue")
        frm_key.rowconfigure(1, minsize=KEY_DISPLAY_HEIGHT)
        frm_key_display.grid(row=1, sticky="nsew")

        # split frm_key_selector in three horizontally
        frm_key_selector.rowconfigure(0, minsize=KEY_SELECTOR_HEIGHT)
        frm_key_selector.columnconfigure([0,1,2], weight=1)
        frm_key_selector_left = tk.Frame(master=frm_key_selector)
        frm_key_selector_left.grid(column=0, row=0, sticky="nsew")
        frm_key_selector_mid = tk.Frame(master=frm_key_selector)
        frm_key_selector_mid.grid(column=1, row=0, sticky="nsew")
        frm_key_selector_right = tk.Frame(master=frm_key_selector)
        frm_key_selector_right.grid(column=2, row=0, sticky="nsew")

        # put stuff in the key selector
        # btn_first_key = tk.Button(master=frm_key_selector_left, text="<<", height=5, width=3)
        # app.key_buttons["first"] = btn_first_key
        # btn_first_key.pack(side="left")
        btn_prev_key = tk.Button(master=frm_key_selector_left, text="<", height=5, width=3)
        app.key_buttons["prev"] = btn_prev_key
        btn_prev_key.pack(side="left")
        # btn_last_key = tk.Button(master=frm_key_selector_right, text=">>", height=5, width=3)
        # app.key_buttons["last"] = btn_last_key
        # btn_last_key.pack(side="right")
        btn_next_key = tk.Button(master=frm_key_selector_right, text=">", height=5, width=3)
        app.key_buttons["next"] = btn_next_key
        btn_next_key.pack(side="right")
        frm_key_selector_mid.columnconfigure([0,1,2], weight=1)
        frm_key_selector_mid.rowconfigure([0,1,2], weight=1)
        lbl_key = tk.Label(master=frm_key_selector_mid, text="Key:", font="Helvetica 24", anchor=tk.CENTER)
        lbl_key.grid(column=1, row=1)
        app.key_label = lbl_key

        # put stuff in the key display
        frm_key_display.rowconfigure([0,1], weight=1)
        frm_key_display.columnconfigure([0,1,2,3,4,5,6], weight=1)

        numerals = ["I", "IIm", "IIIm", "IV", "V", "VIm", "VIIo"]
        for j in range(7):
            lbl_num = tk.Label(master=frm_key_display, text=numerals[j], font="Helvetica 18")
            lbl_num.grid(row=0, column=j, sticky="nsew", padx=10, pady=10)
            lbl_degree = tk.Label(master=frm_key_display, font="Helvetica 18")
            lbl_degree.grid(row=1, column=j, sticky="nsew", padx=10, pady=10)
            app.degree_labels.append(lbl_degree)

        # split prog frame in three horizontally
        frm_prog.rowconfigure(0, minsize=PROG_FRM_HEIGHT)
        frm_prog.columnconfigure([0,1,2], weight=1)
        frm_prog_left = tk.Frame(master=frm_prog)
        frm_prog_left.grid(column=0, row=0, sticky="nsew")
        frm_prog_mid = tk.Frame(master=frm_prog)
        frm_prog_mid.grid(column=1, row=0, sticky="ns")
        app.progression_frame = frm_prog_mid
        frm_prog_right = tk.Frame(master=frm_prog)
        frm_prog_right.grid(column=2, row=0, sticky="nsew")

        # put stuff in prog frame
        # btn_first_prog = tk.Button(master=frm_prog_left, text="", height=5, width=3)
        # btn_first_prog.pack(side="left")
        # app.prog_buttons["first"] = btn_first_prog
        btn_prev_prog = tk.Button(master=frm_prog_left, text="<", height=5, width=3)
        btn_prev_prog.pack(side="left")
        app.prog_buttons["prev"] = btn_prev_prog
        btn_last_prog = tk.Button(master=frm_prog_right, text="|>", height=5, width=3)
        btn_last_prog.pack(side="right")
        app.prog_buttons["last"] = btn_last_prog
        btn_next_prog = tk.Button(master=frm_prog_right, text=">", height=5, width=3)
        btn_next_prog.pack(side="right")
        app.prog_buttons["next"] = btn_next_prog
