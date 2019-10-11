# pyem_1_4c2 - 25/09/2019 @ Giovanni Gatto
# pyem_1_4c3_user_edition_26_set_2019_compiti
# aggiunto ctrl+p per visualizza la singola pagina html generata
# (si poteva fare col pulsante save page)
# pyem2 - correct bug about renaming files
# pyem2b - added at 196 and commented 195 (because of can't find filename) 
            # self.filename = self.lstb.get(index)
# version 1.5 - added menubar
# version 1.6 - added highlight function to higlight code
# if a line starts with ">"... so if there is >>> ...
# 1.8 dark mode and light mode + - button and mousewheel size
# 1.9 #html_convert; without you can use html with no issues
#     # or copy entire html pages

import tkinter as tk
import glob
from time import sleep
import os
import re
from keyword import kwlist
"""
1.2
Added ctrl+s <Control+s> to bind of text
Added label to editor
1.3
added red symbol for rendering html
1.4
Added way to save render single txt file
1.8: added dark and light theme
added ctrl + - to increase decrease letters and menu too
now it opens the first file at start 
"""

class Ebook:
    def __init__(self, root):
        """Define window for the app"""
        self.root = root
        self.root.geometry("850x400")
        self.root["bg"] = "coral"
        self.menu()


        self.filelist() # add for hide *********************
        self.editor()
        self.letter_size = 24
        self.root.bind("<Control-b>", lambda x: self.save_ebook())
        self.root.bind("<Control-+>", lambda x: self.big_letters())
        self.root.bind("<Control-minus>", lambda x: self.small_letters())
        self.root.bind("<Control-MouseWheel>", lambda x: self.wheel(x))

        self.lstb.select_set(0)
        self.filename = self.lstb.get("active")


        self.index = self.lstb.curselection() # add for hide *********
        self.show_text_in_editor()
        self.root.bind("<Control-l>", lambda x: self.hide())

        # new 1
        self.hidden = 0 # add for hide *****************


    # Widgets on the left ===============|
    def menu(self):
        """Listbox on the left with file names"""

        # commit to git
        # self.button_commit = tk.Button(self.frame2, text="Commit", command = self.commit)
        # self.button_commit.pack()

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

    def filelist(self):  # add for hide *******************
        self.frame1 = tk.Frame(self.root)
        self.frame1["bg"] = "coral"
        self.frame1.pack(side='left', fill=tk.Y)
        self.lstb = tk.Listbox(self.frame1, width=30) # selectmode='multiple', exportselection=0)
        self.lstb['bg'] = "black"
        self.lstb['fg'] = 'gold'
        self.lstb.pack(fill=tk.Y, expand=1)
        self.lstb.bind("<<ListboxSelect>>", lambda x: self.show_text_in_editor())
        self.lstb.bind("<F2>", lambda x: self.new_window(Rename))
        self.files = glob.glob("text\\*.txt")

        for file in self.files:
            self.lstb.insert(tk.END, file)


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


    def new_window(self, _class):
        self.new = tk.Toplevel(self.root)
        _class(self.new)

    def commit(self):
        os.startfile("commit.bat")

    def help(self):
        print("Press <F2> to rename files")

    
    def rename(self, filename):
        self.lstb.delete("active")
        os.rename(self.filename, "text\\" + filename)
        self.files = glob.glob("text\\*.txt")
        self.reload_list_files(filename)
        # self.lstb.insert(self.files.index("text\\" + filename), "text\\" + filename)

    def new_chapter(self, filename):
        self.new.destroy()
        if not filename.endswith(".txt"):
            filename += ".txt"
        #os.chdir("text")
        with open("text\\" + filename, "w", encoding="utf-8") as file:
            file.write("")
        self.reload_list_files(filename)

    def reload_list_files(self, filename=""):
        #os.chdir("..")
        self.lstb.delete(0, tk.END)
        self.files = [f for f in glob.glob("text\\*txt")]
        for file in self.files:
            self.lstb.insert(tk.END, file)
        self.lstb.select_set(self.files.index("text\\" + filename))

    def reload_list_files_delete(self, filename=""):
        #os.chdir("..")
        self.lstb.delete(0, tk.END)
        self.files = [f for f in glob.glob("text\\*txt")]
        for file in self.files:
            self.lstb.insert(tk.END, file)

    def delete_file(self):
        for num in self.lstb.curselection():
            os.remove(self.files[num])
        self.reload_list_files_delete()

    def save(self):
        if self.text.get("1.0", tk.END) != "":
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
        current = self.lstb.get(tk.ACTIVE)[:-4] # The file selected without .txt
        with open(f"{current}.html", "w", encoding="utf-8") as htmlfile:
            # opend the active (selected) item in the listbox
            with open(f"{current}.txt", "r", encoding="utf-8") as readfile:
                read = readfile.read() # get the text of the active file

                if "#html_convert" in read:
                    read = read.replace("#html_convert", "<!-- page converted -->")
                    read = self.html_convert(read)
                else:
                    pass# convert this text in html with *^=>
                htmlfile.write(read) # create the new file with the rendered text
        self.label_file_name["text"] += "...page rendered"
        os.startfile(f"{current}.html")
        # os.system("start ../index.html")

    def highlight(self, code):
        "pass a string and it will be highlighted"
        # keywords to be colored in orange
        kw = kwlist
        for k in kw:
            k = k + " "
            code = code.replace(k, "<b style='color:orange'>" + k + "</b>")
        code = code.replace("\n","<br>")
        #print(code)
        # The 'indentation'
        code = code.replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")
        # functions to be clored in blue
        _def= re.findall("\w+\(", code)
        for w in _def:
            code = code.replace(w, "<b style='color:blue'>" + w[:-1] + "</b>(")
        return code

    def html_convert(self, text_to_render):
        """Convert to my Markup language"""
        html = ""
        text_to_render = text_to_render.split("\n")

        for line in text_to_render:
            if line != "":
                if line[0] == ">":
                    line = self.highlight(line) + "<br>"
                    html += line
                elif line[0] == "*":
                    line = line.replace("*","")
                    html += f"<h2>{line}</h2>"
                elif line[0] == "^":
                    line = line.replace("^","")
                    html += f"<h3>{line}</h3>"
                elif line[0] == "§":
                    line = line.replace("§","")
                    if line.startswith("http"):
                        html += f"<img src='{line}' width='100%'><br>"
                    else:                
                        html += f"<img src='img\\{line}' width='100%'><br>"
                elif line[0] == "=" and line[1]== ">":
                    line = line.replace("=>", "")
                    html += f"<span style='color:red'>{line}</span>"
                else:
                    html += f"<p>{line}</p>"

        #html = self.highlight(html)
        return html

    def show_text_in_editor(self):
        """Shows text of selected file in the editor"""
        self.index = self.lstb.curselection() # add for hide ******
        if not self.lstb.curselection() is ():
            #index = self.lstb.curselection()[0]
            #self.filename = self.files[index] # instead of self.lstb.get(index)
            self.filename = self.lstb.get(self.index) # hide: change to self *** 
            with open(self.filename, "r", encoding="utf-8") as file:
                content = file.read()
            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, content)
            self.label_file_name['text'] = self.filename

    def editor(self):
        """The text where you can write"""

        # hide: add frame2 and to label and text
        self.frame2 = tk.Frame(self.root) # hide
        self.frame2["bg"] = "coral" # hide
        self.frame2.pack(side='left', fill=tk.Y) # hide

        self.label_file_name = tk.Label(self.frame2, text="Editor - choose a file on the left")
        self.label_file_name.pack()
        self.text = tk.Text(self.frame2, wrap=tk.WORD)
        self.text['bg'] = "darkgreen"
        self.text['fg'] = 'white'
        self.text['font'] = "Arial 24"
        self.text.pack(fill=tk.Y, expand=1)
        self.text.bind("<Control-s>", lambda x: self.save())
        self.text.bind("<Control-p>", lambda x: self.save_page())


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

class Help():
    def __init__(self, root):
        self.root = root
        self.root.title("Shortcuts")
        self.label_file_name = tk.Label(self.root, text="Shortcuts")
        self.label_file_name.pack()
        istruzioni = """* H2
^ H3
§ <img src=...
=> red
<F2> rename
> To highlight code

HTML
If you want to write html code
or javascript do not write
#html_convert in the page

"""
        self.text = tk.Text(self.root, width=30, height=6)
        self.text.insert("1.0", istruzioni)
        self.text.pack(fill=tk.BOTH, expand=1)

if __name__ == "__main__":
    # =============================== checks if folders exists &
                                   #= creates them if not
    if "text" in os.listdir():
        pass
    else:
        os.mkdir("text")

    if "img" in os.listdir():
        pass
    else:
        os.mkdir("img")

    root = tk.Tk()
    app = Ebook(root)
    app.root.title("PyBook 1.9b")
    root.mainloop()