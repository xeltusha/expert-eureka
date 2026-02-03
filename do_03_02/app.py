import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import random

def saglabat_datus():
    vards = entry_vards.get()
    uzvards = entry_uzvards.get()
    pers_kods = entry_pk.get()
    talrunis = entry_talrunis.get()
    izveletais_pakalpojums = combo_pakalpojums.get()



    con = None
    try:
        con = sqlite3.connect('IKT.db')
        cursor = con.cursor()
 
        cursor.execute("INSERT INTO Klienti (vards, uzvards, pers_kods, talrunis) VALUES (?, ?, ?, ?)",
                       (vards, uzvards, pers_kods, talrunis))
        

        jaunais_klients_id = cursor.lastrowid

        cursor.execute("SELECT Pakalpojums_id FROM Pakalpojumi WHERE apraksts = ?", (izveletais_pakalpojums,))
        rezultats_pakalpojums = cursor.fetchone()

        if rezultats_pakalpojums:
            pakalpojums_id = rezultats_pakalpojums[0]

            cursor.execute("SELECT Darbinieks_id FROM Darbinieki")
            visi_darbinieki = cursor.fetchall()
            
            if visi_darbinieki:
                darbinieks_id = random.choice(visi_darbinieki)[0]

                cursor.execute("INSERT INTO Pasutijumi (Klients_id, Darbinieks_id, Pakalpojums_id) VALUES (?, ?, ?)",
                               (jaunais_klients_id, darbinieks_id, pakalpojums_id))
            

        con.commit()
        messagebox.showinfo("Veiksmīgi", "Jūsu dati tiek apstradāti un iekļauti datu bāzē!")

        
        entry_vards.delete(0, tk.END)
        entry_uzvards.delete(0, tk.END)
        entry_pk.delete(0, tk.END)
        entry_talrunis.delete(0, tk.END)
        combo_pakalpojums.set('')

    except sqlite3.Error as e:
        messagebox.showerror("Kļūda", f"Notika kļūda ar datu bāzi: {e}")
    finally:
        if con:
            con.close()


root = tk.Tk()
root.title("IKT Pakalpojumu Pieteikšana")
root.geometry("400x350")


label_virsraksts = tk.Label(root, text="Pieteikt Pakalpojumu", font=("Arial", 14, "bold"))
label_virsraksts.pack(pady=10)


frame = tk.Frame(root)
frame.pack()


label_vards = tk.Label(frame, text="Vārds:")
label_vards.grid(row=0, column=0, sticky="e", padx=10, pady=5)
entry_vards = tk.Entry(frame)
entry_vards.grid(row=0, column=1, padx=10, pady=5)


label_uzvards = tk.Label(frame, text="Uzvārds:")
label_uzvards.grid(row=1, column=0, sticky="e", padx=10, pady=5)
entry_uzvards = tk.Entry(frame)
entry_uzvards.grid(row=1, column=1, padx=10, pady=5)


label_pk = tk.Label(frame, text="Personas kods:")
label_pk.grid(row=2, column=0, sticky="e", padx=10, pady=5)
entry_pk = tk.Entry(frame)
entry_pk.grid(row=2, column=1, padx=10, pady=5)


label_talrunis = tk.Label(frame, text="Tālrunis:")
label_talrunis.grid(row=3, column=0, sticky="e", padx=10, pady=5)
entry_talrunis = tk.Entry(frame)
entry_talrunis.grid(row=3, column=1, padx=10, pady=5)


label_pakalpojums = tk.Label(frame, text="Pakalpojums:")
label_pakalpojums.grid(row=4, column=0, sticky="e", padx=10, pady=5)


pakalpojumu_saraksts = [
    "operētājsistēmas pārinstalēšana",
    "datu bāzes veidošana",
    "mākoņpakalpojumi"
]
combo_pakalpojums = ttk.Combobox(frame, values=pakalpojumu_saraksts, state="readonly")
combo_pakalpojums.grid(row=4, column=1, padx=10, pady=5)


btn_sutit = tk.Button(root, text="SŪTĪT", command=saglabat_datus, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
btn_sutit.pack(pady=20, ipadx=20)


root.mainloop()