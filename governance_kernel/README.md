# Data Resilience & Event-Driven Architecture

## Message Bus
- `message_bus.py`: KafkaProducer with disk fallback for offline edge nodes.

## ChronoAudit
- `chrono_audit.py`: Multi-region, active-active audit log with Last-Write-Wins conflict resolution.

## Disaster Recovery
- `scripts/disaster_recovery.sh`: Automated DNS failover using Cloudflare API.

## Usage
- Integrate `KafkaProducer` for all event emission (e.g., ECF engine, data fusion).
- Use `ChronoAudit` for all audit/event logs, supporting multi-region sync.
- Schedule `disaster_recovery.sh` as a cron job or health check action.
