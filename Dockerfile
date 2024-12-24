FROM python:3.12-slim-bullseye
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org
COPY . .
CMD ["uvicorn", "app.summer-api.main:app", "--host", "0.0.0.0", "--port", "$PORT"] 

