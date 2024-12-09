import csv
import random
from tkinter import Tk, Canvas, Entry, Button
from PIL import Image, ImageDraw, ImageFont, ImageTk

from time import sleep

class GrammarTrainerApp:
    def __init__(self, root):
        self.root = root
        self.root.configure(background="white")
        self.root.minsize(600, 400)
        
        self.font_path_large = "DejaVuSans-Bold.ttf"
        self.font_path_small = "DejaVuSans.ttf"
        self.font_large = ImageFont.truetype(self.font_path_large, 40)
        self.font_small = ImageFont.truetype(self.font_path_small, 32)
        self.font_score = ImageFont.truetype(self.font_path_small, 24)
        
        self.canvas_width = 600
        self.canvas_height = 300
        
        self.show_start_screen()

    def show_start_screen(self):
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create and configure canvas for start screen
        self.image = Image.new("RGBA", (self.canvas_width, self.canvas_height), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.photo = ImageTk.PhotoImage(self.image)
        
        self.canvas = Canvas(self.root, width=self.canvas_width, height=self.canvas_height, 
                           bg="white", highlightthickness=0)
        self.canvas_image = self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
        self.canvas.pack(pady=20)

        # Draw title
        text = "Choose Training Mode"
        text_bbox = self.draw.textbbox((0, 0), text, font=self.font_large)
        text_width = text_bbox[2] - text_bbox[0]
        x_position = (self.canvas_width - text_width) // 2
        self.draw.text((x_position, 50), text, font=self.font_large, fill="black")

        # Update canvas
        updated_image = ImageTk.PhotoImage(self.image)
        self.canvas.itemconfig(self.canvas_image, image=updated_image)
        self.canvas.image = updated_image

        # Create mode selection buttons
        conjugation_btn = Button(
            self.root,
            text="Conjugation Practice",
            font=("DejaVu Sans", 16),
            command=lambda: self.start_training("conjugation")
        )
        conjugation_btn.pack(pady=10)

        declension_btn = Button(
            self.root,
            text="Declension Practice",
            font=("DejaVu Sans", 16),
            command=lambda: self.start_training("declension")
        )
        declension_btn.pack(pady=10)

    def start_training(self, mode):
        # Set the appropriate files based on mode
        if mode == "conjugation":
            self.dict_file = "test_dict.csv"
            self.eval_file = "eval.csv"
            self.pronouns = self.get_pronouns()
        else:  # declension
            self.dict_file = "decl_dict.csv"
            self.eval_file = "decl_eval.csv"
            self.pronouns = self.get_case_words()
        
        self.setup_new_session()

    def setup_new_session(self):
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        self.data = self.read_csv(self.dict_file)
        self.learned = self.read_csv(self.eval_file)
        
        self.current_word = None
        self.current_form = None
        self.current_word_idx = None
        self.rounds = 0
        self.max_rounds = 10
        self.score = 0
        self.feedback_message_text = ""
        
        self.initialize_gui()

    def initialize_gui(self):
        self.image, self.draw = self.create_pillow_image()
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas, self.canvas_image = self.create_canvas()

        self.input_field = self.create_input_field()

        self.next_round()

    def create_pillow_image(self):
        image = Image.new("RGBA", (self.canvas_width, self.canvas_height), "white")
        draw = ImageDraw.Draw(image)
        return image, draw

    def create_canvas(self):
        canvas = Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white", highlightthickness=0)
        canvas_image = canvas.create_image(0, 0, anchor="nw", image=self.photo)
        canvas.pack()
        return canvas, canvas_image

    def create_input_field(self):
        entry = Entry(self.root, font=("DejaVu Sans", 16))
        entry.place(x=-100, y=-100, width=0, height=0)
        entry.focus()
        entry.bind("<KeyRelease>", self.update_canvas_text)
        entry.bind("<Return>", self.enter_guess)
        return entry

    def draw_score(self):
        score_text = f"{self.score}"
        self.draw.rectangle((self.canvas_width - 150, 10, self.canvas_width - 10, 40), fill="white")
        self.draw.text((self.canvas_width - 30, 10), score_text, font=self.font_score, fill="black")

    def update_canvas_text(self, event=None):
        input_text = self.input_field.get()
        pronoun = self.pronouns[self.current_form - 1]
        self.draw.rectangle((0, 0, self.canvas_width, self.canvas_height), fill="white")
        self.draw.text((100, 100), f"{pronoun}", font=self.font_large, fill="black")
        self.draw.text((225, 100), input_text, font=self.font_large, fill="black")
        if self.current_word:
            base_form = self.current_word[0]
            self.draw.text((100, 200), f"({base_form})", font=self.font_small, fill="gray")
        
        self.draw_score()

        updated_image = ImageTk.PhotoImage(self.image)
        self.canvas.itemconfig(self.canvas_image, image=updated_image)
        self.canvas.image = updated_image

    def update_canvas_prompt(self):
        self.draw.rectangle((0, 0, self.canvas_width, 300), fill="white")
        
        pronoun = self.pronouns[self.current_form - 1]
        self.draw.text((100, 100), f"{pronoun}", font=self.font_large, fill="black")
        self.draw.text((100, 200), f"({self.current_word[0]})", font=self.font_small, fill="gray")
        
        self.draw_score()

        updated_image = ImageTk.PhotoImage(self.image)
        self.canvas.itemconfig(self.canvas_image, image=updated_image)
        self.canvas.image = updated_image
        self.input_field.delete(0, "end")

    def enter_guess(self, event=None):
        input_text = self.input_field.get().strip()
        correct_answer = self.current_word[self.current_form].strip()

        if input_text == correct_answer:
            self.score += 1
            self.learned[self.current_word_idx][self.current_form] = "1"
            self.write_csv(self.learned, self.eval_file)
            self.feedback_message("Correct!", "green")
        else:
            self.feedback_message(f"Nope! Correct: {correct_answer}", "red")
        
        if self.rounds >= self.max_rounds:
            self.root.after(1000, self.end_training)
        else:
            self.root.after(1000, self.next_round)

    def next_round(self):
        if self.rounds >= self.max_rounds:
            self.end_training()
            return

        self.rounds += 1
        while True:
            self.current_word_idx = random.randint(0, len(self.data) - 1)
            self.current_word = self.data[self.current_word_idx]
            self.current_form = random.randint(1, 6)

            if self.learned[self.current_word_idx][self.current_form] != "1":
                break

        self.update_canvas_prompt()

    def feedback_message(self, message, color):
        self.draw.rectangle((0, 250, self.canvas_width, self.canvas_height), fill="white")
        self.draw_score()
        updated_image = ImageTk.PhotoImage(self.image)
        self.canvas.itemconfig(self.canvas_image, image=updated_image)
        self.canvas.image = updated_image

    def end_training(self):
        self.draw.rectangle((0, 0, self.canvas_width, self.canvas_height), fill="white")
        
        text = f"Training Complete! \nScore: {self.score}/{self.max_rounds}"
        text_bbox = self.draw.textbbox((0, 0), text, font=self.font_large)
        text_width = text_bbox[2] - text_bbox[0]
        x_position = (self.canvas_width - text_width) // 2
        
        self.draw.text((x_position, 100), text, font=self.font_large, fill="black")
        
        updated_image = ImageTk.PhotoImage(self.image)
        self.canvas.itemconfig(self.canvas_image, image=updated_image)
        self.canvas.image = updated_image
        
        self.input_field.config(state="disabled")
        
        self.create_restart_button()
        self.create_menu_button()

    def create_restart_button(self):
        self.restart_button = Button(
            self.root,
            text="Restart",
            font=("DejaVu Sans", 16),
            command=self.setup_new_session
        )
        self.restart_button.pack(pady=10)

    def create_menu_button(self):
        self.menu_button = Button(
            self.root,
            text="Main Menu",
            font=("DejaVu Sans", 16),
            command=self.show_start_screen
        )
        self.menu_button.pack(pady=10)

    def read_csv(self, file_path):
        data = []
        with open(file_path, mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)
        return data

    def write_csv(self, data, file_path):
        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(data)

    def get_pronouns(self):
        return ["я", "ты", "он", "мы", "вы", "они"]

    def get_case_words(self):
        return ["1.Sg.", "2.Sg.", "3.Sg.", "4.Sg.", "5.Sg.", "6.Sg."]

if __name__ == "__main__":
    root = Tk()
    root.title('Russian Grammar Trainer')
    app = GrammarTrainerApp(root)
    root.mainloop()