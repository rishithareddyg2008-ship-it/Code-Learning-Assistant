import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import ast

class CodeLearningAssistant:
    def __init__(self):
        self.examples = {
            "for_loop": "for i in range(5):\n    print(i)",
            "if_statement": "x = 10\nif x > 5:\n    print('x is greater than 5')",
            "function": "def greet(name):\n    return f'Hello, {name}!'"
        }

    def analyze_code(self, code):
        try:
            ast.parse(code)
            return True, "Code syntax is correct."
        except SyntaxError as e:
            return False, f"Syntax Error: {e}"

    def debug_code(self, code):
        if "==" not in code and "if" in code:
            return "Hint: Are you missing '==' in your if condition?"
        if "def " in code and ":" not in code:
            return "Hint: Function definitions need a colon ':' at the end."
        return "No obvious issues detected."

    def generate_example(self, topic):
        return self.examples.get(topic, "Example not found for this topic.")

    def provide_hint(self, code):
        if "print(" not in code:
            return "Hint: Remember to use print() to display output."
        return "Keep up the good work!"

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Code Learning Assistant")
        self.geometry("700x600")

        self.assistant = CodeLearningAssistant()

        self.create_widgets()

    def create_widgets(self):
        # Code input area
        ttk.Label(self, text="Enter Your Code:").pack(anchor="w", padx=10, pady=(10, 0))
        self.code_input = scrolledtext.ScrolledText(self, height=10, width=80)
        self.code_input.pack(padx=10, pady=5)

        # Options frame
        options_frame = ttk.Frame(self)
        options_frame.pack(pady=10)

        ttk.Label(options_frame, text="Select Operation:").grid(row=0, column=0, sticky="w")

        self.operation = tk.StringVar(value="analyze")
        ttk.Radiobutton(options_frame, text="Analyze Code", variable=self.operation, value="analyze").grid(row=1, column=0, sticky="w")
        ttk.Radiobutton(options_frame, text="Debug Code", variable=self.operation, value="debug").grid(row=1, column=1, sticky="w")
        ttk.Radiobutton(options_frame, text="Provide Hint", variable=self.operation, value="hint").grid(row=1, column=2, sticky="w")
        ttk.Radiobutton(options_frame, text="Generate Example", variable=self.operation, value="example").grid(row=1, column=3, sticky="w")

        # Example topic entry (only for generate example)
        ttk.Label(options_frame, text="Example Topic:").grid(row=2, column=0, sticky="w", pady=(10,0))
        self.example_topic = ttk.Combobox(options_frame, values=["for_loop", "if_statement", "function"], state="readonly")
        self.example_topic.grid(row=2, column=1, sticky="w", pady=(10,0))
        self.example_topic.current(0)

        # Run button
        run_btn = ttk.Button(self, text="Run", command=self.run_operation)
        run_btn.pack(pady=10)

        # Output area
        ttk.Label(self, text="Output:").pack(anchor="w", padx=10)
        self.output_area = scrolledtext.ScrolledText(self, height=10, width=80, state="disabled")
        self.output_area.pack(padx=10, pady=5)

    def run_operation(self):
        op = self.operation.get()
        code = self.code_input.get("1.0", tk.END).strip()

        if op == "analyze":
            if not code:
                messagebox.showwarning("Input Needed", "Please enter code to analyze.")
                return
            valid, message = self.assistant.analyze_code(code)
            self.display_output(message)

        elif op == "debug":
            if not code:
                messagebox.showwarning("Input Needed", "Please enter code to debug.")
                return
            hint = self.assistant.debug_code(code)
            self.display_output(hint)

        elif op == "hint":
            if not code:
                messagebox.showwarning("Input Needed", "Please enter code for hints.")
                return
            hint = self.assistant.provide_hint(code)
            self.display_output(hint)

        elif op == "example":
            topic = self.example_topic.get()
            example = self.assistant.generate_example(topic)
            self.display_output(example)

    def display_output(self, message):
        self.output_area.config(state="normal")
        self.output_area.delete("1.0", tk.END)
        self.output_area.insert(tk.END, message)
        self.output_area.config(state="disabled")

if __name__ == "__main__":
    app = App()
    app.mainloop()
