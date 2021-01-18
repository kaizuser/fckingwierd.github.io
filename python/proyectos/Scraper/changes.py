from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from tkinter import *
from PIL import ImageTk, Image
from tkinter import ttk
import time
import wget
import os
import glob

class InstaBot:
    def __init__(self,username,password, variable1):
        self.username = username
        self.password = password
        self.bot = webdriver.Firefox()
        self.variable1 = variable1
    
    def window_label(self):
        hashtags = []
        root = Tk()
        def plus_hashtags():
            hashtag = my_scraper.get()
            if len(hashtag) > 1:
                 hashtags.append(str(hashtag))
                 my_scraper.delete(0, END)
                 ready_button = Button (root, text = "Listo", padx = 15, pady = 2, command = ready_func)
                 ready_button.grid(row = 1, column = 2)
            else:
                my_scraper.insert(0, "Introduce hashtags de 2 caracteres o mas")

        def ready_func():
            root.destroy()
            self.penetrating(hashtags)
        

        my_text = Label(root, text = "Introduce Hashtags")
        my_scraper = Entry(root, width = 25, borderwidth = 5)
        ready_button = Button (root, text = "Listo", padx = 15, pady = 2, state = DISABLED )
        plus_button = Button (root, text = "Agregar", padx = 15, pady = 2,  command = plus_hashtags)

        ready_button.grid(row = 1, column = 2)
        plus_button.grid (row = 1, column = 1)
        my_text.grid(row = 0, column = 0, columnspan = 3)
        my_scraper.grid(row = 1, column = 0)

        root.mainloop()
    
    def penetrating(self, hashtags):
        bot = self.bot
        bot.get("https://www.instagram.com/accounts/login/")
        time.sleep(4)
        bot.find_element_by_class_name("KPnG0").click() 
        bot.find_element_by_id("email").send_keys(self.username)
        bot.find_element_by_id("pass").send_keys(self.password + Keys.RETURN)
        time.sleep(9)
        bot.get("https://www.instagram.com/explore/tags/"+hashtags[0]+"/")
        time.sleep(6)
        self.__get_image(3, hashtags, third_iterator)

    def __get_image(self, amount, hashtags, third_iterator):
        root = Tk()
        root.title("Photos")
        bot = self.bot
        iterator = 0
        second_iterator = 0
        image_url = []

        while second_iterator <= amount:
            bot.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
            second_iterator += 1
    
        image_container = bot.find_elements_by_class_name("FFVAD")

        for iterator in range(len(image_container) - 1):
            variable = image_container[iterator]
            second_variable = variable.get_attribute("src")
            image_url.append(second_variable)
            iterator += 1

        def administration():
            global answer
            answer = idk2.get()
            if len(answer) == 0:
                idk2.insert(0, "Tienes que poner un valor numérico")

            else:
                root.destroy()
                answer = int(answer)
                self.__download_image(image_url, answer)

    
        idk = Label(root, text = f"Hay {len(image_url)} posibles descargas en el hashtag \nCuantas fotos quieres descargar? ")
        idk2 = Entry(root, width = 25, borderwidth = 5)
        idk3 = Button (root, text = "Okey", padx = 15, pady = 2, command = administration )

        idk.grid(row = 0, column = 0)
        idk2.grid(row = 1, column = 0)
        idk3.grid(row = 1, column= 1)

        root.mainloop()


        
        
        
        print("\nDescarga completa")
        print (f"Se han registrado {answer} descargas en el hashtag '{hashtags[third_iterator]}'. ")
        respuesta = str(input("Quieres terminar y/n?: "))

        if respuesta.lower() == "y":
            bot.quit()
            self.tkinter_image()
            return

        third_iterator += 1
        if third_iterator == len(hashtags):
            third_iterator = 0

        bot.get(f"https://www.instagram.com/explore/tags/{hashtags[third_iterator]}/")
        time.sleep(6)
        self.__get_image(3, hashtags, third_iterator)

    def __download_image(self, image_url, quantity):
        for i in range(len(image_url) - 1):
            if i == quantity:
                break
            self.variable1 += 1
            wget.download(image_url[i], f"C://Users//Kaiz//Desktop//Programacion//visualstudio//modulo.py//proyectos//Scraper//Photos//{self.variable1}.png")
    
    def tkinter_image(self):
        root = Tk()
        root.title("Instagram Scraper")
        image_list = []
        i = 0
        row = 0
        column = 0

        main_frame = Frame(root)
        main_frame.pack(fill=BOTH, expand = 1)

        my_canvas = Canvas(main_frame)
        my_canvas.pack(side=LEFT, fill=BOTH, expand = 1)

        my_scrollbar = ttk.Scrollbar(main_frame, orient = VERTICAL, command = my_canvas.yview)
        my_scrollbar.pack(side = RIGHT, fill = Y)
        
        my_canvas.configure(yscrollcommand = my_scrollbar.set)
        my_canvas.bind("<Configure>", lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

        second_frame = Frame(my_canvas)

        my_canvas.create_window((0,0), window=second_frame, anchor="nw")
        
        while True:
            try: 
                i += 1
                thing = ImageTk.PhotoImage(Image.open(f"C://Users//Kaiz//Desktop//Programacion//visualstudio//modulo.py//proyectos//Scraper//Photos//{i}.png"))
                image_list.append(thing)

            except FileNotFoundError:
                break

        for photos in range(len(image_list)):
            my_image = Label(second_frame, image = image_list[photos])
            my_image.grid(row = row, column = column)
            column += 1
            if column > 2:
                column = 0
                row += 1

        root.mainloop()
    

third_iterator = 0
ed = InstaBot ("thiagochiesa2010@hotmail.com","flamigera123", 0)
ed.window_label()