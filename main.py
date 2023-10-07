from ui import App
from utils import settings
from asyncio import run
from utils.request_utils import check_api_key

if __name__ == "__main__":
    settings.init()
    settings.setAPIKeyValidity(run(check_api_key()))

    app = App()
    app.after(5, app.tab_press_check, app.tab_press_check)  # Starting the tab check
    app.mainloop()                                          # Starting the app


