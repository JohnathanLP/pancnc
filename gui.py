import Tkinter as tk
from PIL import ImageTk, Image
import Tkinter, Tkconstants, tkFileDialog

window = tk.Tk()
WINDOW_OPEN = True

def load_file():
    window.filename = tkFileDialog.askopenfilename(initialdir = "/home/johnathan/Documents/pancnc/parsed/images",title = "Select file", filetypes = (("png files","*.png"),("all files","*.*")))
    window.img = ImageTk.PhotoImage(Image.open(window.filename).resize((700,700)))   
    window.panel.configure(image = window.img)
    window.panel.image = window.img
    #print(window.filename)

def launch():
    global WINDOW_OPEN
    #This creates the main window of an application
    window.title("PanCNC")
    #window.geometry("900x700")
    #window.attributes('-zoomed', True)
    window.configure(background='grey')

    window.filename = "parsed/images/carrot.png"

    #Image
    window.img = ImageTk.PhotoImage(Image.open(window.filename).resize((700,700)))
    window.panel = tk.Label(window, image = window.img, height = 700, width = 700, background = "blue")
    window.panel.grid(column = 0, row = 0, rowspan = 12)

    def say_hello():
        print ("Hello!")

    #Right bar background
    right_bar = tk.Canvas(background = "lightgray", height = 700, width = 200)
    right_bar.grid(column = 1, row = 0, rowspan = 12)

    #Button to print message to the terminal
    hello_button = tk.Button(window, text = 'Print!', command = say_hello, width = 20)
    hello_button.grid(column = 1, row = 5)

    #Sliders to set darkness
    slider1 = tk.Scale(window, from_ = 0, to = 100, orient = "horizontal", length = 180, label = "Darkness")
    slider1.grid(column = 1, row = 2)

    slider2 = tk.Scale(window, from_ = 0, to = 100, orient = "horizontal", length = 180)
    slider2.grid(column = 1, row = 3)
        
    #Button to lead new image
    load = tk.Button(window, text = 'Load File...', command = load_file, width = 20)
    load.grid(column = 1, row = 0)

    def closeWindow():
        global WINDOW_OPEN
        WINDOW_OPEN = False
        #window.destroy()

    #Button to quit application
    quit_button = tk.Button(window, text = 'Quit!', command = closeWindow, width = 20, background = "red")
    quit_button.grid(column = 1, row = 11)

    #Start the GUI
    #window.mainloop()
    while WINDOW_OPEN:
        window.update_idletasks()
        window.update()
        if slider1.get() > slider2.get():
            slider2.set(slider1.get())

    window.destroy()
