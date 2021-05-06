import os, sys
import csv
from PIL import Image, ImageDraw
import math
import threading
from kivy.resources import resource_add_path, resource_find
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import StringProperty, NumericProperty, ListProperty, ObjectProperty
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView
from kivy.uix.floatlayout import FloatLayout
import winsound
from tkinter import Tk     
from tkinter.filedialog import askopenfilename





Window.clearcolor = (1, 1, 1, 1)
Window.size = (500, 700)



class InfoScreen(ModalView):
    pass

class MainScreen(Widget):
    file_path = StringProperty()
    total_lines = NumericProperty()
    line_count = NumericProperty(0)
    frequency = 500  # Set Frequency To 500 Hertz
    duration = 50  # Set Duration To 500 ms
    
    
    def OpenFileBrowser(self, file_path):
        winsound.Beep(self.frequency, self.duration)
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        self.file_path = file_path
        self.file_path = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        file = open(self.file_path)
        reader = csv.reader(file)
        self.total_lines = len(list(reader)) - 1
        #print(self.file_path)
    
    def StartProcessingThread(self):
        x = threading.Thread(target=self.ProcessData, args=(self.file_path,self.line_count))
        x.start()

    def ProcessData(self, file_path, line_count):
        canvas_new = Image.new("1",(int(self.MaskResolutionInput()),int(self.MaskResolutionInput())), color=0)
        self.file_path = file_path
        self.line_count = line_count
        self.line_count = 0
        #print(file_path)
        winsound.Beep(self.frequency, self.duration)

        with open(file_path) as f_input:
            header = f_input.readline().rstrip()   # "X,Y"

            for row in f_input:
                x, y, trash = row.rstrip().split(',')         # 10,20\n
                draw = ImageDraw.Draw(canvas_new)
                y_factor = (float(y) / float(self.MaskResolutionInput()))
                y_reprojected = (float(1) - float(y_factor)) * float(self.MaskResolutionInput())
                x_reprojected = (float(x) - float(200000))
                draw.ellipse([(float(x_reprojected), float(y_reprojected)), (float(x_reprojected) + float(self.PaintRadiusInput()), float(y_reprojected) + float(self.PaintRadiusInput()))], fill=(1), outline=(1), width=1)
                self.line_count += 1
                #print("Processing line " +str(self.line_count) +"/" +str(self.total_lines))

        #print("Painting done")
        canvas_new.save("export.bmp", "BMP")
        
        for i in range(0, 6):    
            winsound.Beep(self.frequency, self.duration)    
                    


    def MaskResolutionInput(self, *args):
        mask_resolution = StringProperty()
        mask_resolution = (self.ids.maskres.text)
        return mask_resolution

    def PaintRadiusInput(self, *args):
        paint_radius = StringProperty()
        paint_radius = (self.ids.paintradius.text)
        return paint_radius  
    
    def OpenInfoScreen(self):
        info_screen = InfoScreen(size_hint = (0.75, 0.60), auto_dismiss = True)
        info_screen.open()

    
class ForestFloorPainterApp(App):
    def build(self):
        main_screen = MainScreen()
        
        return main_screen
        

if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    ForestFloorPainterApp().run()