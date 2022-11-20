import time
import tkinter as tk

import PIL.Image
import psutil
import pystray
import weather
from pystray import MenuItem as Item
from win32api import GetMonitorInfo, MonitorFromPoint


class Main:
    def __init__(self):
        # create a Tk root window and configuration
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root["bg"] = "skyblue"

        # get taskbar height
        monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
        monitor_area = monitor_info.get("Monitor")
        work_area = monitor_info.get("Work")
        taskbar_height = monitor_area[3] - work_area[3]

        # get screen width and height
        ws = self.root.winfo_screenwidth()  # width of the screen
        hs = self.root.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the root window
        w, h = 200, 50  # window size
        x = ws - w
        y = (hs - taskbar_height) - h

        # set the dimensions of the screen and where it is placed
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.root.resizable(False, False)

        # load all images
        self.bilder = {}
        available_images = ["01", "02", "03", "04", "09", "10", "11", "13", "50"]
        for i in available_images:
            self.bilder[f"{i}d"] = tk.PhotoImage(file=f"./bilder/{i}d.png")
            self.bilder[f"{i}n"] = tk.PhotoImage(file=f"./bilder/{i}d.png")
        self.minus_img = tk.PhotoImage(file=r"./bilder/minus.png")
        self.detail_img = tk.PhotoImage(file=r"./bilder/setting.png")
        self.profile_photo = PIL.Image.open(r"./bilder/10d.png")  # image for taskbaricon

        # define frames
        self.image_frame = tk.Frame(self.root, borderwidth=0, bg="skyblue")
        self.image_frame.place(x=0, y=10)
        self.main_frame = tk.Frame(self.root, bg="skyblue", borderwidth=0)
        self.main_frame.place(x=55)
        self.btn_frame = tk.Frame(self.root, bg="skyblue", borderwidth=0)
        self.btn_frame.place(x=158)

        # define btns
        self.min_btn = tk.Button(self.btn_frame, image=self.minus_img, borderwidth=0, command=self.min)  # minimize App
        self.min_btn.pack(side="right", anchor="n")
        self.detail_btn = tk.Button(self.btn_frame, image=self.detail_img, borderwidth=0,
                                    command=Details, bg="skyblue")  # shows the details
        self.detail_btn.pack(side="right", anchor="n")
        # define systemtrayicons
        self.menu = (Item('Wetteranzeige', self.rebuild, default=True), Item('Beenden', self.close))
        self.icon = pystray.Icon("Wetterapp", self.profile_photo, "Wetter", self.menu)

        # define labels
        self.main_label = tk.Label(self.main_frame, font=("Arial", 15, "bold"),
                                   bg="skyblue", borderwidth=0)  # shows the main content
        self.main_label.pack()
        self.image_ico = tk.Label(self.image_frame, bg="skyblue")  # shows the weather image
        self.image_ico.pack()

        # start programm
        self.update_main_label()
        self.root.mainloop()

    def close(self):
        self.root.destroy()
        self.icon.stop()
        quit()

    def update_main_label(self):  # update the main information(temperature and description)
        self.data = weather.getInfo()  # get all weather information
        logo = self.bilder[self.data["iconname"]]  # choose correct icon

        self.main_label["text"] = f"{self.data['Temperatur']}°C\n{self.data['Beschreibung']}"  # update the text
        self.image_ico["image"] = logo  # update the logo
        self.main_label.after(10000, self.update_main_label)

    def min(self):  # hide main window
        self.root.withdraw()
        self.icon = pystray.Icon("Wetterapp", self.profile_photo, "Wetter", self.menu)
        self.icon.run()

    def rebuild(self):  # show main window
        self.icon.stop()
        self.root.deiconify()


# Create the window with the detailed information
class Details:
    def __init__(self):
        # create detail_window and configuration
        self.detail_window = tk.Tk()
        self.detail_window.title("Details")
        self.detail_window.resizable(False, False)
        self.detail_window["bg"] = "skyblue"
        self.detail_window.attributes('-topmost', True)
        self.detail_window.focus_force()

        self.data = weather.getInfo()
        self.add_data = ["°C", "°C", "%", "", "", "", "", "m/s", ""]  # list with additional data for the labels
        self.labels = []  # define new list to save the labels, so that they can be updated later
        self.row = 0
        try:  # Need try-except: if user close window while creating--> self.detail_window not found error
            for key in self.data:
                if key == "iconname":
                    continue  # Contains a non-weather related information
                tk.Label(self.detail_window, text=key + ":",
                         font=("Arial", 20), bg="skyblue").grid(row=self.row)  # place the first row of labels
                temporary_label = tk.Label(self.detail_window, text=str(self.data[key]) + self.add_data[self.row],
                                           font=("Arial", 20, "bold"), bg="skyblue")  # place the second row of labels
                temporary_label.grid(row=self.row, column=1)  # place the second row of labels
                self.labels.append(temporary_label)  # save the second row of labels, so that they can be updated later
                self.detail_window.update()  # update window
                time.sleep(0.5)  # delay for small animation
                self.row += 1
            self.update()
            self.detail_window.mainloop()
        except:
            pass

    def update(self):
        self.data = weather.getInfo()
        counter = 0
        try:  # Need try-except: if user close window while updating--> label not found error
            for key in self.data:
                if key == "iconname":
                    continue  # Contains a non-weather related information
                self.labels[counter]["text"] = str(self.data[key]) + self.add_data[counter]  # update the labels
                counter += 1
        except Exception as e:
            print(e)
        self.detail_window.after(10000, self.update)


if __name__ == '__main__':
    Main()
