import tkinter as tk
import tkinter.filedialog as filedialog
from tkinter.ttk import *

from xml_viewer import XML_Viwer
import xml.etree.ElementTree as ET
import numpy as np

DEBUG  = True

# class Elements:
#     def __init__(self):
#         self.idx = []
#         self.string = ""
#         self.vals = []

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

    def generate(self):

        # observe what has been selected
        selected_i = self.lb.curselection()
        r_tags = []
        for i in selected_i:
            r_tags.append(self.lb.get(i))
        print(r_tags)

        # save read in data
        idxs = []       # xml index
        strings = []    # xml string (avg)
        stringe = []    # xml string (extent)

        # read in data - mean
        tree = ET.parse(self.urdf_master)
        root = tree.getroot()
        robot_name = str(root.attrib['name'])
        print("Robot Name = " + robot_name)
        idx = [0,0,0,0]
        for child in root:
            if child.tag == "joint":
                idx[1] = 0
                for joint in child:
                    idx[1] += 1
                    pass
            if child.tag == "link":
                idx[1] = 0
                for link in child:
                    if link.tag == "inertial":
                        idx[2] = 0
                        for prop in link:
                            if prop.tag == "mass":
                                idxs.append(list(idx))
                                strings.append(root[idx[0]][idx[1]][idx[2]].attrib["value"])
                                pass
                            if prop.tag == "inertia":
                                idxs.append(list(idx))
                                istring = \
                                root[idx[0]][idx[1]][idx[2]].attrib["ixx"] + " " + \
                                root[idx[0]][idx[1]][idx[2]].attrib["ixy"] + " " + \
                                root[idx[0]][idx[1]][idx[2]].attrib["ixz"] + " " + \
                                root[idx[0]][idx[1]][idx[2]].attrib["iyy"] + " " + \
                                root[idx[0]][idx[1]][idx[2]].attrib["iyz"] + " " + \
                                root[idx[0]][idx[1]][idx[2]].attrib["izz"] + " "
                                strings.append(istring)
                                pass
                            idx[2] += 1
                    if link.tag == "visual":
                        pass
                    if link.tag == "collision":
                        idx[2] = 0
                        for prop in link:
                            if prop.tag == "contact_coefficients":
                                # print("Mu is " + str(prop.attrib["mu"]))
                                idxs.append(list(idx))
                                strings.append(root[idx[0]][idx[1]][idx[2]].attrib["mu"])
                            if prop.tag == "geometry":
                                idx[3] = 0
                                for value in prop:
                                    if value.tag == "box":
                                        pass
                                    idxs.append(list(idx))
                                    strings.append(root[idx[0]][idx[1]][idx[2]][idx[3]].attrib["size"])                              
                                    idx[3] += 1
                            idx[2] += 1
                    idx[1] += 1
            idx[0] += 1

        # read in data - extent
        tree = ET.parse(self.urdf_extent_master)
        root = tree.getroot()
        idx = [0,0,0,0]
        for child in root:
            if child.tag == "joint":
                idx[1] = 0
                for joint in child:
                    idx[1] += 1
                    pass
            if child.tag == "link":
                idx[1] = 0
                for link in child:
                    if link.tag == "inertial":
                        idx[2] = 0
                        for prop in link:
                            if prop.tag == "mass":
                                #idxs.append(list(idx))
                                stringe.append(root[idx[0]][idx[1]][idx[2]].attrib["value"])
                                pass
                            if prop.tag == "inertia":
                                #idxs.append(list(idx))
                                istring = \
                                root[idx[0]][idx[1]][idx[2]].attrib["ixx"] + " " + \
                                root[idx[0]][idx[1]][idx[2]].attrib["ixy"] + " " + \
                                root[idx[0]][idx[1]][idx[2]].attrib["ixz"] + " " + \
                                root[idx[0]][idx[1]][idx[2]].attrib["iyy"] + " " + \
                                root[idx[0]][idx[1]][idx[2]].attrib["iyz"] + " " + \
                                root[idx[0]][idx[1]][idx[2]].attrib["izz"] + " "
                                stringe.append(istring)
                                pass
                            idx[2] += 1
                    if link.tag == "visual":
                        pass
                    if link.tag == "collision":
                        idx[2] = 0
                        for prop in link:
                            if prop.tag == "contact_coefficients":
                                # print("Mu is " + str(prop.attrib["mu"]))
                                #idxs.append(list(idx))
                                stringe.append(root[idx[0]][idx[1]][idx[2]].attrib["mu"])
                            if prop.tag == "geometry":
                                idx[3] = 0
                                for value in prop:
                                    if value.tag == "box":
                                        pass
                                    #idxs.append(list(idx))
                                    stringe.append(root[idx[0]][idx[1]][idx[2]][idx[3]].attrib["size"])                              
                                    idx[3] += 1
                            idx[2] += 1
                    idx[1] += 1
            idx[0] += 1

        # generate random values
        
        gen_vals = []
        for e in range(0, len(idxs)):
            
            mean_s = strings[e]
            std_s = stringe[e]

            mean_s = mean_s.split()
            std_s =  std_s.split()

            # gen
            rval_s = []
            for s in range(0, len(mean_s)):
                mean = float(mean_s[s])
                std = float(std_s[s])
                
                # THIS LINE MAKES STD BE IGNORED, INSTEAD USES 5%!!!
                std = mean*0.05

                rval_list = np.random.normal(mean,std,int(self.num_generations))
                rval_s.append(rval_list)

            # rearrange
            rvals = []
            for i in range(0,int(self.num_generations)):
                full_string = ""
                for ii in range(0, len(rval_s)):
                    st = str(rval_s[ii][i])
                    full_string = full_string + " " + st
                rvals.append(full_string)
            gen_vals.append(rvals)

        # save generated values to tree
        for i in range(int(self.num_generations)):
            self.progress['value'] = (int(i)+1)/int(self.num_generations)*100

            new_tree = ET.parse(self.urdf_master)
            new_root = new_tree.getroot()

            mean_tree = ET.parse(self.urdf_master)
            mean_root = mean_tree.getroot()

            std_tree = ET.parse(self.urdf_extent_master)
            std_root = std_tree.getroot()

            # edit new_tree
            print("TEST")
            for idxx in range(0, len(idxs)):
                idx = idxs[idxx]
                val = gen_vals[idxx][i]
                print(idx)
                try:
                    attrib = new_root[idx[0]][idx[1]][idx[2]][idx[3]].attrib
                    tag = new_root[idx[0]][idx[1]][idx[2]][idx[3]].tag
                    print(new_root[idx[0]][idx[1]][idx[2]][idx[3]].attrib)
                    print(new_root[idx[0]][idx[1]][idx[2]][idx[3]].tag)
                except:
                    print("EXCP")
                    attrib = new_root[idx[0]][idx[1]][idx[2]].attrib
                    tag = new_root[idx[0]][idx[1]][idx[2]].tag
                    print(new_root[idx[0]][idx[1]][idx[2]].attrib)
                    print(new_root[idx[0]][idx[1]][idx[2]].tag)

                # add in checks on selection here
                gval = gen_vals[idxx][i]

                if tag == "mass":
                    new_root[idx[0]][idx[1]][idx[2]].attrib["value"] = gval
                if tag == "inertia":
                    gval = gval.split()
                    new_root[idx[0]][idx[1]][idx[2]].attrib["ixx"] = gval[0]
                    new_root[idx[0]][idx[1]][idx[2]].attrib["ixy"] = gval[1]
                    new_root[idx[0]][idx[1]][idx[2]].attrib["ixz"] = gval[2]
                    new_root[idx[0]][idx[1]][idx[2]].attrib["iyy"] = gval[3]
                    new_root[idx[0]][idx[1]][idx[2]].attrib["iyz"] = gval[4]
                    new_root[idx[0]][idx[1]][idx[2]].attrib["izz"] = gval[5]  

                if tag == "contact_coefficients":
                    new_root[idx[0]][idx[1]][idx[2]].attrib["mu"] = gval
                if tag == "box":
                    new_root[idx[0]][idx[1]][idx[2]][idx[3]].attrib["size"] = gval #collision
                    new_root[idx[0]][0][idx[2]][idx[3]].attrib["size"] = gval #visual - assumes above collision

            new_tree.write(self.save_directory + "/generated_" + str(i) + ".xml")
        print("Finished")

# run app
root = tk.Tk()
app = Application(master=root)
app.mainloop()