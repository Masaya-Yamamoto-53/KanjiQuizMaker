# Widget.py
import customtkinter as ctk

class Widget:
    Event_RegisterStudent = 0
    Event_DeleteStudent   = 1
    Event_SelectStudent   = 2
    Event_SelectWorksheet = 3
    Event_CheckButton     = 4
    Event_ChangeNumberOfProblem = 5
    Event_Generate = 6
    Event_Print = 7
    Event_OnScoringButtonClick = 8
    Event_OnAllCorrectClicked = 9
    Event_OnAllIncorrectClicked = 10
    Event_OnScoringDone = 11

    def __init__(self):
        pass

    def create_frame(self, frame, row, column, columnspan):
        frame = ctk.CTkFrame(frame, corner_radius = 10)
        frame.grid(
              row = row
            , column = column
            , columnspan = columnspan
            , padx = 5, pady = 5
            , sticky = 'nesw'
        )
        return frame

    def create_label(self, frame, row, column, text):
        label = ctk.CTkLabel(
              frame
            , text = text
            , font = ctk.CTkFont(family = 'Yu Gothic UI', size = 18, weight = 'bold')
        )
        label.grid(
              row = row
            , column = column
            , padx = 5, pady = 5
            , sticky = 'nw'
        )

    def create_text_label(self, frame, row, column, text, columnspan=None):
        label = ctk.CTkLabel(
              frame
            , text = text
            , font = ctk.CTkFont(family = 'Yu Gothic UI', size = 14)
        )
        label.grid(
              row = row
            , column = column
            , columnspan = columnspan
            , padx = 5, pady = 5
            , sticky='n'
        )

    def create_entry(
              self
            , frame
            , row
            , column
            , width
            , placeholder_text = None
            , attr_name = None
            , textvariable = None
            , state = 'normal'):

        entry = ctk.CTkEntry(
              frame
            , placeholder_text = placeholder_text
            , textvariable = textvariable
            , width = width
            , height = 36
            , state = state
        )
        entry.grid(
              row = row
            , column = column
            , padx = 5, pady = 5
            , sticky = 'nesw'
        )
        if attr_name:
            setattr(self, attr_name, entry)

        return entry

    def create_button(self, frame, row, column, text, command, attr_name):
        button = ctk.CTkButton(
              frame
            , text = text
            , command = command
            , width = 80
            , height = 36
            , state = ctk.DISABLED
        )
        button.grid(
              row = row
            , column = column
            , padx = 5, pady = 5
            , sticky = 'nesw'
        )
        setattr(self, attr_name, button)
