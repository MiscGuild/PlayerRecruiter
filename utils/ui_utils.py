
from customtkinter import CTkButton, CTkFrame, CTkLabel, CTkImage, CTkFont, CENTER, CTkTextbox

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

    def add_item(self, label_text, button_image):
        self.add_item(label_text=label_text, button_image=button_image)


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
