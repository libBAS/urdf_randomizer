import tkinter as tk
import tkinter.filedialog as filedialog

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()


    def create_widgets(self):
        self.b_1 = tk.Button(self)
        self.b_1["text"] = "Select URDF"
        self.b_1["command"] = self.get_urdf_file
        self.b_1.pack(side="top")

        self.l_1_v = tk.StringVar()
        self.l_1 = tk.Label(self.master, textvariable=self.l_1_v)
        self.l_1.pack(side="top")

        self.b_2 = tk.Button(self)
        self.b_2["text"] = "Select generation directory"
        self.b_2["command"] = self.get_save_directory
        self.b_2.pack(side="top")

        self.l_2_v = tk.StringVar()
        self.l_2 = tk.Label(self.master, textvariable=self.l_2_v)
        self.l_2.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def get_urdf_file(self):
        root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("URDF files","*.xml"),("all files","*.*")))
        self.urdf_master = root.filename
        self.l_1_v.set("Using base URDF:\n" + self.urdf_master + "\n")
        print("Using base URDF:\n" + self.urdf_master + "\n")
    
    def get_save_directory(self):
        root.filename =  filedialog.askdirectory()
        self.save_directory = root.filename
        self.l_2_v.set("Saving generated URDFs to:\n" + self.save_directory + "\n")
        print("Saving generated URDFs to:\n" + self.save_directory + "\n")

root = tk.Tk()
app = Application(master=root)
app.mainloop()