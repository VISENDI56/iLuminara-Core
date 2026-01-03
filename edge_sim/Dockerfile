FROM nvcr.io/nvidia/l4t-pytorch:r36.2.0-pth2.3-py3  # Jetson L4T base (Orin-compatible)

RUN apt-get update && apt-get install -y python3-pip git
COPY requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

WORKDIR /app
COPY . /app

CMD ["python", "demo_full_integration.py"]
