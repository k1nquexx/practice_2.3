import tkinter as tk
from tkinter import messagebox
import psutil


def update_info():
    try:
        cpu_load = psutil.cpu_percent()
        ram_load = psutil.virtual_memory().percent
        disk_load = psutil.disk_usage('/').percent

        lbl_cpu.config(text=f"Загрузка CPU: {cpu_load}%")
        lbl_ram.config(text=f"Использование RAM: {ram_load}%")
        lbl_disk.config(text=f"Загруженность диска: {disk_load}%")

        window.after(1000, update_info)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Сбой при получении данных: {e}")


window = tk.Tk()
window.title("Задание 2: Монитор ресурсов")
window.geometry("300x200")

tk.Label(window, text="Системный монитор", font=("Arial", 14)).pack(pady=10)

lbl_cpu = tk.Label(window, text="Загрузка CPU: ...", font=("Arial", 12))
lbl_cpu.pack(pady=5)

lbl_ram = tk.Label(window, text="Использование RAM: ...", font=("Arial", 12))
lbl_ram.pack(pady=5)

lbl_disk = tk.Label(window, text="Загруженность диска: ...", font=("Arial", 12))
lbl_disk.pack(pady=5)

update_info()

window.mainloop()