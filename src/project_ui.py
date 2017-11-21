import tkinter
from tkinter import messagebox
import tkinter.ttk as ttk
from web_topic_analyzer import WebTopicAnalyzer
import datetime

actual_url = ""
#import words
import requests

tokens = []

def check_url(url):
    try:
        request = requests.get(url)
        if request.status_code == 200:
            
            return True
        else:
            return False

    except:
        return False

def on_reset():
    enter_user_url_label.delete(0,'end')
    label_op1.pack_forget()
    for label in labels:
        label.pack_forget()
    progress_bar_label.pack_forget()
        
def no_url():
    tkinter.messagebox.showerror("Error","Website does not exist or it is forbidden, Please check it!")

def on_extract():
    #pack the label
    #please_wait_label.pack_forget()
    actual_url = current_url.get()


    if check_url(actual_url) == True:
        progress_bar_label = ttk.Progressbar(frame_progress_bar,orient='horizontal', mode='indeterminate')
        progress_bar_label.pack(expand = True,fill = "both", side = "top")
        progress_bar_label.start()

      
        a = datetime.datetime.now()
        analyzer = WebTopicAnalyzer(actual_url);
        try:
           tokens = analyzer.process();
           label_op1.config(text = "Tokens for the webpage", height = 3, anchor = "center", fg = "brown" , font = ("calibri",20))
           label_op1.pack(side = "top")
        
           for label_index in range(len(tokens)):
                if label_index < 5:
                    labels[label_index].config(text = str(tokens[label_index]))
                    labels[label_index].pack(fill= "x",side = "left")
                elif label_index >= 5 and label_index < 10:
                    labels[label_index].config(text = str(tokens[label_index]))
                    labels[label_index].pack(fill= "x",side = "left")
                else:
                    labels[label_index].config(text = str(tokens[label_index]))
                    labels[label_index].pack(fill= "x",side = "left")
        except Exception as ex:
            print(ex);
            #TODO: How to show error message in ui
            
        b = datetime.datetime.now()
        c = b - a
        print("Total time taken : ", c.seconds, " seconds")
        progress_bar_label.destroy()
    else:
        no_url()
          
                
    
               
    
    

master = tkinter.Tk()
master.geometry("1000x1000+0+0")
frame_header = tkinter.Frame(master,height = 50,width = 1000)
frame_url = tkinter.Frame(master,height = 50,width = 1000)
frame_buttons = tkinter.Frame(master,height = 50,width = 1000)
frame_progress_bar = tkinter.Frame(master,height = 50, width = 1000)
frame_output_heading = tkinter.Frame(master,height = 200,width = 1000)
frame_output_set_1 = tkinter.Frame(master,height = 200,width = 1000)
frame_output_set_2 = tkinter.Frame(master,height = 200,width = 1000)
frame_output_set_3 = tkinter.Frame(master,height = 200,width = 1000)
frame_header.pack()
frame_url.pack()
frame_buttons.pack()
frame_progress_bar.pack()
frame_output_heading.pack()
frame_output_set_1.pack()
frame_output_set_2.pack()
frame_output_set_3.pack()





current_url= tkinter.StringVar()
#label for header text title

title_label = tkinter.Label(frame_header, text = "Web Page Token Analyzer", anchor = "center", fg = "brown", height = 2)
title_label.config(font = ("Calibri", 40))
title_label.pack()

#label for user text

enter_url_label = tkinter.Label(frame_url,text = "Enter the URL     ")
enter_url_label.config(font = ("Calibri", 16))

enter_url_label.pack(side= "left")

#entry for user to enter the url


enter_user_url_label = tkinter.Entry(frame_url,width=100,textvariable = current_url)

enter_user_url_label.pack(side= "left")

#button

#reset button
reset_button = tkinter.Button(frame_buttons,text = "Reset",width = 10,command = on_reset)
reset_button.pack(side = "left")

#extract button
extract_button = tkinter.Button(frame_buttons,text = "Extract",width=10,command = on_extract)
extract_button.pack(side = "left")

label_op1 = tkinter.Label(frame_output_heading)
labels= []

for i in range(15):
     label_text = "Label_" + str(i)
     if i < 5:
         label = tkinter.Label(frame_output_set_1, height = 3, justify = "center", anchor = "center",pady = 2,font = "Calibri", fg= "brown",wraplength = 250, relief = "ridge",width = 20, padx = 5)
     if i >=5 and i < 10:
         label = tkinter.Label(frame_output_set_2, height = 3 ,justify = "center",anchor = "center",pady = 2,font = "Calibri", fg = "brown",wraplength = 250 ,relief = "ridge",width = 20, padx = 5)
     if i >= 10:
         label = tkinter.Label(frame_output_set_3,height = 3, justify = "center",anchor = "center",pady = 2, font = "Calibri", fg = "brown",wraplength = 250, relief = "ridge",width = 20, padx = 5)
     labels.append(label)

#progress bar

master.mainloop()

