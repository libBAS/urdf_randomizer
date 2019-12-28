import tkinter as tk
import tkinter.filedialog as filedialog

from xml_viewer import XML_Viwer

DEBUG  = True
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.xml_string = ""


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

        self.b_3 = tk.Button(self)
        self.b_3["text"] = "Set generation #"
        self.b_3["command"] = self.set_num_gens
        self.b_3.pack(side="top")

        self.l_3_v = tk.StringVar()
        self.l_3 = tk.Label(self.master, textvariable=self.l_3_v)
        self.l_3.pack(side="top")

        self.i_3 = tk.Entry(self)
        self.i_3.insert(10, "15")
        self.i_3.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def get_urdf_file(self):
        if DEBUG:
            root.filename = "example.xml"
        else:
            root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("URDF files","*.xml"),("all files","*.*")))
        self.urdf_master = root.filename
        self.l_1_v.set("Using base URDF:\n" + self.urdf_master + "\n")
        print("Using base URDF:\n" + self.urdf_master + "\n")

        # load xml into string
        self.xml_string = open(self.urdf_master).read()
        # display
        self.urdf_tree = XML_Viwer(root, self.xml_string, heading_text="Original").pack(side="left")
    
    def get_save_directory(self):
        if DEBUG:
            root.filename = "generated"
        else:
            root.filename =  filedialog.askdirectory()
        self.save_directory = root.filename
        self.l_2_v.set("Saving generated URDFs to:\n" + self.save_directory + "\n")
        print("Saving generated URDFs to:\n" + self.save_directory + "\n")
    
    def set_num_gens(self):
        self.num_generations = self.i_3.get()
        self.l_3_v.set("# of Generations: " + str(self.num_generations))
        

root = tk.Tk()
app = Application(master=root)

xml = """
<messages>
    <note id="501">
    <to>Tove</to>
    <from>Jani</from>
    <heading>Reminder</heading>
    <body>Don't forget me this weekend!</body>
    </note>
    <note id="502">
    <to>Jani</to>
    <from>Tove</from>
    <heading>Re: Reminder</heading>
    <body>I will not</body>
    </note>
</messages>"""
# XML_Viwer(root, xml, heading_text="Original").pack(side="left")
XML_Viwer(root, xml, heading_text="Extent").pack(side="right")

app.mainloop()