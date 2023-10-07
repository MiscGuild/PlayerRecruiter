import asyncio
from functools import partial

import customtkinter

from utils import settings
from utils.chatGrabber import grabChat
from utils.setup import setup
from utils.ui_utils import CustomNavigationButton, CustomButton, CustomFrame, CustomLabel, CustomEntry, CustomComboBox, \
    select_frame_by_name, ScrollableLabelButtonFrame

from CTkMessagebox import CTkMessagebox




class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        setup(self)

        # create navigation frame
        self.navigation_frame = CustomFrame(self)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = CustomLabel(self.navigation_frame, text="Player Recruitment",
                                                  fSize=25, fWeight="bold", dimensions=(0, 0), pad=(20, 20),
                                                  columnspan=2)

        # create the "All" filter button | Home Button
        self.home_button = CustomNavigationButton(self,
                                                  text="Home",
                                                  image=self.home_image,
                                                  command=self.home_button_event,
                                                  row=1)

        # create the "meets requirements" filter button
        self.meets_requirements_button = CustomNavigationButton(self, text="Meets Requirements",
                                                                image=self.meets_requirements,
                                                                command=self.meets_requirements_button_event,
                                                                row=2)

        # create the "guildless" filter button
        self.guildless_button = CustomNavigationButton(self,
                                                       text="Guildless & Meets Requirements",
                                                       image=self.guildless,
                                                       command=self.guildless_button_event,
                                                       row=3)

        # create the "errors" filter button
        self.errors_button = CustomNavigationButton(self,
                                                    text="Errors",
                                                    image=self.question_mark,
                                                    command=self.errors_button_event,
                                                    row=5)

        # create the "find players" filter button
        self.find_players_button = CustomButton(self.navigation_frame,
                                                text="Find Players",
                                                command=self.find_players_button_event,
                                                row=6,
                                                column=0,
                                                pad=15)

        self.settings_button = CustomButton(self.navigation_frame,
                                            command=self.settings_button_event,
                                            image=self.settings_icon,
                                            dimensions=(20, 20),
                                            fg_color="transparent",
                                            hover_color="#8369ff",
                                            row=6,
                                            column=1,
                                            pad=5)

        # create home frame
        self.home_frame = CustomFrame(self)
        self.home_no_players_label = CustomLabel(self.home_frame,
                                                 text="No players found.\nPlease run /list in a lobby\nand then click Find Players.",
                                                 rel=(0.5, 0.5))

        # create second frame | No players found
        self.meets_requirements_frame = CustomFrame(self)
        self.meets_requirements_frame_no_players_label = CustomLabel(self.meets_requirements_frame,
                                                                     text="No players found.\nPlease run /list in a lobby\nand then click Find Players.",
                                                                     rel=(0.5, 0.5))

        # create third frame | No players found
        self.guildless_frame = CustomFrame(self)
        self.guildless_frame_no_players_label = CustomLabel(self.guildless_frame,
                                                            text="No players found.\nPlease run /list in a lobby\nand then click Find Players.",
                                                            rel=(0.5, 0.5))

        self.errors_frame = CustomFrame(self)

        # create "stat settings" frame
        self.settings_frame = CustomFrame(self)
        self.settings_frame.text_inputs = []

        api_key_text = "HIDDEN" if settings.API_KEY_VALID else ""

        self.api_key = CustomEntry(app=self,
                                   frame=self.settings_frame,
                                   text="API Key:",
                                   eRow=0,
                                   eCol=1,
                                   eHeight=1,
                                   hasLabel=True,
                                   lRow=0,
                                   lCol=0,
                                   defaultVal=api_key_text,
                                   append=True)

        self.path = CustomComboBox(app=self,
                                   frame=self.settings_frame,
                                   text="Path:",
                                   cRow=0,
                                   cCol=3,
                                   values=["Lunar Client", "Badlion Client", "Feather Client", "Vanilla"],
                                   defaultVal=settings.PATH,
                                   hasLabel=True,
                                   lRow=0,
                                   lCol=2,
                                   append=True)

        self.skywars_wins = CustomEntry(app=self,
                                        frame=self.settings_frame,
                                        text="SkyWars Wins:",
                                        eRow=3,
                                        eCol=1,
                                        hasLabel=True,
                                        lRow=3,
                                        lCol=0,
                                        defaultVal=settings.SKYWARS_WINS,
                                        append=True)

        self.skywars_level = CustomEntry(app=self,
                                         frame=self.settings_frame,
                                         text="SkyWars Level:",
                                         eRow=3,
                                         eCol=3,
                                         hasLabel=True,
                                         lRow=3,
                                         lCol=2,
                                         defaultVal=settings.SKYWARS_LEVEL,
                                         append=True)

        self.bedwars_wins = CustomEntry(app=self,
                                        frame=self.settings_frame,
                                        text="BedWars Wins:",
                                        eRow=4,
                                        eCol=1,
                                        hasLabel=True,
                                        lRow=4,
                                        lCol=0,
                                        defaultVal=settings.BEDWARS_WINS,
                                        append=True)

        self.bedwars_stars = CustomEntry(app=self,
                                         frame=self.settings_frame,
                                         text="BedWars Stars:",
                                         eRow=4,
                                         eCol=3,
                                         hasLabel=True,
                                         lRow=4,
                                         lCol=2,
                                         defaultVal=settings.BEDWARS_STARS,
                                         append=True)

        self.bedwars_index = CustomEntry(app=self,
                                         frame=self.settings_frame,
                                         text="BedWars Index:",
                                         eRow=5,
                                         eCol=1,
                                         hasLabel=True,
                                         lRow=5,
                                         lCol=0,
                                         defaultVal=settings.BEDWARS_INDEX,
                                         append=True)

        self.bedwars_fkdr = CustomEntry(app=self,
                                        frame=self.settings_frame,
                                        text="BedWars FKDR:",
                                        eRow=5,
                                        eCol=3,
                                        hasLabel=True,
                                        lRow=5,
                                        lCol=2,
                                        defaultVal=settings.BEDWARS_FKDR,
                                        append=True)

        self.duels_wins = CustomEntry(app=self,
                                      frame=self.settings_frame,
                                      text="Duels Wins:",
                                      eRow=6,
                                      eCol=1,
                                      hasLabel=True,
                                      lRow=6,
                                      lCol=0,
                                      defaultVal=settings.DUELS_WINS,
                                      append=True)

        self.duels_wlr = CustomEntry(app=self,
                                     frame=self.settings_frame,
                                     text="Duels WLR:",
                                     eRow=6,
                                     eCol=3,
                                     hasLabel=True,
                                     lRow=6,
                                     lCol=2,
                                     defaultVal=settings.DUELS_WLR,
                                     append=True)

        self.arcade_wins = CustomEntry(app=self,
                                       frame=self.settings_frame,
                                       text="Arcade Wins:",
                                       eRow=7,
                                       eCol=1,
                                       hasLabel=True,
                                       lRow=7,
                                       lCol=0,
                                       defaultVal=settings.ARCADE_WINS,
                                       append=True)

        self.murder_mystery_wins = CustomEntry(app=self,
                                               frame=self.settings_frame,
                                               text="Murder Mystery Wins:",
                                               eRow=7,
                                               eCol=3,
                                               hasLabel=True,
                                               lRow=7,
                                               lCol=2,
                                               defaultVal=settings.MURDER_MYSTERY_WINS,
                                               append=True)

        self.minimum_gexp = CustomEntry(app=self,
                                        frame=self.settings_frame,
                                        text="Minimum GEXP:",
                                        eRow=8,
                                        eCol=1,
                                        hasLabel=True,
                                        lRow=8,
                                        lCol=0,
                                        defaultVal=settings.MINIMUM_GEXP,
                                        append=True)

        self.maximum_guild_level = CustomEntry(app=self,
                                               frame=self.settings_frame,
                                               text="Max Guild Level:",
                                               eRow=8,
                                               eCol=3,
                                               hasLabel=True,
                                               lRow=8,
                                               lCol=2,
                                               defaultVal=settings.MAXIMUM_GUILD_LEVEL,
                                               append=True)

        self.minimum_network_level = CustomEntry(app=self,
                                                 frame=self.settings_frame,
                                                 text="Network Level:",
                                                 eRow=9,
                                                 eCol=1,
                                                 hasLabel=True,
                                                 lRow=9,
                                                 lCol=0,
                                                 defaultVal=settings.NETWORK_LEVEL,
                                                 append=True)

        self.save_button = CustomButton(self.settings_frame,
                                        text="Save",
                                        command=self.save_settings,
                                        row=10,
                                        column=3,
                                        pad=0,
                                        dimensions=(80, 10))

        # select default frame
        if not settings.API_KEY:
            select_frame_by_name(self, "settings_frame")
        if not settings.API_KEY_VALID:
            CTkMessagebox(title="Error", message="Your API Key is invalid!", icon="warning")
            select_frame_by_name(self, "settings_frame")
        else:
            select_frame_by_name(self, "home")

    def find_players(self):

        all_players, guildless, meets_requirements, errors = asyncio.run(grabChat())
        if all_players is not None and set(all_players) != set(self.all_players):
            self.guildless_frame_no_players_label.destroy()
            self.meets_requirements_frame_no_players_label.destroy()
            self.home_no_players_label.destroy()

            self.home_frame = ScrollableLabelButtonFrame(master=self, fg_color="transparent")
            self.home_frame.set_focus()
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


    def home_button_event(self):
        select_frame_by_name(self, "home")

    def meets_requirements_button_event(self):
        select_frame_by_name(self, "guildless_frame")

    def guildless_button_event(self):
        select_frame_by_name(self, "meets_requirements_frame")

    def errors_button_event(self):
        select_frame_by_name(self, "errors_frame")

    def settings_button_event(self):
        select_frame_by_name(self, "settings_frame")

    def find_players_button_event(self):
        self.find_players()

    # Event that gets called every 5 millisecond, makes user focus on next text box if tab is pressed
    def tab_press_check(self, event):
        if "text_inputs" in dir(self.selected_frame):
            helper = self.tab_fix()
            if helper[0]:
                self.selected_text_box_pos = helper[1] + 1
                if self.selected_text_box_pos >= len(self.selected_frame.text_inputs):
                    self.selected_text_box_pos = 0
                self.selected_frame.text_inputs[self.selected_text_box_pos].focus_set()
        self.after(5, self.tab_press_check, self.tab_press_check)  # Schedules itself to run again

    # Returns True if Tab is in any text boxes, also removes the Tab, if no Tabs then it returns False
    def tab_fix(self):
        for textbox in enumerate(self.selected_frame.text_inputs):
            try:
                contents = textbox[1].get(1.0, "end-1c")
            except:
                contents = textbox[1].get()
            if self.switch_text in contents:
                contents = contents.split(self.switch_text)[0]
                textbox[1].delete(1.0, "end-1c")
                textbox[1].insert(text=contents, index=1.0)
                return (True, textbox[0])
        return (False, textbox[0])

    def save_settings(self):

        API_KEY = (self.api_key.get(1.0, "end-1c"))
        PATH = (self.path.get())
        SKYWARS_WINS = int(self.skywars_wins.get(1.0, "end-1c"))
        SKYWARS_LEVEL = int(self.skywars_level.get(1.0, "end-1c"))
        BEDWARS_STARS = int(self.bedwars_stars.get(1.0, "end-1c"))
        BEDWARS_WINS = int(self.bedwars_wins.get(1.0, "end-1c"))
        BEDWARS_INDEX = int(self.bedwars_index.get(1.0, "end-1c"))
        BEDWARS_FKDR = int(self.bedwars_fkdr.get(1.0, "end-1c"))
        DUELS_WINS = int(self.duels_wins.get(1.0, "end-1c"))
        DUELS_WLR = int(self.duels_wlr.get(1.0, "end-1c"))
        ARCADE_WINS = int(self.arcade_wins.get(1.0, "end-1c"))
        MURDER_MYSTERY_WINS = int(self.murder_mystery_wins.get(1.0, "end-1c"))
        MINIMUM_GEXP = int(self.minimum_gexp.get(1.0, "end-1c"))
        MAXIMUM_GUILD_LEVEL = int(self.maximum_guild_level.get(1.0, "end-1c"))
        NETWORK_LEVEL = int(self.minimum_network_level.get(1.0, "end-1c"))

        settings.updateSettings(API_KEY, PATH, SKYWARS_WINS, SKYWARS_LEVEL, BEDWARS_STARS, BEDWARS_WINS, BEDWARS_INDEX,
                                BEDWARS_FKDR,
                                DUELS_WINS, DUELS_WLR, ARCADE_WINS, MURDER_MYSTERY_WINS, MINIMUM_GEXP,
                                MAXIMUM_GUILD_LEVEL, NETWORK_LEVEL)
        asyncio.run(asyncio.sleep(0.5))

        select_frame_by_name(self, "home")
