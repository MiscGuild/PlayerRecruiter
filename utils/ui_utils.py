import pyperclip
from functools import partial
from customtkinter import CTkButton, CTkFrame, CTkLabel, CTkImage, CTkFont, CENTER, CTkTextbox, CTkComboBox, CTkScrollableFrame

# Define the UI element classes here

class CustomButton(CTkButton):
    def __init__(self, frame, command, row, column, pad, dimensions=(None, None), fg_color="#8369ff",hover_color=("gray70", "gray30"), text=None, image=None):
        # Call the parent class's constructor with necessary arguments
        super().__init__(master=frame, text=text, image=image, command=command)
        if any(dimensions):
            self.configure(width=dimensions[0], height=dimensions[1])

        # Configure the button
        self.configure(
            corner_radius=10,
            border_spacing=5,
            text_color=("gray10", "gray90"),
            hover_color=hover_color,
            fg_color=fg_color
        )

        # Place the button in the grid with specified row, column, padx, and pady
        self.grid(row=row, column=column, padx=pad, pady=pad)


class CustomNavigationButton(CTkButton):
    def __init__(self, app, text, image, command, row, column=0, columnspan=2):
        # Call the parent class's constructor with necessary arguments
        super().__init__(master=app.navigation_frame, text=text, image=image, command=command)

        # Configure the button
        self.configure(
            corner_radius=0,
            height=40,
            border_spacing=10,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w"
        )

        # Place the button in the grid
        self.grid(row=row, column=column, sticky="ew", columnspan=columnspan)


class CustomFrame(CTkFrame):
    def __init__(self, frame, corner_radius=0, fg_color="transparent"):
        # Call the parent class's constructor with necessary arguments
        super().__init__(master=frame, corner_radius=corner_radius, fg_color=fg_color)



class ScrollableLabelButtonFrame(CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.label_list = []
        self.button_list = []

    def add_item(self, label_text, label_image=None, button_image=None, button_type=1):
        label = CTkLabel(self, text=label_text, image=label_image, compound="left", padx=5, anchor="w")
        label.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w")
        if button_type == 1:
            button = CTkButton(self, image=button_image, fg_color="transparent", hover_color="#8369ff",
                                             width=20, text=None, height=20)
            button.grid(row=len(self.button_list), column=1, pady=(0, 10), padx=5)
            button.configure(command=partial(pyperclip.copy, label_text))
            self.button_list.append(button)

        self.label_list.append(label)


class CustomLabel(CTkLabel):
    def __init__(self, frame, text, rel=(None, None), dimensions=(None, None), pad=(None, None), columnspan=None, justify=CENTER, anchor="center", fSize = 30, fWeight = "normal"):
        super().__init__(master=frame, text=text, font=CTkFont(size=fSize, weight=fWeight))
        if any(rel):
            self.place(relx=rel[0], rely=rel[1])
        if anchor:
            self.place(anchor=anchor)
        if any(dimensions):
            self.grid(width=dimensions[0], height=dimensions[1])
        if any(pad):
            self.grid(padx=pad[0], pady=pad[1])
        if columnspan:
            self.grid(columnspan=columnspan)

    def destroy(self):
        super().destroy()

class CustomEntry(CTkTextbox):
    def __init__(self, app, frame, text, eRow, eCol, eWidth=80, eHeight=1, ePad=(10,10), eSticky='w', hasLabel = False, lRow=None, lCol=None, lPad=(10,10), lsticky='w', defaultVal=None, append=False):
        super().__init__(master=frame, width=eWidth, height=eHeight)
        self.grid(row=eRow, column=eCol, padx=ePad[0], pady=ePad[1], sticky=eSticky)
        if defaultVal is not None:
            self.insert(0.0, str(defaultVal))
        if hasLabel:
            label = CustomLabel(frame, text, rel=(lRow, lCol), pad=lPad, anchor=lsticky, fSize=12)
            label.grid(row=lRow, column=lCol, padx=lPad[0], pady=lPad[1], sticky=lsticky)
        if append:
            frame.text_inputs.append(self)

class CustomComboBox(CTkComboBox):
    def __init__(self, app, frame, text, cRow, cCol, values,cWidth=150, cHeight=20, cPad=(10,10), cSticky='w', hasLabel = False, lRow=None, lCol=None, lPad=(10,10), lsticky='w', defaultVal=None, append=False):
        super().__init__(master=frame, width=cWidth, height=cHeight, values=values)
        self.grid(row=cRow, column=cCol, padx=cPad[0], pady=cPad[1], sticky=cSticky)
        if defaultVal is not None:
            self.set(defaultVal)
        if hasLabel:
            label = CustomLabel(frame, text, rel=(lRow, lCol), pad=lPad, anchor=lsticky, fSize=12)
            label.grid(row=lRow, column=lCol, padx=lPad[0], pady=lPad[1], sticky=lsticky)
        if append:
            frame.text_inputs.append(self)

def select_frame_by_name(app, name):
    # set button color for selected button
    fg_color = ("gray75", "gray25")
    app.home_button.configure(fg_color=fg_color if name == "home" else "transparent")
    app.meets_requirements_button.configure(fg_color=fg_color if name == "guildless_frame" else "transparent")
    app.guildless_button.configure(fg_color=fg_color if name == "meets_requirements_frame" else "transparent")
    app.errors_button.configure(fg_color=fg_color if name == "errors_frame" else "transparent")
    app.settings_frame.configure(fg_color=fg_color if name == "settings_frame" else "transparent")

    # show selected frame
    if name == "home":
        app.home_frame.grid(row=0, column=1, sticky="nsew")
        app.selected_frame = app.home_frame
    else:
        app.home_frame.grid_forget()
    if name == "guildless_frame":
        app.meets_requirements_frame.grid(row=0, column=1, sticky="nsew")
        app.selected_frame = app.meets_requirements_frame
    else:
        app.meets_requirements_frame.grid_forget()
    if name == "meets_requirements_frame":
        app.guildless_frame.grid(row=0, column=1, sticky="nsew")
        app.selected_frame = app.guildless_frame
    else:
        app.guildless_frame.grid_forget()
    if name == "errors_frame":
        app.errors_frame.grid(row=0, column=1, sticky="nsew")
        app.selected_frame = app.errors_frame
    else:
        app.errors_frame.grid_forget()
    if name == "settings_frame":
        app.settings_frame.grid(row=0, column=1, sticky="nsew")
        app.selected_frame = app.settings_frame
    else:
        app.settings_frame.grid_forget()

