import tkinter as tk
import tkinter.filedialog as filedialog
from tkinter.ttk import *

from xml_viewer import XML_Viwer
import xml.etree.ElementTree as ET
import numpy as np

DEBUG  = True

class E:
    # def __init__(self):
    #     self.idx = []
    #     self.string = ""
    #     self.vals = []

    # def __init__(self, idx, string, vals):
    #     self.idx = idx
    #     self.string = string
    #     self.vals = vals

    def __init__(self, idx, string):
        self.idx = idx
        self.string = string
        self.vals = []

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.xml_string = ""


    def create_widgets(self):
        self.winfo_toplevel().title("URDF Generator")

        self.b_0 = tk.Button(self)
        self.b_0["text"] = "Select extent URDF"
        self.b_0["command"] = self.get_urdf_extent_file
        self.b_0.pack(side="top")

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


      
        self.l_lb = tk.Label(self.master, text="Features to randomize:")
        self.l_lb.pack(side="top")

        self.lb = tk.Listbox(selectmode=tk.EXTENDED)
        self.lb.insert(tk.END,"box") #box size
        self.lb.insert(tk.END,"mass") #mass value
        self.lb.insert(tk.END,"inertia") #inertia i__
        self.lb.insert(tk.END,"contact_coefficients") #contact_coefficients mu
        self.lb.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

        self.b_4 = tk.Button(self, fg="green")
        self.b_4["text"] = "Generate"
        self.b_4["command"] = self.generate
        self.b_4.pack(side="top")

        self.progress = Progressbar(root, orient = tk.HORIZONTAL, 
              length = 100, mode = 'determinate') 
        self.progress.pack(side="bottom")

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
        self.urdf_tree = XML_Viwer(root, self.xml_string, heading_text="Original").pack(fill="x")
    
    def get_urdf_extent_file(self):
        if DEBUG:
            root.filename = "example_extent.xml"
        else:
            root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("URDF files","*.xml"),("all files","*.*")))
        self.urdf_extent_master = root.filename
        self.l_1_v.set("Using extent URDF:\n" + self.urdf_extent_master + "\n")
        print("Using extent URDF:\n" + self.urdf_extent_master + "\n")

        # load xml into string
        self.xml_extent_string = open(self.urdf_extent_master).read()
        # display
        self.urdf_extent_tree = XML_Viwer(root, self.xml_extent_string, heading_text="Extent").pack(fill="x")#side="right")

    def get_save_directory(self):
        if DEBUG:
            root.filename = "generated"
        else:
            root.filename =  filedialog.askdirectory()
        self.save_directory = root.filename
        self.l_2_v.set("Will save generated URDFs to:\n" + self.save_directory + "\n")
        print("Will save generated URDFs to:\n" + self.save_directory + "\n")
    
    def set_num_gens(self):
        self.num_generations = self.i_3.get()
        self.l_3_v.set("# of Generations: " + str(self.num_generations))

    # class Elements:
    #     def __init__(self):
    #         self.idx = []
    #         self.string = ""
    #         self.vals = []

    def generate(self):
        Elist = []

        # print(self.urdf_tree._element_tree)
        selected_i = self.lb.curselection()
        # print(selected_i)
        r_tags = []
        for i in selected_i:
            # print(i)
            r_tags.append(self.lb.get(i))
            # print("t")
        print(r_tags)

        tree = ET.parse(self.urdf_master)
        root = tree.getroot()

        robot_name = str(root.attrib['name'])
        print("Robot Name = " + robot_name)
        idx = [0,0,0,0]
        for child in root:

            if child.tag == "joint":
                print("JOINT")
                idx[1] = 0
                for joint in child:
                    idx[1] += 1
                    pass

            if child.tag == "link":
                print("LINK")
                idx[1] = 0
                for link in child:

                    if link.tag == "inertial":
                        print("INERT")
                        idx[2] = 0
                        for prop in link:
                            if prop.tag == "mass":
                                print("MASS")
                                string = root[idx[0]][idx[1]][idx[2]].attrib["value"]
                                Elist.append(E(idx, string))
                                pass
                            if prop.tag == "inertia":
                                print("INERTIA")
                                string = root[idx[0]][idx[1]][idx[2]].attrib["ixx"] # FIX
                                Elist.append(E(idx,string))
                                pass
                            idx[2] += 1
                    if link.tag == "visual":
                        print("VIS")
                        pass
                    if link.tag == "collision":
                        print("COL")
                        idx[2] = 0
                        for prop in link:
                            if prop.tag == "contact_coefficients":
                                print("CONT COEF")
                                print("Mu is " + str(prop.attrib["mu"]))
                                string = root[idx[0]][idx[1]][idx[2]].attrib["mu"]
                                Elist.append(E(idx,string))
                            if prop.tag == "geometry":
                                print("GEOM")
                                idx[3] = 0
                                for value in prop:
                                    if value.tag == "box":
                                        print("BOX")
                                        pass
                                    # print(value.tag)
                                    # print(value.attrib)

                                    # print(idx)
                                    # print(root[idx[0]][idx[1]][idx[2]][idx[3]].attrib["size"])
                                    string = root[idx[0]][idx[1]][idx[2]][idx[3]].attrib["size"]
                                    Elist.append(E(idx,string))

                                    print()

                                    
                                    idx[3] += 1
                            idx[2] += 1
                    idx[1] += 1
            idx[0] += 1

        print(len(Elist))
        for e in Elist:
            print(e.idx)
            print(e.string)
            # print(e.vals)

        mean = 5
        std = 1
        print(np.random.normal(mean,std,int(self.num_generations)))

        for i in range(int(self.num_generations)):
            self.progress['value'] = (int(i)+1)/int(self.num_generations)*100

            new_tree = ET.parse(self.urdf_master)
            new_root = new_tree.getroot()

            mean_tree = ET.parse(self.urdf_master)
            mean_root = mean_tree.getroot()

            std_tree = ET.parse(self.urdf_extent_master)
            std_root = std_tree.getroot()

            new_tree.write(self.save_directory + "/generated_" + str(i) + ".xml")
        

root = tk.Tk()
app = Application(master=root)

# xml = """
# <messages>
#     <note id="501">
#     <to>Tove</to>
#     <from>Jani</from>
#     <heading>Reminder</heading>
#     <body>Don't forget me this weekend!</body>
#     </note>
#     <note id="502">
#     <to>Jani</to>
#     <from>Tove</from>
#     <heading>Re: Reminder</heading>
#     <body>I will not</body>
#     </note>
# </messages>"""
# XML_Viwer(root, xml, heading_text="Original").pack(side="left")
# XML_Viwer(root, xml, heading_text="Extent").pack(side="right")

app.mainloop()