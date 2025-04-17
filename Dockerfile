#Use a more compatible base image
#FROM python:3.11-slim

# Set working directory
#WORKDIR /app

# Install system dependencies (optional, for safety)
#RUN apt-get update && apt-get install -y build-essential && apt-get clean

# Copy and install Python dependencies
#COPY requirements.txt .
#RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy your notebook or app
#COPY women_health/main.ipynb .

# Expose Jupyter Notebook port
#EXPOSE 8888

# Run Jupyter Notebook
#CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
#CMD ["uvicorn", "women_health.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y build-essential gcc \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean

COPY women_health ./women_health


CMD ["uvicorn", "women_health.main:app", "--host", "0.0.0.0", "--port", "8000"]


