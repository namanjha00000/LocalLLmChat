@echo off

:: Create a virtual environment
python -m venv venv

:: Activate the virtual environment
call venv\Scripts\activate

:: Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

:: Run Streamlit app
streamlit run main.py
