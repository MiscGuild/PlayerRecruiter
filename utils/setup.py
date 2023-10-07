import customtkinter
import os
from PIL import Image

def setup(app):
    customtkinter.set_appearance_mode("dark")

    app.all_players = []
    app.selected_frame = None  # Storing which frame the user is currently looking at
    app.selected_text_box_pos = 0  # Helper variable for tab check
    app.switch_text = '\t'  # Helper variable for tab check
    app.fix_offset_character = '               '  # Fixing issue where some labels have an offset

    app.title("Player Recruitment")
    app.geometry(f"{800}x{500}+0+0")
    # set grid layout 1x2
    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(1, weight=1)

    # load images with light and dark mode image
    image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../images")
    app.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "misc.png")), size=(50, 50))
    app.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")),
                                                   size=(20, 20))
    app.home_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "home_light.png")),
                                             size=(20, 20))
    app.meets_requirements = customtkinter.CTkImage(
        dark_image=Image.open(os.path.join(image_path, "white_tick.png")), size=(20, 20))
    app.guildless = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "white_guildless.png")),
                                            size=(20, 15))
    app.dms_enabled = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "chat_light.png")),
                                              size=(20, 20))
    app.need_to_friend = customtkinter.CTkImage(
        dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))
    app.copy_icon = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "white_copy.png")),
                                            size=(20, 20))
    app.settings_icon = customtkinter.CTkImage(
        dark_image=Image.open(os.path.join(image_path, "white_settings_icon.png")),
        size=(20, 20))
    app.question_mark = customtkinter.CTkImage(
        dark_image=Image.open(os.path.join(image_path, "white_question_mark.png")),
        size=(20, 25))
    app.iconbitmap(os.path.join(image_path, "misc.ico"))
