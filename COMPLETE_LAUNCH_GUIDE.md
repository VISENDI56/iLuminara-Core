# iLuminara Complete System Launch Guide

## 🚀 Overview

This guide provides instructions for launching all iLuminara services, including all ports, apps, platforms, and dashboards.

## 📋 System Components

### Streamlit Dashboards (Ports 8501-8503)
1. **Command Console** (Port 8501)
   - Leadership HUD and primary demonstration interface
   - Real-time outbreak monitoring
   - Z-Score analysis and bond status
   - Geographic visualization

2. **Transparency Audit** (Port 8502)
   - Clinical staff audit view
   - Decision reasoning (SHAP analysis)
   - Protocol validation console
   - Time-to-action metrics

3. **Field Validation** (Port 8503)
   - CHW mobile interface
   - Field validation form
   - Alert verification
   - Human-in-the-loop completion

### Docker Services (When Available)
- **Core API** (Port 8080) - Main REST API
- **Core HTTPS** (Port 8443) - Secure API endpoint
- **Governance Service** (Port 5000) - Legal compliance engine
- **Data Fusion Service** (Port 5001) - Golden Thread processor
- **Prometheus** (Port 9091) - Metrics collection
- **Grafana** (Port 3000) - Visualization dashboard
- **Nginx** (Ports 80, 443) - Reverse proxy

### Support Services
- **Port Forwarder** - Internal port mapping tool

## 🎯 Quick Start

### Option 1: Launch All Services (Recommended)

```bash
./launch_all_services.sh
```

This script will:
1. Check and install Python dependencies
2. Generate outbreak simulation data
3. Start port forwarder
4. Launch all 3 Streamlit dashboards
5. Start Docker services (if available)
6. Verify all services are running

### Option 2: Launch Individual Components

#### Streamlit Dashboards Only
```bash
# Command Console
streamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0 --server.headless true

# Transparency Audit
streamlit run transparency_view.py --server.port 8502 --server.address 0.0.0.0 --server.headless true

# Field Validation
streamlit run field_validation_form.py --server.port 8503 --server.address 0.0.0.0 --server.headless true
```

#### Docker Services Only
```bash
docker-compose up -d
```

## 🛠️ Prerequisites

### Required
- Python 3.8 or higher
- pip (Python package manager)

### Optional
- Docker and Docker Compose (for containerized services)
- 8GB RAM minimum (recommended)
- 2+ CPU cores

### Python Dependencies
The launch script will automatically install these if missing:
- streamlit
- pandas
- pydeck
- numpy
- plotly

## 📊 Accessing the Services

Once launched, access the services at:

### Streamlit Dashboards
- **Command Console**: http://localhost:8501 or http://0.0.0.0:8501
- **Transparency Audit**: http://localhost:8502 or http://0.0.0.0:8502
- **Field Validation**: http://localhost:8503 or http://0.0.0.0:8503

### Docker Services (if running)
- **Core API**: http://localhost:8080
- **Core HTTPS**: https://localhost:8443
- **Grafana**: http://localhost:3000 (admin/iluminara)
- **Prometheus**: http://localhost:9091
- **Nginx**: http://localhost:80

## 🔍 Monitoring and Management

### Check Service Status
```bash
./check_services_status.sh
```

This will show:
- Running processes and PIDs
- Port status for all services
- Docker container status
- Data file presence
- System resource usage

### View Logs
```bash
# View all logs
tail -f logs/*.log

# View specific service logs
tail -f logs/dashboard.log
tail -f logs/transparency.log
tail -f logs/field_validation.log
tail -f logs/docker_compose.log
```

### Stop All Services
```bash
./stop_all_services.sh
```

This will gracefully stop:
- All Streamlit dashboards
- Port forwarder
- Docker services

## 🐛 Troubleshooting

### Services Not Starting

**Problem**: Streamlit dashboards fail to start
**Solution**:
```bash
# Reinstall dependencies
pip install --upgrade streamlit pandas pydeck numpy plotly

# Check for port conflicts
lsof -i :8501
lsof -i :8502
lsof -i :8503
```

**Problem**: Docker services fail to start
**Solution**:
```bash
# Check Docker is running
docker ps

# Build images first
docker-compose build

# Check logs
docker-compose logs
```

### Data Files Missing

**Problem**: Dashboard shows "DATA NOT FOUND" error
**Solution**:
```bash
# Generate outbreak data
python3 edge_node/frenasa_engine/simulate_outbreak.py

# Verify file was created
ls -lh simulated_outbreak.json
```

### Port Already in Use

**Problem**: Port conflicts (8501, 8502, 8503)
**Solution**:
```bash
# Find process using the port
lsof -i :8501

# Kill the process
kill -9 <PID>

# Or stop all services first
./stop_all_services.sh
```

### Permissions Issues

**Problem**: Scripts won't execute
**Solution**:
```bash
# Make scripts executable
chmod +x launch_all_services.sh
chmod +x stop_all_services.sh
chmod +x check_services_status.sh
```

## 📁 File Structure

```
iLuminara-Core/
├── launch_all_services.sh       # Master launch script
├── stop_all_services.sh         # Shutdown script
├── check_services_status.sh     # Status checker
├── launch_war_room.sh           # Original demo launcher
├── dashboard.py                 # Command Console app
├── transparency_view.py         # Audit view app
├── field_validation_form.py     # Field validation app
├── docker-compose.yml           # Docker orchestration
├── logs/                        # Service logs
│   ├── dashboard.log
│   ├── transparency.log
│   ├── field_validation.log
│   └── docker_compose.log
├── governance_kernel/           # Legal compliance engine
├── edge_node/                   # Edge computing components
├── cloud_oracle/                # Cloud services
└── hardware/                    # Hardware attestation
```

## 🔐 Security Notes

- All services run with **data sovereignty** by default
- Health data (PHI) cannot leave sovereign territory
- Compliance enforced via `SovereignGuardrail` class
- GDPR, HIPAA, KDPA, POPIA, and 10+ frameworks supported
- Offline-first architecture - no internet required

## 📚 Additional Resources

- **README.md** - Complete system documentation
- **QUICKSTART_DEMO.md** - 5-minute demo guide
- **LAUNCH_CHECKLIST.md** - Demo preparation checklist
- **DEMO_PROTOCOL.md** - Full presentation script

## ✨ Demo Flow

For presentations and demos:

1. **Start Services**
   ```bash
   ./launch_all_services.sh
   ```

2. **Open Dashboards**
   - Tab 1: http://0.0.0.0:8501 (Command Console)
   - Tab 2: http://0.0.0.0:8502 (Transparency)
   - Tab 3: http://0.0.0.0:8503 (Field Validation)

3. **Generate Fresh Data** (Optional)
   ```bash
   python3 edge_node/frenasa_engine/simulate_outbreak.py
   ```

4. **Show System Working**
   - Use hour slider in Command Console
   - Watch metrics update in real-time
   - Show transparency audit
   - Demonstrate field validation

5. **Stop Services** (After demo)
   ```bash
   ./stop_all_services.sh
   ```

## 🎯 Success Metrics

Services are ready when:
- ✅ All 3 Streamlit dashboards accessible
- ✅ No errors in log files
- ✅ simulated_outbreak.json exists
- ✅ Ports 8501-8503 are listening
- ✅ Status check shows all green

## 🌍 Mission

> "Transform preventable suffering from statistical inevitability to historical anomaly."

Every service running is a step toward that goal.

## 📞 Support

For issues or questions:
1. Check logs: `tail -f logs/*.log`
2. Run status check: `./check_services_status.sh`
3. Review troubleshooting section above
4. Consult README.md for detailed documentation

---

**Status**: ✅ READY FOR DEPLOYMENT  
**Last Updated**: December 2025  
**Confidence**: MAXIMUM
