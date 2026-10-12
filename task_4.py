import tkinter as tk
from tkinter import messagebox
import requests


def fetch_profile():
    user = entry.get()
    if user == "":
        messagebox.showwarning("Внимание", "Сначала введите имя пользователя!")
        return

    try:
        url = f"https://api.github.com/users/{user}"
        res = requests.get(url)
        data = res.json()

        # Если гитхаб вернул сообщение Not Found
        if data.get('message') == 'Not Found':
            messagebox.showerror("Ошибка", "Такого пользователя нет на GitHub.")
            return

        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, "=== ИНФОРМАЦИЯ О ПРОФИЛЕ ===\n")
        text_box.insert(tk.END, f"Имя: {data.get('name', 'Не указано')}\n")
        text_box.insert(tk.END, f"Ссылка: {data.get('html_url')}\n")
        text_box.insert(tk.END, f"Кол-во репозиториев: {data.get('public_repos')}\n")
        text_box.insert(tk.END, f"Подписчиков: {data.get('followers')}\n")
        text_box.insert(tk.END, f"Подписок: {data.get('following')}\n")

    except Exception as e:
        messagebox.showerror("Ошибка сети", str(e))


def fetch_repos():
    user = entry.get()
    if user == "":
        messagebox.showwarning("Внимание", "Сначала введите имя пользователя!")
        return

    try:
        url = f"https://api.github.com/users/{user}/repos"
        res = requests.get(url)
        data = res.json()

        if type(data) == dict and data.get('message') == 'Not Found':
            messagebox.showerror("Ошибка", "Пользователь не найден.")
            return

        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, f"=== РЕПОЗИТОРИИ ПОЛЬЗОВАТЕЛЯ {user} ===\n")

        for item in data:
            repo_name = item.get('name')
            language = item.get('language', 'Не определен')
            visibility = item.get('visibility', 'public')
            branch = item.get('default_branch')

            text_box.insert(tk.END, f"Название: {repo_name}\n")
            text_box.insert(tk.END, f"Язык: {language} | Ветка: {branch} | Статус: {visibility}\n")
            text_box.insert(tk.END, "-" * 40 + "\n")

    except Exception as e:
        messagebox.showerror("Ошибка сети", str(e))


window = tk.Tk()
window.title("Задание 4: GitHub API")
window.geometry("550x450")

tk.Label(window, text="Введите логин на GitHub:").pack(pady=5)

entry = tk.Entry(window, width=30)
entry.pack(pady=5)

btn_frame = tk.Frame(window)
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="Получить профиль", command=fetch_profile).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Получить репозитории", command=fetch_repos).grid(row=0, column=1, padx=5)

text_box = tk.Text(window, width=60, height=20)
text_box.pack(pady=10)

window.mainloop()