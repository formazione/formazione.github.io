# pyem personal3
# added ctrl + p to render single page
# personal 3b
# corrected bug about renaming files
# 3b - 27/9/19
# - now saves page when you render the single page
# [+] 207 self.filename = self.lstb.get(index)
# commented 206 for a bug linked to not find filename
  # project: 
# personal3c30092019 - bug: do not connect to a link index.html => render page => newlink.js
# look for the ...

import tkinter as tk
import glob
from time import sleep
import os
# update the repository where this file is (the home dir is ..)
from commit import commit

class Ebook:
    def __init__(self, root):
        """Define window for the app"""
        self.root = root
        self.root.geometry("850x400")
        self.root["bg"] = "coral"
        self.menu()
        self.editor()
        self.root.bind("<Control-b>", lambda x: self.save_ebook())
        self.lstb.select_set(0)
        self.filename = self.lstb.get("active")
        self.show_text_in_editor()

    # Widgets on the left ===============|
    def menu(self):
        """Listbox on the left with file names"""

        # The menubar
        self.menubar = tk.Menu(self.root)
        # List of themes
        self.themes = tk.Menu(self.root)
        self.themes.add_command(label="Dark mode", command=self.dark)
        self.themes.add_command(label="Light mode", command=self.light)

        self.letters = tk.Menu(self.root)
        self.letters.add_command(label="Big", command=self.big_letters)
        self.letters.add_command(label="Small", command=self.small_letters)

        self.menubar.add_command(label="+", command = lambda: self.new_window(Win1))
        self.menubar.add_command(label="DELETE", command= lambda: self.delete_file())
        self.menubar.add_command(label="RENAME", command= lambda: self.new_window(Rename))
        self.menubar.add_command(label="Render Page", command = self.save_page)
        self.menubar.add_command(label="Render Ebook", command = self.save_ebook)
        self.menubar.add_command(label="SAVE", command = self.save)       
        self.menubar.add_command(label="HELP", command= lambda: self.new_window(Help))
        self.menubar.add_cascade(label="THEME", menu=self.themes)
        self.menubar.add_cascade(label="LETTERS", menu=self.letters)
        #self.root.config(menu=self.menu_theme)
        self.root.config(menu=self.menubar)




        ####################################




        self.frame1 = tk.Frame(self.root)
        self.frame1["bg"] = "coral"
        self.frame1.pack(side='left', fill=tk.Y)
        self.lstb = tk.Listbox(self.frame1, width=30) # selectmode='multiple', exportselection=0)
        self.lstb['bg'] = "black"
        self.lstb['fg'] = 'gold'
        self.lstb.pack(fill=tk.Y, expand=1)
        self.lstb.bind("<<ListboxSelect>>", lambda x: self.show_text_in_editor())
        self.lstb.bind("<F2>", lambda x: self.new_window(Rename))
        self.files = glob.glob("text_5ce\\*.txt")
        print("self.files", self.files)
        for file in self.files:
            self.lstb.insert(tk.END, file)
        self.lstb.bind("<Control-p>", lambda x: self.save_page())

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
        num = self.lstb.curselection()
        print("delete: " + self.lstb.get(num))
        try:
            os.remove("{}.html".format(self.lstb.get(num)[:-4]))
        except:
            # in case the html file has not been rendered
            pass
        # remove the file selected
        os.remove(self.lstb.get(num))
        # reload the list updated
        self.reload_list_files_delete()

    def editor(self):
        """The text where you can write"""
        self.label_file_name = tk.Label(self.root, text="Editor - choose a file on the left")
        self.label_file_name.pack()
        self.text = tk.Text(self.root, wrap=tk.WORD)
        self.text['bg'] = "darkgreen"
        self.text['fg'] = 'white'
        self.text['font'] = "Arial 24"
        self.text.pack(fill=tk.Y, expand=1)
        self.text.bind("<Control-s>", lambda x: self.save())
        self.text.bind("<Control-p>", lambda x: self.save_page())

    def html_convert(self, text_to_render):
        """Convert to my Markup language"""
        html = ""
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
        #os.chdir("text_5ce")
        with open("text_5ce\\" + filename, "w", encoding="utf-8") as file:
            file.write("")
        self.reload_list_files(filename)

    def reload_list_files(self, filename=""):
        #os.chdir("..")
        self.lstb.delete(0, tk.END)
        self.files = [f for f in glob.glob("text_5ce\\*txt")]
        for file in self.files:
            self.lstb.insert(tk.END, file)
        self.lstb.select_set(self.files.index("text_5ce\\" + filename))

    def reload_list_files_delete(self, filename=""):
        #os.chdir("..")
        self.lstb.delete(0, tk.END)
        self.files = [f for f in glob.glob("text_5ce\\*txt")]
        for file in self.files:
            self.lstb.insert(tk.END, file)

    def rename(self, new_filename):
        num = self.lstb.curselection()
        text_file = self.lstb.get(num)
        file_html = text_file[:-4] + ".html"
        # substitute the old filename with the new filename
        # self.filename (old)
        os.rename(self.filename, "text_5ce\\" + new_filename)
        os.rename(file_html, "text_5ce\\" + new_filename[:-4] + ".html")
        #self.lstb.delete("active")
        
        
        self.files = glob.glob("text_5ce\\*.txt")
        self.reload_list_files(new_filename)


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

    def save_page(self):
        """Save a single page v. 1.4 23/09/2019 at 05:40"""
        self.save()
        html = ""
        self.current = self.lstb.get(tk.ACTIVE)[:-4] # The file selected without .txt
        with open(f"{self.current}.html", "w", encoding="utf-8") as htmlfile:
            # opend the active (selected) item in the listbox
            with open(f"{self.current}.txt", "r", encoding="utf-8") as readfile:
                read = readfile.read() # get the text of the active file
                if "#html_convert" in read:
                    read = read.replace("#html_convert", "<!-- page converted -->")
                    read = self.html_convert(read)
                else:
                    pass# convert this text in html with *^=>with *^=>
                htmlfile.write(read) # create the new file with the rendered text
        self.create_newlinks()
    
    def create_newlinks(self):    
        with open("..\\newlinks_5ce.js", "w") as filejs:
            linka = str(self.lstb.get(tk.ACTIVE))
            linka = linka.split("\\")[1]
            self.current = self.current.split("\\")[1]

            # WE CAN HAVE MORE PYEMP FOR DIFFERENT CLASSES THAT SAVES INTO DIFFERENT FOLDERS
            # THEY WILL SHOW UP INTO DIFFERENT DIVS???
            # CREATE THE LINKS TO THE HTML PAGES SAVED AS SINGLE FILES
            listofhtml = []
            for file in os.listdir("text_5ce"):
                if file.endswith(".html"):
                    listofhtml.append(file)
            html1 = ""

            for file in listofhtml:
                # I write the new link from the above list into the js file... then git commit to
                # have it on the web site
                # We will have a DIV THAT GETS THE LINKS FOR THIS PYEM AND RELATIVE FOLDER
                # WE NEED A DIV newlinks_5ce and a js file newlinks_5ce.js and a <script src="newlinks5ce"
                # just copy everything in index.html, put in place and copy th js fil
                html1+= """newlinks_5ce.innerHTML += "<a href='Programmi20192020/text_5ce/{}'>{}</a><br>"
                """.format(file, file)
            filejs.write(html1)



        self.label_file_name["text"] += "...page rendered +"
        os.startfile("text_5ce\\{}.html".format(self.current))
        os.system("start ../index.html")

    def show_text_in_editor(self):
        """Shows text of selected file in the editor"""
        if not self.lstb.curselection() is ():
            index = self.lstb.curselection()[0]
            #self.filename = self.files[index] # instead of self.lstb.get(index)
            self.filename = self.lstb.get(index)
            with open(self.filename, "r", encoding="utf-8") as file:
                content = file.read()
            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, content)
            self.label_file_name['text'] = self.filename

class Rename():
    def __init__(self, root):
        self.root = root
        self.root.geometry("300x100+200+200")
        self.root.title("Insert new file name")
        self.label_file_name = tk.Label(self.root, text="Enter a name")
        self.label_file_name.pack()
        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(self.root, textvariable=self.entry_var)
        self.entry.pack()
        self.entry.focus()
        self.entry_var.set(app.filename.split("\\")[1])
        self.entry.bind("<Return>", lambda x: app.rename(self.entry.get()))

class Win1():
    def __init__(self, root):
        self.root = root
        self.root.geometry("300x100")
        self.root.title("Insert new file name")
        self.label_file_name = tk.Label(self.root, text="Enter a name")
        self.label_file_name.pack()
        self.entry = tk.Entry(self.root)
        self.entry.pack()
        self.entry.focus()
        self.entry.bind("<Return>", lambda x: app.new_chapter(self.entry.get()))


if __name__ == "__main__":
    #  checks if folders exists & creates them if not
    if "text_5ce" in os.listdir():
        print("text_5ce folder exists")
    else:
        os.mkdir("text_5ce")
        print("text_5ce folder created")
    if "img" in os.listdir():
        print("img folder exists")
    else:
        os.mkdir("img")
        print("text_5ce folder created")
    root = tk.Tk()
    app = Ebook(root)
    app.root.title("Appunti 5ce PyEMP3c")
    root.mainloop()