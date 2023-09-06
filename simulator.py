import tkinter as tk
import numpy as np

def get_hex_code(pixel: np.ndarray):
    return f'#{pixel[0]:02x}{pixel[1]:02x}{pixel[2]:02x}'

# 基础静态图形基类
class StaticGraphic:
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.dataArray = np.zeros((self.X, self.Y, 3), dtype=np.uint8)
    def draw(self, screen):
        for x in range(self.X):
            for y in range(self.Y):
                pixel = self.dataArray[x, y]
                screen.set_pixel_color(x, y, pixel)

# 像素类
class Pixel:
    def __init__(self, R=0, G=0, B=0):
        self.R = R
        self.G = G
        self.B = B
        self.hex = f'#{self.R:02x}{self.G:02x}{self.B:02x}'

# 虚拟屏幕类
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
        self.recreate_pixel_matrix()

    def recreate_pixel_matrix(self):
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
                color = get_hex_code(pixel)
                x1, y1 = x * 10, y * 10
                x2, y2 = x1 + 10, y1 + 10
                self.__canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    def mark_origin_point(self):
        self.set_pixel_color(0, 0, Pixel(255, 255, 255))

    def show(self):
        self.draw_pixels()
        self.__window.mainloop()

    def draw_static_content(self, static_data):
        if static_data is not None and isinstance(static_data, StaticGraphic):
            static_data.draw(self)
        else:
            self.recreate_pixel_matrix()
            raise "Wrong datatype"

    def draw_dynamic_content(self, dynamic_data, refresh_rate=10):
        num_frames, x_dim, y_dim = dynamic_data.shape

        for frame in range(num_frames):
            for x in range(x_dim):
                for y in range(y_dim):
                    color = dynamic_data[frame, x, y]
                    self.set_pixel_color(x, y, color)

            self.draw_pixels()
            self.__window.update()  # 更新窗口以显示新帧
            self.__window.after(refresh_rate)  # 延迟一段时间以控制帧率

# 使用DDA定义直线
class Line(StaticGraphic):
    k: float
    b: float
    color: Pixel

    def __init__(self, k: float, b: float, color=Pixel(255, 0, 0)):
        super().__init__(200, 200)  # 定义一个200x200的静态图形
        self.k = k
        self.b = b
        self.color = color

        if abs(self.k) < 1:
            self.x = np.arange(self.X)
            self.y = np.round(self.x * self.k + self.b).astype(int)
        else:
            self.y = np.arange(self.Y)
            self.x = np.round((self.y - self.b) / self.k).astype(int)

        # 设置线的颜色
        for i in range(len(self.x)):
            self.dataArray[self.x[i], self.y[i]] = np.array([self.color.R, self.color.G, self.color.B], dtype=np.uint8)


if __name__ == "__main__":
    myScreen = Screen(1920, 1080, True)

    myLine = Line(k=0.5, b=10)  # 创建一条直线
    myScreen.draw_static_content(myLine)  # 绘制直线数据到屏幕
    myScreen.show()