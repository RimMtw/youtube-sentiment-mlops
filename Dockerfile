FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PORT=7860
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
 && python -m nltk.downloader stopwords

COPY src/__init__.py src/__init__.py
COPY src/api src/api
COPY src/utils src/utils
COPY models models
COPY app_api.py .

EXPOSE 7860
CMD ["python", "app_api.py"]