from tkinter import *
from tkinter import ttk
import pygame # for music later
#----------CONSTANTS--------#
MAROON = '#B22222'
ORANGE = '#FF6F3C'
GREEN = '#347433'
YELLOW = '#FFC107'
WHITE = "white"
FONT_NAME = "Comic Sans MS"
currently_typing = None # Use this to check if user is typing later
timer_id = None # Timer to cancel later when they aren't typing
initial_length = 0 # Length to start
#-------USEFUL FUNCTIONS-------#
# Clear home screen
def clear_home():
    frame.grid_forget()
    title_lbl.grid_forget()
    subtitle_lbl.grid_forget()
    canvas.grid_forget()
    start_btn.grid_forget()
    about_btn.grid_forget()
    canvas2.grid_forget()

# Delete widget
def delete_widget(widget):
    widget.destroy()

# Clear current UI (takes multiple args for multiple widgets)
def clear_current_ui(*args):
    for arg in args:
        delete_widget(arg)

# Return home screen
def return_home():
    global currently_typing
    currently_typing = None # Resets currently typing variable to prevent future errors
    frame.grid(row=3, column=1, columnspan=2)
    title_lbl.grid(row=0, column=1)
    subtitle_lbl.grid(row=1, column=1)
    canvas.grid(row=2, column=1)
    start_btn.grid(row=3, column=1, padx=10)
    about_btn.grid(row=3, column=2, padx=10)
    canvas2.grid(row=4, column=1)

# Entry check
def entry_check(entry, label):
    global currently_typing, timer_id, initial_length

    le_text = entry.get()

    if len(le_text) > initial_length:
        currently_typing = True

        if timer_id: # check if timer id exists to be safe
            screen.after_cancel(timer_id) # Cancel the timer

        text_config_func(label, le_text) # Call before changing initial length, or else it will never run!

        # Start new 3 sec timer
        timer_id = screen.after(3000, reset_text, entry, label)

        initial_length = len(le_text)
    else:
        currently_typing = False

    screen.after(30, entry_check, entry, label) # Every 30 ms, 1 ms is a little too fast for tkinter lol

# Text config and stuff
def text_config_func(label, text):
    global currently_typing
    if currently_typing:
        length_check(label, text)

# Adjust label by length (add new line)
def length_check(le_label, texty):
    chunks = [] # text chunks by the 20s
    for num in range(0, len(texty), 30): # Start at zero, step by 30, until you hit the end of string or greater (len)
        chunk = texty[num:num+30] # the loop basically only goes for as many 30 char intervals there are
        chunks.append(chunk) # If text is less than 30 char long, when you step it'll be greater, and therefore it will only run once. (range = 0)
    joined_text = "\n".join(chunks)    # 0 + 30 is the full text. This means there will be no joining, because there will only be one string in the list!
    le_label.config(text=joined_text)
    # P.S, 'chunk' if less than 30 is the text string from beginning to end. A string of
    # 12 characters from index 0 to index 30 has to stop at the end lol, can't have imaginary letters

# Helper function to reset label text
def reset_text(entry, label):
    entry.delete(0, END)
    label.config(text="")
    global currently_typing, initial_length # Reset variables along with text and entry
    initial_length = 0
    currently_typing = False
#--------BUTTON COMMANDS/FUNCTIONS-----------#
def about_page():
    clear_home()
    about_pg_title = Label(text="About page!", fg=YELLOW, bg=MAROON,
                           font=(FONT_NAME, 32, "bold"))
    about_pg_title.grid(row=0, column=1)
    about_desc = Label(text="Howdy! This app was made by Elisha"
                            "N. (HolaSenorPython on GitHub).\nThis app is the"
                            " assignment for day 90 of the course, and is meant to\n"
                            "aid writers with writers block by DELETING their writing"
                            " if they\ndon't keep typing. Crazy huh? Anyway I hope you enjoy!"
                            " Sorry\nthe colors are wonky, It's clear i've made too many "
                            "tkinter apps...", bg=MAROON, fg=YELLOW, font=(FONT_NAME, 14))
    about_desc.grid(row=1, column=1, pady=10)
    about_canvas = Canvas(width=256, height=256, highlightthickness=0, bg=MAROON)
    havertz_path = 'images/havertz.png'
    about_canvas.havertz_img = PhotoImage(file=havertz_path)
    about_canvas.create_image(128, 128, image=about_canvas.havertz_img)
    about_canvas.grid(row=2, column=1, pady=10)
    done_reading = Button(text="I'm done reading!", bg=GREEN, fg=WHITE,
                          font=(FONT_NAME, 20, "bold"), relief="flat", highlightthickness=0,
                          command=lambda: [clear_current_ui(about_pg_title, about_desc,
                                                            about_canvas, done_reading), return_home()])
    done_reading.grid(row=3, column=1)

def get_started():
    global currently_typing, timer_id
    clear_home()

    frame2 = ttk.Frame(screen, padding=10)
    frame2.grid(row=1, column=1, rowspan=2)

    start_typing_lbl = Label(text="Start typing in the entry below,\n"
                                  "and watch your text come to life!\n"
                                  "(for 3 seconds)", bg=MAROON, fg=YELLOW, font=(FONT_NAME, 26, "bold"))
    start_typing_lbl.grid(row=0, column=1)

    user_entry_area = Entry(frame2, width=50)
    user_entry_area.grid(row=1, column=1)

    return_home_btn = Button(frame2, text="Return Home!", bg=GREEN, fg=WHITE, font=(FONT_NAME, 16, "bold"),
                             relief="flat", highlightthickness=0, command=lambda: [clear_current_ui(frame2, start_typing_lbl,
                                                                                                    user_entry_area, return_home_btn, users_text_lbl),
                                                                                   return_home()])
    return_home_btn.grid(row=2, column=1, pady=10)

    users_text_lbl = Label(text="", bg=MAROON, fg=YELLOW, font=(FONT_NAME, 14))
    users_text_lbl.grid(row=3, column=1, columnspan=2)

    # Do the dynamic typing logic
    screen.after(1, entry_check, user_entry_area, users_text_lbl)
#-------HOME SCREEN AND UI SETUP-------#
screen = Tk()
screen.title("Disappearing Text App")
screen.minsize(width=620, height=700)
screen.config(bg=MAROON, padx=50, pady=50)

# Make a frame for the two buttons
style = ttk.Style()
style.configure("TFrame", background=MAROON)
frame = ttk.Frame(screen, padding=10)
frame.grid(row=3, column=1, columnspan=2)

# Make title text and images and stuff
title_lbl = Label(text="Disappearing Text App!", fg=YELLOW, bg=MAROON,
                  font=(FONT_NAME, 32, "bold"))
title_lbl.grid(row=0, column=1)

subtitle_lbl = Label(text="This app is meant for you to keep"
                          " your writing\na secret. Or to defeat"
                          " writers block.", bg=MAROON, fg=YELLOW,
                     font=(FONT_NAME, 18))
subtitle_lbl.grid(row=1, column=1)

canvas = Canvas(width=128, height=128, bg=MAROON, highlightthickness=0)
spongebob_img_path = 'images/spongebob_writing.png'
sponge_img = PhotoImage(file=spongebob_img_path)
canvas.create_image(64, 64, image=sponge_img)
canvas.grid(row=2, column=1)

start_btn = Button(frame, text="Get Started!", bg=GREEN, fg=WHITE, relief="flat",
                   highlightthickness=0, font=(FONT_NAME, 16, "bold"), command=get_started)
start_btn.grid(row=3, column=1, padx=10)

about_btn = Button(frame, text="About page!", bg=GREEN, fg=WHITE, relief="flat",
                   highlightthickness=0, font=(FONT_NAME, 16, "bold"), command=about_page)
about_btn.grid(row=3, column=2, padx=10)

# Another canvas for ronny pic 👄
canvas2 = Canvas(width=256, height=256, bg=MAROON, highlightthickness=0)
ronny_path = 'images/ronaldo_2008.png'
ronny_img = PhotoImage(file=ronny_path)
canvas2.create_image(128,128, image=ronny_img)
canvas2.grid(row=4, column=1)

# Set up music
pygame.mixer.init()
song_path = 'audio/pixel_peeker_polka.mp3'
pygame.mixer.music.load(song_path)
pygame.mixer.music.play(-1) # Loop the music infinitely (-1 times lol)
pygame.mixer.music.set_volume(0.8) # Remove 20% of volume


screen.mainloop() # Keep screen open unless closed