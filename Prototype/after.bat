@echo off
call .\.venv\Scripts\activate
pip install Flask
pip freeze > requirements.txt
python app.py
