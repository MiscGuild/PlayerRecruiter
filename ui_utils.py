import asyncio
import os
from functools import partial

import customtkinter
import pyperclip
from PIL import Image

import settings
from chatGrabber import grabChat


class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.label_list = []
        self.button_list = []

    def add_item(self, label_text, label_image=None, button_image=None, button_type=1):
        label = customtkinter.CTkLabel(self, text=label_text, image=label_image, compound="left", padx=5, anchor="w")
        label.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w")
        if button_type == 1:
            button = customtkinter.CTkButton(self, image=button_image, fg_color="transparent", hover_color="#8369ff",
                                             width=20, text=None, height=20)
            button.grid(row=len(self.button_list), column=1, pady=(0, 10), padx=5)
            button.configure(command=partial(pyperclip.copy, label_text))
            self.button_list.append(button)

        self.label_list.append(label)

    def copy_button_event(self, index):
        print(index)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        customtkinter.set_appearance_mode("dark")

        self.all_players = []

        self.title("Player Recruitment")
        self.geometry(f"{800}x{500}+0+0")
        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "misc.png")), size=(50, 50))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")),
                                                       size=(20, 20))
        self.home_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "home_light.png")),
                                                 size=(20, 20))
        self.meets_requirements = customtkinter.CTkImage(
            dark_image=Image.open(os.path.join(image_path, "white_tick.png")), size=(20, 20))
        self.guildless = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "white_guildless.png")),
                                                size=(20, 15))
        self.dms_enabled = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "chat_light.png")),
                                                  size=(20, 20))
        self.need_to_friend = customtkinter.CTkImage(
            dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))
        self.copy_icon = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "white_copy.png")),
                                                size=(20, 20))
        self.settings_icon = customtkinter.CTkImage(
            dark_image=Image.open(os.path.join(image_path, "white_settings_icon.png")),
            size=(20, 20))
        self.question_mark = customtkinter.CTkImage(
            dark_image=Image.open(os.path.join(image_path, "white_question_mark.png")),
            size=(20, 25))
        self.iconbitmap(os.path.join(image_path, "misc.ico"))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="Player Recruitment",
                                                             justify=customtkinter.CENTER, fg_color="transparent",
                                                             font=customtkinter.CTkFont(size=25, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20, columnspan=2)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                                   text="All",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew", columnspan=2)

        self.meets_requirements_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                                 border_spacing=10, text="Meets Requirements",
                                                                 fg_color="transparent",
                                                                 text_color=("gray10", "gray90"),
                                                                 hover_color=("gray70", "gray30"),
                                                                 image=self.meets_requirements, anchor="w",
                                                                 command=self.meets_requirements_button_event)
        self.meets_requirements_button.grid(row=2, column=0, sticky="ew", columnspan=2)

        self.guildless_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                        border_spacing=10, text="Guildless & Meets Requirements",
                                                        fg_color="transparent", text_color=("gray10", "gray90"),
                                                        hover_color=("gray70", "gray30"),
                                                        image=self.guildless, anchor="w",
                                                        command=self.guildless_button_event)
        self.guildless_button.grid(row=3, column=0, sticky="ew", columnspan=2)

        self.errors_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                     border_spacing=10, text="Errors",
                                                     fg_color="transparent", text_color=("gray10", "gray90"),
                                                     hover_color=("gray70", "gray30"),
                                                     image=self.question_mark, anchor="w",
                                                     command=self.errors_button_event)
        self.errors_button.grid(row=5, column=0, sticky="ew", columnspan=2)

        self.find_players_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=10, border_spacing=5,
                                                           text="Find Players", text_color=("gray10", "gray90"),
                                                           hover_color=("gray70", "gray30"), fg_color="#8369ff",
                                                           command=self.find_players_button_event)
        self.find_players_button.grid(row=6, column=0, padx=15, pady=15, sticky="ew")

        self.settings_button = customtkinter.CTkButton(self.navigation_frame, image=self.settings_icon,
                                                       fg_color="transparent", text=None, width=20,
                                                       height=20, command=self.settings_button_event,
                                                       hover_color="#8369ff")
        self.settings_button.grid(row=6, column=1, padx=5)

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame_no_players_label = customtkinter.CTkLabel(self.home_frame,
                                                                  text="No players found.\nPlease run /list in a lobby\nand then click Find Players.",
                                                                  font=customtkinter.CTkFont(size=30))
        self.home_frame_no_players_label.place(relx=0.5, rely=0.5, anchor="center")

        # create second frame
        self.meets_requirements_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.meets_requirements_frame_no_players_label = customtkinter.CTkLabel(self.meets_requirements_frame,
                                                                                text="No players found.\nPlease run /list in a lobby\nand then click Find Players.",
                                                                                font=customtkinter.CTkFont(size=30))
        self.meets_requirements_frame_no_players_label.place(relx=0.5, rely=0.5, anchor="center")

        # create third frame
        self.guildless_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.guildless_frame_no_players_label = customtkinter.CTkLabel(self.guildless_frame,
                                                                       text="No players found.\nPlease run /list in a lobby\nand then click Find Players.",
                                                                       font=customtkinter.CTkFont(size=30))
        self.guildless_frame_no_players_label.place(relx=0.5, rely=0.5, anchor="center")

        self.errors_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.settings_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.api_key = customtkinter.CTkLabel(self.settings_frame,
                                              text="API Key: ")
        self.api_key.grid(row=0, column=0, padx=10, pady=10)
        self.api_key_entry = customtkinter.CTkTextbox(self.settings_frame, width=300, height=1)
        self.api_key_entry.grid(row=0, column=1, padx=10, pady=10, columnspan=4)
        self.api_key_entry.insert(0.0, settings.API_KEY)

        self.path = customtkinter.CTkLabel(self.settings_frame,
                                           text="Path: ")
        self.path.grid(row=1, column=0, padx=10, pady=10)

        self.path_dropdown = customtkinter.CTkComboBox(self.settings_frame,
                                                       width=300,
                                                       values=["Lunar Client",
                                                               "Badlion Client",
                                                               "Feather Client",
                                                               "Vanilla"])
        self.path_dropdown.grid(row=1, column=1, padx=10, pady=10, columnspan=4)

        self.skywars_wins = customtkinter.CTkLabel(self.settings_frame,
                                                   text="Skywars Wins: ")
        self.skywars_wins.grid(row=3, column=0, padx=10, pady=10)
        self.skywars_wins_entry = customtkinter.CTkTextbox(self.settings_frame, width=80, height=1)
        self.skywars_wins_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        self.skywars_wins_entry.insert(0.0, settings.SKYWARS_WINS)

        self.skywars_level = customtkinter.CTkLabel(self.settings_frame,
                                                    text="Skywars Level: ")
        self.skywars_level.grid(row=3, column=2, padx=10, pady=10, sticky="w")
        self.skywars_level_entry = customtkinter.CTkTextbox(self.settings_frame, width=80, height=1)
        self.skywars_level_entry.grid(row=3, column=3, padx=10, pady=10, sticky="w")
        self.skywars_level_entry.insert(0.0, settings.SKYWARS_LEVEL)

        self.bedwars_wins = customtkinter.CTkLabel(self.settings_frame,
                                                   text="Bedwars Wins: ")
        self.bedwars_wins.grid(row=4, column=0, padx=10, pady=10)
        self.bedwars_wins_entry = customtkinter.CTkTextbox(self.settings_frame, width=80, height=1)
        self.bedwars_wins_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        self.bedwars_wins_entry.insert(0.0, settings.BEDWARS_WINS)

        self.bedwars_index = customtkinter.CTkLabel(self.settings_frame,
                                                    text="Bedwars Index: ")
        self.bedwars_index.grid(row=4, column=2, padx=10, pady=10, sticky="w")
        self.bedwars_index_entry = customtkinter.CTkTextbox(self.settings_frame, width=80, height=1)
        self.bedwars_index_entry.grid(row=4, column=3, padx=10, pady=10, sticky="w")
        self.bedwars_index_entry.insert(0.0, settings.BEDWARS_INDEX)

        self.bedwars_fkdr = customtkinter.CTkLabel(self.settings_frame,
                                                   text="Bedwars FKDR: ")
        self.bedwars_fkdr.grid(row=5, column=0, padx=10, pady=10)
        self.bedwars_fkdr_entry = customtkinter.CTkTextbox(self.settings_frame, width=80, height=1)
        self.bedwars_fkdr_entry.grid(row=5, column=1, padx=10, pady=10, sticky="w")
        self.bedwars_fkdr_entry.insert(0.0, settings.BEDWARS_FKDR)

        self.duels_wins = customtkinter.CTkLabel(self.settings_frame,
                                                 text="Duels Wins: ")
        self.duels_wins.grid(row=5, column=2, padx=10, pady=10, sticky="w")
        self.duels_wins_entry = customtkinter.CTkTextbox(self.settings_frame, width=80, height=1)
        self.duels_wins_entry.grid(row=5, column=3, padx=10, pady=10, sticky="w")
        self.duels_wins_entry.insert(0.0, settings.DUELS_WINS)

        self.duels_wlr = customtkinter.CTkLabel(self.settings_frame,
                                                text="Duels WLR: ")
        self.duels_wlr.grid(row=6, column=0, padx=10, pady=10)
        self.duels_wlr_entry = customtkinter.CTkTextbox(self.settings_frame, width=80, height=1)
        self.duels_wlr_entry.grid(row=6, column=1, padx=10, pady=10, sticky="w")
        self.duels_wlr_entry.insert(0.0, settings.DUELS_WLR)

        self.arcade_wins = customtkinter.CTkLabel(self.settings_frame,
                                                  text="Arcade Wins: ")
        self.arcade_wins.grid(row=6, column=2, padx=10, pady=10, sticky="w")
        self.arcade_wins_entry = customtkinter.CTkTextbox(self.settings_frame, width=80, height=1)
        self.arcade_wins_entry.grid(row=6, column=3, padx=10, pady=10, sticky="w")
        self.arcade_wins_entry.insert(0.0, settings.ARCADE_WINS)

        self.murder_mystery_wins = customtkinter.CTkLabel(self.settings_frame,
                                                          text="Murder Mystery Wins: ")
        self.murder_mystery_wins.grid(row=7, column=0, padx=10, pady=10)
        self.murder_mystery_wins_entry = customtkinter.CTkTextbox(self.settings_frame, width=80, height=1)
        self.murder_mystery_wins_entry.grid(row=7, column=1, padx=10, pady=10, sticky="w")
        self.murder_mystery_wins_entry.insert(0.0, settings.MURDER_MYSTERY_WINS)

        self.minumum_gexp = customtkinter.CTkLabel(self.settings_frame,
                                                   text="Minimum GEXP: ")
        self.minumum_gexp.grid(row=7, column=2, padx=10, pady=10, sticky="w")
        self.minumum_gexp_entry = customtkinter.CTkTextbox(self.settings_frame, width=80, height=1)
        self.minumum_gexp_entry.grid(row=7, column=3, padx=10, pady=10, sticky="w")
        self.minumum_gexp_entry.insert(0.0, settings.MINIMUM_GEXP)

        self.maximum_guild_level = customtkinter.CTkLabel(self.settings_frame,
                                                          text="Max Guild Level: ")
        self.maximum_guild_level.grid(row=8, column=0, padx=10, pady=10, sticky="w")
        self.maximum_guild_level_entry = customtkinter.CTkTextbox(self.settings_frame, width=80, height=1)
        self.maximum_guild_level_entry.grid(row=8, column=1, padx=10, pady=10, sticky="w")
        self.maximum_guild_level_entry.insert(0.0, settings.MAXIMUM_GUILD_LEVEL)

        self.save_button = customtkinter.CTkButton(self.settings_frame, text="Save", command=self.save_settings,
                                                   width=80, height=10, corner_radius=20, fg_color="#8369ff",
                                                   hover_color=("gray70", "gray30"))
        self.save_button.grid(row=9, column=3, padx=0, pady=0, sticky="w")

        # select default frame
        if not settings.API_KEY:
            self.select_frame_by_name("settings_frame")
        else:
            self.select_frame_by_name("home")

    def find_players(self):
        self.meets_requirements_frame_no_players_label.destroy()
        self.guildless_frame_no_players_label.destroy()
        self.home_frame_no_players_label.destroy()

        all_players, guildless, meets_requirements, errors = asyncio.run(grabChat())
        if all_players is not None and set(all_players) != set(self.all_players):
            self.home_frame = ScrollableLabelButtonFrame(master=self, fg_color="transparent")
            for player in all_players:
                if player:
                    self.home_frame.add_item(label_text=player, button_image=self.copy_icon)

            self.meets_requirements_frame = ScrollableLabelButtonFrame(master=self, fg_color="transparent")
            for player in meets_requirements:
                if player:
                    self.meets_requirements_frame.add_item(label_text=player, button_image=self.copy_icon)

            self.guildless_frame = ScrollableLabelButtonFrame(master=self, fg_color="transparent")
            for player in guildless:
                if player:
                    self.guildless_frame.add_item(label_text=player, button_image=self.copy_icon)

            self.errors_frame = ScrollableLabelButtonFrame(master=self, fg_color="transparent")
            for player in errors:
                if player:
                    self.errors_frame.add_item(label_text=player, button_type=1)
        self.all_players = all_players

    def select_frame_by_name(self, name):
        # set button color for selected button
        fg_color = ("gray75", "gray25")
        self.home_button.configure(fg_color=fg_color if name == "home" else "transparent")
        self.meets_requirements_button.configure(fg_color=fg_color if name == "guildless_frame" else "transparent")
        self.guildless_button.configure(fg_color=fg_color if name == "meets_requirements_frame" else "transparent")
        self.errors_button.configure(fg_color=fg_color if name == "errors_frame" else "transparent")
        self.settings_frame.configure(fg_color=fg_color if name == "settings_frame" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "guildless_frame":
            self.meets_requirements_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.meets_requirements_frame.grid_forget()
        if name == "meets_requirements_frame":
            self.guildless_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.guildless_frame.grid_forget()
        if name == "errors_frame":
            self.errors_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.errors_frame.grid_forget()
        if name == "settings_frame":
            self.settings_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.settings_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def meets_requirements_button_event(self):
        self.select_frame_by_name("guildless_frame")

    def guildless_button_event(self):
        self.select_frame_by_name("meets_requirements_frame")

    def errors_button_event(self):
        self.select_frame_by_name("errors_frame")

    def settings_button_event(self):
        self.select_frame_by_name("settings_frame")

    def find_players_button_event(self):
        self.find_players()

    def save_settings(self):
        API_KEY = (self.api_key_entry.get(1.0, "end-1c"))
        PATH = (self.path_dropdown.get())
        SKYWARS_WINS = int(self.skywars_wins_entry.get(1.0, "end-1c"))
        SKYWARS_LEVEL = int(self.skywars_level_entry.get(1.0, "end-1c"))
        BEDWARS_WINS = int(self.bedwars_wins_entry.get(1.0, "end-1c"))
        BEDWARS_INDEX = int(self.bedwars_index_entry.get(1.0, "end-1c"))
        BEDWARS_FKDR = int(self.bedwars_fkdr_entry.get(1.0, "end-1c"))
        DUELS_WINS = int(self.duels_wins_entry.get(1.0, "end-1c"))
        DUELS_WLR = int(self.duels_wlr_entry.get(1.0, "end-1c"))
        ARCADE_WINS = int(self.arcade_wins_entry.get(1.0, "end-1c"))
        MURDER_MYSTERY_WINS = int(self.murder_mystery_wins_entry.get(1.0, "end-1c"))
        MINIMUM_GEXP = int(self.minumum_gexp_entry.get(1.0, "end-1c"))
        MAXIMUM_GUILD_LEVEL = int(self.maximum_guild_level_entry.get(1.0, "end-1c"))

        settings.updateSettings(API_KEY, PATH, SKYWARS_WINS, SKYWARS_LEVEL, BEDWARS_WINS, BEDWARS_INDEX, BEDWARS_FKDR,
                                DUELS_WINS, DUELS_WLR, ARCADE_WINS, MURDER_MYSTERY_WINS, MINIMUM_GEXP,
                                MAXIMUM_GUILD_LEVEL)
        asyncio.run(asyncio.sleep(0.5))
        self.select_frame_by_name("home")
