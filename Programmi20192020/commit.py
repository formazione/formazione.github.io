import os

def commit():
    os.chdir("..")
    print(os.getcwd())
    #os.system("git pull")
    os.system("git add .")
    os.system("git commit -m \"another update\"")
    os.system("git push")
    #os.startfile("..\\commit.bat")
    print("All done")

commit()