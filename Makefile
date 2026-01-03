.PHONY: help install test validate deploy clean docker docker-run

help:
@echo "iLuminara-Core Development Commands:"
@echo "  make install     Install dependencies"
@echo "  make test        Run tests"
@echo "  make validate    Run security validation"
@echo "  make deploy      Deploy edge node"
@echo "  make clean       Clean temporary files"
@echo "  make docker      Build Docker image"
@echo "  make docker-run  Run Docker container"

install:
pip install -r requirements.txt

test:
python -m pytest tests/ -v

validate:
./scripts/validation/validate_fortress.sh

deploy:
./scripts/deployment/deploy_edge_node.sh test solar 131072 minimal

clean:
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete
find . -type f -name ".coverage" -delete
find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name "*.egg" -exec rm -rf {} + 2>/dev/null || true

docker:
docker build -t iluminara-core:latest .

docker-run:
docker run -p 8501:8501 iluminara-core:latest
