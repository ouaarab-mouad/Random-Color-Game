import tkinter as tk
import random

# Function to generate a random hex color
def random_color():
    return f'#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}'

# Function to check the player's choice
def check_answer(selected_color):
    if selected_color == correct_color:
        result_label.config(text="🎉 Correct! Well done!", fg="green")
    else:
        result_label.config(text="❌ Wrong! Try again.", fg="red")

    # Disable buttons after a guess
    for btn in color_buttons:
        btn.config(state="disabled")

    # Show the play again button
    play_again_button.pack(pady=10)

# Function to generate new colors and refresh the UI
def generate_colors():
    global correct_color
    correct_color = random_color()
    
    # Generate a list of 6 colors, including the correct one
    colors = [correct_color] + [random_color() for _ in range(5)]
    random.shuffle(colors)  # Shuffle the colors to random positions

    # Update buttons with new colors
    for i in range(6):
        color_buttons[i].config(bg=colors[i], activebackground=colors[i], state="normal", command=lambda c=colors[i]: check_answer(c))

    # Update the displayed RGB color text
    rgb_label.config(text=f"Guess the color: {correct_color}")

    # Hide play again button and reset result text
    result_label.config(text="")
    play_again_button.pack_forget()

# Create the GUI window
root = tk.Tk()
root.title("🎨 Guess the RGB Game")
root.geometry("500x600")
root.configure(bg="#f4f4f4")

# Title label
title_label = tk.Label(root, text="🎨 Guess the RGB Color!", font=("Arial", 20, "bold"), bg="#f4f4f4", fg="#333")
title_label.pack(pady=20)

# Instruction label
rgb_label = tk.Label(root, text="", font=("Arial", 16, "bold"), bg="#f4f4f4", fg="#555")
rgb_label.pack(pady=10)

# Create a frame for color buttons
button_frame = tk.Frame(root, bg="#f4f4f4")
button_frame.pack(pady=20)

# Create buttons for color choices
color_buttons = []
for i in range(6):
    btn = tk.Button(button_frame, width=15, height=2, font=("Arial", 12, "bold"), relief="raised", borderwidth=3)
    btn.grid(row=i//3, column=i%3, padx=10, pady=10)  # Arrange in 2 rows, 3 buttons per row
    color_buttons.append(btn)

# Result label
result_label = tk.Label(root, text="", font=("Arial", 16, "bold"), bg="#f4f4f4")
result_label.pack(pady=20)

# Play Again button (hidden by default)
play_again_button = tk.Button(root, text="🔄 Play Again", font=("Arial", 14, "bold"), bg="#007bff", fg="white", relief="raised", borderwidth=3, command=generate_colors)

# Start the game
generate_colors()

# Run the Tkinter event loop
root.mainloop()
