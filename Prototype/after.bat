@echo off
call .\.venv\Scriptsctivate
pip install Flask
pip freeze > requirements.txt
python app.py
