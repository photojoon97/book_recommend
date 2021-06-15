import tkinter as tk
from tkinter import ttk #for Combobox
from tkinter import Scrollbar, Widget, font
from tkinter.constants import END
from recommend import *

class Application(tk.Frame, Recommend):
    def __init__(self, master=None):
        Recommend.__init__(self,'./extract_data_add_score.csv','stopwords.csv') #부모 클래스 생성자 호출
        super().__init__(master)
        self.master = master
        self.pack()

        self.booknamelist= ['']

        self.create_widgets()

    def book_search_btn(self):
        #2018038092 안준
        input_bookname = self.bookname.get() # 입력창 문자열 가져옴
        #print('\ninput bookname : ',input_bookname)
        titles = Recommend.search_titles(self, input_bookname) #검색결과 가져옴
        #print('\ntitles = [\n',titles['title'])

        #데이터프레임의 인덱스와 제목 정보를 리스트에 함께 저장해야 함

        for title in titles['title']:
            print(title)
            self.booknamelist.append(title)

    def update_combobox(self):
        #2020039043 한지성

        #self.combobox.clear() 
        self.combobox["values"] = self.booknamelist
    
    def recommend(self):
        #2018038092 안준
        book_info = Recommend.select_book(self, self.combobox.get())
        index = book_info.index
        index = index.values.tolist()
        print(type(index), index[0])

        self.result = Recommend.search(self,index[0])
        print(type(self.result))

        for i in self.result.index:
            title = self.result.at[i,'title']
            self.listbox.insert(END, title)
    
    def export_result(self):
        #2018038092 안준
        f = open("추천결과", "w")
        for line in self.result.index:
            title = str(self.result.at[line,'title']) + "\n"
            print(title)
            f.write(title)
        f.close()

        
    def create_widgets(self):
        #2020039043 한지성, 2018038092 안준

        self.label_search = tk.Label(root, text = "도서 검색")
        self.label_search.place(x=80, y=20)

        self.bookname = tk.Entry(root, width=40, font=12)
        self.bookname.place(x=80,y=50)
        
        self.btn1 = tk.Button(root, text="검색", command = self.book_search_btn)
        self.btn1.place(x=480,y=50)

        self.label_select = tk.Label(root, text='도서 선택')
        self.label_select.place(x=80,y=110)
        self.combobox = ttk.Combobox(root, width = 40,values = self.booknamelist,postcommand=self.update_combobox, state='readonly')
        self.combobox.place(x=80, y=140) 
        self.combobox.current(0)

        self.btn2 = tk.Button(root, text="추천", command = self.recommend)
        self.btn2.place(x=480,y=140)

        self.label_result = tk.Label(root, text="추천 결과")
        self.label_result.place(x=80, y = 200)

        self.frame = tk.Frame(root)
        self.frame.pack()
        self.frame.place(x=80,y=230)

        self.listbox = tk.Listbox(self.frame, width=40, height=8, font=12)
        self.listbox.pack(side='left', fill='y')

        self.scroll = tk.Scrollbar(self.frame, orient='vertical')
        self.scroll.config(command=self.listbox.yview)
        self.scroll.pack(side='right', fill='y')

        self.listbox.config(yscrollcommand=self.scroll.set)

        self.label_export = tk.Label(root, text="결과 내보내기")
        self.label_export.place(x = 80, y = 400)

        self.btn_export = tk.Button(root, text="내보내기", command=self.export_result)
        self.btn_export.place(x=80, y = 430)
        

root = tk.Tk()
app = Application(master=root)
app.master.title('BOOK RECOMMEND')
app.master.geometry("600x500")
app.mainloop()