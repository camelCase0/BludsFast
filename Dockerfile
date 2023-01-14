FROM python
WORKDIR /code
COPY ./requirements.txt .
RUN pip install -r ./requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
