FROM python

RUN mkdir -p /app
WORKDIR /app
COPY . /app
RUN pip install loguru

CMD ["python", "main.py"]