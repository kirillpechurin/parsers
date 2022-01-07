FROM python:3.8.3
WORKDIR /frontend
COPY requirements.txt requirements.txt
RUN /usr/local/bin/python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
