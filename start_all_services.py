# ------------------------------------------------------------------------------
# Copyright (c) 2025 iLuminara (VISENDI56). All Rights Reserved.
# Licensed under the Polyform Shield License 1.0.0.
# 
# COMPETITOR EXCLUSION: Commercial use by entities offering Sovereign/Health OS 
# solutions is STRICTLY PROHIBITED without a commercial license.
# 
# The Sovereign Immune System (Omni-Law) and JEPA-MPC Architecture are 
# proprietary inventions of iLuminara.
# ------------------------------------------------------------------------------

#!/usr/bin/env python3
"""
iLuminara Multi-Service Launcher
═════════════════════════════════════════════════════════════════════════════

Starts all iLuminara services on their designated ports:
- Port 8080: Main API (voice processing, outbreak prediction)
- Port 8443: HTTPS API (TLS-enabled endpoints)
- Port 9090: Prometheus metrics exporter
- Port 5000: Governance service (sovereignty validation)
- Port 5001: Data fusion service (Golden Thread)
"""

import sys
import os
import subprocess
import time
import signal
from typing import List

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class ServiceManager:
    """Manages multiple iLuminara services."""
    
    def __init__(self):
        self.processes: List[subprocess.Popen] = []
        self.services = {
            'main_api': {'port': 8080, 'script': 'api_service.py'},
            'https_api': {'port': 8443, 'script': 'https_service.py'},
            'metrics': {'port': 9090, 'script': 'metrics_service.py'},
            'governance': {'port': 5000, 'script': 'governance_service.py'},
            'data_fusion': {'port': 5001, 'script': 'data_fusion_service.py'}
        }
    
    def start_service(self, name: str, config: dict):
        """Start a single service."""
        script = config['script']
        port = config['port']
        
        if not os.path.exists(script):
            print(f"⚠️  {name}: {script} not found, skipping...")
            return None
        
        print(f"Starting {name} on port {port}...")
        
        env = os.environ.copy()
        env['API_PORT'] = str(port)
        
        try:
            process = subprocess.Popen(
                [sys.executable, script],
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.processes.append(process)
            print(f"✓ {name} started (PID: {process.pid})")
            return process
        except Exception as e:
            print(f"✗ Failed to start {name}: {e}")
            return None
    
    def start_all(self):
        """Start all services."""
        print("=" * 80)
        print("iLuminara Multi-Service Launcher")
        print("=" * 80)
        print("")
        
        for name, config in self.services.items():
            self.start_service(name, config)
            time.sleep(1)  # Stagger startup
        
        print("")
        print("=" * 80)
        print("All Services Started")
        print("=" * 80)
        print("")
        self.print_status()
    
    def print_status(self):
        """Print status of all services."""
        print("Service Status:")
        print("")
        
        for name, config in self.services.items():
            port = config['port']
            script = config['script']
            
            if os.path.exists(script):
                # Check if process is running
                running = any(p.poll() is None for p in self.processes)
                status = "🟢 RUNNING" if running else "🔴 STOPPED"
            else:
                status = "⚪ NOT CONFIGURED"
            
            print(f"  {status}  Port {port}: {name}")
        
        print("")
        print("Available Endpoints:")
        print("  http://localhost:8080/health         - Main API health check")
        print("  http://localhost:8080/process-voice  - Voice processing")
        print("  http://localhost:8080/predict        - Outbreak prediction")
        print("  https://localhost:8443/health        - HTTPS API health check")
        print("  http://localhost:9090/metrics        - Prometheus metrics")
        print("  http://localhost:5000/validate       - Governance validation")
        print("  http://localhost:5001/fuse           - Data fusion")
        print("")
    
    def stop_all(self):
        """Stop all services."""
        print("")
        print("Stopping all services...")
        
        for process in self.processes:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
        
        print("✓ All services stopped")
    
    def monitor(self):
        """Monitor services and keep them running."""
        print("Monitoring services (Press Ctrl+C to stop)...")
        print("")
        
        try:
            while True:
                time.sleep(5)
                
                # Check if any process died
                for i, process in enumerate(self.processes):
                    if process.poll() is not None:
                        print(f"⚠️  Service {i} died with code {process.returncode}")
                
        except KeyboardInterrupt:
            print("")
            print("Received shutdown signal...")


def main():
    """Main entry point."""
    manager = ServiceManager()
    
    # Set up signal handlers
    def signal_handler(sig, frame):
        manager.stop_all()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start all services
    manager.start_all()
    
    # Monitor services
    manager.monitor()


if __name__ == '__main__':
    main()
