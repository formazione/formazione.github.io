# v.1.1.1 - 16/09/2019 @ Giovanni Gatto

import tkinter as tk
import glob
from time import sleep
import os
"""
aggiunto ctrl+s <Control+s> to bind of text
aggiunta label all'editor
"""

class Ebook:
    def __init__(self, root):
        """Define window for the app"""
        self.root = root
        self.root.geometry("850x400")
        self.root["bg"] = "coral"
        self.menu()
        self.editor()

    # Widgets on the left ===============|
    def menu(self):
        """Listbox on the left with file names"""
        self.frame2 = tk.Frame(self.root)
        self.frame2["bg"] = "coral"
        self.frame2.pack(side='left', fill=tk.Y)

        self.button = tk.Button(self.frame2, text="Save", command = self.save)
        self.button.pack()
        self.button_ebook = tk.Button(self.frame2, text="Save ebook", command = self.save_ebook)
        self.button_ebook.pack()

        self.button_plus = tk.Button(self.frame2, text="+", command =lambda: self.new_window(Win1))
        self.button_plus.pack()

        self.button_rename = tk.Button(self.frame2, text = "Rename file",
            command= lambda: self.new_window(Rename))
        self.button_rename.pack()

        self.button_delete = tk.Button(self.frame2, text = "delete file",
            command= lambda: self.delete_file())
        self.button_delete.pack()

        self.lab_help = tk.Label(self.frame2, text="Symbols:\n-------\n* = <h2>\n^ = <h3>\n# = <img...", bg="coral")
        self.lab_help.pack()

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
        print("self.files", self.files)
        for file in self.files:
            self.lstb.insert(tk.END, file)

    def new_window(self, _class):
        self.new = tk.Toplevel(self.root)
        _class(self.new)
    
    def rename(self, filename):
        print(f"Renaming {self.filename}")
        os.rename(self.filename, "text\\" + filename)
        self.files = glob.glob("text\\*.txt")
        self.lstb.delete("active")
        self.lstb.insert(self.files.index("text\\" + filename), "text\\" + filename)

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
        with open(self.filename, "w", encoding="utf-8") as file:
            file.write(self.text.get("1.0", tk.END))
        self.label_file_name["text"] += "...saved"

    def save_ebook(self):
        html = ""
        with open("ebook.html", "w", encoding="utf-8") as htmlfile:
            for file in self.files:
                with open(file, "r", encoding="utf-8") as singlefile:
                    # ================= SYMBOL => HTML ==============
                    for line in singlefile:
                        if line[0] == "*":
                            line = line.replace("*","")
                            html += f"<h2>{line}</h2>"
                        elif line[0] == "^":
                            line = line.replace("^","")
                            html += f"<h3>{line}</h3>"
                        elif line[0] == "#":
                            line = line.replace("#","")
                            html += f"<img src='img\\{line}' width='100%'><br>"
                        else:
                            html += f"<p>{line}</p>"
            htmlfile.write(html)
        os.startfile("ebook.html")


    def show_text_in_editor(self):
        """Shows text of selected file in the editor"""
        if not self.lstb.curselection() is ():
            index = self.lstb.curselection()[0]
            self.filename = self.files[index] # instead of self.lstb.get(index)
            with open(self.filename, "r", encoding="utf-8") as file:
                content = file.read()
            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, content)
            self.label_file_name['text'] = self.filename

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


if __name__ == "__main__":
    # =============================== checks if folders exists &
                                   #= creates them if not
    if "text" in os.listdir():
        print("text folder exists")
    else:
        os.mkdir("text")
        print("text folder created")
    if "img" in os.listdir():
        print("img folder exists")
    else:
        os.mkdir("img")
        print("text folder created")
    root = tk.Tk()
    app = Ebook(root)
    app.root.title("Lezioni")
    root.mainloop()