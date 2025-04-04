import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
import sys

def format_time(timedelta_obj):
    hours, remainder = divmod(timedelta_obj.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def arbeitszeit_berechnen():
    ankunftszeit = eingabe.get()
    try:
        ankunft_datetime = datetime.strptime(ankunftszeit, "%H:%M")
        aktuelle_zeit = datetime.now().replace(year=1900, month=1, day=1)
        
        gearbeitete_zeit = aktuelle_zeit - ankunft_datetime
        erforderliche_arbeitszeit = timedelta(hours=8, minutes=9)
        verbleibende_zeit = erforderliche_arbeitszeit - gearbeitete_zeit
        max_arbeitszeit = timedelta(hours=10, minutes=45)
        
        if verbleibende_zeit.total_seconds() > 0:
            nachricht = f"Arbeitszeit: {format_time(gearbeitete_zeit)}\n"
            nachricht += f"Verbleibend: {format_time(verbleibende_zeit)}\n"
            feierabend = aktuelle_zeit + verbleibende_zeit
            nachricht += f"Feierabend: {feierabend.strftime('%H:%M')}\n"
            max_feierabend = ankunft_datetime + max_arbeitszeit
            nachricht += f"Spätester Feierabend: {max_feierabend.strftime('%H:%M')}"
            ergebnis_label.config(text=nachricht, foreground="green")
        else:
            nachricht = f"Arbeitszeit abgeschlossen!\n"
            nachricht += f"Überstunden: {format_time(abs(verbleibende_zeit))}\n"
            max_feierabend = ankunft_datetime + max_arbeitszeit
            nachricht += f"Spätester Feierabend: {max_feierabend.strftime('%H:%M')}"
            ergebnis_label.config(text=nachricht, foreground="red")
        
        eingabe.pack_forget()
        berechnen_button.pack_forget()
        zuruck_button.pack(pady=15)
        title_label.config(text="Ihre Arbeitszeiten")
    except ValueError:
        messagebox.showerror("Fehler", "Bitte geben Sie die Zeit im Format HH:MM ein.")

    root.after(1000, update_time)  # Refresh every second

def update_time():
    if zuruck_button.winfo_viewable():
        arbeitszeit_berechnen()

def zuruck_zur_eingabe():
    ergebnis_label.config(text="", foreground="black")
    zuruck_button.pack_forget()
    eingabe.pack()
    berechnen_button.pack(pady=15)
    title_label.config(text="Ankunftszeit (HH:MM):")


def on_closing():
    if messagebox.askokcancel("Beenden :'(", "SICHER?"):
        root.destroy()
        sys.exit()

root = tk.Tk()
root.title("Arbeitszeitrechner")
root.geometry("400x300")
root.configure(bg="#f0f0f0")  # Light gray background

style = ttk.Style()
style.theme_use('clam')
style.configure("TFrame", background="#f0f0f0")
style.configure("TLabel", background="#f0f0f0", foreground="#333333")
style.configure("TButton", background="#4CAF50", foreground="white")
style.map("TButton", background=[('active', '#45a049')])
style.configure("TEntry", fieldbackground="white", foreground="#333333")

main_frame = ttk.Frame(root, padding="20", style="TFrame")
main_frame.pack(fill=tk.BOTH, expand=True)

title_label = ttk.Label(main_frame, text="Ankunftszeit (HH:MM):", font=('Roboto', 14, 'bold'), style="TLabel")
title_label.pack(pady=(0, 10))

eingabe = ttk.Entry(main_frame, font=('Roboto', 12), width=10, justify='center', style="TEntry")
eingabe.pack()

berechnen_button = ttk.Button(main_frame, text="Berechnen", command=arbeitszeit_berechnen, style="TButton")
berechnen_button.pack(pady=15)

zuruck_button = ttk.Button(main_frame, text="Zurück zur Eingabe", command=zuruck_zur_eingabe, style="TButton")

ergebnis_label = ttk.Label(main_frame, text="", wraplength=350, justify="center", font=('Roboto', 11), style="TLabel")
ergebnis_label.pack(pady=10)

luca_label = ttk.Label(root, text="Von Luca :3", font=('Roboto', 8), style="TLabel")
luca_label.pack(side=tk.BOTTOM, anchor=tk.SW, padx=5, pady=5)

root.bind('<Return>', lambda event: arbeitszeit_berechnen())

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()