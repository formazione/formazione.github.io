import tkinter as tk
import tkinter.ttk as ttk

class App(tk.Tk):
   def __init__(self):
      tk.Tk.__init__(self)
      self.geometry('200x200')
      self.title('Page test')
      
      self.frame1 = ttk.Frame(self)
      self.frame1.pack(side="top", fill="both", expand=True)
      self.frame1_bot = ttk.Frame(self.frame1)
      self.frame1_bot.pack(side="bottom", fill="x")
      self.next_btn = ttk.Button(self.frame1_bot, text="Next", command=self.frame2_visible)
      self.next_btn.pack(side="right")
      
      self.frame2 = ttk.Frame(self)
      self.frame2_bot = ttk.Frame(self.frame2)
      self.frame2_bot.pack(side="bottom", fill="x")
      self.back_btn = ttk.Button(self.frame2_bot, text="Back", command=self.frame1_visible)
      self.back_btn.pack(side="left")
            
   def frame2_visible(self):
      self.frame1.pack_forget()
      self.frame2.pack(side="top", fill="both", expand=True)
      
   def frame1_visible(self):
      self.frame2.pack_forget()
      self.frame1.pack(side="top", fill="both", expand=True)
      
App().mainloop()