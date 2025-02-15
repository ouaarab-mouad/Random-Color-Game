import tkinter as tk
import random

# Global variables
history = []  # Stores history of attempts
correct_color = ""
dark_mode = False

def toggle_mode():
    global dark_mode
    dark_mode = not dark_mode
    if dark_mode:
        root.configure(bg="#121212")
        title_label.config(bg="#121212", fg="white")
        rgb_label.config(bg="#121212", fg="yellow")
        result_label.config(bg="#121212", fg="white")
        button_frame.config(bg="#121212")
        toggle_button.config(text="🌞 Light Mode", bg="#f8f8f8", fg="#121212")
    else:
        root.configure(bg="white")
        title_label.config(bg="white", fg="black")
        rgb_label.config(bg="white", fg="black")
        result_label.config(bg="white", fg="black")
        button_frame.config(bg="white")
        toggle_button.config(text="🌙 Dark Mode", bg="#121212", fg="white")

def random_color():
    return f'#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}'

def check_answer(selected_color):
    if selected_color == correct_color:
        result_label.config(text="🎉 Correct! Well done!", fg="green")
    else:
        result_label.config(text=f"❌ Wrong! The correct color was {correct_color}", fg="red")
    history.append({"Chosen": selected_color, "Correct": correct_color})
    for btn in color_buttons:
        btn.config(state="disabled")
    play_again_button.pack(pady=5)
    save_history_button.pack(pady=5)

def generate_colors():
    global correct_color
    correct_color = random_color()
    colors = [correct_color] + [random_color() for _ in range(5)]
    random.shuffle(colors)
    for i in range(6):
        color_buttons[i].config(bg=colors[i], activebackground=colors[i], state="normal", command=lambda c=colors[i]: check_answer(c))
    rgb_label.config(text=f"Guess the color: {correct_color}")
    result_label.config(text="")
    play_again_button.pack_forget()
    save_history_button.pack_forget()

def show_history():
    if not history:
        return
    history_window = tk.Toplevel(root)
    history_window.title("🎨 Guess History")
    history_window.geometry("350x400")
    history_window.configure(bg="#f8f8f8" if not dark_mode else "#121212")
    tk.Label(history_window, text="📝 Your Guess History", font=("Arial", 14, "bold"), bg="#f8f8f8" if not dark_mode else "#121212", fg="black" if not dark_mode else "white").pack(pady=10)
    for i, entry in enumerate(history, 1):
        text = f"#{i} Chosen: {entry['Chosen']}  ✅ Correct: {entry['Correct']}"
        tk.Label(history_window, text=text, font=("Arial", 10), bg="#f8f8f8" if not dark_mode else "#121212", fg="black" if not dark_mode else "white").pack(pady=2)

root = tk.Tk()
root.title("🎨 Guess the RGB Game")
root.geometry("500x650")
root.configure(bg="white")

title_label = tk.Label(root, text="🎨 Guess the RGB Color!", font=("Arial", 20, "bold"), fg="black", bg="white")
title_label.pack(pady=20)

rgb_label = tk.Label(root, text="", font=("Arial", 16, "bold"), fg="black", bg="white")
rgb_label.pack(pady=10)

button_frame = tk.Frame(root, bg="white")
button_frame.pack(pady=20)

color_buttons = []
for i in range(6):
    btn = tk.Button(button_frame, width=15, height=2, font=("Arial", 12, "bold"), relief="raised", borderwidth=3)
    btn.grid(row=i//3, column=i%3, padx=10, pady=10)
    color_buttons.append(btn)

result_label = tk.Label(root, text="", font=("Arial", 16, "bold"), fg="black", bg="white")
result_label.pack(pady=10)

play_again_button = tk.Button(root, text="🔄 Play Again", font=("Arial", 14, "bold"), bg="#007bff", fg="white", relief="raised", borderwidth=3, command=generate_colors)
save_history_button = tk.Button(root, text="📜 Save to History", font=("Arial", 14, "bold"), bg="#28a745", fg="white", relief="raised", borderwidth=3)
show_history_button = tk.Button(root, text="🔍 Show History", font=("Arial", 14, "bold"), bg="#ff9800", fg="white", relief="raised", borderwidth=3, command=show_history)
show_history_button.pack(pady=10)

toggle_button = tk.Button(root, text="🌙 Dark Mode", font=("Arial", 14, "bold"), bg="#121212", fg="white", relief="raised", borderwidth=3, command=toggle_mode)
toggle_button.pack(pady=10)

generate_colors()
root.mainloop()
