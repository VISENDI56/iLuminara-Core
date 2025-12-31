-- Enable Spatial Intelligence
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;

-- Enable Time-Series Partitioning (Simulated logic for standard Postgres)
CREATE TABLE IF NOT EXISTS sensor_telemetry (
        time TIMESTAMPTZ NOT NULL,
            device_id TEXT,
                location GEOMETRY(POINT, 4326),
                    reading JSONB
) PARTITION BY RANGE (time);

-- Create partition for current month
CREATE TABLE sensor_telemetry_y2026m01 PARTITION OF sensor_telemetry
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');