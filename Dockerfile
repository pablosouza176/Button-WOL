FROM python:3.12-slim

# Instala wakeonlan e cliente SSH
RUN apt-get update && apt-get install -y --no-install-recommends \
  wakeonlan \
  openssh-client \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8081

CMD ["python", "app.py"]
