import tkinter as tk
import fluteParamsCalc
import os
import sys
from subprocess import check_call, call

last_key = ""
od = 0.0
wt = 0.0
od_picked = False
wt_picked = False
blender_folder = ""
final_filename = ""
existing_filename = ""
tki = tk.Tk()
canvas = tk.Canvas(tki, width=800, height=500, bg="bisque2")
entry2 = tk.Entry(tki, font=('Tahoma 16 bold '))
entry3 = tk.Entry(tki, font=('Tahoma 16 bold '))
entry4 = tk.Entry(tki, font=('Tahoma 16 bold '))
entry5 = tk.Entry(tki, font=('Tahoma 16 bold '))

def install(package):
    check_call([sys.executable, "-m", "pip", "install", package])


def open_blender_file():
    work_directory = fluteParamsCalc.og_directory
    os.chdir(work_directory)
    filename = final_filename + ".blend"
    os.system(filename)
    return


def make_path_work(pathstr):
    new_path = ""
    for char in pathstr:
        if (char == '\\'):
            new_path += r"\\"
        else:
            new_path += char
    return new_path


def exit_create_a_flute():
    tki.destroy()


def final_window():
    canvas.delete('all')
    canvas.create_text(400, 50, anchor='c', text="Creating the flute :)", fill="black", font=('Tahoma 20 bold'))
    canvas.create_text(300, 100, anchor='c', text="Calculating the flute parameters.... ", fill="black",
                       font=('Tahoma 16 bold'))
    canvas.pack()
    fluteParamsCalc.start_calculation(last_key, od, wt, od_picked, wt_picked)
    if fluteParamsCalc.valid_res == False:
        canvas.create_text(550, 100, anchor='c', text="Failed!", fill="red", font=('Tahoma 16 bold'))
        canvas.create_text(400, 150, anchor='c', justify = tk.CENTER, text="The additional parameters specified can't be used to create a flute! Please choose other parameters", fill="red", font=('Tahoma 16 bold'), width = 750)
        button15 = tk.Button(tki, font=('Tahoma 16 bold '), text="Choose new parameters", command=pick_OD_and_thickness)
        canvas.create_window(400, 250, anchor='c', window=button15)
    else:
        if fluteParamsCalc.params_calculated == True:
            canvas.create_text(550, 100, anchor='c', text="Done!", fill="black", font=('Tahoma 16 bold'))
        else:
            canvas.create_text(550, 100, anchor='c', text="Failed!", fill="red", font=('Tahoma 16 bold'))
        canvas.create_text(340, 150, anchor='c', text="Building the model.... ", fill="black", font=('Tahoma 16 bold'))
        fluteParamsCalc.build_the_model(blender_folder, final_filename)
        if fluteParamsCalc.model_built == True:
            canvas.create_text(550, 150, anchor='c', text="Done!", fill="black", font=('Tahoma 16 bold'))
        else:
            canvas.create_text(550, 150, anchor='c', text="Failed!", fill="red", font=('Tahoma 16 bold'))
        button13 = tk.Button(tki, font=('Tahoma 16 bold '), text="Open the file ", command=open_blender_file)
        canvas.create_window(400, 200, anchor='c', window=button13)
        button14 = tk.Button(tki, font=('Tahoma 16 bold '), text="Exit", command=exit_create_a_flute)
        canvas.create_window(400, 250, anchor='c', window=button14)

def check_if_legal_filename(name):
    illegal_chars = ['<', '>', ':', '"', '\/', '\\', '|', '?', '*']
    res_words = ["CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4",
                 "COM5", "COM6", "COM7", "COM8", "COM9", "COM0", "LPT1", "LPT2",
                 "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9", "LPT0"]
    if name == "":
        return False
    for char in name:
        for il_char in illegal_chars:
            if char == il_char:
                return False
    for res_word in res_words:
        if name == res_word:
            return False
    return True

def replace_file():
    global final_filename
    filename = existing_filename + ".blend"
    os.remove(filename)
    final_filename = existing_filename
    final_window()
                          
def custom_name_file():
    global final_filename
    file_name_try = entry5.get()
    if check_if_legal_filename(file_name_try) == False: 
        canvas.delete('FilenameTitle')
        canvas.create_text(400, 100, anchor='c', justify = tk.CENTER,
                       text="Invalid filename. Please choose another filename",
                       fill="red", font=('Tahoma 20 bold'), width=750, tags = ('FilenameTitle'))
    elif os.path.isfile(file_name_try + ".blend"):
        canvas.delete('FilenameTitle')
        canvas.delete('Replacebutton')
        canvas.create_text(400, 100, anchor='c', justify = tk.CENTER,
                       text="A file with the name "  +file_name_try + ".blend already exists. Please rename your file or click the replace button to replace the existing file with the new one",
                       fill="red", font=('Tahoma 20 bold'), width=750, tags = ('FilenameTitle'))
        global existing_filename
        existing_filename = file_name_try
        button19 = tk.Button(tki, font=('Tahoma 14 bold '),
                         text="Replace the existing " + file_name_try + ".blend file",
                         command=replace_file)
        canvas.create_window(400, 200, anchor='c', window=button19, tags = 'Replacebutton')
    else:
        canvas.delete('FilenameTitle')
        final_filename = file_name_try
        final_window()        
        
def default_name_file():
    global final_filename
    if os.path.isfile("flute.blend"):
        canvas.delete('FilenameTitle')
        canvas.delete('Replacebutton')
        canvas.create_text(400, 100, anchor='c', justify = tk.CENTER,
                       text="A file with the name flute.blend already exists. Please rename your file or click the replace button to replace the existing file with the new one",
                       fill="red", font=('Tahoma 20 bold'), width=750, tags = ('FilenameTitle'))
        global existing_filename
        existing_filename = "flute"
        button19 = tk.Button(tki, font=('Tahoma 14 bold '),
                         text="Replace the existing flute.blend file",
                         command=replace_file)
        canvas.create_window(400, 200, anchor='c', window=button19, tags = 'Replacebutton') 
    else:
        final_filename = "flute"
        final_window()
    
def blend_name_choosing():
    canvas.delete('all')
    canvas.create_text(400, 100, anchor='c', justify = tk.CENTER,
                       text="How would you like your blend file to be called?.\n\nThe default is 'flute'",
                       fill="black", font=('Tahoma 20 bold'), width=750, tags = ("FilenameTitle"))
    canvas.create_text(400, 250, anchor='c', justify = tk.CENTER,
                       text="(No need to specify the .blend extension)",
                       fill="black", font=('Tahoma 16 bold'), width=750)
    canvas.create_window(400, 300, anchor='c', window=entry5, height=30, width=400)
    button17 = tk.Button(tki, font=('Tahoma 14 bold '),
                         text="That's the file name I want - make the flute! (this can take a few seconds)",
                         command=custom_name_file)
    canvas.create_window(400, 350, anchor='c', window=button17)
    button18 = tk.Button(tki, font=('Tahoma 14 bold '),
                         text="Use the default name for the file - make the flute! (this can take a few seconds)",
                         command=default_name_file)
    canvas.create_window(400, 400, anchor='c', window=button18)

    
def custom_blender_folder_check():
    canvas.delete('all')
    blender_folder_try = entry4.get()
    if os.path.isdir(blender_folder_try) == False or os.path.isfile(blender_folder_try + "\\blender.exe") == False:
        canvas.create_text(400, 50, anchor='c',
                           text="Either the directory doesn't exist or it doesn't contain blender.exe. Please change the specified directory",
                           fill="red", font=('Tahoma 16 bold'), width=750)
        button12 = tk.Button(tki, font=('Tahoma 16 bold '), text="Specify the correct blender directory ",
                             command=pre_final_window)
        canvas.create_window(400, 120, anchor='c', window=button12)
    else:
        global blender_folder
        blender_folder = blender_folder_try
        blend_name_choosing()


def default_blender_folder_check():
    canvas.delete('all')
    blender_folder_try = "C:\Program Files\Blender Foundation\Blender 3.0"
    if os.path.isdir(blender_folder_try) == False or os.path.isfile(blender_folder_try + "\\blender.exe") == False:
        canvas.create_text(400, 50, anchor='c', text="Invalid directory, please change the specified directory",
                           fill="red", font=('Tahoma 16 bold'))
        button12 = tk.Button(tki, font=('Tahoma 16 bold '), text="Specify the correct blender directory ",
                             command=pre_final_window)
        canvas.create_window(400, 100, anchor='c', window=button12)
    else:
        global blender_folder
        blender_folder = blender_folder_try
        blend_name_choosing()


def pre_final_window():
    canvas.delete("all")
    canvas.create_text(400, 100, anchor='c',
                       text="Please specify the blender installation folder.\n\nThe default folder is C:\Program Files\Blender Foundation\Blender 3.0",
                       fill="black", font=('Tahoma 20 bold'), width=750)
    canvas.create_window(400, 250, anchor='c', window=entry4, height=30, width=400)
    button10 = tk.Button(tki, font=('Tahoma 14 bold '),
                         text="Thats my folder",
                         command=custom_blender_folder_check)
    canvas.create_window(400, 300, anchor='c', window=button10)
    button11 = tk.Button(tki, font=('Tahoma 14 bold '),
                         text="My folder is the default folder",
                         command=default_blender_folder_check)
    canvas.create_window(400, 350, anchor='c', window=button11)


def parameters_confirmation():
    canvas.delete("all")
    canvas.create_text(400, 50, anchor='c', text="The chosen parameters are: ", fill="black", font=('Tahoma 20 bold'))
    canvas.create_text(400, 150, anchor='c', text="Key Note: " + last_key, fill="black", font=('Tahoma 16 bold'))
    canvas.create_text(400, 200, anchor='c', text="Additional Parameters: ", fill="black", font=('Tahoma 12'))
    if od_picked == True:
        canvas.create_text(400, 250, anchor='c', text="Outer Diameter: " + od, fill="black", font=('Tahoma 16 bold'))
    else:
        canvas.create_text(400, 250, anchor='c', text="Outer Diameter: Default", fill="black", font=('Tahoma 16 bold'))
    if wt_picked == True:
        canvas.create_text(400, 300, anchor='c', text="Wall Thickness: " + wt, fill="black", font=('Tahoma 16 bold'))
    else:
        canvas.create_text(400, 300, anchor='c', text="Wall Thickness: Default", fill="black", font=('Tahoma 16 bold'))
    button8 = tk.Button(tki, font=('Tahoma 16 bold '), text="Continue to the flute!", command=pre_final_window)
    canvas.create_window(400, 400, anchor='c', window=button8)
    button9 = tk.Button(tki, font=('Tahoma 16 bold '), text="Change the additional parameters",
                        command=pick_OD_and_thickness)
    canvas.create_window(400, 450, anchor='c', window=button9)


def set_OD():
    od_try = entry2.get()
    try:
        od_try = float(od_try)
        canvas.delete('od_status')
        if od_try < 0:
            canvas.create_text(400, 160, anchor='c', text="Invalid OD value! The value needs to be a positive number!", fill="red", font=('Tahoma 16 bold'),
                           tags=('od_status'))   
        else:
            canvas.create_text(400, 160, anchor='c', text="OD is set", fill="black", font=('Tahoma 16 bold'),
                           tags=('od_status'))
            global od
            od = str(od_try)
            global od_picked
            od_picked = True
    except ValueError:
        canvas.delete('od_status')
        canvas.create_text(400, 160, anchor='c', text="Invalid OD value! The value needs to be a positive number!", fill="red", font=('Tahoma 16 bold'),
                           tags=('od_status'))


def set_WT():
    wt_try = entry3.get()
    try:
        wt_try = float(wt_try)
        canvas.delete('thick_status')
        if wt_try < 0:
            canvas.create_text(400, 280, anchor='c', text="Invalid WT value! The value needs to be a positive number!", fill="red", font=('Tahoma 16 bold'),
                           tags=('thick_status'))
        else:
            canvas.create_text(400, 280, anchor='c', text="WT is set", fill="black", font=('Tahoma 16 bold'),
                               tags=('thick_status'))
            global wt
            wt = str(wt_try)
            global wt_picked
            wt_picked = True
    except ValueError:
        canvas.delete('thick_status')
        canvas.create_text(400, 280, anchor='c', text="Invalid WT value! The value needs to be a positive number!", fill="red", font=('Tahoma 16 bold'),
                           tags=('thick_status'))

def default_the_parameters():
    global od_picked
    global wt_picked
    od_picked = False
    wt_picked = False  
    parameters_confirmation()
    
def pick_OD_and_thickness():
    canvas.delete("all")
    canvas.create_text(400, 50, anchor='c', justify=tk.CENTER,
                       text="Pick the outer diameter and the thickness \n of the walls of the flute:", fill="black",
                       font=('Tahoma 20 bold'), tags=('prompt'))
    canvas.create_text(100, 120, anchor='w', text="Outer Diameter of the flute:", fill="black", font=('Tahoma 16'),
                       tags=('prompt'))
    canvas.create_text(70, 240, anchor='w', text="Thickness of the walls of the flute:", fill="black",
                       font=('Tahoma 16'), tags=('prompt'))
    canvas.create_window(440, 120, anchor='w', window=entry2, height=30, width=150)
    canvas.create_window(440, 240, anchor='w', window=entry3, height=30, width=150)
    button5 = tk.Button(tki, font=('Tahoma 16 bold '), text="Set OD", command=set_OD)
    button6 = tk.Button(tki, font=('Tahoma 16 bold '), text="Set WT", command=set_WT)
    canvas.create_window(610, 120, anchor='w', window=button5)
    canvas.create_window(610, 240, anchor='w', window=button6)
    button7 = tk.Button(tki, font=('Tahoma 16 bold '), text="Done!", command=parameters_confirmation)
    canvas.create_window(550, 350, anchor='c', window=button7)
    button16 = tk.Button(tki, font=('Tahoma 16 bold '), text="Use the default parameters", command=default_the_parameters)
    canvas.create_window(300, 350, anchor='c', window=button16)

def additional_parameters():
    canvas.delete("all")
    canvas.create_text(400, 50, anchor='c', justify=tk.CENTER,
                           text="Do you want to pick the outer diameter and the \n thickness of the walls of the flute?",
                           fill="black", font=('Tahoma 16 bold '), tags=('additional_params_question'))
    button3 = tk.Button(tki, font=('Tahoma 16 bold '), text="No, use the default values",
                            command=parameters_confirmation)
    button4 = tk.Button(tki, font=('Tahoma 16 bold '), text="Yes!", command=pick_OD_and_thickness)
    canvas.create_window(350, 120, anchor='c', window=button3)
    canvas.create_window(550, 120, anchor='c', window=button4)


def callback(selection):
    global last_key
    last_key = selection
    canvas.create_text(400, 250, anchor='c', text="Great! We can continue", fill="black",
                       font=('Tahoma 20 bold '), tags=('key_status_text'))
    button2 = tk.Button(tki, font=('Tahoma 16 bold '), text="Let's continue!", command=additional_parameters)
    canvas.create_window(400, 300, anchor='c', window=button2, tags='button2')
    
def main():
    tki.title("Create A Flute")
    canvas.create_text(400, 50, text="Welcome to Create A Flute!", fill="black", font=('Tahoma 32 bold '))
    canvas.create_text(400, 100, anchor='c', text="Please enter the key note you want the flute to be played in:",
                       fill="black", font=('Tahoma 16'))
    options_list = ["A", "B", "C", "D", "E", "F", "G"]
    value_inside = tk.StringVar(tki)
    value_inside.set("Select a key note")
    question_menu = tk.OptionMenu(tki, value_inside, *options_list, command=callback)
    question_menu.config(font = ('Tahoma 20 bold'), width = 220)
    inner_menu = tki.nametowidget(question_menu.menuname)
    inner_menu.config(font=('Tahoma 20 bold ')) 
    selection = value_inside.get()
    canvas.create_window(400, 175, anchor='c', window=question_menu, height=50, width = 300)
    canvas.pack()
    tki.mainloop()


if __name__ == '__main__':
    main()
