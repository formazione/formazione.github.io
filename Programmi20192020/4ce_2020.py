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
folder = "4ce"
from ebook import Ebook
# from commit import commit




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


global js_link_to_html
# this file is in the root folder of github.io where index.html is
"""
formazione.github.io
    |
    newlinks_4ce.js            # contains newlinks_4ce.innerHTML += "<a href='Programmi20192020/text_4ce/
                                    Compiti.html'>Compiti.html</a><br>" (made by create_newlinks called by
                                    render_page that renders the page in html in the folder called text)
    index.html                 # This calles the script above and has a div id=newlinks_4ce that loads the links
    programmi20192020
        |
        PyEbook_4CE_3b.py
        imgs
        text
            |
            file.txt
            file.htm

To create a new indipendent PyEbook that creates contents in html that will 
automatically go into index.html
1. Create the PyEbook
2. Change the js_link_to_html with the name of a js file in the root of github.io
3. give a name to the folder (this creates a new folder for the html file)
4. Open index.html, call the js script with the name you choose in js_link_to_html
5. Create a div with the same name of the js file above without the .js
"""

# This folder is in the folder of this script;
# This script is into a folder (programmi20192020) of the root folder of github.io

if __name__ == "__main__":
    #  checks if folders exists & creates them if not
    if f"{folder}" in os.listdir():
        print(f"{folder} folder exists")
    else:
        os.mkdir(f"{folder}")
        print(f"{folder} folder created")
    if "img" in os.listdir():
        print("img folder exists")
    else:
        os.mkdir("img")
        print(f"{folder} folder created")
    root = tk.Tk()
    app = Ebook(root, "4ce", "newlinks_4ce_2020")
    app.root.title("4ce 2020 2021")
    root.mainloop()