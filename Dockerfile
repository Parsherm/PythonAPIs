FROM python:3.11

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-tk \
        tk \
        libgl1-mesa-glx \
        libx11-6 \
        libxext6 \
        libxrender1 \
        libsm6 \
        libice6 \
        wget \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
