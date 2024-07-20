from tkinter import *
import time
from tkinter import filedialog, messagebox

start_time = time.time()
timer_running = False
time_duration = None
last_keypress_time = None

def start_test():
    global start_time, timer_running, time_duration, last_keypress_time


    start_button.config(state='disabled')
    difficulty_menu.config(state='disabled')
    instruction_button.config(state='disabled')

    timer_running = True
    if difficulty_var.get() == 'Easy':
        time_duration = 10
    elif difficulty_var.get() == 'Medium':
        time_duration = 7
    else:
        time_duration = 5


    user_typing.config(state='normal', fg='black', bg='snow')
    user_typing.delete('1.0', END)
    user_typing.focus()

    start_time = time.time()  # Set start time here
    last_keypress_time = start_time

    timer_function()

def timer_function():
    global time_duration, timer_running, last_keypress_time, start_time
    if timer_running:
        current_time = time.time()
        remaining_time = time_duration - (current_time - last_keypress_time)  # Calculate remaining time

        if remaining_time <= 0:
            text = user_typing.get("1.0", END)
            remaining_time = 0
            timer_running = False
            start_button.config(state='normal')
            difficulty_menu.config(state='normal')
            instruction_button.config(state='normal')
            user_typing.delete('1.0', END)
            user_typing.insert('1.0','Text deleted due to inactivity.')
            user_typing.config(bg='thistle1', state='disabled')
            start_button.config(state='normal')
            print('Timer Ended....')
            save_file(text)


        timer_label.config(text=f"Timer: {remaining_time:.0f} seconds", fg='gold')

        if f'{remaining_time:.0f}' == '3':
            user_typing.config(fg='firebrick1')
            timer_label.config(fg='firebrick1')
        elif f'{remaining_time:.0f}' == '2':
            user_typing.config(fg='red2')
            timer_label.config(fg='red2')
        elif f'{remaining_time:.0f}' == '1':
            user_typing.config(fg='red4')
            timer_label.config(fg='red4')
        elif f'{remaining_time:.0f}' == '0':
            timer_label.config(fg='firebrick4')
        else:
            user_typing.config(fg='black')
            timer_label.config(fg='gold')

        if remaining_time > 0:
            info_frame.after(1000, timer_function)



def save_file(text):
    # Open a dialog to ask for the save file location
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        try:
            # Retrieve all text from the Text widget
            text = text
            with open(file_path, 'w') as file:
                file.write(text)
            messagebox.showinfo("Save", "File saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

def on_key_press(event):
    global last_keypress_time
    last_keypress_time = time.time()

def instructions():
    user_typing.config(fg='darkorchid')
    user_typing.insert('1.0', "Welcome to text disappearing app.\nWhere your text disappear based on difficulty set by you."
                              "\nEach difficulty has time, when writing each character, Timer get reset to it original state."
                              "\n\nEasy: 10 Seconds\n"
                              "Medium: 7 Seconds\n"
                              "Hard: 5 Seconds")


window = Tk()
window.config(height=800, width=1000, padx=20, pady=20, bg='black')
window.title('Text Disappearing App')

label_fonts = ("Verdana", 14)

# Frame For Typing
typing_frame = Frame(window, bg='black')
typing_frame.grid(row=0, column=0, padx=10, pady=10)

# Frame For info
info_frame = Frame(window, bg='black')
info_frame.grid(row=0, column=1, padx=20, pady=10, sticky='n')

write_below = Label(typing_frame,
                    text='Text Disappearing App',
                    bg='black',
                    fg='lightcyan',
                    font=("Georgia", 14)
                    )
write_below.grid(row=0, column=0, pady=(10, 5))

user_typing = Text(typing_frame,
                   font=label_fonts,
                   width=80,
                   height=10
                   )
user_typing.grid(row=1, column=0, pady=(10, 5))
# user_typing.config(state='disabled')
user_typing.bind("<KeyPress>", on_key_press)

instruction_button = Button(typing_frame,
                            text='Instructions',
                            bg='black',
                            fg='mediumpurple',
                            font=label_fonts,
                            activeforeground='black',
                            activebackground='deeppink2',
                            width=10,
                            command=instructions
                            )
instruction_button.grid(row=2, column=0, pady=(20, 0), sticky='nw')

######################   Control Panel

timer_label = Label(info_frame,
                    text='Timer: 00',
                    bg='black',
                    fg='aquamarine',
                    font=label_fonts
                    )
timer_label.grid(row=1, column=0, padx=(10, 10), pady=(10, 10))

difficulty_label = Label(info_frame,
                         text="Select Difficulty",
                         font=("Segoeui", 14),
                         bg='black',
                         fg='deepskyblue')
difficulty_label.grid(row=2, column=0, pady=(10, 10), padx=(10, 10))

difficulty_var = StringVar(info_frame, value="Easy")  # Get Answer by "difficulty_var.get()".
difficulty_options = ["Easy", "Medium", "Hard"]
difficulty_menu = OptionMenu(info_frame, difficulty_var, *difficulty_options)
difficulty_menu.grid(row=2, column=1, pady=(10, 10), padx=(10, 10), sticky='ne')

start_button = Button(info_frame,
                      text='Start',
                      bg='black',
                      fg='olivedrab1',
                      font=label_fonts,
                      activeforeground='black',
                      activebackground='olivedrab1',
                      width=10,
                      command=start_test
                      )
start_button.grid(row=3, column=0, pady=(10, 10))



window.mainloop()

