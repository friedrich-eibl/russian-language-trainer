from tkinter import Tk, Canvas, Entry
from PIL import Image, ImageDraw, ImageFont, ImageTk

import csv
import random

dict_file = "test_dict.csv"
eval_file = "eval.csv"

def initialize_tkinter_root():
    """Initialize and configure the tkinter root."""
    root = Tk()
    root.configure(background="white")
    root.minsize(600, 400)
    return root

def create_pillow_image(width, height, base_form, font_large, font_small):
    """Create a Pillow image with initial text and return the image and drawing context."""
    image = Image.new("RGBA", (width, height), "white")
    draw = ImageDraw.Draw(image)
    draw.text((100, 200), f"({base_form})", font=font_small, fill="gray")  # Draw base form
    return image, draw

def update_canvas_text(event=None):
    """Update the text on the canvas based on the input field."""
    input_text = input_field.get()  # Get the current input
    draw.rectangle((0, 0, canvas_width, canvas_height), fill="white")  # Clear the canvas
    draw.text((100, 100), input_text, font=font_large, fill="black")  # Draw the updated text
    draw.text((100, 200), f"({base_form})", font=font_small, fill="gray")  # Draw base form again

    # Convert updated Pillow image to Tkinter PhotoImage
    updated_image = ImageTk.PhotoImage(image)
    canvas.itemconfig(canvas_image, image=updated_image)  # Refresh canvas display
    canvas.image = updated_image  # Prevent garbage collection of the image

def create_canvas(root, width, height, initial_image):
    """Create and return a tkinter canvas with the given dimensions and initial image."""
    canvas = Canvas(root, width=width, height=height, bg="white", highlightthickness=0)
    canvas_image = canvas.create_image(0, 0, anchor="nw", image=initial_image)
    canvas.pack()
    return canvas, canvas_image

def create_input_field(root):
    """Create and configure the input field for capturing user input."""
    entry = Entry(root, font=("DejaVu Sans", 16))
    entry.place(x=-100, y=-100, width=0, height=0) 
    entry.focus()
    entry.bind("<KeyRelease>", update_canvas_text) 
    entry.bind("<Return>", enter_guess)
    return entry


def enter_guess(event=None):
	if not any('0' in word_learned for word_learned in learned):
            print('nothing left to learn !!!')
            return
	while (True):
		word_idx = random.randint(0, len(data) - 1)
		word = data[word_idx]
		form = random.randint(1, 6)

		if learned[word_idx][form] != 1:
		    break
	rounds+=1
	if rounds >= max_rounds:
		return
	input_text = input_field.get()
	print(input_text)
	
	
	if input_text == word[form].strip():
            score+=1
            learned[word_idx][form] = 1
            write_csv(learned, eval_file)
            print('correct\n')
	else:
            print('nope\n')
            #print(word[form]) ## debug


	input_field.delete(0, 'end')

def read_csv(file_path):
	data = []
	with open(file_path, mode='r') as file:
		reader = csv.reader(file)
		for row in reader:
		    data.append(row)
	return data
	
def get_pronouns():
	return ["я", "ты", "он", "мы", "вы", "они"]



data = read_csv(dict_file)
learned = read_csv(eval_file)
rounds = 0
max_rounds = 30
score = 0
pronouns = get_pronouns()

canvas_width, canvas_height = 600, 300
base_form = "играть"
font_path_large = "DejaVuSans-Bold.ttf"
font_path_small = "DejaVuSans.ttf"

font_large = ImageFont.truetype(font_path_large, 40)
font_small = ImageFont.truetype(font_path_small, 32)

root = initialize_tkinter_root()
image, draw = create_pillow_image(canvas_width, canvas_height, base_form, font_large, font_small)
photo = ImageTk.PhotoImage(image)
canvas, canvas_image = create_canvas(root, canvas_width, canvas_height, photo)
input_field = create_input_field(root)
root.mainloop()

