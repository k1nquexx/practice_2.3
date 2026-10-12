import tkinter as tk
from tkinter import messagebox
import requests


def check_sites():
    urls = [
        "https://github.com/",
        "https://www.binance.com/en",
        "https://moodle-tomtit.tomsk.ru/",
        "https://jsonplaceholder.typicode.com/",
    ]

    text_box.delete("1.0", tk.END)

    for url in urls:
        try:
            res = requests.get(url, timeout=3)
            code = res.status_code

            if 200 <= code < 300:
                status = "доступен"
            elif code == 401 or code == 403:
                status = "вход запрещен"
            elif code == 404:
                status = "не найден"
            elif code >= 500:
                status = "ошибка сервера"
            else:
                status = "неизвестно"

            result_string = f"{url} - {status} - {code}\n"
            text_box.insert(tk.END, result_string)

        except requests.exceptions.RequestException:
            text_box.insert(tk.END, f"{url} - не доступен - Ошибка сети\n")

    messagebox.showinfo("Готово", "Все сайты проверены!")


window = tk.Tk()
window.title("Задание 1: Статус сайтов")
window.geometry("500x350")

label = tk.Label(window, text="Нажмите кнопку для проверки сайтов:")
label.pack(pady=10)

btn = tk.Button(window, text="Проверить", command=check_sites)
btn.pack(pady=5)

text_box = tk.Text(window, height=12, width=60)
text_box.pack(pady=10)

window.mainloop()
