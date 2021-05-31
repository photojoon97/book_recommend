from tkinter import *

root = Tk()
root.title("BOOK RECOMMAND")
root.geometry("720x500")

bookname=Entry(root,width=40,font=12)
bookname.place(x=80,y=30)
btn1 = Button(root, text="검색")
btn1.place(x=550,y=20)

booknamelist=[
    "A",
    "B",
    "C",
    "D"
    ]

variable = StringVar(root)
variable.set(booknamelist[0])

opt = OptionMenu(root, variable, *booknamelist)
opt.config(width=40, font=12)
opt.place(x=80,y=80)

frame=Frame(root)
frame.pack()
frame.place(x=100,y=200)
listbook=Listbox(frame, width = 40 , height = 8 , font=12)
listbook.pack(side="left", fill="y")
scrollbar=Scrollbar(frame, orient="vertical")
scrollbar.config(command=listbook.yview)
scrollbar.pack(side="right", fill="y")
listbook.config(yscrollcommand=scrollbar.set)

for x in range(100):
    listbook.insert(END,str(x))

btn2 = Button(root, text="텍스트 파일로 내보내기")
btn2.place(x=250,y=400)


root.mainloop()