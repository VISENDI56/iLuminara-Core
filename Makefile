.PHONY: setup test run clean audit docker-build

setup:
	@echo "[*] Setting up iLuminara Environment..."
	pip install -r requirements.txt
	chmod +x scripts/configure_gpu.sh
	./scripts/configure_gpu.sh

test:
	@echo "[*] Running Unit Tests..."
	python3 -m pytest tests/

stress-test:
	@echo "[*] Running Ghost-Nexus Simulation..."
	python3 tests/simulation/ghost_nexus.py

run:
	@echo "[*] Launching Enterprise Command Center..."
	streamlit run Home.py

audit:
	@echo "[*] Generating Transparency & Security Audit..."
	python3 -m pytest tests/ --cov=core
	trivy fs .

docker-build:
	docker build -t iluminara-core:latest .

clean:
	rm -rf __pycache__ .pytest_cache .coverage