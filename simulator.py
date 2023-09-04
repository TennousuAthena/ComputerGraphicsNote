import tkinter as tk
import numpy as np

"""
定义像素点类
"""
class Pixel:
    def __init__(self, R=0, G=0, B=0):
        self.R = R
        self.G = G
        self.B = B

    def getHexCode(self):
        return f'#{self.R:02x}{self.G:02x}{self.B:02x}'

"""
定义虚拟屏幕类
"""
class Screen:
    heightPerPixel = 10
    widthPerPixel = 10
    def __init__(self, windowWidth, windowHeight, fullscreen=False):
        self.windowHeight = windowHeight
        self.windowWidth = windowWidth
        self.screenWidth = windowWidth // self.heightPerPixel
        self.screenHeight = windowHeight // self.widthPerPixel
        self.pixel_matrix = np.empty((self.screenWidth, self.screenHeight), dtype=object)
        self.__window = tk.Tk()
        self.__canvas = tk.Canvas(self.__window, width=windowWidth, height=windowHeight)
        self.__canvas.pack()
        self.__window.title("myScreen")
        if fullscreen:
            self.__window.attributes('-fullscreen', True) 

    def create_pixel_matrix(self):
        for x in range(self.screenWidth):
            for y in range(self.screenHeight):
                self.pixel_matrix[x, y] = Pixel(0, 0, 0)

    def set_pixel_color(self, x, y, color):
        if 0 <= x < self.screenWidth and 0 <= y < self.screenHeight:
            self.pixel_matrix[x, y] = color

    def draw_pixels(self):
        for x in range(self.screenWidth):
            for y in range(self.screenHeight):
                pixel = self.pixel_matrix[x, y]
                color = pixel.getHexCode()
                x1, y1 = x * 10, y * 10
                x2, y2 = x1 + 10, y1 + 10
                self.__canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    def show_result(self):
        self.__window.mainloop()

"""
使用DDA定义直线
"""
class Line:
    k: float
    b: float
    x: np.ndarray
    y: np.ndarray

    def __init__(self, k, b):
        self.k = k
        self.b = b

        self.minLen = 190

        if abs(self.k) < 1:
            self.x = np.arange(self.minLen)
            self.y = np.round(self.x * self.k + self.b).astype(int)
        else:
            self.y = np.arange(self.minLen)
            self.x = np.round((self.y - self.b) / self.k).astype(int)


if __name__ == "__main__":
    myScreen = Screen(1920, 1080, True)
    myScreen.create_pixel_matrix()
    myLine = Line(k=0.1, b=0)


    
    for i in range(myLine.minLen):
        myScreen.set_pixel_color(int(myLine.x[i]), int(myLine.y[i]), Pixel(255, 0, 0))


    
    myScreen.set_pixel_color(0, 0, Pixel(255, 255, 255)) #(0,0位置)
    myScreen.draw_pixels()
    myScreen.show_result()
