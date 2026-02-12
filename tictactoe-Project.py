from tkinter import *
import random
# -------------------------------
# Globals
# -------------------------------
animating = False        # animation running undo enn check cheyyan
x_score = 0              # X player score
o_score = 0              # O player score
BG = "#0B1020"           # background color
blink_id = None          # blinking animation id store cheyyan
# -------------------------------
# Animations
# -------------------------------
def animate_win(cells, colors, index=0, cycles=0, max_cycles=12):
    global blink_id
    if cycles >= max_cycles:
        for cell in cells:
            cell.config(bg="#1A1A40")   # reset color
        return
    # alternate color blink
    for cell in cells:
        cell.config(bg=colors[index % len(colors)])
    # schedule again and save id
    blink_id = window.after(150, animate_win, cells, colors, index+1, cycles+1, max_cycles)
# -------------------------------
# Game logic
# -------------------------------
def next_turn(r, c):
    global player, x_score, o_score, animating
    if buttons[r][c]["text"] != "" or animating:
        return
    buttons[r][c].config(
        text=player,
        fg="#FF00FF" if player == "X" else "#00FFFF"
    )
    result = check_winner()
    if result is False:
        player = "O" if player == "X" else "X"
        label.config(text=f"{player} turn")
    elif result is True:
        label.config(text=f"{player} Wins!")
        animating = True
        if player == "X":
            x_score += 1
        else:
            o_score += 1
        score_label.config(text=f"X: {x_score}   O: {o_score}")
    else:
        label.config(text="Draw!!!")
def check_winner():
    global animating
    for i in range(3):
        # row check
        if buttons[i][0]["text"] == buttons[i][1]["text"] == buttons[i][2]["text"] != "":
            animating = True
            animate_win([buttons[i][0], buttons[i][1], buttons[i][2]], ["#FFD700", "#1A1A40"])
            return True
        # column check
        if buttons[0][i]["text"] == buttons[1][i]["text"] == buttons[2][i]["text"] != "":
            animating = True
            animate_win([buttons[0][i], buttons[1][i], buttons[2][i]], ["#FFD700", "#1A1A40"])
            return True
    # diagonals
    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != "":
        animating = True
        animate_win([buttons[0][0], buttons[1][1], buttons[2][2]], ["#FFD700", "#1A1A40"])
        return True
    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != "":
        animating = True
        animate_win([buttons[0][2], buttons[1][1], buttons[2][0]], ["#FFD700", "#1A1A40"])
        return True
    # tie check
    if all(buttons[r][c]["text"] != "" for r in range(3) for c in range(3)):
        return "Tie"
    return False
def new_game():
    global player, animating, blink_id
    animating = False
    if blink_id:
        window.after_cancel(blink_id)   # stop blinking immediately
        blink_id = None
    player = random.choice(["X", "O"])
    label.config(text=f"{player} turn")
    for r in range(3):
        for c in range(3):
            buttons[r][c].config(text="", bg="#1A1A40")
# -------------------------------
# UI
# -------------------------------
window = Tk()
window.title("Tic Tac Toe")
window.geometry("800x800")
window.configure(bg=BG)
player = random.choice(["X", "O"])
# Header
top_frame = Frame(window, bg=BG)
top_frame.pack(side="top", fill="x", pady=10)
title_label = Label(top_frame, text="Tic Tac Toe", font=("Comic Sans MS", 45, "bold"),
                    fg="#AA00FF", bg=BG)
title_label.pack()
label = Label(top_frame, text=f"{player} turn", font=("Arial Black", 30),
              fg="#FFFFFF", bg=BG)
label.pack()
score_label = Label(top_frame, text="X: 0   O: 0", font=("Consolas", 20),
                    fg="#FFFFFF", bg=BG)
score_label.pack()
reset_button = Button(top_frame, text="Restart", font=("Comic Sans MS", 18, "bold"),
                      bg="#00FF00", command=new_game)
reset_button.pack(pady=5)
# Game frame
frame = Frame(window, bg=BG)
frame.pack(expand=True, fill="both", padx=20, pady=20)
# Buttons
buttons = [[None]*3 for _ in range(3)]
for i in range(3):
    frame.grid_rowconfigure(i, weight=1)
    frame.grid_columnconfigure(i, weight=1)
for r in range(3):
    for c in range(3):
        btn = Button(
            frame,
            text="",
            font=("Comic Sans MS", 45),
            bg="#1A1A40",
            fg="#FFFFFF",
            activebackground="#2B2B52",
            command=lambda rr=r, cc=c: next_turn(rr, cc)
        )
        btn.grid(row=r, column=c, sticky="nsew", padx=6, pady=6)
        buttons[r][c] = btn
window.mainloop()