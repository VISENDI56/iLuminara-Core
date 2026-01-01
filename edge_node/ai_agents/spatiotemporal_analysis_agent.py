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

"""
Spatiotemporal Analysis Agent
═════════════════════════════════════════════════════════════════════════════

Specialized AI agent for multi-scale spatiotemporal analysis of disease patterns.
Performs spatial clustering, hotspot detection, temporal trend analysis, and
geographic risk mapping across multiple temporal and spatial scales.

Core Capabilities:
- Multi-scale spatial clustering (neighborhood, district, regional, national)
- Hotspot detection using spatial statistics (Getis-Ord Gi*, Moran's I)
- Temporal pattern recognition (seasonality, cyclic trends, anomalies)
- Space-time interaction analysis
- Geographic risk surface generation
- Movement pattern analysis and transmission pathway inference
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import math

# Statistical constants for Getis-Ord Gi* hotspot detection
GI_STAR_CRITICAL_VALUE_99 = 2.58  # 99% confidence level (p < 0.1)
GI_STAR_CRITICAL_VALUE_95 = 1.96  # 95% confidence level (p < 0.5)
P_VALUE_HIGHLY_SIGNIFICANT = 0.1
P_VALUE_SIGNIFICANT = 0.5
P_VALUE_MARGINALLY_SIGNIFICANT = 0.1

# Risk calculation constants
RISK_NORMALIZATION_FACTOR = 10000  # Population exposure risk normalization


class SpatialScale(Enum):
    """Spatial analysis scales."""
    HYPERLOCAL = "Hyperlocal"  # <1 km
    NEIGHBORHOOD = "Neighborhood"  # 1-5 km
    DISTRICT = "District"  # 5-50 km
    REGIONAL = "Regional"  # 50-500 km
    NATIONAL = "National"  # >500 km


class TemporalScale(Enum):
    """Temporal analysis scales."""
    REALTIME = "Realtime"  # Minutes to hours
    DAILY = "Daily"  # 1-7 days
    WEEKLY = "Weekly"  # 7-30 days
    MONTHLY = "Monthly"  # 30-90 days
    SEASONAL = "Seasonal"  # 90-365 days
    YEARLY = "Yearly"  # >365 days


@dataclass
class SpatialCluster:
    """Detected spatial cluster of cases."""
    cluster_id: str
    center_lat: float
    center_lon: float
    radius_km: float
    case_count: int
    population_density: float
    risk_score: float  # 0.0 to 1.0
    start_date: datetime
    end_date: datetime
    locations: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Hotspot:
    """Identified disease hotspot with statistical significance."""
    hotspot_id: str
    location: Tuple[float, float]  # (lat, lon)
    gi_star_score: float  # Getis-Ord Gi* statistic
    p_value: float  # Statistical significance
    intensity: str  # "High", "Medium", "Low"
    temporal_window: Tuple[datetime, datetime]
    affected_population: int
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SpatiotemporalAnalysis:
    """Complete spatiotemporal analysis result."""
    analysis_date: datetime
    spatial_scale: str
    temporal_scale: str
    clusters: List[SpatialCluster]
    hotspots: List[Hotspot]
    temporal_trends: Dict[str, Any]
    risk_surface: Dict[str, Any]
    transmission_pathways: List[Dict[str, Any]]
    summary_statistics: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize analysis to dictionary."""
        return {
            "analysis_date": self.analysis_date.isoformat(),
            "spatial_scale": self.spatial_scale,
            "temporal_scale": self.temporal_scale,
            "clusters": [
                {
                    "cluster_id": c.cluster_id,
                    "center": [c.center_lat, c.center_lon],
                    "radius_km": c.radius_km,
                    "case_count": c.case_count,
                    "risk_score": c.risk_score,
                    "start_date": c.start_date.isoformat(),
                    "end_date": c.end_date.isoformat(),
                }
                for c in self.clusters
            ],
            "hotspots": [
                {
                    "hotspot_id": h.hotspot_id,
                    "location": h.location,
                    "gi_star_score": h.gi_star_score,
                    "p_value": h.p_value,
                    "intensity": h.intensity,
                }
                for h in self.hotspots
            ],
            "temporal_trends": self.temporal_trends,
            "risk_surface": self.risk_surface,
            "transmission_pathways": self.transmission_pathways,
            "summary_statistics": self.summary_statistics,
            "metadata": self.metadata,
        }


class SpatiotemporalAnalysisAgent:
    """
    Autonomous AI agent specialized in multi-scale spatiotemporal analysis.
    
    This agent analyzes disease patterns across space and time, identifying
    clusters, hotspots, and transmission dynamics at multiple scales.
    
    Usage:
        agent = SpatiotemporalAnalysisAgent(region="East Africa")
        analysis = agent.analyze(
            case_data=cases,
            spatial_scale=SpatialScale.DISTRICT,
            temporal_scale=TemporalScale.WEEKLY
        )
    """

    def __init__(self, region: str, coordinate_bounds: Optional[Dict[str, float]] = None):
        """
        Initialize the spatiotemporal analysis agent.
        
        Args:
            region: Geographic region name
            coordinate_bounds: Optional dict with 'min_lat', 'max_lat', 'min_lon', 'max_lon'
        """
        self.region = region
        self.coordinate_bounds = coordinate_bounds or {
            "min_lat": -4.0, "max_lat": 4.0,
            "min_lon": 33.0, "max_lon": 42.0
        }
        self.analysis_history = []
        
    def analyze(
        self,
        case_data: List[Dict[str, Any]],
        spatial_scale: SpatialScale = SpatialScale.DISTRICT,
        temporal_scale: TemporalScale = TemporalScale.WEEKLY,
        population_data: Optional[Dict[str, Any]] = None,
    ) -> SpatiotemporalAnalysis:
        """
        Perform comprehensive spatiotemporal analysis on case data.
        
        Args:
            case_data: List of case records with location and timestamp
            spatial_scale: Scale of spatial analysis
            temporal_scale: Scale of temporal analysis
            population_data: Optional population density data
            
        Returns:
            SpatiotemporalAnalysis with clusters, hotspots, and trends
        """
        # Spatial clustering
        clusters = self._detect_spatial_clusters(case_data, spatial_scale, population_data)
        
        # Hotspot detection
        hotspots = self._detect_hotspots(case_data, spatial_scale)
        
        # Temporal trend analysis
        temporal_trends = self._analyze_temporal_trends(case_data, temporal_scale)
        
        # Generate risk surface
        risk_surface = self._generate_risk_surface(clusters, hotspots)
        
        # Infer transmission pathways
        transmission_pathways = self._infer_transmission_pathways(case_data, clusters)
        
        # Calculate summary statistics
        summary_stats = self._calculate_summary_statistics(
            case_data, clusters, hotspots, temporal_trends
        )
        
        analysis = SpatiotemporalAnalysis(
            analysis_date=datetime.utcnow(),
            spatial_scale=spatial_scale.value,
            temporal_scale=temporal_scale.value,
            clusters=clusters,
            hotspots=hotspots,
            temporal_trends=temporal_trends,
            risk_surface=risk_surface,
            transmission_pathways=transmission_pathways,
            summary_statistics=summary_stats,
            metadata={
                "region": self.region,
                "total_cases": len(case_data),
            }
        )
        
        self.analysis_history.append(analysis)
        return analysis
    
    def _detect_spatial_clusters(
        self,
        case_data: List[Dict[str, Any]],
        scale: SpatialScale,
        population_data: Optional[Dict[str, Any]],
    ) -> List[SpatialCluster]:
        """
        Detect spatial clusters using DBSCAN-like algorithm.
        
        Clusters are detected based on spatial density and temporal coherence.
        """
        if not case_data:
            return []
        
        # Scale-dependent parameters
        scale_params = {
            SpatialScale.HYPERLOCAL: {"radius": 1.0, "min_points": 3},
            SpatialScale.NEIGHBORHOOD: {"radius": 3.0, "min_points": 5},
            SpatialScale.DISTRICT: {"radius": 10.0, "min_points": 10},
            SpatialScale.REGIONAL: {"radius": 50.0, "min_points": 20},
            SpatialScale.NATIONAL: {"radius": 200.0, "min_points": 50},
        }
        
        params = scale_params[scale]
        radius_km = params["radius"]
        min_points = params["min_points"]
        
        # Extract spatial points
        points = [
            {
                "lat": record.get("lat", record.get("latitude", 0.0)),
                "lon": record.get("lon", record.get("longitude", 0.0)),
                "timestamp": record.get("timestamp"),
                "record": record,
            }
            for record in case_data
            if "lat" in record or "latitude" in record
        ]
        
        if not points:
            return []
        
        # Simple clustering: group points within radius
        clusters = []
        visited = set()
        
        for i, point in enumerate(points):
            if i in visited:
                continue
            
            # Find neighbors within radius
            neighbors = []
            for j, other in enumerate(points):
                if j != i and j not in visited:
                    dist = self._haversine_distance(
                        point["lat"], point["lon"],
                        other["lat"], other["lon"]
                    )
                    if dist <= radius_km:
                        neighbors.append((j, other, dist))
            
            if len(neighbors) >= min_points - 1:
                # Create cluster
                cluster_points = [point] + [n[1] for n in neighbors]
                visited.add(i)
                for n in neighbors:
                    visited.add(n[0])
                
                # Calculate cluster center
                center_lat = sum(p["lat"] for p in cluster_points) / len(cluster_points)
                center_lon = sum(p["lon"] for p in cluster_points) / len(cluster_points)
                
                # Calculate cluster radius (max distance from center)
                cluster_radius = max(
                    self._haversine_distance(center_lat, center_lon, p["lat"], p["lon"])
                    for p in cluster_points
                )
                
                # Extract temporal bounds
                timestamps = [
                    self._parse_timestamp(p["timestamp"])
                    for p in cluster_points
                    if p.get("timestamp")
                ]
                start_date = min(timestamps) if timestamps else datetime.utcnow()
                end_date = max(timestamps) if timestamps else datetime.utcnow()
                
                # Calculate risk score
                population_density = self._get_population_density(
                    center_lat, center_lon, population_data
                )
                risk_score = self._calculate_cluster_risk(
                    len(cluster_points), cluster_radius, population_density
                )
                
                cluster = SpatialCluster(
                    cluster_id=f"CLUSTER_{len(clusters) + 1}",
                    center_lat=center_lat,
                    center_lon=center_lon,
                    radius_km=cluster_radius,
                    case_count=len(cluster_points),
                    population_density=population_density,
                    risk_score=risk_score,
                    start_date=start_date,
                    end_date=end_date,
                    locations=[p["record"] for p in cluster_points],
                )
                clusters.append(cluster)
        
        return clusters
    
    def _detect_hotspots(
        self,
        case_data: List[Dict[str, Any]],
        scale: SpatialScale,
    ) -> List[Hotspot]:
        """
        Detect statistically significant hotspots using Getis-Ord Gi* statistic.
        
        Hotspots are areas with significantly higher case concentrations.
        """
        hotspots = []
        
        if not case_data:
            return hotspots
        
        # Create spatial grid
        grid = self._create_spatial_grid(case_data, scale)
        
        # Calculate Gi* for each grid cell
        for cell_id, cell_data in grid.items():
            gi_star, p_value = self._calculate_gi_star(cell_data, grid)
            
            # Significant hotspot if p < 0.5 and positive Gi*
            if p_value < P_VALUE_SIGNIFICANT and gi_star > 0:
                intensity = "High" if gi_star > GI_STAR_CRITICAL_VALUE_99 else (
                    "Medium" if gi_star > GI_STAR_CRITICAL_VALUE_95 else "Low"
                )
                
                timestamps = [
                    self._parse_timestamp(case.get("timestamp"))
                    for case in cell_data["cases"]
                    if case.get("timestamp")
                ]
                temporal_window = (
                    min(timestamps) if timestamps else datetime.utcnow(),
                    max(timestamps) if timestamps else datetime.utcnow(),
                )
                
                hotspot = Hotspot(
                    hotspot_id=f"HOTSPOT_{len(hotspots) + 1}",
                    location=(cell_data["center_lat"], cell_data["center_lon"]),
                    gi_star_score=gi_star,
                    p_value=p_value,
                    intensity=intensity,
                    temporal_window=temporal_window,
                    affected_population=len(cell_data["cases"]),
                    metadata={"cell_id": cell_id}
                )
                hotspots.append(hotspot)
        
        return hotspots
    
    def _analyze_temporal_trends(
        self,
        case_data: List[Dict[str, Any]],
        scale: TemporalScale,
    ) -> Dict[str, Any]:
        """
        Analyze temporal patterns in case data.
        
        Identifies trends, seasonality, and anomalies.
        """
        if not case_data:
            return {}
        
        # Extract time series
        time_series = self._build_time_series(case_data, scale)
        
        # Detect trend (increasing, decreasing, stable)
        trend = self._detect_trend(time_series)
        
        # Detect seasonality
        seasonality = self._detect_seasonality(time_series, scale)
        
        # Detect anomalies
        anomalies = self._detect_temporal_anomalies(time_series)
        
        # Calculate velocity (rate of change)
        velocity = self._calculate_velocity(time_series)
        
        return {
            "trend": trend,
            "seasonality": seasonality,
            "anomalies": anomalies,
            "velocity": velocity,
            "time_series": time_series,
        }
    
    def _generate_risk_surface(
        self,
        clusters: List[SpatialCluster],
        hotspots: List[Hotspot],
    ) -> Dict[str, Any]:
        """
        Generate continuous risk surface from discrete clusters and hotspots.
        
        Uses kernel density estimation for smooth risk interpolation.
        """
        # Create risk grid
        lat_range = (self.coordinate_bounds["min_lat"], self.coordinate_bounds["max_lat"])
        lon_range = (self.coordinate_bounds["min_lon"], self.coordinate_bounds["max_lon"])
        
        grid_resolution = 0.1  # degrees
        risk_grid = {}
        
        # Sample grid points
        lat = lat_range[0]
        while lat <= lat_range[1]:
            lon = lon_range[0]
            while lon <= lon_range[1]:
                # Calculate risk at this point from clusters and hotspots
                cluster_risk = sum(
                    c.risk_score * self._gaussian_kernel(
                        self._haversine_distance(lat, lon, c.center_lat, c.center_lon),
                        c.radius_km * 2
                    )
                    for c in clusters
                )
                
                hotspot_risk = sum(
                    (1.0 if h.intensity == "High" else 0.7 if h.intensity == "Medium" else 0.4) *
                    self._gaussian_kernel(
                        self._haversine_distance(lat, lon, h.location[0], h.location[1]),
                        10.0  # bandwidth
                    )
                    for h in hotspots
                )
                
                total_risk = min(1.0, cluster_risk + hotspot_risk)
                
                if total_risk > 0.1:  # Only store significant risk points
                    grid_key = f"{lat:.2f},{lon:.2f}"
                    risk_grid[grid_key] = {
                        "lat": lat,
                        "lon": lon,
                        "risk": total_risk,
                    }
                
                lon += grid_resolution
            lat += grid_resolution
        
        return {
            "grid_resolution": grid_resolution,
            "risk_points": list(risk_grid.values()),
            "max_risk": max((p["risk"] for p in risk_grid.values()), default=0.0),
            "high_risk_areas": sum(1 for p in risk_grid.values() if p["risk"] > 0.7),
        }
    
    def _infer_transmission_pathways(
        self,
        case_data: List[Dict[str, Any]],
        clusters: List[SpatialCluster],
    ) -> List[Dict[str, Any]]:
        """
        Infer likely transmission pathways between clusters.
        
        Uses temporal sequence and spatial proximity to identify potential
        disease spread routes.
        """
        pathways = []
        
        # Sort clusters by start date
        sorted_clusters = sorted(clusters, key=lambda c: c.start_date)
        
        for i, source in enumerate(sorted_clusters):
            for target in sorted_clusters[i + 1:]:
                # Check if target started after source
                time_diff = (target.start_date - source.start_date).days
                
                if 0 < time_diff <= 14:  # Within 2 weeks
                    distance = self._haversine_distance(
                        source.center_lat, source.center_lon,
                        target.center_lat, target.center_lon
                    )
                    
                    # Plausible transmission if within reasonable distance
                    if distance < 200:  # km
                        confidence = 1.0 - (distance / 200) * (time_diff / 14)
                        
                        pathway = {
                            "source_cluster": source.cluster_id,
                            "target_cluster": target.cluster_id,
                            "distance_km": distance,
                            "time_lag_days": time_diff,
                            "confidence": confidence,
                            "estimated_speed_km_per_day": distance / time_diff if time_diff > 0 else 0,
                        }
                        pathways.append(pathway)
        
        return pathways
    
    def _calculate_summary_statistics(
        self,
        case_data: List[Dict[str, Any]],
        clusters: List[SpatialCluster],
        hotspots: List[Hotspot],
        temporal_trends: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Calculate summary statistics for the analysis."""
        return {
            "total_cases": len(case_data),
            "total_clusters": len(clusters),
            "total_hotspots": len(hotspots),
            "high_risk_hotspots": sum(1 for h in hotspots if h.intensity == "High"),
            "largest_cluster_cases": max((c.case_count for c in clusters), default=0),
            "mean_cluster_size": sum(c.case_count for c in clusters) / len(clusters) if clusters else 0,
            "temporal_trend": temporal_trends.get("trend", "Unknown"),
            "velocity": temporal_trends.get("velocity", 0.0),
        }
    
    # Helper methods
    
    def _haversine_distance(
        self,
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float,
    ) -> float:
        """Calculate distance between two points in kilometers using Haversine formula."""
        R = 6371  # Earth radius in km
        
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2)
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c
    
    def _parse_timestamp(self, timestamp: Any) -> datetime:
        """Parse timestamp from various formats."""
        if isinstance(timestamp, datetime):
            return timestamp
        elif isinstance(timestamp, str):
            try:
                return datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                return datetime.utcnow()
        else:
            return datetime.utcnow()
    
    def _get_population_density(
        self,
        lat: float,
        lon: float,
        population_data: Optional[Dict[str, Any]],
    ) -> float:
        """Get population density for location (people per km²)."""
        if not population_data:
            return 1000.0  # Default density
        
        # Simple lookup (would use actual population data in production)
        return population_data.get("density", 1000.0)
    
    def _calculate_cluster_risk(
        self,
        case_count: int,
        radius_km: float,
        population_density: float,
    ) -> float:
        """Calculate risk score for a cluster."""
        # Risk factors: case density, population exposure
        case_density = case_count / (math.pi * radius_km ** 2) if radius_km > 0 else case_count
        exposure_risk = min(1.0, (case_density * population_density) / RISK_NORMALIZATION_FACTOR)
        
        return min(1.0, max(0.0, exposure_risk))
    
    def _create_spatial_grid(
        self,
        case_data: List[Dict[str, Any]],
        scale: SpatialScale,
    ) -> Dict[str, Dict[str, Any]]:
        """Create spatial grid for hotspot analysis."""
        # Grid cell size based on scale
        cell_sizes = {
            SpatialScale.HYPERLOCAL: 0.1,
            SpatialScale.NEIGHBORHOOD: 0.5,
            SpatialScale.DISTRICT: 0.1,
            SpatialScale.REGIONAL: 0.5,
            SpatialScale.NATIONAL: 1.0,
        }
        cell_size = cell_sizes[scale]
        
        grid = {}
        for case in case_data:
            lat = case.get("lat", case.get("latitude", 0.0))
            lon = case.get("lon", case.get("longitude", 0.0))
            
            # Assign to grid cell
            cell_lat = int(lat / cell_size) * cell_size
            cell_lon = int(lon / cell_size) * cell_size
            cell_id = f"{cell_lat:.2f},{cell_lon:.2f}"
            
            if cell_id not in grid:
                grid[cell_id] = {
                    "center_lat": cell_lat + cell_size / 2,
                    "center_lon": cell_lon + cell_size / 2,
                    "cases": [],
                }
            grid[cell_id]["cases"].append(case)
        
        return grid
    
    def _calculate_gi_star(
        self,
        cell_data: Dict[str, Any],
        grid: Dict[str, Dict[str, Any]],
    ) -> Tuple[float, float]:
        """
        Calculate Getis-Ord Gi* statistic for hotspot detection.
        
        Returns: (gi_star_score, p_value)
        """
        # Simplified Gi* calculation
        cell_cases = len(cell_data["cases"])
        
        # Find neighbors
        neighbor_cases = []
        for other_id, other_data in grid.items():
            dist = self._haversine_distance(
                cell_data["center_lat"], cell_data["center_lon"],
                other_data["center_lat"], other_data["center_lon"]
            )
            if 0 < dist < 50:  # Neighbor threshold
                neighbor_cases.append(len(other_data["cases"]))
        
        if not neighbor_cases:
            return 0.0, 1.0
        
        # Calculate z-score
        mean_cases = sum(neighbor_cases) / len(neighbor_cases)
        std_cases = (sum((x - mean_cases) ** 2 for x in neighbor_cases) / len(neighbor_cases)) ** 0.5
        
        if std_cases == 0:
            return 0.0, 1.0
        
        gi_star = (cell_cases - mean_cases) / std_cases
        
        # Convert to p-value based on z-score thresholds
        if abs(gi_star) > GI_STAR_CRITICAL_VALUE_99:
            p_value = P_VALUE_HIGHLY_SIGNIFICANT
        elif abs(gi_star) > GI_STAR_CRITICAL_VALUE_95:
            p_value = P_VALUE_SIGNIFICANT
        else:
            p_value = P_VALUE_MARGINALLY_SIGNIFICANT
        
        return gi_star, p_value
    
    def _build_time_series(
        self,
        case_data: List[Dict[str, Any]],
        scale: TemporalScale,
    ) -> List[Dict[str, Any]]:
        """Build time series from case data."""
        # Group cases by time window
        time_windows = {}
        
        for case in case_data:
            timestamp = self._parse_timestamp(case.get("timestamp"))
            
            # Round to time window based on scale
            if scale == TemporalScale.DAILY:
                window = timestamp.date()
            elif scale == TemporalScale.WEEKLY:
                window = timestamp.date() - timedelta(days=timestamp.weekday())
            elif scale == TemporalScale.MONTHLY:
                window = timestamp.date().replace(day=1)
            else:
                window = timestamp.date()
            
            window_key = str(window)
            if window_key not in time_windows:
                time_windows[window_key] = {"date": str(window), "count": 0}
            time_windows[window_key]["count"] += 1
        
        # Sort by date
        return sorted(time_windows.values(), key=lambda x: x["date"])
    
    def _detect_trend(self, time_series: List[Dict[str, Any]]) -> str:
        """Detect overall trend in time series."""
        if len(time_series) < 2:
            return "Insufficient data"
        
        first_half_avg = sum(t["count"] for t in time_series[:len(time_series)//2]) / (len(time_series)//2)
        second_half_avg = sum(t["count"] for t in time_series[len(time_series)//2:]) / (len(time_series) - len(time_series)//2)
        
        if second_half_avg > first_half_avg * 1.2:
            return "Increasing"
        elif second_half_avg < first_half_avg * 0.8:
            return "Decreasing"
        else:
            return "Stable"
    
    def _detect_seasonality(
        self,
        time_series: List[Dict[str, Any]],
        scale: TemporalScale,
    ) -> Dict[str, Any]:
        """Detect seasonal patterns."""
        # Placeholder for seasonality detection
        return {
            "detected": False,
            "period": None,
            "amplitude": 0.0,
        }
    
    def _detect_temporal_anomalies(
        self,
        time_series: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Detect anomalous time points."""
        if len(time_series) < 3:
            return []
        
        # Simple anomaly detection: values > 2 std deviations from mean
        counts = [t["count"] for t in time_series]
        mean = sum(counts) / len(counts)
        std = (sum((x - mean) ** 2 for x in counts) / len(counts)) ** 0.5
        
        anomalies = []
        for t in time_series:
            if abs(t["count"] - mean) > 2 * std:
                anomalies.append({
                    "date": str(t["date"]),
                    "count": t["count"],
                    "deviation": abs(t["count"] - mean) / std if std > 0 else 0,
                })
        
        return anomalies
    
    def _calculate_velocity(self, time_series: List[Dict[str, Any]]) -> float:
        """Calculate rate of change in cases."""
        if len(time_series) < 2:
            return 0.0
        
        # Average daily change
        total_change = time_series[-1]["count"] - time_series[0]["count"]
        return total_change / len(time_series)
    
    def _gaussian_kernel(self, distance: float, bandwidth: float) -> float:
        """Gaussian kernel for spatial smoothing."""
        return math.exp(-(distance ** 2) / (2 * bandwidth ** 2))
    
    def get_analysis_summary(self) -> Dict[str, Any]:
        """Get summary of all analyses performed."""
        return {
            "region": self.region,
            "total_analyses": len(self.analysis_history),
            "analyses": [a.to_dict() for a in self.analysis_history],
        }
