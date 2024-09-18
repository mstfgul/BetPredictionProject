FROM python:3.11

WORKDIR fixture_project

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /fixture_project

RUN airflow db init

CMD ["sh", "-c", "airflow webserver --port 8080 & streamlit run Bet_Prediction.py"]
