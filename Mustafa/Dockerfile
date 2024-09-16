# ?? not sure
FROM python:3.11

# main file
WORKDIR fixture_project


#requir...
COPY requirements.txt ./

#requirements install
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


#allpyfilesanddags
COPY . /fixture_project


#app running
CMD ["airflow", "webserver", "--port", "8080"]
