from flask import Flask, render_template, request, jsonify
import ast

app = Flask(__name__)

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

assistant = CodeLearningAssistant()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    operation = data.get('operation')
    code = data.get('code', '')
    topic = data.get('topic', '')

    if operation == 'analyze':
        valid, message = assistant.analyze_code(code)
        return jsonify({'result': message})

    elif operation == 'debug':
        message = assistant.debug_code(code)
        return jsonify({'result': message})

    elif operation == 'hint':
        message = assistant.provide_hint(code)
        return jsonify({'result': message})

    elif operation == 'example':
        message = assistant.generate_example(topic)
        return jsonify({'result': message})

    return jsonify({'result': 'Invalid operation'})

if __name__ == '__main__':
    app.run(debug=True)
