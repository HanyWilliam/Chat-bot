import tkinter as tk
from tkinter import scrolledtext
from helpers import get_current_time  
from user_interaction import handle_user_input  
from data import question_and_answers


def handle_chat():
    user_input = user_entry.get().strip()
    if user_input:
        chat_log.insert(tk.END, f"User: {user_input}\n")
        response = handle_user_input(user_input, question_and_answers) 
        chat_log.insert(tk.END, f"ChatBot: {response}\n\n")
        user_entry.delete(0, tk.END)  


root = tk.Tk()
root.title("ChatBot Application")


chat_log = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20, state="normal")
chat_log.grid(row=0, column=0, columnspan=2, padx=10, pady=10)


user_entry = tk.Entry(root, width=40)
user_entry.grid(row=1, column=0, padx=10, pady=10)


send_button = tk.Button(root, text="Send", command=handle_chat)
send_button.grid(row=1, column=1, padx=10, pady=10)

root.mainloop()
