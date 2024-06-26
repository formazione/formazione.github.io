import tkinter as tk
import glob
import os


class Ebook:
    def __init__(self, root, folder, js_link_to_html):
        """Define window for the app"""
        self.root = root
        self.folder = folder
        self.js_link_to_html = js_link_to_html
        self.root.geometry("850x400")
        self.root["bg"] = "coral"
        self.menu()
        self.filelist()
        self.editor()
        self.root.bind("<Control-b>", lambda x: self.save_ebook())
        self.lstb.select_set(0)
        self.filename = self.lstb.get("active")
        self.index = self.lstb.curselection()
        self.show_text_in_editor()
        self.hidden = 0
        self.rootbind()
        self.letter_size = 16

    def rootbind(self):
        self.root.bind("<Control-l>", lambda x: self.hide())
        self.root.bind("<Control-minus>", lambda x: self.small_letters())
        self.root.bind("<Control-MouseWheel>", lambda x: self.wheel(x))

    # Widgets on the left ===============|
    def menu(self):
        """Listbox on the left with file names"""

        self.menubar = tk.Menu(self.root)
        # List of themes
        self.themes = tk.Menu(self.root)
        self.themes.add_command(label="Dark mode", command=self.dark)
        self.themes.add_command(label="Light mode", command=self.light)


        self.menubar.add_command(label="+", command = lambda: self.new_window(Win1))
        self.menubar.add_command(label="DELETE", command= lambda: self.delete_file())
        self.menubar.add_command(label="RENAME", command= lambda: self.new_window(Rename))

        # ========= SUB RENDER ============
        self.menubar.add_command(label="Render Page", command = self.render_page)
        self.menubar.add_command(label="Render Ebook", command = self.save_ebook)


        self.menubar.add_command(label="SAVE", command = self.save)       
        self.menubar.add_command(label="HELP", command= lambda: self.new_window(Help))
        self.menubar.add_cascade(label="THEME", menu=self.themes)
        #self.root.config(menu=self.menu_theme)
        self.root.config(menu=self.menubar)

    def filelist(self):
        self.frame1 = tk.Frame(self.root)
        self.frame1["bg"] = "coral"
        self.frame1.pack(side='left', fill=tk.BOTH)
        #self.frame1.pack()
        self.lstb = tk.Listbox(self.frame1, width=30) # selectmode='multiple', exportselection=0)
        self.lstb['bg'] = "black"
        self.lstb['fg'] = 'gold'
        self.lstb.pack(fill=tk.BOTH, expand=1)
        self.lstb.bind("<<ListboxSelect>>", lambda x: self.show_text_in_editor())
        self.lstb.bind("<F2>", lambda x: self.new_window(Rename))
        self.files = glob.glob(f"{self.folder}\\*.txt")
        #print("self.files", self.files)
        for file in self.files:
            self.lstb.insert(tk.END, file)
        self.lstb.bind("<Control-p>", lambda x: self.render_page())


    def hide(self):
        if self.hidden == 0:
            
            self.frame1.destroy()
            self.hidden = 1
        else:
            self.frame2.destroy()
            self.filelist()
            self.editor()
            self.lstb.select_set(self.index)
            self.show_text_in_editor()
            self.hidden = 0


    # Themes
    def dark(self):
        self.text['bg'] = "black"
        self.text['fg'] = 'white'

    def light(self):
        self.text['bg'] = "darkgreen"
        self.text['fg'] = 'white'
        self.text['font'] = "Arial 24"

    def big_letters(self):
        if self.letter_size < 72:
            self.letter_size += 2
        self.text['font'] = "Arial " + str(self.letter_size)

    def wheel(self, event):
        print(event.delta)
        if event.delta == 120:
            self.big_letters()
        else:
            self.small_letters()

    def small_letters(self):
        if self.letter_size >8:
            self.letter_size -= 2
        self.text['font'] = "Arial " + str(self.letter_size)


    def delete_file(self):
        for num in self.lstb.curselection():
            filehtml = "{}.html".format(self.files[num][:-4])
            if os.path.exists(filehtml): # because not all files are renered
                os.remove("{}.html".format(self.files[num][:-4]))
            os.remove(self.files[num])
        self.reload_list_files_delete()

    def editor(self):
        """The text where you can write"""
        self.frame2 = tk.Frame(self.root)
        self.frame2["bg"] = "coral"
        self.frame2.pack(side='left', fill=tk.Y)
        self.scrollbar = tk.Scrollbar(self.frame2)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.label_file_name = tk.Label(self.frame2, text="Editor - choose a file on the left")
        self.label_file_name.pack(fill=tk.BOTH, expand=1)
        self.text = tk.Text(self.frame2, wrap=tk.WORD)
        self.text['bg'] = "darkgreen"
        self.text['fg'] = 'white'
        self.text['font'] = "Arial 24"
        self.text.pack(fill=tk.Y, expand=1)
        self.text.bind("<Control-s>", lambda x: self.save())
        self.text.bind("<Control-p>", lambda x: self.render_page())
        self.text.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text.yview)

    def html_convert(self, text_to_render):
        """Convert to my Markup language"""
        html = "<style>body{margin:5%;font-size:2em;}</style>"
        text_to_render = text_to_render.split("\n")
        print(text_to_render)
        for line in text_to_render:
            if line != "":
                if line[0] == "*":
                    line = line.replace("*","")
                    html += f"<h2>{line}</h2>"
                elif line[0] == "^":
                    line = line.replace("^","")
                    html += f"<h3>{line}</h3>"
                elif line[0] == "#":
                    line = line.replace("#","")
                    if line.startswith("http"):
                        html += f"<img src='{line}' /><br>"
                    else:                
                        html += f"<img src='img\\{line}' /><br>"
                elif line[0] == "=" and line[1]== ">":
                    line = line.replace("=>", "")
                    html += f"<span style='color:red'>{line}</span>"
                else:
                    html += f"<p>{line}</p>"
        return html

    def new_window(self, _class):
        self.new = tk.Toplevel(self.root)
        _class(self.new)

    def new_chapter(self, filename):
        self.new.destroy()
        if not filename.endswith(".txt"):
            filename += ".txt"
        #os.chdir(f"{self.folder}")
        with open(f"{self.folder}\\" + filename, "w", encoding="utf-8") as file:
            file.write("")
        self.reload_list_files(filename)

    def reload_list_files(self, filename=""):
        #os.chdir("..")
        self.lstb.delete(0, tk.END)
        self.files = [f for f in glob.glob(f"{self.folder}\\*txt")]
        for file in self.files:
            self.lstb.insert(tk.END, file)
        self.lstb.select_set(self.files.index(f"{self.folder}\\" + filename))

    def reload_list_files_delete(self, filename=""):
        #os.chdir("..")
        self.lstb.delete(0, tk.END)
        self.files = [f for f in glob.glob(f"{self.folder}\\*txt")]
        for file in self.files:
            self.lstb.insert(tk.END, file)

    def rename(self, filename):
        # renames also the html rendered file if it exists
        self.current = self.lstb.get(tk.ACTIVE)[:-4]
        print(self.current)
        filehtml = "{}.html".format(self.current)
        print("=>", filename)
        print("==>", filehtml)
        if os.path.exists(filehtml):
            os.rename(filehtml , f"{self.folder}\\" + filename[:-4] + ".html")
        self.lstb.delete("active")
        os.rename(self.filename, f"{self.folder}\\" + filename)
        self.files = glob.glob(f"{self.folder}\\*.txt")
        self.reload_list_files(filename)

    def save(self):
        with open(self.filename, "w", encoding="utf-8") as file:
            file.write(self.text.get("1.0", tk.END))
        self.label_file_name["text"] += "...saved"

    def save_ebook(self):
        html = ""
        with open("ebook.html", "w", encoding="utf-8") as htmlfile:
            for file in self.files: # this is the name of each file
                with open(file, "r", encoding="utf-8") as singlefile:
                    # ================= SYMBOL => HTML ==============
                    html += self.html_convert(singlefile.read())
            htmlfile.write(html)
        self.label_file_name["text"] += "...Opening Ebook"
        os.startfile("ebook.html")

    def convert_if(self, read):
        if "#html_convert" in read:
            read = read.replace("#html_convert", "<!-- page converted -->")
            read = self.html_convert(read)
        else:
            pass# convert this text in html with *^=>
        return read

    def render_page(self):
        """Save a single page v. 1.4 23/09/2019 at 05:40"""
        self.save()
        html = ""
        self.current = self.lstb.get(tk.ACTIVE)[:-4] # The file selected without .txt
        with open(f"{self.current}.html", "w", encoding="utf-8") as htmlfile:
            # opend the active (selected) item in the listbox
            with open(f"{self.current}.txt", "r", encoding="utf-8") as readfile:
                read = readfile.read() # get the text of the active file
                read = self.convert_if(read) # searches for #html_convert tag
                htmlfile.write(read) # create the new file with the rendered text
        self.create_newlinks()
    
    def create_newlinks(self):
        """This creates a list of links to the web pages created with render page"""
        with open("..\\{}.js".format(self.js_link_to_html), "w") as filejs:
            linka = str(self.lstb.get(tk.ACTIVE))
            linka = linka.split("\\")[1]
            self.current = self.current.split("\\")[1]

            # WE CAN HAVE MORE PYEMP FOR DIFFERENT CLASSES THAT SAVES INTO DIFFERENT self.FOLDERS
            # THEY WILL SHOW UP INTO DIFFERENT DIVS???
            # CREATE THE LINKS TO THE HTML PAGES SAVED AS SINGLE FILES
            listofhtml = []
            for file in os.listdir(f"{self.folder}"):
                if file.endswith(".html"):
                    listofhtml.append(file)
            html1 = ""

            for file in listofhtml:
                # I write the new link from the above list into the js file... then git commit to
                # have it on the web site
                # We will have a DIV THAT GETS THE LINKS FOR THIS PYEM AND RELATIVE self.FOLDER
                # WE NEED A DIV {} and a js file {}.js and a <script src="newlinks4ce"
                # just copy everything in index.html, put in place and copy th js fil
                html1+= """{}.innerHTML += "<a href='Programmi20192020/{}/{}'>{}</a><br>"
                """.format(self.js_link_to_html, self.folder, file, file[:-5])
            filejs.write(html1)

        self.label_file_name["text"] += "...page rendered +"
        os.startfile("{}\\{}.html".format(self.folder, self.current))
        os.system("start ../index.html")

    def show_text_in_editor(self):
        """Shows text of selected file in the editor"""
        self.index = self.lstb.curselection()
        if self.lstb.curselection() != ():
            #self.index = self.lstb.curselection()
            #index = self.lstb.curselection()[0]
            #self.filename = self.files[index] # instead of self.lstb.get(index)
            self.filename = self.lstb.get(self.index)
            with open(self.filename, "r", encoding="utf-8") as file:
                content = file.read()
            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, content)
            self.label_file_name['text'] = self.filename