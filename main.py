# Import the applicable modules
import random
from tkinter import *
import datetime as dt
from difflib import SequenceMatcher

# Define global variables to keep track of start / stop time, speed and the reference
# text to be displayed. We need reference text to display and also to compare for accuracy.
START_TIME = None
STOP_TIME = None
RESULT = None
DISPLAY_TEXT = None


# Create a dictionary of random text
def dict_of_text():
    # To throw a random text for typing, we need to first build the same.
    # using a text file, generate a dictionary of 50 paras.
    # I have created a Text file with content from https://randomwordgenerator.com/paragraph.php
    with open("sample_text_for_display.txt", mode="r", encoding="utf-8") as file:
        para_list = file.read().split("\n")

    # To create a dictionary, we need a list of index.
    index = list(range(1, 51))
    # now that we have a list of text and index, create a dictionary for storage
    text_dict = dict(zip(index, para_list))
    return text_dict

# Create a function that takes two strings and returns the accuracy
# Use the inbuilt Sequence matcher to perform this task.
def word_score(typed_string):
    return SequenceMatcher(None, DISPLAY_TEXT, typed_string).ratio()

def word_speed_calculator():
    # Steps to build a word type speed calculator
    # Generate a Tkinter Window
    window = Tk()
    window.title("Word Speed Calculator")
    # window.minsize(width=500, height=500)
    window.config(padx=10, pady=20)

    # Create a Label text speed calculator
    label = Label(text="This is a word speed calculator. \nWhen you press the return key, "
                       "the program calculates typing speed in WPM", borderwidth=10,
                  font="helvetica 11 bold")
    label.grid(row=1, column=2, columnspan=1)

    # Generate a result window where the user performance will be shown
    def display_refresh():
        global DISPLAY_TEXT
        DISPLAY_TEXT = dict_of_text()[random.randint(1, 50)]
        # print(DISPLAY_TEXT)
        return DISPLAY_TEXT

    display = Label(width=80, text=DISPLAY_TEXT, background="#F3E9DD",
                    wraplength=900, font=("helvetica 14"))
    display.config(borderwidth=30)
    display.grid(row=2, column=2, pady=10)



    # Create a function & start button - which when clicked, should save start time as a global variable
    def start_time():
        global START_TIME
        display_refresh()
        display.config(text=DISPLAY_TEXT)
        START_TIME = dt.datetime.now()
        entry.delete(0, END)  # Delete the text in the entry to start another round

    start = Button(text='Click me to start', command=start_time, borderwidth=2, highlightcolor="red",
                   font="helvetica 11 bold")
    start.grid(row=3, column=2, pady=10)

    # Generate a Text window to type words in
    # This will also record the STOP time upon press of Enter key and return the text
    # Build a speed calculator to return speed in Words Per Min

    def on_change(e):
        global START_TIME, STOP_TIME, RESULT
        if START_TIME == None:
            RESULT = "You did not click the start button"
        else:
            STOP_TIME = dt.datetime.now()
            out = e.widget.get()
            n_words = len(out.split(" "))
            time_taken = (STOP_TIME - START_TIME).seconds
            type_speed = "%.2f" % (n_words * 60 / max(1, (STOP_TIME - START_TIME).seconds))
            # Using 1 sec as min to avoid div by zero error, also formatting to 2 dec places
            RESULT = f"Words Typed: {n_words}\n" \
                     f"Time elapsed: {time_taken} Seconds\n" \
                     f"Speed: {type_speed} WPM\n" \
                     f"Accuracy: {'%.2f' % (word_score(out)*100)} %"

        # print(RESULT)
        # To bring the start time to it's default State
        START_TIME = None

        result.config(text=RESULT)
        return RESULT

    entry = Entry(width=40, borderwidth=1, selectborderwidth=2, font="helvetica 15 bold" )
    entry.bind("<Return>", on_change)
    entry.grid(columnspan=1, row=6, column=2)

    # Generate a result window where the user performance will be shown
    result = Label(width=40, text=RESULT, background="#F3E9DD", font="helvetica 11 bold")
    result.config(borderwidth=20)
    result.grid(row=8, column=2, pady=20)

    # Keep the main loop running till exit is clicked

    def end_loop():
        window.quit()

    end = Button(text='Click here to end', command=end_loop, borderwidth=2,
                 font="helvetica 11 bold")
    end.grid(row=10, column=2, pady=5)
    window.mainloop()

word_speed_calculator()