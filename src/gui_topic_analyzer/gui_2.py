import tkinter
from tkinter import messagebox
import tkinter.ttk as ttk

actual_url = ""
import words
import requests

class applicationUI:
    def __init__(self,master):
        self.master = master
        master.title = "Web Page Token Analyzer Application"
        self.current_url = tkinter.StringVar()
        #initialize the frames needed

        self.frame_header = tkinter.Frame(master,height = 50,width = 1000) #for the header , that holds the title in the screen
        self.frame_url = tkinter.Frame(master,height = 50,width = 1000) #  frame which holds the "enter the URL " label and the "Entry" field where the user can enter the URL
        self.frame_buttons = tkinter.Frame(master,height = 50,width = 1000) # frame to hold the extract and the reset buttons
        self.frame_progress_bar = tkinter.Frame(master,height = 50, width = 1000) # frame to hold the progress bar
        self.frame_output_heading = tkinter.Frame(master,height = 200,width = 1000) #  frame to hold the heading label while extracting the webpage
        self.frame_output_set_1 = tkinter.Frame(master,height = 200,width = 1000) # frame to hold the first five token labels
        self.frame_output_set_2 = tkinter.Frame(master,height = 200,width = 1000)# frame to hold the next five token labels
        self.frame_output_set_3 = tkinter.Frame(master,height = 200,width = 1000)# frame to hold the last five set of token labels

        #packing all the frames in the desired order
        self.frame_header.pack()
        frame_url.pack()
        frame_buttons.pack()
        frame_progress_bar.pack()
        frame_output_heading.pack()
        frame_output_set_1.pack()
        frame_output_set_2.pack()
        frame_output_set_3.pack()

        #labels
        #title label
        self.title_label = tkinter.Label(frame_header, text = "Web Page Token Analyzer", anchor = "center", fg = "brown", height = 2)
        self.title_label.config(font = ("Calibri", 40)) 
        self.title_label.pack() #pack it

        #label for to hold the "enter the URL" value

        self.enter_url_label = tkinter.Label(frame_url,text = "Enter the URL     ")
        self.enter_url_label.config(font = ("Calibri", 16))

        self.enter_url_label.pack(side= "left")

        #label to hold the heading when displaying the tokens
        self.label_op1 = tkinter.Label(frame_output_heading)

        #runtime dynamic labels to display the tokens

        self.labels= []

        for i in range(15):
             label_text = "Label_" + str(i)
             if i < 5:
                 label = tkinter.Label(frame_output_set_1, height = 3, justify = "center", anchor = "center",pady = 2,font = "Calibri", fg= "brown",wraplength = 250, relief = "ridge",width = 20, padx = 5)
             if i >=5 and i < 10:
                 label = tkinter.Label(frame_output_set_2, height = 3 ,justify = "center",anchor = "center",pady = 2,font = "Calibri", fg = "brown",wraplength = 250 ,relief = "ridge",width = 20, padx = 5)
             if i >= 10:
                 label = tkinter.Label(frame_output_set_3,height = 3, justify = "center",anchor = "center",pady = 2, font = "Calibri", fg = "brown",wraplength = 250, relief = "ridge",width = 20, padx = 5)
             labels.append(label)
        
        
        #entry widget for getting the user's value

        self.enter_user_url_label = tkinter.Entry(frame_url,width=100,textvariable = current_url)

        self.enter_user_url_label.pack(side= "left")

        #buttons
        #reset button
        self.reset_button = tkinter.Button(frame_buttons,text = "Reset",width = 10,command = on_reset)
        self.reset_button.pack(side = "left")

        #extract button
        self.extract_button = tkinter.Button(frame_buttons,text = "Extract",width=10,command = on_extract)
        self.extract_button.pack(side = "left")
        

    def check_url(self,url):
        #this function is for validating the 
        try:
        request = requests.get(url)
        if request.status_code == 200:
            
            return True
        else:
            return False

        except:
            return False

        
        
        
