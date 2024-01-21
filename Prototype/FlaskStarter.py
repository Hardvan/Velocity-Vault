import os
import subprocess
import threading


# Function to create virtual environment
def create_venv():
    subprocess.run(["python", "-m", "venv", ".venv"], check=True)


# Create a thread for creating the virtual environment
venv_thread = threading.Thread(target=create_venv)
venv_thread.start()
print("🧵 Starting virtual environment creation via thread...")


# Create app.py (overwrite if exists)
app_code = '''from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
'''
with open("app.py", "w") as app_file:
    app_file.write(app_code)
print("✅ Created app.py")

# Set up templates and static folders (overwrite if exists)
os.makedirs("templates", exist_ok=True)
os.makedirs("static/css", exist_ok=True)
os.makedirs("static/js", exist_ok=True)
os.makedirs("static/images", exist_ok=True)
os.makedirs("static/favicon", exist_ok=True)
print("✅ Created templates and static folders")

# Inside templates folder, create index.html (overwrite if exists)
index_html_code = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>

    <!-- Favicon -->
    <link
      rel="shortcut icon"
      href="{{ url_for('static', filename='favicon/favicon.png') }}"
      type="image/x-icon"
    />

    <!-- Custom CSS -->
    <link
      rel="stylesheet"
      href="{{ url_for('static', filename='css/index.css') }}"
    />
  </head>

  <body>
    <h1 class="title">Hello, World!</h1>

    <!-- Custom JS -->
    <script src="{{ url_for('static', filename='js/index.js') }}"></script>
  </body>
</html>

"""
with open("templates/index.html", "w") as index_html:
    index_html.write(index_html_code)
print("✅ Created index.html")

# Inside static folder, create css/index.css and js/index.js (overwrite if exists)
css_code = """html {
  padding: 0;
  margin: 0;
}

body {
  padding: 0;
  margin: 0;
}

/* Disable vertical scrollbar */
::-webkit-scrollbar {
  display: none;
}

.title {
  font-size: 3rem;
  text-align: center;
}
\n"""
with open("static/css/index.css", "w") as css_file:
    css_file.write(css_code)
print("✅ Created index.css")

js_code = '// Add your JavaScript code here\n'
with open("static/js/index.js", "w") as js_file:
    js_file.write(js_code)
print("✅ Created index.js")

# Create .gitignore (overwrite if exists)
gitignore_content = '.venv/\n__pycache__/\n.vscode/\n.env\n'
with open(".gitignore", "w") as gitignore_file:
    gitignore_file.write(gitignore_content)
print("✅ Created .gitignore")

print("🎉 Flask project setup complete.")
print("📦 Installing dependencies...")

# Wait for virtual environment to be created
venv_thread.join()
print("✅ Virtual environment created")

# Create the batch file
batch_content = '''@echo off
call .\.venv\Scripts\\activate
pip install Flask
pip freeze > requirements.txt
python app.py
'''
with open("after.bat", "w") as batch_file:
    batch_file.write(batch_content)
print("✅ Created batch file")

# Execute the batch file
subprocess.run(["after.bat"], shell=True, check=True)
print("✅ Installed dependencies")


print("Run the following commands to complete the setup:")

print("\n1️⃣  Activate the virtual environment:")
print("For Windows:")
print(".\.venv\Scripts\\activate")
print("For Mac/Linux:")
print("source .venv/bin/activate")

print("\n2️⃣  Run the app:")
print("python app.py")

print("\nHappy coding 😊 !")
