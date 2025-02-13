import tkinter as tk
import random

# Global variables
history = []  # Stores history of attempts
correct_color = ""

# Function to generate a random hex color
def random_color():
    return f'#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}'

# Function to check the player's choice
def check_answer(selected_color):
    if selected_color == correct_color:
        result_label.config(text="🎉 Correct! Well done!", fg="green")
    else:
        result_label.config(text=f"❌ Wrong! The correct color was {correct_color}", fg="red")

    # Save attempt to history
    history.append({"Chosen": selected_color, "Correct": correct_color})

    # Disable buttons after a guess
    for btn in color_buttons:
        btn.config(state="disabled")

    # Show "Play Again" and "Save to History" buttons
    play_again_button.pack(pady=5)
    save_history_button.pack(pady=5)

# Function to generate new colors and refresh the UI
def generate_colors():
    global correct_color
    correct_color = random_color()
    
    # Generate 6 colors (1 correct + 5 random)
    colors = [correct_color] + [random_color() for _ in range(5)]
    random.shuffle(colors)

    # Update buttons with new colors
    for i in range(6):
        color_buttons[i].config(bg=colors[i], activebackground=colors[i], state="normal", command=lambda c=colors[i]: check_answer(c))

    # Update displayed RGB color text
    rgb_label.config(text=f"Guess the color: {correct_color}")

    # Hide buttons and reset result text
    result_label.config(text="")
    play_again_button.pack_forget()
    save_history_button.pack_forget()

# Function to show history in a new window
def show_history():
    if not history:
        return

    history_window = tk.Toplevel(root)
    history_window.title("🎨 Guess History")
    history_window.geometry("350x400")
    history_window.configure(bg="#f8f8f8")

    # Title
    tk.Label(history_window, text="📝 Your Guess History", font=("Arial", 14, "bold"), bg="#f8f8f8").pack(pady=10)

    # Show attempts
    for i, entry in enumerate(history, 1):
        text = f"#{i} Chosen: {entry['Chosen']}  ✅ Correct: {entry['Correct']}"
        tk.Label(history_window, text=text, font=("Arial", 10), bg="#f8f8f8").pack(pady=2)

# Create the GUI window
root = tk.Tk()
root.title("🎨 Guess the RGB Game")
root.geometry("500x650")
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
result_label.pack(pady=10)

# Buttons for history and replay
play_again_button = tk.Button(root, text="🔄 Play Again", font=("Arial", 14, "bold"), bg="#007bff", fg="white", relief="raised", borderwidth=3, command=generate_colors)
save_history_button = tk.Button(root, text="📜 Save to History", font=("Arial", 14, "bold"), bg="#28a745", fg="white", relief="raised", borderwidth=3)
show_history_button = tk.Button(root, text="🔍 Show History", font=("Arial", 14, "bold"), bg="#ff9800", fg="white", relief="raised", borderwidth=3, command=show_history)
show_history_button.pack(pady=10)

# Start the game
generate_colors()

# Run the Tkinter event loop
root.mainloop()
