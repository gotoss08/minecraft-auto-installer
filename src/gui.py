import tkinter as tk
from subprocess import call


class GuiApp():
    def __init__(self):
        self.root = tk.Tk()
        self.buttons = {}
        self.add_button('install_client_b', 'Install client', self.installClientCallback)
        self.add_button('install_server_b', 'Install server', self.installServerCallback)
        self.add_button('run_server_b', 'Run server', self.runServerCallback)

        self.status_text = tk.StringVar()
        self.status_label = tk.Label(self.root, bd=1, relief=tk.SUNKEN, anchor=tk.W, textvariable=self.status_text)
        self.status_label.pack(fill=tk.X)

    def update_status(self, text, color='black'):
        self.status_label['fg'] = color
        self.status_text.set(text)
        self.root.update()

    def add_button(self, id, text, command):
        button = tk.Button(self.root, padx=25, pady=25, text=text, command=command)
        button.pack(padx=10, pady=5, expand='true', fill=tk.BOTH)
        self.buttons[id] = button

    def get_button(self, id):
        return self.buttons[id]

    def installClientCallback(self):
        self.update_status('Installing client...')
        self.root.update()
        call('install-client.bat')
        self.update_status('Client installed.', 'green')

    def installServerCallback(self):
        self.update_status('Installing server...')
        call(['install-client.bat', '--server'])
        self.update_status('Server installed.', 'green')

    def runServerCallback(self):
        self.update_status('Server is running...', 'green')
        self.get_button('run_server_b')['text'] = 'Stop server'
        self.update_status('Server stopped.', 'red')


app = GuiApp()

w = 240 # width for the Tk root
h = 280 # height for the Tk root

# get screen width and height
ws = app.root.winfo_screenwidth() # width of the screen
hs = app.root.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)

# set the dimensions of the screen
# and where it is placed
app.root.geometry('%dx%d+%d+%d' % (w, h, x, y))

app.root.wm_title('Minecraft mods installer gui-client')
app.root.mainloop()
