FROM python:3.10.13-alpine
EXPOSE 5000

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./ .


CMD ["python","waitress_model_openai.py"]