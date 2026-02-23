import tkinter
from tkinter import scrolledtext, messagebox, filedialog, ttk
import pyperclip
from parser import compute_halstead

class RustParserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Анализатор метрик Холстеда (Rust)")
        self.root.configure(bg="#e2dbcc")
        self.root.geometry('712x500')
        self.root.resizable(False, False)

# region внешний вид

        main_frame = tkinter.Frame(root, bg="#ffffff")
        main_frame.pack(fill='both', expand=True, padx=8, pady=8)

        
        self.text_area = scrolledtext.ScrolledText(main_frame, width=50, height=25, wrap='none', font=('Consolas', 10))
        self.text_area.grid(row=0, column=0, padx=4, pady=4, sticky='nsew')
        self.text_area.insert('1.0', 'Введите код на Rust для анализа...')

        btn_frame = tkinter.Frame(main_frame, bg="#ffffff")
        btn_frame.grid(row=1, column=0, pady=4)

        tkinter.Button(btn_frame, text="Открыть файл", command=self.load_file, width=25).grid(row=0, column=0, padx=2)
        # tkinter.Button(btn_frame, text="Вставить из буфера", command=self.paste_code, width=16).grid(row=0, column=1, padx=2)
        tkinter.Button(btn_frame, text="Рассчитать метрики", command=self.parse_code, width=25).grid(row=0, column=1, padx=2)

        
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=0, column=1, rowspan=2, padx=4, pady=4, sticky='nsew')

        
        metrics_frame = tkinter.Frame(self.notebook)
        self.metrics_tree = ttk.Treeview(metrics_frame, columns=('metric', 'value'), show='headings', height=20)
        self.metrics_tree.heading('metric', text='Метрика')
        self.metrics_tree.heading('value', text='Значение')
        self.metrics_tree.column('metric', width=200, anchor='w')
        self.metrics_tree.column('value', width=100, anchor='center')
        self.metrics_tree.pack(fill='both', expand=True)
        self.notebook.add(metrics_frame, text='Метрики')

        
        ops_frame = tkinter.Frame(self.notebook)
        self.ops_tree = ttk.Treeview(ops_frame, columns=('idx', 'op', 'freq'), show='headings', height=20)
        self.ops_tree.heading('idx', text='№')
        self.ops_tree.heading('op', text='Оператор')
        self.ops_tree.heading('freq', text='f1j')
        self.ops_tree.column('idx', width=40, anchor='center')
        self.ops_tree.column('op', width=180, anchor='w')
        self.ops_tree.column('freq', width=80, anchor='center')
        self.ops_tree.pack(fill='both', expand=True)
        self.notebook.add(ops_frame, text='Операторы')

        
        opd_frame = tkinter.Frame(self.notebook)
        self.opd_tree = ttk.Treeview(opd_frame, columns=('idx', 'operand', 'freq'), show='headings', height=20)
        self.opd_tree.heading('idx', text='№')
        self.opd_tree.heading('operand', text='Операнд')
        self.opd_tree.heading('freq', text='f2i')
        self.opd_tree.column('idx', width=40, anchor='center')
        self.opd_tree.column('operand', width=180, anchor='w')
        self.opd_tree.column('freq', width=80, anchor='center')
        self.opd_tree.pack(fill='both', expand=True)
        self.notebook.add(opd_frame, text='Операнды')

#endregion

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("Rust files", "*.rs"), ("All files", "*.*")])
        if path:
            with open(path, "r", encoding="utf8") as f:
                self.text_area.delete("1.0", tkinter.END)
                self.text_area.insert(tkinter.END, f.read())

    # def paste_code(self):
    #     self.text_area.delete("1.0", tkinter.END)
    #     self.text_area.insert(tkinter.END, pyperclip.paste())

    def parse_code(self):
        code = self.text_area.get("1.0", tkinter.END).strip()
        if not code:
            messagebox.showwarning("Ошибка", "Введите код для анализа")
            return
        try:
            metrics, operators, operands = compute_halstead(code)

            # Метрики
            for i in self.metrics_tree.get_children():
                self.metrics_tree.delete(i)
            for k, v in metrics.items():
                self.metrics_tree.insert('', tkinter.END, values=(k, v))

            # Операторы
            for i in self.ops_tree.get_children():
                self.ops_tree.delete(i)
            for idx, (k, v) in enumerate(operators.items(), start=1):
                self.ops_tree.insert('', tkinter.END, values=(idx, k, v))

            # Операнды
            for i in self.opd_tree.get_children():
                self.opd_tree.delete(i)
            for idx, (k, v) in enumerate(operands.items(), start=1):
                self.opd_tree.insert('', tkinter.END, values=(idx, k, v))

            self.notebook.select(0)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
