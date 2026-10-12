import tkinter as tk
from tkinter import messagebox, simpledialog
import requests
import json
import os

API_URL = "https://www.cbr-xml-daily.ru/daily_json.js"
FILE_NAME = "save.json"

user_groups = {}


def get_data_from_api():
    try:
        res = requests.get(API_URL)
        data = res.json()
        return data.get('Valute', {})
    except Exception as e:
        messagebox.showerror("Ошибка", "Нет связи с API ЦБ.")
        return {}


def show_all_currencies():
    valutes = get_data_from_api()
    if not valutes: return

    text_box.delete("1.0", tk.END)
    for code, info in valutes.items():
        text_box.insert(tk.END, f"{code} ({info['Name']}): {info['Value']} руб.\n")


def find_currency():
    code = simpledialog.askstring("Поиск", "Введите код валюты (USD, EUR):")
    if code:
        code = code.upper()
        valutes = get_data_from_api()

        if code in valutes:
            name = valutes[code]['Name']
            value = valutes[code]['Value']
            messagebox.showinfo("Результат", f"{name}: {value} руб.")
        else:
            messagebox.showwarning("Ошибка", "Такой валюты нет.")


def add_group():
    global user_groups
    group_name = simpledialog.askstring("Группа", "Название новой группы:")
    if group_name:
        code = simpledialog.askstring("Валюта", "Какую валюту добавить (код):")
        if code:
            user_groups[group_name] = [code.upper()]
            save_to_json()


def save_to_json():
    try:
        with open(FILE_NAME, 'w', encoding='utf-8') as f:
            json.dump(user_groups, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Сохранение", "Группы сохранены в save.json")
    except Exception as e:
        messagebox.showerror("Ошибка", "Не удалось сохранить файл.")


def load_from_json():
    global user_groups
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, 'r', encoding='utf-8') as f:
                user_groups = json.load(f)
        except:
            user_groups = {}


def show_groups():
    load_from_json()
    text_box.delete("1.0", tk.END)

    if not user_groups:
        text_box.insert(tk.END, "Группы пока не созданы.\n")
        return

    valutes = get_data_from_api()
    for group, codes in user_groups.items():
        text_box.insert(tk.END, f"--- Группа: {group} ---\n")
        for c in codes:
            if c in valutes:
                text_box.insert(tk.END, f"  {c}: {valutes[c]['Value']} руб.\n")
            else:
                text_box.insert(tk.END, f"  {c}: Нет данных\n")


window = tk.Tk()
window.title("Задание 3: Курс валют")
window.geometry("500x450")

load_from_json()

btn_frame = tk.Frame(window)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Все валюты", command=show_all_currencies).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Найти валюту", command=find_currency).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Создать группу", command=add_group).grid(row=1, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="Показать группы", command=show_groups).grid(row=1, column=1, padx=5, pady=5)

text_box = tk.Text(window, width=55, height=20)
text_box.pack(pady=10)

window.mainloop()