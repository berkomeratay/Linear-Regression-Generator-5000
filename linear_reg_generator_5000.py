# -*- coding: utf-8 -*-
"""
@author: berkomeratay
"""

from tkinter import*

from PIL import ImageTk, Image
import pandas as pd
import statsmodels.api as sm
from patsy import dmatrices
quitter = 0
var_list = list()
sev_dec = 0

def close_window(): 
    root.destroy()
    global quitter
    quitter += 1
    

root_temp = Tk()
label_n = Label(root_temp,text = r"Please Enter the Directory of the Dataset (example: C:\Users\HP\Desktop\schooling_earnings.csv): )
label_n.pack()
root_temp.title("Linear Regression Generator 5000")
root_temp.geometry('600x300') 
def retrieve_input_3():
    global inputValue3
    inputValue3 = str(direc.get("1.0","end-1c"))
    print(inputValue3)
    temp_frame.place(relx = 0.5, rely = 0.6, relwidth = 0.3, relheight = 0.3, anchor = "n")
    typelabel = Label(root_temp, text = "Please Choose the Type of the Dataset")
    typelabel.place(anchor = 'n', relx = 0.5, rely = 0.5)
    XLSXButton.pack(side = "left", fill = "both", expand = "True")
    CSVButton.pack(side = "left", fill = "both", expand = "True")
    dtaButton.pack(side = "left", fill = "both", expand = "True")
direc = Text(root_temp,height = 3, width = 50, bg= "lightgreen")
direc.pack()

temp_frame = Frame(root_temp, height = 3, width = 5, bg = "black")

def retrieve_excel():
    global chooser
    chooser = 0
    
def retrieve_csv():
    global chooser
    chooser = 1

def retrieve_dta():
    global chooser
    chooser = 2   



def button_show():
    next_frame = Frame(root_temp, bg= "black", height = 20, width = 20)
    next_frame.place( relx = 0.7, rely = 0.8 ,relwidth = 0.2, relheight = 0.1)
    
    next_button = Button(next_frame, text = "Next", command = root_temp.destroy,bg = "green", fg= "white")
    next_button.pack(fill = "both", expand = "True")
    


var_done = Button(root_temp,text = "Save the Directory",bg = "lightblue", command = lambda : [retrieve_input_3()])
var_done.place(relx = 0.5, rely = 0.25, relwidth = 0.25, relheight = 0.1, anchor = "n")

XLSXButton = Button(temp_frame,text = ".xlsx\n.xls",bg = "blue",fg = "white" ,command = lambda : [retrieve_excel(),button_show()])
CSVButton = Button(temp_frame,text = ".csv",bg = "green",fg = "white",command = lambda : [retrieve_csv(),button_show()])
dtaButton = Button(temp_frame,text = ".dta",bg = "red",fg = "white",command = lambda : [retrieve_dta(),button_show()] )



root_temp.mainloop()

def reg_generator():
    
    if chooser == 0:
        reader_func = pd.read_excel
    elif chooser == 1:
        reader_func = pd.read_csv
    else:
        reader_func = pd.read_stata
    
    global model_data
    model_data = reader_func(inputValue3)
    label1 = Label(root,text = "\nFor regression variables, please use the codes given below.\nIf necessary, scroll down in the section below to see all the variables:\n ", font=("arial",9,"bold"), fg = "white", bg = "grey")
    label1.pack()
    b = 1
    list_box_1 = Listbox(root)
    list_box_1.pack()
    for i in model_data.columns:
        list_box_1.insert(END,i)
    
    def retrieve_input_1():
        global inputValue1
        inputValue1 = str(depp.get("1.0","end-1c"))
        print(inputValue1)
    def retrieve_input_2():
        global inputValue2
        inputValue2 = str(indepp.get("1.0","end-1c"))
        print(inputValue2)
    
    
    label_m = Label(root,text="Please Enter the Name of the Dependent Variable: ",font=("arial",9,"bold"), fg = "white", bg = "grey")
    label_m.pack()
    
    depp = Text(root,height = 1, width = 20, bg= "lightgreen")
    depp.pack()
    label_n = Label(root,text = "Please Enter the Name of the Independent Variables by Putting '+' Sign Inbetween Them,\n For Interaction Terms Please Use '*' Sign Between Variables: ",font=("arial",9,"bold"), fg = "white", bg = "grey")
    label_n.pack()
    
    indepp = Text(root,height = 3, width = 40, bg= "lightgreen")
    indepp.pack()
    
    global rob_error
    rob_error = IntVar()
    checker = Checkbutton(root, text = "Use Heteroskedasticity Robust Standart Errors" , variable = rob_error, bg = "grey")
    checker.pack()
    
    var_done = Button(root,text = "Save the Variables and Run the Regression",bg = "lightblue", command = lambda : [retrieve_input_1(),retrieve_input_2(),root.destroy()])
    var_done.pack()

root = Tk()

root.attributes('-fullscreen', True)
root.title("Linear Regression Generator 5000")


canvas = Canvas(root)
canvas.pack()

bck_image = PhotoImage(file = "stats_wallpaper.gif")
bck_label = Label(image = bck_image)
bck_label.place(relx = 0, rely = 0, relwidth = 1, relheight= 1,anchor = "nw")


upper_frame = Frame(root, bg = "black", bd = 5)
upper_frame.place(relx = 0.5,rely = 0.1, relwidth = 0.7, relheight = 0.1, anchor = "n")
reg_open = Label(upper_frame,text = "You are working with LINEAR REGRESSION GENERATOR 5000 for econometric analysis powered by Python\n\ndeveloped by BERK ÖMER ATAY", font=("ariel",10,"bold"), fg = "white", bg = "grey")
reg_open.place(relwidth = 1, relheight = 1)

middle_frame = Frame(root, bg = "black", bd = 5)
middle_frame.place(relx = 0.5,rely = 0.22, relwidth = 0.17, relheight = 0.1, anchor = "n")
starter_button = Button(middle_frame,text = "Click Here to Start to Analysis!",command = lambda: reg_generator(), fg = "blue", activebackground = "lightblue")
starter_button.pack(fill = "both", expand = "True")
quit_button = Button(middle_frame,text = "Click Here to Quit the Analysis!",command = close_window, fg = "red")
quit_button.pack(fill = "both", expand = "True")

root.mainloop()
if quitter == 0:
    
    if rob_error.get() == 0:
        y,x = dmatrices("{} ~ {}".format(inputValue1,inputValue2) , data = model_data)
        model_fit = sm.OLS(y,x)
        results = model_fit.fit()
        xb = results.predict(x)
    elif rob_error.get() == 1:
        y,x = dmatrices("{} ~ {}".format(inputValue1,inputValue2) , data = model_data)
        model_fit = sm.OLS(y,x)
        results = model_fit.fit(cov_type='HC3')
        xb = results.predict(x)
    root_2 = Tk()
    root_2.title("Linear Regression Generator 5000")
    label_end = Label(root_2, text = results.summary())
    label_end.pack()
    endButton = Button(root_2, text = "Close the Analysis",command = lambda : root_2.destroy(), fg = "red")
    endButton.pack()
    def saver():
        global sev_dec
        sev_dec = 1
        root_2.destroy()
    saveButton = Button(root_2, text = "Save the Results", command = saver,fg = "blue")
    saveButton.pack()
    root_2.mainloop()
   
        
if sev_dec == 1:
   
    saving_root = Tk()
    saving_root.title("Linear Regression Generator 5000")
    saving_root.geometry("600x300")
    saverLabel = Label(saving_root, text = "Please Enter a Name for the .txt file")
    saverLabel.pack()
    saverText = Text(saving_root,height = 2, width = 25, bg= "lightgreen")
    saverText.pack()
        
    def save_close():
        print(latex_val.get())
        global txt_direc
        txt_direc = str(saverText.get("1.0","end-1c")+".txt")
        text_file = open(txt_direc, "w")
        text_file.write(str(results.summary()))
        text_file.close()
        if latex_val.get() == 1:
            global txt_direc_2
            txt_direc_2 = str(saverText.get("1.0","end-1c")+"_LaTeX"+".txt")
            text_file_2 = open(txt_direc_2, "w")
            text_file_2.write(str(results.summary().as_latex()))
            text_file_2.close()
        else:
            pass
            
        saving_root.destroy() 
        
    global latex_val
    latex_val = IntVar()

    latex_check = Checkbutton(saving_root, text = "Save the LaTeX Code in a Seperate .txt File",onvalue = 1, offvalue = 0, variable = latex_val).pack()
    direc_puller = Button(saving_root, text = "Save and Close", command = save_close,fg = "white",bg = "green")
        
    direc_puller.pack()
        
    saving_root.mainloop()
