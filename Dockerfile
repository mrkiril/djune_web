FROM python:3.11-slim
WORKDIR /app

RUN pip3 install --upgrade pip wheel

ADD requirements .
RUN pip3 --no-cache-dir install -r ./dev.txt

RUN rm -rf ~/.cache/pip
COPY . .

CMD ["python3", "main.py"]
