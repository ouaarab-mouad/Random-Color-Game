import tkinter as tk
import random
import math
import json
import os
from datetime import datetime
import time

# Global variables
history = []  # Stores history of attempts
correct_color = ""
dark_mode = False
difficulty = "medium"  # Default difficulty
current_score = 0
high_score = 0
timer_active = False
countdown = 0
timer_id = None
hint_used = False

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
        score_label.config(bg="#121212", fg="white")
        difficulty_frame.config(bg="#121212")
        for radio in difficulty_radios:
            radio.config(bg="#121212", fg="white", selectcolor="#333333")
        timer_frame.config(bg="#121212")
        timer_label.config(bg="#121212", fg="white")
        timer_checkbox.config(bg="#121212", fg="white", selectcolor="#333333")
    else:
        root.configure(bg="white")
        title_label.config(bg="white", fg="black")
        rgb_label.config(bg="white", fg="black")
        result_label.config(bg="white", fg="black")
        button_frame.config(bg="white")
        toggle_button.config(text="🌙 Dark Mode", bg="#121212", fg="white")
        score_label.config(bg="white", fg="black")
        difficulty_frame.config(bg="white")
        for radio in difficulty_radios:
            radio.config(bg="white", fg="black", selectcolor="white")
        timer_frame.config(bg="white")
        timer_label.config(bg="white", fg="black")
        timer_checkbox.config(bg="white", fg="black", selectcolor="white")

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def color_distance(color1, color2):
    """Calculate Euclidean distance between two colors"""
    r1, g1, b1 = hex_to_rgb(color1)
    r2, g2, b2 = hex_to_rgb(color2)
    return math.sqrt((r2 - r1) ** 2 + (g2 - g1) ** 2 + (b2 - b1) ** 2)

def random_color():
    return f'#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}'

def generate_similar_colors(base_color, num_colors, similarity_factor):
    """Generate colors similar to base_color. Lower similarity_factor means more similar colors."""
    colors = [base_color]
    base_rgb = hex_to_rgb(base_color)
    
    while len(colors) < num_colors + 1:  # +1 because we already have the base color
        # Adjust the variation based on difficulty
        variation = int(255 * similarity_factor)
        
        # Generate a new color with variations
        new_r = max(0, min(255, base_rgb[0] + random.randint(-variation, variation)))
        new_g = max(0, min(255, base_rgb[1] + random.randint(-variation, variation)))
        new_b = max(0, min(255, base_rgb[2] + random.randint(-variation, variation)))
        
        new_color = f'#{new_r:02x}{new_g:02x}{new_b:02x}'
        
        # Make sure the color is distinct enough
        if all(color_distance(new_color, c) > 20 for c in colors):
            colors.append(new_color)
    
    return colors[1:]  # Return all except the first (base) color

def check_answer(selected_color):
    global current_score, high_score, hint_used, timer_id
    
    # Stop timer if it's running
    if timer_active and timer_id is not None:
        root.after_cancel(timer_id)
        timer_id = None
    
    distance = color_distance(selected_color, correct_color)
    
    # Calculate score based on difficulty, timer, and distance
    diff_multiplier = {"easy": 1, "medium": 2, "hard": 3}
    time_bonus = countdown if timer_active else 0
    hint_penalty = 5 if hint_used else 0
    
    if selected_color == correct_color:
        points = 10 * diff_multiplier[difficulty] + time_bonus - hint_penalty
        current_score += points
        result_text = f"🎉 Correct! +{points} points"
        result_color = "green"
        if current_score > high_score:
            high_score = current_score
            result_text += " (New High Score!)"
    else:
        # Provide feedback based on how close the guess was
        if distance < 50:
            closeness = "Very close!"
        elif distance < 100:
            closeness = "Close!"
        elif distance < 150:
            closeness = "Getting there!"
        else:
            closeness = "Not close"
            
        result_text = f"❌ Wrong! {closeness} The correct color was {correct_color}"
        result_color = "red"
    
    result_label.config(text=result_text, fg=result_color)
    history.append({
        "Chosen": selected_color, 
        "Correct": correct_color, 
        "Difficulty": difficulty,
        "Score": current_score,
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    for btn in color_buttons:
        btn.config(state="disabled")
    
    # Update score display
    score_label.config(text=f"Score: {current_score} | High Score: {high_score}")
    
    play_again_button.pack(pady=5)
    save_history_button.pack(pady=5)

def generate_colors():
    global correct_color, hint_used, countdown, timer_id
    
    # Reset hint status
    hint_used = False
    
    # Generate a random correct color
    correct_color = random_color()
    
    # Generate colors based on difficulty
    similarity_factors = {"easy": 0.8, "medium": 0.5, "hard": 0.2}
    colors = [correct_color] + generate_similar_colors(
        correct_color, 5, similarity_factors[difficulty]
    )
    random.shuffle(colors)
    
    for i in range(6):
        color_buttons[i].config(
            bg=colors[i], 
            activebackground=colors[i], 
            state="normal", 
            command=lambda c=colors[i]: check_answer(c)
        )
    
    # Update the display based on current mode
    if display_mode.get() == "hex":
        rgb_label.config(text=f"Guess the color: {correct_color}")
    elif display_mode.get() == "rgb":
        r, g, b = hex_to_rgb(correct_color)
        rgb_label.config(text=f"Guess the color: RGB({r}, {g}, {b})")
    else:  # name mode - simplified color naming
        r, g, b = hex_to_rgb(correct_color)
        # Simple color naming logic
        color_names = ["Red", "Green", "Blue", "Yellow", "Purple", "Orange", "Pink", "Brown", "Gray"]
        # This is a very simplified color naming algorithm
        max_val = max(r, g, b)
        if r > 200 and g < 100 and b < 100:
            color_name = "Red"
        elif r < 100 and g > 200 and b < 100:
            color_name = "Green"
        elif r < 100 and g < 100 and b > 200:
            color_name = "Blue"
        elif r > 200 and g > 200 and b < 100:
            color_name = "Yellow"
        elif r > 150 and g < 100 and b > 150:
            color_name = "Purple"
        elif r > 200 and g > 100 and b < 100:
            color_name = "Orange"
        elif r > 200 and g > 150 and b > 150:
            color_name = "Pink"
        elif r < 150 and g < 100 and b < 50:
            color_name = "Brown"
        else:
            color_name = "Gray"
        rgb_label.config(text=f"Guess the color: {color_name}")
    
    result_label.config(text="")
    play_again_button.pack_forget()
    save_history_button.pack_forget()
    hint_button.config(state="normal")
    
    # Start timer if timer mode is active
    if timer_active:
        countdown = 30  # Reset countdown to 30 seconds
        update_timer()

def update_timer():
    global countdown, timer_id
    
    if countdown > 0 and timer_active:
        timer_label.config(text=f"Time: {countdown}s")
        countdown -= 1
        timer_id = root.after(1000, update_timer)
    elif countdown <= 0 and timer_active:
        timer_label.config(text="Time's up!")
        # Auto-select the first option (as a penalty)
        for btn in color_buttons:
            if btn['state'] != 'disabled':
                check_answer(btn.cget('bg'))
                break

def show_history():
    if not history:
        return
    history_window = tk.Toplevel(root)
    history_window.title("🎨 Guess History")
    history_window.geometry("500x500")
    history_window.configure(bg="#f8f8f8" if not dark_mode else "#121212")
    
    tk.Label(
        history_window, 
        text="📝 Your Guess History", 
        font=("Arial", 14, "bold"), 
        bg="#f8f8f8" if not dark_mode else "#121212", 
        fg="black" if not dark_mode else "white"
    ).pack(pady=10)
    
    # Create a scrollable frame for history
    frame = tk.Frame(history_window, bg="#f8f8f8" if not dark_mode else "#121212")
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    canvas = tk.Canvas(frame, bg="#f8f8f8" if not dark_mode else "#121212")
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f8f8f8" if not dark_mode else "#121212")
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Add headers
    header_frame = tk.Frame(scrollable_frame, bg="#f8f8f8" if not dark_mode else "#121212")
    header_frame.pack(fill="x", padx=5, pady=5)
    
    headers = ["#", "Chosen", "Correct", "Difficulty", "Score", "Date"]
    widths = [30, 100, 100, 80, 60, 180]
    
    for i, header in enumerate(headers):
        tk.Label(
            header_frame, 
            text=header, 
            font=("Arial", 10, "bold"),
            width=widths[i]//10,
            bg="#f8f8f8" if not dark_mode else "#121212", 
            fg="black" if not dark_mode else "white"
        ).grid(row=0, column=i, padx=2)
    
    # Add history entries
    for i, entry in enumerate(history, 1):
        row_frame = tk.Frame(scrollable_frame, bg="#f8f8f8" if not dark_mode else "#121212")
        row_frame.pack(fill="x", padx=5, pady=2)
        
        # Number column
        tk.Label(
            row_frame, text=str(i), width=3,
            bg="#f8f8f8" if not dark_mode else "#121212", 
            fg="black" if not dark_mode else "white"
        ).grid(row=0, column=0, padx=2)
        
        # Chosen color
        chosen_frame = tk.Frame(row_frame, width=20, height=20, bg=entry['Chosen'])
        chosen_frame.grid(row=0, column=1, padx=2)
        tk.Label(
            row_frame, text=entry['Chosen'], 
            bg="#f8f8f8" if not dark_mode else "#121212", 
            fg="black" if not dark_mode else "white"
        ).grid(row=0, column=1, padx=(25, 2))
        
        # Correct color
        correct_frame = tk.Frame(row_frame, width=20, height=20, bg=entry['Correct'])
        correct_frame.grid(row=0, column=2, padx=2)
        tk.Label(
            row_frame, text=entry['Correct'], 
            bg="#f8f8f8" if not dark_mode else "#121212", 
            fg="black" if not dark_mode else "white"
        ).grid(row=0, column=2, padx=(25, 2))
        
        # Difficulty, Score, Date
        tk.Label(
            row_frame, text=entry.get('Difficulty', 'medium'), width=8,
            bg="#f8f8f8" if not dark_mode else "#121212", 
            fg="black" if not dark_mode else "white"
        ).grid(row=0, column=3, padx=2)
        
        tk.Label(
            row_frame, text=str(entry.get('Score', 0)), width=6,
            bg="#f8f8f8" if not dark_mode else "#121212", 
            fg="black" if not dark_mode else "white"
        ).grid(row=0, column=4, padx=2)
        
        tk.Label(
            row_frame, text=entry.get('Date', ''), width=18,
            bg="#f8f8f8" if not dark_mode else "#121212", 
            fg="black" if not dark_mode else "white"
        ).grid(row=0, column=5, padx=2)

def save_history():
    """Save game history to a JSON file"""
    if not history:
        result_label.config(text="No history to save", fg="orange")
        return
    
    try:
        # Create directory if it doesn't exist
        if not os.path.exists("game_history"):
            os.makedirs("game_history")
        
        filename = f"game_history/rgb_game_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, "w") as f:
            json.dump(history, f, indent=4)
        
        result_label.config(text=f"History saved to {filename}", fg="green")
    except Exception as e:
        result_label.config(text=f"Error saving history: {str(e)}", fg="red")

def change_difficulty():
    """Update game when difficulty changes"""
    global difficulty
    difficulty = difficulty_var.get()
    generate_colors()

def toggle_timer():
    """Enable/disable timer mode"""
    global timer_active
    timer_active = timer_var.get()
    if timer_active:
        timer_label.config(text="Time: 30s")
        if any(btn['state'] != 'disabled' for btn in color_buttons):
            # If game is active, start the timer
            global countdown
            countdown = 30
            update_timer()
    else:
        timer_label.config(text="Timer Off")
        # Cancel the timer if it's running
        global timer_id
        if timer_id is not None:
            root.after_cancel(timer_id)
            timer_id = None

def give_hint():
    """Provide a hint by disabling two incorrect options"""
    global hint_used
    
    # Only allow hint if the game is active and hint wasn't used yet
    if any(btn['state'] != 'disabled' for btn in color_buttons) and not hint_used:
        hint_used = True
        
        # Find buttons with incorrect colors
        incorrect_buttons = [btn for btn in color_buttons if btn.cget('bg') != correct_color and btn['state'] != 'disabled']
        
        # Disable two random incorrect buttons
        if len(incorrect_buttons) >= 2:
            to_disable = random.sample(incorrect_buttons, 2)
            for btn in to_disable:
                btn.config(state="disabled", bg="gray")
            
            result_label.config(text="Hint used: 2 wrong colors removed (-5 points)", fg="orange")
        
        # Disable the hint button after use
        hint_button.config(state="disabled")

def change_display_mode():
    """Update the display when the mode changes"""
    if any(btn['state'] != 'disabled' for btn in color_buttons):
        # If game is active, update the display
        if display_mode.get() == "hex":
            rgb_label.config(text=f"Guess the color: {correct_color}")
        elif display_mode.get() == "rgb":
            r, g, b = hex_to_rgb(correct_color)
            rgb_label.config(text=f"Guess the color: RGB({r}, {g}, {b})")
        else:  # name mode
            r, g, b = hex_to_rgb(correct_color)
            # Simple color naming logic (same as in generate_colors)
            if r > 200 and g < 100 and b < 100:
                color_name = "Red"
            elif r < 100 and g > 200 and b < 100:
                color_name = "Green"
            elif r < 100 and g < 100 and b > 200:
                color_name = "Blue"
            elif r > 200 and g > 200 and b < 100:
                color_name = "Yellow"
            elif r > 150 and g < 100 and b > 150:
                color_name = "Purple"
            elif r > 200 and g > 100 and b < 100:
                color_name = "Orange"
            elif r > 200 and g > 150 and b > 150:
                color_name = "Pink"
            elif r < 150 and g < 100 and b < 50:
                color_name = "Brown"
            else:
                color_name = "Gray"
            rgb_label.config(text=f"Guess the color: {color_name}")

# Initialize the main window
root = tk.Tk()
root.title("🎨 Guess the RGB Game")
root.geometry("600x750")
root.configure(bg="white")

# Title Label
title_label = tk.Label(root, text="🎨 Guess the RGB Color!", font=("Arial", 20, "bold"), fg="black", bg="white")
title_label.pack(pady=20)

# Score Display
score_label = tk.Label(root, text=f"Score: {current_score} | High Score: {high_score}", font=("Arial", 14, "bold"), fg="black", bg="white")
score_label.pack(pady=5)

# Difficulty Selection
difficulty_frame = tk.Frame(root, bg="white")
difficulty_frame.pack(pady=10)

tk.Label(difficulty_frame, text="Difficulty:", font=("Arial", 12), bg="white", fg="black").grid(row=0, column=0, padx=10)

difficulty_var = tk.StringVar(value=difficulty)
difficulty_radios = []

for i, diff in enumerate(["easy", "medium", "hard"]):
    radio = tk.Radiobutton(
        difficulty_frame, 
        text=diff.capitalize(), 
        variable=difficulty_var, 
        value=diff, 
        command=change_difficulty,
        font=("Arial", 10),
        bg="white",
        fg="black"
    )
    radio.grid(row=0, column=i+1, padx=5)
    difficulty_radios.append(radio)

# Display Mode Selection
display_frame = tk.Frame(root, bg="white")
display_frame.pack(pady=5)

tk.Label(display_frame, text="Show as:", font=("Arial", 12), bg="white", fg="black").grid(row=0, column=0, padx=10)

display_mode = tk.StringVar(value="hex")
modes = [("Hex", "hex"), ("RGB", "rgb"), ("Name", "name")]

for i, (text, mode) in enumerate(modes):
    tk.Radiobutton(
        display_frame, 
        text=text, 
        variable=display_mode, 
        value=mode, 
        command=change_display_mode,
        font=("Arial", 10),
        bg="white",
        fg="black"
    ).grid(row=0, column=i+1, padx=5)

# Timer Option
timer_frame = tk.Frame(root, bg="white")
timer_frame.pack(pady=5)

timer_var = tk.BooleanVar(value=False)
timer_checkbox = tk.Checkbutton(
    timer_frame, 
    text="Enable Timer Mode", 
    variable=timer_var,
    command=toggle_timer,
    font=("Arial", 12),
    bg="white",
    fg="black"
)
timer_checkbox.pack(side="left", padx=10)

timer_label = tk.Label(timer_frame, text="Timer Off", font=("Arial", 12), bg="white", fg="black")
timer_label.pack(side="left", padx=10)

# RGB Display Label
rgb_label = tk.Label(root, text="", font=("Arial", 16, "bold"), fg="black", bg="white")
rgb_label.pack(pady=10)

# Color Buttons Frame
button_frame = tk.Frame(root, bg="white")
button_frame.pack(pady=20)

# Create color buttons
color_buttons = []
for i in range(6):
    btn = tk.Button(button_frame, width=15, height=2, font=("Arial", 12, "bold"), relief="raised", borderwidth=3)
    btn.grid(row=i//3, column=i%3, padx=10, pady=10)
    color_buttons.append(btn)

# Result Label
result_label = tk.Label(root, text="", font=("Arial", 16, "bold"), fg="black", bg="white")
result_label.pack(pady=10)

# Game Control Buttons
control_frame = tk.Frame(root, bg="white")
control_frame.pack(pady=5)

play_again_button = tk.Button(
    control_frame, 
    text="🔄 Play Again", 
    font=("Arial", 14, "bold"), 
    bg="#007bff", 
    fg="white", 
    relief="raised", 
    borderwidth=3, 
    command=generate_colors
)

save_history_button = tk.Button(
    control_frame, 
    text="📜 Save to File", 
    font=("Arial", 14, "bold"), 
    bg="#28a745", 
    fg="white", 
    relief="raised", 
    borderwidth=3,
    command=save_history
)

hint_button = tk.Button(
    control_frame, 
    text="💡 Use Hint", 
    font=("Arial", 14, "bold"), 
    bg="#9c27b0", 
    fg="white", 
    relief="raised", 
    borderwidth=3,
    command=give_hint
)
hint_button.pack(pady=5)

show_history_button = tk.Button(
    control_frame, 
    text="🔍 Show History", 
    font=("Arial", 14, "bold"), 
    bg="#ff9800", 
    fg="white", 
    relief="raised", 
    borderwidth=3, 
    command=show_history
)
show_history_button.pack(pady=5)

# Dark Mode Toggle
toggle_button = tk.Button(
    root, 
    text="🌙 Dark Mode", 
    font=("Arial", 14, "bold"), 
    bg="#121212", 
    fg="white", 
    relief="raised", 
    borderwidth=3, 
    command=toggle_mode
)
toggle_button.pack(pady=10)

# Start the game
generate_colors()

# Start the main loop
root.mainloop()
