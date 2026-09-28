import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Project")
app.geometry("360x500")
app.resizable(0, 0)
app.grid_columnconfigure(0, weight=1)
main_frame = ctk.CTkFrame(app)

def button9():
    return 0
def button8():
    return 0
def button7():
    return 0
def button6():
    return 0
def button5():
    return 0
def button4():
    return 0
def button3():
    return 0
def button2():
    return 0
def button1():
    return 0
def button0():
    return 0
def buttonumn():
    return 0
def buttonplus():
    return 0
def buttonminus():
    return 0
def buttoncel():
    return 0

label = ctk.CTkEntry(app, font=("Helvetica", 37), width= 327, height=90, text_color="white", state="disabled").grid(row=0, column=0, columnspan= 4, padx=(3, 0), pady= (35, 10))
button = ctk.CTkButton(app, text="7", corner_radius=10, height= 60, width=60, fg_color="#505050", 
                       text_color="white", font=("Helvetica", 37), hover_color="#7D7D7D", 
                       anchor="center",border_width=2, border_color="#A2A0A0", command=button7).grid(row=1, column=0, padx= 15, pady=15)
button = ctk.CTkButton(app, text="8", corner_radius=10, height= 60, width=60, fg_color="#505050", 
                       text_color="white", font=("Helvetica", 37), hover_color="#7D7D7D", 
                       anchor="center",border_width=2, border_color="#A2A0A0", command=button8).grid(row=1, column=1, padx= 12, pady=15)
button = ctk.CTkButton(app, text="9", corner_radius=10, height= 60, width=60, fg_color="#505050", 
                       text_color="white", font=("Helvetica", 37), hover_color="#7D7D7D", 
                       anchor="center",border_width=2, border_color="#A2A0A0", command=button9).grid(row=1, column=2, padx= 15, pady=15)
button = ctk.CTkButton(app, text="×", corner_radius=10, height= 60, width=60, fg_color="#505050", 
                       text_color="white", font=("Helvetica", 40), hover_color="#7D7D7D", 
                       anchor="center",border_width=2, border_color="#A2A0A0", command=buttonumn).grid(row=1, column=3, padx= 15, pady=15)
button = ctk.CTkButton(app, text="4", corner_radius=10, height= 60, width=60, fg_color="#505050", 
                       text_color="white", font=("Helvetica", 37), hover_color="#7D7D7D", 
                       anchor="center",border_width=2, border_color="#A2A0A0", command=button4).grid(row=2, column=0, padx= 15, pady=15)
button = ctk.CTkButton(app, text="5", corner_radius=10, height= 60, width=60, fg_color="#505050", 
                       text_color="white", font=("Helvetica", 37), hover_color="#7D7D7D", 
                       anchor="center",border_width=2, border_color="#A2A0A0", command=button5).grid(row=2, column=1, padx= 12, pady=15)
button = ctk.CTkButton(app, text="6", corner_radius=10, height= 60, width=60, fg_color="#505050", 
                       text_color="white", font=("Helvetica", 37), hover_color="#7D7D7D", 
                       anchor="center",border_width=2, border_color="#A2A0A0", command=button6).grid(row=2, column=2, padx= 15, pady=15)
button = ctk.CTkButton(app, text="-", corner_radius=10, height= 60, width=60, fg_color="#505050", 
                       text_color="white", font=("Helvetica", 40), hover_color="#7D7D7D", 
                       anchor="center",border_width=2, border_color="#A2A0A0", command=buttonminus).grid(row=2, column=3, padx= 15, pady=15)
button = ctk.CTkButton(app, text="1", corner_radius=10, height= 60, width=60, fg_color="#505050", 
                       text_color="white", font=("Helvetica", 37), hover_color="#7D7D7D", 
                       anchor="center",border_width=2, border_color="#A2A0A0", command=button1).grid(row=3, column=0, padx= 15, pady=15)
button = ctk.CTkButton(app, text="2", corner_radius=10, height= 60, width=60, fg_color="#505050", 
                       text_color="white", font=("Helvetica", 37), hover_color="#7D7D7D", 
                       anchor="center",border_width=2, border_color="#A2A0A0", command=button2).grid(row=3, column=1, padx= 12, pady=15)
button = ctk.CTkButton(app, text="3", corner_radius=10, height= 60, width=60, fg_color="#505050", 
                       text_color="white", font=("Helvetica", 37), hover_color="#7D7D7D", 
                       anchor="center",border_width=2, border_color="#A2A0A0", command=button3).grid(row=3, column=2, padx= 15, pady=15)
button = ctk.CTkButton(app, text="+", corner_radius=10, height= 60, width=60, fg_color="#505050", 
                       text_color="white", font=("Helvetica", 40), hover_color="#7D7D7D", 
                       anchor="center",border_width=2, border_color="#A2A0A0", command=buttonplus).grid(row=3, column=3, padx= 15, pady=15)
button = ctk.CTkButton(app, text=" ", corner_radius=10, height= 60, width=60, fg_color="#505050", 
                       text_color="white", font=("Helvetica", 37), hover_color="#7D7D7D", 
                       anchor="center",border_width=2, border_color="#A2A0A0", command=button1).grid(row=4, column=0, padx= 15, pady=15)
button = ctk.CTkButton(app, text="0", corner_radius=10, height= 60, width=60, fg_color="#505050", 
                       text_color="white", font=("Helvetica", 37), hover_color="#7D7D7D", 
                       anchor="center",border_width=2, border_color="#A2A0A0", command=button0).grid(row=4, column=1, padx= 12, pady=15)
button = ctk.CTkButton(app, text=",", corner_radius=10, height= 60, width=60, fg_color="#505050", 
                       text_color="white", font=("Helvetica", 50), hover_color="#7D7D7D", 
                       anchor="s",border_width=2, border_color="#A2A0A0", command=buttoncel).grid(row=4, column=2, padx= 15, pady=15)
button = ctk.CTkButton(app, text="×", corner_radius=10, height= 60, width=60, fg_color="#505050", 
                       text_color="white", font=("Helvetica", 40), hover_color="#7D7D7D", 
                       anchor="center",border_width=2, border_color="#A2A0A0", command=buttonumn).grid(row=4, column=3, padx= 15, pady=15)

app.mainloop()