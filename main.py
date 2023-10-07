from ui import App
from utils import settings

if __name__ == "__main__":
    settings.init()

    app = App()
    app.after(5, app.tab_press_check, app.tab_press_check)  # Starting the tab check
    app.mainloop()                                          # Starting the app


