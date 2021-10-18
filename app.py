from flask import jsonify, request, Flask
from pandas import read_csv
from tensorflow.keras.models import load_model

from embed import embed_for_request, embed_for_serving
from predict import predict

from tkinter import *


BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"
app = Flask(__name__)

class ChatApplication:

    def __init__(self):
        self.window = Tk()
        self._setup_main_window()

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("Help - AI Testing tool")
        self.window.resizable(width=True, height=True)
        self.window.configure(width=470, height=550, bg=BG_COLOR)

        # head label
        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR,
                           text="Welcome", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)

        # tiny divider
        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)

        # text widget
        self.text_widget = Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR,
                                font=FONT, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)

        # scroll bar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)

        # bottom label
        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)

        # message entry box
        self.msg_entry = Entry(bottom_label, bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.65, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)

        # image button
        image_button = Button(bottom_label, text="Add Image", font=FONT_BOLD, width=20, bg=BG_GRAY,
                             command=lambda: self._on_enter_pressed(None))
        image_button.place(relx=0.57, rely=0.008, relheight=0.06, relwidth=0.16)

        # send button
        send_button = Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_GRAY,
                             command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.16)


    # def _on _added_image():


    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self._insert_message(msg, "You")

    def _insert_message(self, msg, sender):
        if not msg:
            return

        self.msg_entry.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)

        msg2 = f"Spartan: {get_response(msg)}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state=DISABLED)

        self.text_widget.see(END)

def init_app(model_path, response_data_path):
    app.model = load_model(model_path)

    app.df, app.vocabs, app.candidates = embed_for_serving()

    resp_data = read_csv(response_data_path)
    app.response_map = {}
    for index, row in read_csv(response_data_path).iterrows():
        app.response_map[row["Question"]] = row["Response"]
    appi = ChatApplication()
    appi.run()

def get_response(question):
    # body = request.get_json()
    # if not body:
    #     return "Bad requerst: expected json body", 400

    # question = body["question"]
    # if not question:
    #     return "Bad request: expected key \"question\"", 400

    answer_count = 10
    # if "answer_count" in body:
    #     try:
    #         answer_count = int(body["answer_count"])
    #     except ValueError:
    #         return "Bad request: \"answer_count\" is not a valid integer", 400

    left, right = embed_for_request(app.df, app.vocabs, question)
    answers = predict(app.model, app.candidates,
                      app.response_map, left, right, answer_count)
    return answers