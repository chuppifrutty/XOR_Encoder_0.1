from CodeGenerator import CodeGenerator
from SimpleEncryptor import SimpleEncryptor
from SimpleCompressor import SimpleCompressor
from tkinter import filedialog, messagebox
import tkinter as tk
import os

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Шифратор")

        font1 = ("Helvetica", 12)
        font2 = ("Helvetica", 20)

        self.label_file = tk.Label(root, text="Выберите файл")
        self.label_file.grid(row=0, column=0, padx=10, pady=5)

        self.button_browse = tk.Button(root, text="🔍", font=font1, command=self.browse_file)
        self.button_browse.grid(row=0, column=1, padx=10, pady=5)

        self.label_filename = tk.Label(root, text="", width=10, anchor="w")
        self.label_filename.grid(row=0, column=2, padx=10, pady=5)

        self.label_operation = tk.Label(root, text="Выберите операцию")
        self.label_operation.grid(row=1, column=0, padx=10, pady=5)

        self.operation = tk.StringVar(value="encrypt")
        self.radio_encrypt = tk.Radiobutton(root, text="🔐", font=font2, variable=self.operation, value="encrypt", command=self.update_ui)
        self.radio_encrypt.grid(row=1, column=1, padx=5, pady=5)

        self.radio_decrypt = tk.Radiobutton(root, text="🔓", font=font2, variable=self.operation, value="decrypt", command=self.update_ui)
        self.radio_decrypt.grid(row=1, column=2, padx=5, pady=5)

        self.label_code = tk.Label(root, text="Вставьте код")
        self.label_code.grid(row=2, column=0, padx=10, pady=5)

        self.entry_code = tk.Entry(root)
        self.entry_code.grid(row=2, column=1, columnspan=2, padx=10, pady=5)
        self.entry_code.config(state=tk.NORMAL)
        self.entry_code.event_add('<<Paste>>', '<Control-igrave>')


        self.use_compression = tk.BooleanVar()
        self.check_compression = tk.Checkbutton(root, text="Использовать компрессию", variable=self.use_compression)
        self.check_compression.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

        self.button_submit = tk.Button(root, text="Начать", command=self.process_file)
        self.button_submit.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        self.file_path = None

        self.update_ui()

    def update_ui(self):
        if self.operation.get() == "encrypt":
            self.label_code.grid_remove()
            self.entry_code.grid_remove()
            self.check_compression.grid(row=3, column=0, columnspan=3, padx=10, pady=5)
        else:
            self.label_code.grid(row=2, column=0, padx=10, pady=5)
            self.entry_code.grid(row=2, column=1, columnspan=2, padx=10, pady=5)
            self.check_compression.grid_remove()

    def browse_file(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            filename = os.path.basename(self.file_path)
            self.label_filename.config(text=filename[:8] + '...' if len(filename) > 8 else filename)

    def process_file(self):
        if not self.file_path:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите файл.")
            return

        operation = self.operation.get()
        code = self.entry_code.get()
        use_compression = self.use_compression.get()

        with open(self.file_path, 'rb') as file:
            data = file.read()

        if operation == "encrypt":
            code = CodeGenerator.generate_code()
            processed_data = SimpleEncryptor.encrypt(data, code.encode())
            if use_compression:
                processed_data = SimpleCompressor.compress(processed_data)
            processed_file_path = os.path.join(os.path.dirname(self.file_path),
                                               'ENC_' + os.path.basename(self.file_path))
            with open(processed_file_path, 'wb') as file:
                file.write(processed_data)
            self.copy_to_clipboard(code)
            messagebox.showinfo("Успех", f"Файл успешно зашифрован. Код дешифровки скопирован в буфер обмена: {code}")
        elif operation == "decrypt":
            if not code:
                messagebox.showerror("Ошибка", "Для дешифровки требуется код.")
                return
            if use_compression:
                data = SimpleCompressor.decompress(data)
            processed_data = SimpleEncryptor.decrypt(data, code.encode())
            processed_file_path = os.path.join(os.path.dirname(self.file_path),
                                               'DEC_' + os.path.basename(self.file_path))
            with open(processed_file_path, 'wb') as file:
                file.write(processed_data)
            messagebox.showinfo("Успех", "Файл успешно дешифрован.")
        else:
            messagebox.showerror("Ошибка", "Неверная операция.")
            return

        self.file_path = None
        self.label_filename.config(text="")

    def copy_to_clipboard(self, text):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
