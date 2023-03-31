import tkinter as tk
import pdfkit
import os
import codecs


path_wkhtmltopdf = 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
# pdfkit.from_url("http://google.com", "out.pdf", configuration=config)

def check_text_file():
    if "notebook_1.html" in os.listdir():
        with codecs.open("E:\\formazione.github.io\\notebook_1.html", encoding="utf-8") as file:
            cont = file.read()
    else:
        cont = ""
    for line in cont:
        txbx.insert(tk.END, line)


def write_html(event=""):
    global content
    
    # content = txbx.get("0.0", tk.END)
    # if test:
    #     print(content)
    html_file = "E:\\formazione.github.io\\notebook_1.html"
    with open(html_file, "w", encoding="utf-8") as file:
        file.write(content)
    return html_file, content



def pdf(event=""):
    global content

    filename = "E:\\formazione.github.io\\notebook_1.pdf"
    content = txbx.get("0.0", tk.END)
    # write_html(content)
    content = content.replace("\n", "<br>")
    html_file = write_html(content)
    # print(content)
    pdfkit.from_file(html_file, filename)
    print("pdf created")
    os.startfile("notebook_1.pdf")

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