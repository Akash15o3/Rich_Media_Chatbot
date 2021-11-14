from flask import jsonify, request, Flask
from pandas import read_csv
from tensorflow.keras.models import load_model

from embed import embed_for_request, embed_for_serving
from predict import predict

from tkinter import *
from PIL import  Image,ImageTk
from tkinter import filedialog
import pytesseract
import cv2
import tkinter as tk

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
BG_WHITE = "#f3ebe4"
BG_BLUE = "#3498DB"
BG_YELLOW = "#FCF3CF"
TEXT_COLOR = "#000000"
TEXT_COLOR1 = "#EAECEE"
TEXT_COLOR2 = "#34495E"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"
app = Flask(__name__)

class ChatApplication:

    def __init__(self):
        self.window = Tk()
        self._setup_main_window()
        self.count = 0

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("Spartan Chatbot")
        self.window.iconbitmap("favicon.ico")
        self.window.resizable(width=True, height=True)
        self.window.configure(width=470, height=550, bg=BG_COLOR)
      
        
        # p1 = PhotoImage(file = 'SJSU_logo (1) copy.png')
        # # Setting icon of master window
        # self.window.iconphoto(False, p1)
        #self.window.iconbitmap(r'favicon.ico')
        

        # head label
        head_label = Label(self.window, bg=BG_BLUE, fg=TEXT_COLOR, text="Welcome", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)

        # tiny divider
        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)

        # text widget
        self.text_widget = Text(self.window, width=20, height=2, bg=BG_WHITE, fg=TEXT_COLOR, 
                                font=FONT, padx=5, pady=5,wrap=WORD)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)

        # #Adding background
        # bg = PhotoImage(file = "SJSU_logo.png")
        # # Create Canvas
        # canvas1 = Canvas( self.window, width = 400,height = 400)
        # canvas1.pack(fill = "both", expand = True)

        # canvas1.create_image( 0, 0, image = bg, 
        #              anchor = "nw")

        # # scroll bar
        # scrollbar = Scrollbar(self.text_widget)
        # scrollbar.place(relheight=1, relx=0.974)
        # scrollbar.configure(command=self.text_widget.yview)

        # bottom label
        bottom_label = Label(self.window, bg=BG_BLUE, height=80)
        bottom_label.place(relwidth=1, rely=0.825)

        # message entry box
        self.msg_entry = Entry(bottom_label, bg=BG_WHITE, fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.60, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)

        # image button
        image_button = Button(bottom_label, text="Add Image", font=FONT_BOLD, width=20, bg=BG_YELLOW,
                             command=lambda: self.open_img())
        image_button.place(relx=0.62, rely=0.008, relheight=0.06, relwidth=0.18)

        # send button
        send_button = Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_BLUE,
                             command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.81, rely=0.008, relheight=0.06, relwidth=0.18)

    def openfilename(self):
        # open file dialog box to select image
        # The dialogue box has a title "Open"
        filename = filedialog.askopenfilename(title='Add Image')
        return filename

    def open_img(self):
        # Select the Imagename  from a folder
        input_image = self.openfilename()
        print("firstIN",input_image)
        # opens the image
        img = Image.open(input_image)
        # resize the image and apply a high-quality down sampling filter
        img = img.resize((250, 250), Image.ANTIALIAS)
        img1 = cv2.imread(input_image)
        extracted_information = pytesseract.image_to_string(img1)
        print(extracted_information)
        self._insert_message(extracted_information, "You", "image", input_image)
        
               
    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self._insert_message(msg, "You" , 'text', "null")

    def _insert_message(self, msg, sender, input_type, source):
        global my_image
        global my_image_2
        if not msg:
            return

        if (input_type=="text"):
            self.msg_entry.delete(0, END)
            msg1 = f"{sender}: {msg}\n\n"
            self.text_widget.configure(state=NORMAL)
            self.text_widget.insert(INSERT, msg1,)
            self.text_widget.configure(state=DISABLED)

            msg2 = f"SPARTAN: {get_response(msg)}\n\n"
            self.text_widget.configure(state=NORMAL)
            self.text_widget.insert(INSERT, msg2)
            self.text_widget.configure(state=DISABLED)

        elif (input_type=="image"):
            self.source_list = []
            self.source_list.append(source)
            print("COUNT",self.count)
            
            if self.count == 0:
                img = Image.open(source)
                img = img.resize((250, 250), Image.ANTIALIAS)
                my_image = ImageTk.PhotoImage(img)
                self.msg_entry.delete(0, END)
                msg1 = f"{sender}: {msg}\n\n"
                self.text_widget.configure(state=NORMAL)
                
                self.text_widget.image_create(END, image = my_image)
                self.text_widget.insert(END, '\n')
                self.text_widget.insert(END, '\n')
                self.text_widget.configure(state=DISABLED)

                msg2 = f"SPARTAN: {get_response(msg)}\n\n"
                self.text_widget.configure(state=NORMAL)
                self.text_widget.insert(END, msg2)
                self.text_widget.configure(state=DISABLED)
            
            elif self.count == 1:
                img = Image.open(source)
                img = img.resize((250, 250), Image.ANTIALIAS)
                my_image_2 = ImageTk.PhotoImage(img)
                self.msg_entry.delete(0, END)
                msg1 = f"{sender}: {msg}\n\n"
                self.text_widget.configure(state=NORMAL)
                
                self.text_widget.image_create(END, image = my_image_2)
                self.text_widget.insert(END, '\n')
                self.text_widget.insert(END, '\n')
                self.text_widget.configure(state=DISABLED)

                msg2 = f"SPARTAN: {get_response(msg)}\n\n"
                self.text_widget.configure(state=NORMAL)
                self.text_widget.insert(END, msg2)
                self.text_widget.configure(state=DISABLED)

        self.text_widget.see(END)
        self.count+=1

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
        
        answer_count = 5
        left, right = embed_for_request(app.df, app.vocabs, question)
        answers = predict(app.model, app.candidates,
                        app.response_map, left, right, answer_count)
        print(type(answers))
        ans = answers[0]+answers[1]+answers[2]+answers[3]+answers[4]
        return ans
