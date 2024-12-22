import tkinter as tk
from PIL import Image, ImageTk
import keyboard


class MovingSplashScreen(tk.Tk):
    def __init__(self, image_path, duration=3000000, minus_x=0):
        super().__init__()

        self.overrideredirect(True)

        self.image = Image.open(image_path)
        self.image = self.image.resize((100, 100), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)

        self.label = tk.Label(self, image=self.photo)
        self.label.pack()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 100) // 2
        y = (screen_height - 100) // 2
        self.geometry(f"100x100+{x}+{y}")

        self.dx = 5
        self.dy = 5
        self.after(duration, self.destroy)
        self.moving = False
        keyboard.add_hotkey("ctrl+alt+d", lambda: self.key_moving())
        self.after(1, self.check_moving)

    def key_moving(self):
        self.moving = not self.moving

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

        self.geometry(f"+{x + self.dx}+{y + self.dy}")

        self.after(10, self.animate)


if __name__ == "__main__":
    app = MovingSplashScreen("img/wallpaper.png")
    app.mainloop()
