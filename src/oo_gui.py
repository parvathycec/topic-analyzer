import tkinter
from tkinter import messagebox
import tkinter.ttk as ttk
from web_topic_analyzer import WebTopicAnalyzer
import datetime
import threading
import time

actual_url = ""
#import words
import requests

tokens = []


class project_GUI:
    def __init__(self,master):
        self.master = master
        self.master.title("Web Page Token Analyzer")
        #self.master.geometry("2000x2000+0+0")

        #frames

        self.frame_header = tkinter.Frame(self.master,height = 50,width = 1000)
        self.frame_url = tkinter.Frame(self.master,height = 50,width = 1000)
        self.frame_buttons = tkinter.Frame(self.master,height = 50,width = 1000)
        self.frame_progress_bar = tkinter.Frame(self.master,height = 50, width = 1000)
        self.frame_output_heading = tkinter.Frame(self.master,height = 200,width = 1000)
        self.frame_output_set_1 = tkinter.Frame(self.master,height = 200,width = 1000)
        self.frame_output_set_2 = tkinter.Frame(self.master,height = 200,width = 1000)
        self.frame_output_set_3 = tkinter.Frame(self.master,height = 200,width = 1000)

        #packing all the frames
        
        self.frame_header.pack()
        self.frame_url.pack()
        self.frame_buttons.pack()
        self.frame_progress_bar.pack()
        self.frame_output_heading.pack()
        self.frame_output_set_1.pack()
        self.frame_output_set_2.pack()
        self.frame_output_set_3.pack()
        

        self.current_url= tkinter.StringVar()

        #label for header text title

        self.title_label = tkinter.Label(self.frame_header, text = "Web Page Token Analyzer", anchor = "center", fg = "brown", height = 2)
        self.title_label.config(font = ("Calibri", 40))
        self.title_label.pack()

        #label for loading message

        self.loading_text = tkinter.Label(self.frame_progress_bar, bd = 4, font = "Calibri", fg = "brown" , anchor = "center", height = 2)
        
        
        #label for user text

        self.enter_url_label = tkinter.Label(self.frame_url,text = "Enter the URL     ")
        self.enter_url_label.config(font = ("Calibri", 16))

        self.enter_url_label.pack(side= "left")

        #entry for user to enter the url


        self.enter_user_url_label = tkinter.Entry(self.frame_url,width=100,textvariable = self.current_url)

        self.enter_user_url_label.pack(side= "left")
        self.enter_user_url_label.focus()
        

        #button

        #reset button
        self.reset_button = tkinter.Button(self.frame_buttons,text = "Reset",width = 10,command = self.on_reset)
        self.reset_button.pack(side = "left")

        #extract button
        self.extract_button = tkinter.Button(self.frame_buttons,text = "Extract",width=10,command = self.on_extract)
        self.extract_button.pack(side = "left")

        self.label_op1 = tkinter.Label(self.frame_output_heading)
        self.labels= []

        for i in range(15):
             label_text = "Label_" + str(i)
             if i < 5:
                 label = tkinter.Label(self.frame_output_set_1, height = 3, justify = "center", anchor = "center",pady = 2,font = ("Calibri",14), fg= "brown",wraplength = 250, relief = "ridge",width = 30, padx = 1)
             if i >=5 and i < 10:
                 label = tkinter.Label(self.frame_output_set_2, height = 3 ,justify = "center",anchor = "center",pady = 2,font = ("Calibri",14), fg = "brown",wraplength = 250 ,relief = "ridge",width = 30, padx = 1)
             if i >= 10:
                 label = tkinter.Label(self.frame_output_set_3,height = 3, justify = "center",anchor = "center",pady = 2, font = ("Calibri",14), fg = "brown",wraplength = 250, relief = "ridge",width = 30, padx = 1)
             self.labels.append(label)


    def check_url(self,url):
        try:
            request = requests.get(url)
            if request.status_code == 200 and ("text/html" in request.headers["content-type"]):  
                return True
            else:
                return False

        except:
            return False

    def pack_loading(self):
        self.loading_text.config(text = "Loading...")
        self.loading_text.pack()
        
    def on_reset(self):
        self.enter_user_url_label.delete(0,'end')
        self.label_op1.pack_forget()
        for label in self.labels:
            label.pack_forget()


    def no_url(self):
        tkinter.messagebox.showerror("Error","Website does not exist or it is forbidden, Please check it!")

       
        
    def on_extract(self):
        #pack the label
        #please_wait_label.pack_forget()
        actual_url = self.current_url.get()
                
        if self.check_url(actual_url) == True:
           
           a = datetime.datetime.now()
           analyzer = WebTopicAnalyzer(actual_url);
           process_result = analyzer.process();
           if 'error' in process_result:
            tkinter.messagebox.showerror("Error",process_result['error']);
           elif 'words' in process_result:
            tokens = process_result['words'];
            self.label_op1.config(text = "Tokens for the webpage", height = 3, anchor = "center", fg = "brown" , font = ("calibri",20))
            self.label_op1.pack(side = "top")
            
            for label_index in range(len(tokens)):
                if label_index < 5:
                    self.labels[label_index].config(text = str(tokens[label_index]))
                    self.labels[label_index].pack(fill= "x",side = "left")
                elif label_index >= 5 and label_index < 10:
                    self.labels[label_index].config(text = str(tokens[label_index]))
                    self.labels[label_index].pack(fill= "x",side = "left")
                else:
                    self.labels[label_index].config(text = str(tokens[label_index]))
                    self.labels[label_index].pack(fill= "x",side = "left")

            self.loading_text.pack_forget()
        
            b = datetime.datetime.now()
            c = b - a
            print("Total time taken : ", c.seconds, " seconds")
           
          
            
        else:
            self.no_url()
            
            
   

master = tkinter.Tk()
master.state('zoomed')
p = project_GUI(master)

master.mainloop()


