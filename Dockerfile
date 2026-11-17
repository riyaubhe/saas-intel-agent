FROM python:3.12-slim

WORKDIR /app

# install packages first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# then copy the code
COPY . .

EXPOSE 8501

# start the dashboard
CMD ["streamlit", "run", "dashboard.py", "--server.address=0.0.0.0"]
