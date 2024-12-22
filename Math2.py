import tkinter as tk
from PIL import Image, ImageTk
import keyboard

class MovingSplashScreen(tk.Toplevel):
    def __init__(self, master, image_path, minus_x=0, minus=1):
        super().__init__(master)

        self.overrideredirect(True)

        self.image = Image.open(image_path)
        self.image = self.image.resize((100, 100), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)

        self.label = tk.Label(self, image=self.photo)
        self.label.pack()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 100) // 2 + minus_x
        y = (screen_height - 100) // 2
        self.geometry(f"100x100+{x}+{y}")

        self.dx = 5 * minus
        self.dy = 5 * minus
        self.moving = False
        self.other_window = None

    def set_other_window(self, other_window):
        self.other_window = other_window

    def key_moving(self):
        self.moving = not self.moving
        if self.other_window:
            self.other_window.moving = self.moving

    def check_moving(self):
        if self.moving:
            self.animate()
        else:
            self.after(1, self.check_moving)

    def animate(self):
        x, y = map(int, self.geometry().split('+')[1:])

        if x + 100 >= self.winfo_screenwidth() or x <= 0:
            self.dx = -self.dx
        if y + 100 >= self.winfo_screenheight() or y <= 0:
            self.dy = -self.dy

        if self.other_window:
            other_x, other_y = map(int, self.other_window.geometry().split('+')[1:])
            if (x < other_x + 100 and x + 100 > other_x and
                y < other_y + 100 and y + 100 > other_y):
                self.dx, self.other_window.dx = self.other_window.dx, self.dx
                self.dy, self.other_window.dy = self.other_window.dy, self.dy

        self.geometry(f"+{x + self.dx}+{y + self.dy}")

        self.after(10, self.animate)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    app1 = MovingSplashScreen(root, "img/wallpaper.png", minus_x=-100, minus=2)
    app2 = MovingSplashScreen(root, "img/wallpaper.png", minus_x=100, minus=-2)

    app1.set_other_window(app2)
    app2.set_other_window(app1)

    keyboard.add_hotkey("ctrl+alt+d", lambda: app1.key_moving())

    app1.after(1, app1.check_moving)
    app2.after(1, app2.check_moving)

    root.mainloop()
