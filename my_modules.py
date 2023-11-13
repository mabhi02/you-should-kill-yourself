from flask import Flask, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/run_files', methods=['POST'])
def run_files():
    # Replace 'file1.py', 'file2.py', and 'file3.py' with your actual file names
    files_to_run = ['file1.py', 'file2.py', 'file3.py']

    for file in files_to_run:
        try:
            # Run each file using subprocess
            subprocess.run(['python', py/], check=True)
        except subprocess.CalledProcessError as e:
            # Handle errors, if any
            return f"Error running {file}: {e}", 500

    return "Files executed successfully!"

if __name__ == '__main__':
    app.run(debug=True)
