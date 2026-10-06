FROM python:3.11-slim
WORKDIR /work
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY data ./data
COPY experiments ./experiments
COPY tests ./tests
CMD ["python", "experiments/02_benchmark_scoring.py"]
