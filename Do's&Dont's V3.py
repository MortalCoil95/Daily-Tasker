import random
import tkinter as tk
from PIL import Image, ImageTk
import threading
import time
import pygame

# Function to generate a random list of habits for a day
def generate_daily_habits():
    good_habits = good_habits_entry.get().split(',')
    bad_habits = bad_habits_entry.get().split(',')

    # Shuffle the lists of good_habits and bad_habits
    random.shuffle(good_habits)
    random.shuffle(bad_habits)

    # Get the number of "Do's" and "Don'ts" from user input
    num_do = int(num_do_entry.get())
    num_dont = int(num_dont_entry.get())

    # Ensure unique habits in both "Do's" and "Don'ts"
    do_habits = random.sample(set(good_habits).union(bad_habits), num_do)
    dont_habits = random.sample(set(good_habits).union(bad_habits), num_dont)

    return {"Do's": do_habits, "Don'ts": dont_habits}

# Function to update the UI with the daily habits
def update_ui():
    daily_habits = generate_daily_habits()
    do_text.set("\n".join(daily_habits["Do's"]))
    dont_text.set("\n".join(daily_habits["Don'ts"]))

# Function to set the alarm time and start the update thread
def set_alarm():
    alarm_time = alarm_entry.get()
    try:
        alarm_hour, alarm_minute = map(int, alarm_time.split(':'))
        threading.Thread(target=alarm_thread, args=(alarm_hour, alarm_minute)).start()
    except ValueError:
        alarm_label.config(text="Invalid time format")

# Function for the alarm thread
def alarm_thread(hour, minute):
    while True:
        current_time = time.localtime()
        if current_time.tm_hour == hour and current_time.tm_min == minute:
            update_ui()
            alarm_label.config(text="Habits updated!")
            play_alarm_sound()  # Play the alarm sound
            time.sleep(60)  # Wait for a minute to avoid continuous updates
        time.sleep(1)

# Initialize pygame
pygame.mixer.init()

# Function to play the alarm sound
def play_alarm_sound():
    try:
        pygame.mixer.music.load("C:\\Users\\snehi\\Desktop\\amazing_spiderman_2.wav")  # Load the sound file
        pygame.mixer.music.play()
        # Add a delay to allow the sound to play
        pygame.time.delay(5000)  # Adjust the delay as needed
    except Exception as e:
        print("Error playing alarm sound:", e)

# Function to rotate the image at a slow speed
def rotate_image():
    global angle
    rotation_increment = 0.1  # Adjust the rotation speed as needed
    angle += rotation_increment
    angle %= 360

    # Update the canvas image with the rotated image
    rotated_image = original_image.rotate(angle)
    image = ImageTk.PhotoImage(rotated_image)
    canvas.itemconfig(image_id, image=image)
    canvas.image = image  # To prevent garbage collection

    root.after(100, rotate_image)  # Update every 100 milliseconds

# Load the image (replace 'spiral_galaxy.png' with your image file)
original_image = Image.open("C:\\Users\\snehi\\Desktop\\Pinwheel_galaxy.png")

angle = 0

# Create the main window with a black background
root = tk.Tk()
root.configure(bg='black')
root.title("Daily Habits")

# Create a Frame for the GUI elements with a black background
frame = tk.Frame(root, bg='black')
frame.pack()

# Create and configure UI elements
good_habits_label = tk.Label(frame, text="Good Habits (comma-separated):", bg='black', fg='white')
good_habits_label.pack()
good_habits_entry = tk.Entry(frame, bg='black', fg='white')
good_habits_entry.pack()

bad_habits_label = tk.Label(frame, text="Bad Habits (comma-separated):", bg='black', fg='white')
bad_habits_label.pack()
bad_habits_entry = tk.Entry(frame, bg='black', fg='white')
bad_habits_entry.pack()

do_label = tk.Label(frame, text="Do:", bg='black', fg='green')
do_label.pack()
do_text = tk.StringVar()
do_display = tk.Label(frame, textvariable=do_text, fg="green", bg='black')
do_display.pack()

dont_label = tk.Label(frame, text="Don't:", bg='black', fg='red')
dont_label.pack()
dont_text = tk.StringVar()
dont_display = tk.Label(frame, textvariable=dont_text, fg="red", bg='black')
dont_display.pack()

num_do_label = tk.Label(frame, text="Number of 'Do's:", bg='black', fg='white')
num_do_label.pack()
num_do_entry = tk.Entry(frame, bg='black', fg='white')
num_do_entry.pack()

num_dont_label = tk.Label(frame, text="Number of 'Don'ts:", bg='black', fg='white')
num_dont_label.pack()
num_dont_entry = tk.Entry(frame, bg='black', fg='white')
num_dont_entry.pack()

generate_button = tk.Button(frame, text="Generate Daily Habits", command=update_ui, bg='black', fg='white')
generate_button.pack()

alarm_label = tk.Label(frame, text="Set Alarm (HH:MM):", bg='black', fg='white')
alarm_label.pack()
alarm_entry = tk.Entry(frame, bg='black', fg='white')
alarm_entry.pack()
set_alarm_button = tk.Button(frame, text="Set Alarm", command=set_alarm, bg='black', fg='white')
set_alarm_button.pack()

# Create a Canvas widget for displaying the image with a black background
canvas = tk.Canvas(frame, width=700, height=500, bg="black")
canvas.pack()

# Function to update the image display
def update_image():
    global image_id
    rotated_image = original_image.rotate(angle)

    # Convert the PIL Image to a PhotoImage and display it in the Canvas
    image = ImageTk.PhotoImage(rotated_image)
    image_id = canvas.create_image(400, 300, image=image)
    canvas.image = image  # To prevent garbage collection

# Start updating the image
update_image()

# Start rotating the image
rotate_image()

# Summary on how to use the application
summary_label = tk.Label(root, text="How to Use:\n1. Enter your good and bad habits.\n2. Set the number of 'Do's' and 'Don'ts'.\n3. Set the alarm time and click 'Set Alarm'.\n4. Your daily habits will be updated at the alarm time.\n5. Habits with a green label are 'Do's', and habits with a red label are 'Don'ts'.", bg='black', fg='white')
summary_label.pack(side="right", anchor="nw")

# Start the Tkinter main loop
root.mainloop()
