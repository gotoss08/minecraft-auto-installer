import tkinter as tk
from subprocess import Popen, call
from threading import Thread


class GuiApp():
    def __init__(self):
        self.root = tk.Tk()
        self.buttons = {}
        self.add_button('install_client_b', 'Install client', self.installClientCallback)
        self.clientThread = None
        self.serverThread = None
        self.add_button('install_server_b', 'Install server', self.installServerCallback)
        self.add_button('run_server_b', 'Run server(NOT WORKING)', self.runServerCallback)

        self.status_text = tk.StringVar()
        self.status_label = tk.Label(self.root, bd=1, relief=tk.SUNKEN, anchor=tk.W, textvariable=self.status_text)
        self.status_label.pack(fill=tk.X)

    def update_status(self, text, color='black'):
        self.status_label['fg'] = color
        self.status_text.set(text)
        self.root.update()

    def add_button(self, id, text, command):
        button = tk.Button(self.root, padx=10, pady=5, text=text, command=command)
        button.pack(padx=10, pady=5, expand='true', fill=tk.BOTH)
        self.buttons[id] = button

    def get_button(self, id):
        return self.buttons[id]

    def installClient(self):
        self.update_status('Installing client...')
        self.root.update()
        call('install-client.bat')
        self.update_status('Client installed.', 'green')

    def installClientCallback(self):
        if not self.clientThread or not self.clientThread.is_alive():
            self.clientThread = Thread(None, self.installClient)
            self.clientThread.start()

    def installServerCallback(self):
        self.update_status('Installing server...')
        call(['install-server.bat'])
        self.update_status('Server installed.', 'green')

    def runServer(self):
        self.update_status('Server is running...', 'green')
        self.get_button('run_server_b')['text'] = 'Stop server'
        self.server_proc = Popen('server/start-server_x64.bat', shell=False)

    def stopServer(self):
        self.update_status('Server stopped.', 'red')
        self.get_button('run_server_b')['text'] = 'Start server'

        if self.server_proc:
            self.server_proc.kill()

    def runServerCallback(self):
        pass
        # if not self.serverThread or not self.serverThread.is_alive():
        #     self.serverThread = Thread(None, self.runServer)
        #     self.serverThread.start()
        # else:
        #     self.stopServer()

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
