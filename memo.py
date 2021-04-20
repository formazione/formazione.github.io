import tkinter as tk
import pdfkit
import os
import codecs


def check_text_file():
    if "memo.html" in os.listdir():
        with codecs.open("memo.html", encoding="utf-8") as file:
            cont = file.read()
    else:
        cont = ""
    for line in cont:
        txbx.insert(tk.END, line)


def write_html(event=""):
    # content = txbx.get("0.0", tk.END)
    # if test:
    #     print(content)
    html_file = "memo.html"
    with open(html_file, "w", encoding="utf-8") as file:
        file.write(content)
    return html_file, content



def pdf(event=""):
    filename = "memo.pdf"
    content = txbx.get("0.0", tk.END)
    # write_html(content)
    content = content.replace("\n", "<br>")
    html_file = write_html(content)
    # print(content)
    pdfkit.from_url(html_file, filename)
    print("pdf created")
    os.startfile("memo.pdf")

if __name__ == "__main__":
    test = 1
else:
    test = 0

root = tk.Tk()
# WIDGETS: text box => Text class of tkinter (tk)

# MENU
menubar = tk.Menu(root)
menubar.add_command(label="Create pdf", command=pdf)
root.config(menu=menubar)

# LABEL
label = tk.Label(root, text="CTRL + b to make a page (use also html)")
label.pack()

# TEXT BOX
txbx = tk.Text(root, height=20, insertbackground="white")
txbx['font'] = "Arial 14"
txbx['bg'] = "black"
txbx['fg'] = "white"
txbx['borderwidth'] = 2
txbx.pack(fill=tk.BOTH, expand=1)
txbx.focus()
# Command that creates the pdf from the text
txbx.bind("<Control-b>", pdf)
txbx.bind("<Control-s>", write_html)
check_text_file()

root.mainloop()