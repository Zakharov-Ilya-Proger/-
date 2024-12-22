import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            if 'А' <= char <= 'Я':
                shift_base = ord('А')
                result += chr((ord(char) - shift_base + shift) % 32 + shift_base)
            elif 'а' <= char <= 'я':
                shift_base = ord('а')
                result += chr((ord(char) - shift_base + shift) % 32 + shift_base)
            else:
                result += char
        else:
            result += char
    return result

def encrypt():
    text = input_text_encrypt.get()
    shift = int(shift_encrypt.get())
    encrypted_text = caesar_cipher(text, shift)
    encrypted_text_var.set(encrypted_text)

def decrypt():
    text = input_text_decrypt.get()
    shift = int(shift_decrypt.get())
    decrypted_text = caesar_cipher(text, -shift)
    decrypted_text_var.set(decrypted_text)

# Создание основного окна
root = tk.Tk()
root.title("Шифр Цезаря")

# Создание фреймов для колонок
frame_encrypt = tk.Frame(root)
frame_encrypt.pack(side=tk.LEFT, padx=10, pady=10)

frame_decrypt = tk.Frame(root)
frame_decrypt.pack(side=tk.RIGHT, padx=10, pady=10)

# Ввод сообщения для зашифровки
input_label_encrypt = tk.Label(frame_encrypt, text="Ввод сообщения для зашифровки")
input_label_encrypt.pack()
input_text_encrypt = tk.Entry(frame_encrypt, width=50)
input_text_encrypt.pack()

# Поле для ввода сдвига для зашифровки
shift_label_encrypt = tk.Label(frame_encrypt, text="Сдвиг")
shift_label_encrypt.pack()
shift_encrypt = tk.Entry(frame_encrypt, width=10)
shift_encrypt.pack()

# Зашифрованное сообщение
encrypted_label = tk.Label(frame_encrypt, text="Зашифрованное сообщение")
encrypted_label.pack()
encrypted_text_var = tk.StringVar()
encrypted_text = tk.Entry(frame_encrypt, textvariable=encrypted_text_var, width=50)
encrypted_text.pack()

# Кнопка зашифровать
encrypt_button = tk.Button(frame_encrypt, text="Зашифровать", command=encrypt)
encrypt_button.pack()

# Ввод сообщения для расшифровки
input_label_decrypt = tk.Label(frame_decrypt, text="Ввод сообщения для расшифровки")
input_label_decrypt.pack()
input_text_decrypt = tk.Entry(frame_decrypt, width=50)
input_text_decrypt.pack()

# Поле для ввода сдвига для расшифровки
shift_label_decrypt = tk.Label(frame_decrypt, text="Сдвиг")
shift_label_decrypt.pack()
shift_decrypt = tk.Entry(frame_decrypt, width=10)
shift_decrypt.pack()

# Расшифрованное сообщение
decrypted_label = tk.Label(frame_decrypt, text="Расшифрованное сообщение")
decrypted_label.pack()
decrypted_text_var = tk.StringVar()
decrypted_text = tk.Entry(frame_decrypt, textvariable=decrypted_text_var, width=50)
decrypted_text.pack()

# Кнопка расшифровать
decrypt_button = tk.Button(frame_decrypt, text="Расшифровать", command=decrypt)
decrypt_button.pack()

# Запуск основного цикла
root.mainloop()
