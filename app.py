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
TEXT_COLOR = "#EAECEE"

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
        self.window.resizable(width=True, height=True)
        self.window.configure(width=470, height=550, bg=BG_COLOR)
        
        # p1 = PhotoImage(file = 'SJSU_logo (1) copy.png')
        # # Setting icon of master window
        # self.window.iconphoto(False, p1)
        self.window.iconbitmap('SJSU_logo (1).ico')


        # head label
        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR, text="Welcome", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)

        # tiny divider
        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)

        # text widget
        self.text_widget = Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR, 
                                font=FONT, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)

        #Adding background
        # bg = PhotoImage(file="Tower_Hall.png")

        # my_label = Label(self.window, image = bg)
        # my_label.place(x=0,y=0,relwidth=1,relheight=1)

        # my_text = Label(self.window, text = "Spartan Welcomes You",font=("Helvetica", 30),fg="yellow",bg="blue")
        # my_text.pack(pady=50)

        # img_file = Image.open('towelHall.jpeg')
        # bg = ImageTk.PhotoImage(img_file)
        # bgl = Label(self.window,image=bg)
        # bgl.place(x=0, y=0, relwidth=1,relheight=1)


        # # scroll bar
        # scrollbar = Scrollbar(self.text_widget)
        # scrollbar.place(relheight=1, relx=0.974)
        # scrollbar.configure(command=self.text_widget.yview)

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
                             command=lambda: self.open_img())
        image_button.place(relx=0.57, rely=0.008, relheight=0.06, relwidth=0.16)

        # send button
        send_button = Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_GRAY,
                             command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.16)

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
        # add_image(input_image)
        img1 = cv2.imread(input_image)
        
        # PhotoImage class is used to add image to widgets, icons etc
        # img = ImageTk.PhotoImage(img)
        
        extracted_information = pytesseract.image_to_string(img1)
        print(extracted_information)

        # msg = self.msg_entry.get()
        self._insert_message(extracted_information, "YOU", "image", input_image)
        

    def add_image(self, event):
            img2 = tk.PhotoImage(file = event)
            self.text_widget.image_create(tk.END, image = img2) # Example 1
            #self.text_widget.window_create(tk.END, window = tk.Label(self.text_widget, image = img2)) # Example 2

            # self.window = tk.Tk()

            # self.text_widget = tk.Text(self.window)
            # self.text_widget.pack(padx = 20, pady = 20)

            tk.image_button(self.window, text = "Insert").pack()

                
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
            self.text_widget.insert(END, msg1)
            self.text_widget.configure(state=DISABLED)

            msg2 = f"SPARTAN: {get_response(msg)}\n\n"
            self.text_widget.configure(state=NORMAL)
            self.text_widget.insert(END, msg2)
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
        # body = request.get_json()
        # if not body:
        #     return "Bad requerst: expected json body", 400

        # question = body["question"]
        # if not question:
        #     return "Bad request: expected key \"question\"", 400

        answer_count = 5
        # if "answer_count" in body:
        #     try:
        #         answer_count = int(body["answer_count"])
        #     except ValueError:
        #         return "Bad request: \"answer_count\" is not a valid integer", 400

        left, right = embed_for_request(app.df, app.vocabs, question)
        answers = predict(app.model, app.candidates,
                        app.response_map, left, right, answer_count)
        print(type(answers))
        ans = answers[0]+answers[1]+answers[2]+answers[3]+answers[4]
        return ans

# def add_image(input_image):
#     screen.image_create(END, image=input_image )