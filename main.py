import sys
from pygame import time
import launchpad_py as launchpad
from tkinter import *
from tkinter import filedialog
from json import dump, load
import os
import subprocess
from infi.systray import SysTrayIcon

try:
    print("-" * 50)
    print(" " * 20 + "LaunchApp")
    print(" " * 13 + "Check tray icon for options.")
    print("-" * 50)
except:
    pass

root = Tk()
root.withdraw()
binding_toggle = False
key_toggle = False

def msgbox(x, y):
    top = Toplevel()
    top.title = x
    Message(top, text= y, padx=20, pady=20).pack()
    Button(top, text = "ok", padx = 10, command = top.destroy).pack()
    top.after(10000, top.destroy)
    
try:
    lp = launchpad.Launchpad()
    lp.Open()
    lp.Reset()
except AttributeError:
    msgbox("Error!", "Failed to connect the launchpad!")

bind_list = [
    
]

def launch(k):
    if binding_toggle:
        return
    keys = [k for _, k in bind_list]
    try:
        ki = keys.index(k) # Finding program path
    except ValueError:
        return
    program_path = bind_list[ki][0]
    try:
        subprocess.Popen(program_path)
    except:
        msgbox("Error!", "Program was moved or deleted.")
        bind_list.pop(ki) # If the path no longer exists it gets deleted.
        lp.Reset()

def bindToggle():
    global binding_toggle
    binding_toggle = not binding_toggle
    if binding_toggle is True:
        lp.LedAllOn(1)
    elif binding_toggle is False:
        lp.LedAllOn(0)

def keyToggle():
    global key_toggle
    key_toggle = not key_toggle
    print("binding {}.".format(key_toggle))
    if key_toggle is True:
        lp.LedAllOn(72)
    elif key_toggle is False:
        lp.LedAllOn(0)

def specialkeys(k):
    if (k == [0,0]):
        bindToggle()

def bind(k):
    global binding_toggle
    bindvalue = [i[1] for i in bind_list]
    try:
        index = bindvalue.index(k)
    except ValueError:
        pass
    if binding_toggle and k not in bindvalue:
        if k == [0,0]:
            pass
        else:
            currdir = os.getcwd()
            try:
                f = str(filedialog.askopenfilename(initialdir=currdir, title="Please Select a Directory",  filetypes = (("Exe files","*.exe"), ("ONLY .exe", "*.exe"))))
            except:
                pass
            if f != "":
                bind_list.append([f, k])
            elif f == "":
                pass
    elif binding_toggle and k in bindvalue:
        del bind_list[index]
        bind(k)

def key(e):
    return list(e[:-1])

def save_binds(systray):
    with open("save.json", "w", encoding="utf8") as f:
        dump(bind_list, f)

def load_binds(systray):
    global bind_list
    with open("save.json", "r", encoding="utf8") as f:
        bind_list = load(f)
        

def clear_binds(systray):
    global bind_list
    global binding_toggle
    bind_list.clear()
    lp.Reset()
    binding_toggle = False
    light_bound_keys()
def exitapp():
    lp.Reset()
    lp.Close()
    exit(0)

def on_quit_callback(systray):
    sys.exit()

menu_options = (("Save", None, save_binds),("Load", None, load_binds),("Reset binds", None, clear_binds),)
systray = SysTrayIcon("icon.ico", "LaunchAPP", menu_options, on_quit= on_quit_callback)
systray.start()

def light_bound_keys():
    try:
        keys = [k for _, k in bind_list]
        
        for x,y in keys:
            lp.LedCtrlXY(x,y,3,0)
    except:
        pass

while True:
    root.update()
    try:
        btns = lp.ButtonStateXY()
    except:
        pass
    light_bound_keys()
    try:
        lp.LedCtrlXY(0,0,3,3)
    except:
        pass
    try:
        if len(btns) > 0 and btns[2] is True:
            k = key(btns)
            specialkeys(k)
            bind(k)
            launch(k)
    except NameError:
        pass
