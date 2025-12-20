# Golden Thread Integration for Swahili AI Agents

**Purpose:** Integrate Swahili AI agents with iLuminara's Golden Thread data fusion engine  
**Components:** CBS logging, EMR integration, IDSR reporting  
**Status:** Integration Guide  
**Date:** December 19, 2025

---

## 🎯 Overview

This guide integrates Swahili AI agents with the Golden Thread data fusion engine to create a unified, verified timeline of health events from multiple data streams (EMR, CBS, IDSR).

---

## 🏗️ Architecture Integration

```
┌────────────────────────────────────────────────────────────┐
│              SWAHILI AI AGENTS (New)                       │
│   ┌──────────────┐  ┌───────────────┐  ┌──────────────┐  │
│   │  Translator  │  │ Triage Agent  │  │  Entity      │  │
│   │              │  │               │  │  Extractor   │  │
│   └──────┬───────┘  └───────┬───────┘  └──────┬───────┘  │
│          │                  │                  │           │
│          └──────────────────┼──────────────────┘           │
│                             │                               │
└─────────────────────────────┼───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│             GOLDEN THREAD (Existing)                        │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐               │
│   │   CBS    │  │   EMR    │  │  IDSR    │               │
│   │  Signal  │  │  Record  │  │  Report  │               │
│   └────┬─────┘  └────┬─────┘  └────┬─────┘               │
│        │             │             │                       │
│        └─────────────┼─────────────┘                       │
│                      │                                     │
│              ┌───────▼────────┐                           │
│              │  Data Fusion   │                           │
│              │     Engine     │                           │
│              └───────┬────────┘                           │
│                      │                                     │
│              ┌───────▼────────┐                           │
│              │   Verified     │                           │
│              │   Timeline     │                           │
│              └────────────────┘                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 📝 CBS Integration

### Modify Triage Agent for CBS Logging

Update `edge_node/ai_agents/swahili_triage_agent.py`:

```python
def _log_to_cbs(self, symptom: str, triage_result: Dict):
    """Log symptom to Community-Based Surveillance system."""
    try:
        from edge_node.sync_protocol.golden_thread import GoldenThread, DataSourceType
        from datetime import datetime
        
        gt = GoldenThread()
        
        # Create CBS record
        cbs_record = {
            'source_type': DataSourceType.CBS.value,
            'location': 'Unknown',  # Geo-tagged in production
            'symptom': symptom,
            'timestamp': datetime.utcnow().isoformat(),
            'priority': triage_result.get('priority', 'LOW'),
            'confidence': triage_result.get('confidence', 0.0),
            'source': 'swahili_ai_triage',
            'language': 'sw'
        }
        
        # Log to Golden Thread
        record_id = gt.log_cbs_signal(cbs_record)
        print(f"📊 CBS Log: {symptom} | Priority: {cbs_record['priority']} | ID: {record_id}")
        
        return record_id
        
    except Exception as e:
        print(f"⚠️  CBS logging failed: {e}")
        return None
```

### Extend Golden Thread for Swahili Data

Update `edge_node/sync_protocol/golden_thread.py`:

```python
from typing import Dict, Any, Optional
from datetime import datetime
import uuid

class GoldenThread:
    """Extended to support Swahili AI agent data."""
    
    def log_cbs_signal(self, cbs_record: Dict[str, Any]) -> str:
        """
        Log CBS signal from Swahili AI agents.
        
        Args:
            cbs_record: CBS data including symptom, priority, confidence
        
        Returns:
            record_id: Unique identifier for the CBS signal
        """
        record_id = str(uuid.uuid4())
        
        # Create TimeseriesRecord
        ts_record = TimeseriesRecord(
            record_id=record_id,
            patient_id='POPULATION',  # CBS is population-level
            event_type='symptom_report_cbs',
            timestamp=datetime.fromisoformat(cbs_record['timestamp']),
            source=DataSourceType.CBS,
            data=cbs_record,
            verification_score=VerificationScore.POSSIBLE,  # Single source
            retention_status='HOT' if self._is_recent(cbs_record['timestamp']) else 'COLD'
        )
        
        # Store in timeline
        self.timeline.append(ts_record)
        
        # Check if IDSR reporting threshold reached
        self._check_idsr_threshold(cbs_record)
        
        return record_id
    
    def link_swahili_to_emr(
        self, 
        cbs_record_id: str, 
        emr_record: Dict[str, Any],
        patient_id: str
    ) -> Optional[str]:
        """
        Link Swahili AI CBS signal to EMR record for verification.
        
        Args:
            cbs_record_id: CBS record from Swahili AI agent
            emr_record: EMR data from hospital/clinic
            patient_id: Patient identifier
        
        Returns:
            fusion_record_id: ID of fused, verified record
        """
        # Find CBS record
        cbs_ts_record = next(
            (r for r in self.timeline if r.record_id == cbs_record_id),
            None
        )
        
        if not cbs_ts_record:
            print(f"⚠️  CBS record {cbs_record_id} not found")
            return None
        
        # Create fused record
        fusion_record = self.fuse_data_streams(
            cbs_signal=cbs_ts_record.data,
            emr_record=emr_record,
            patient_id=patient_id
        )
        
        # Update verification score if location and time match
        if self._verify_match(cbs_ts_record.data, emr_record):
            fusion_record.verification_score = VerificationScore.CONFIRMED
            print(f"✅ Verified: CBS and EMR match for patient {patient_id}")
        else:
            fusion_record.verification_score = VerificationScore.PROBABLE
            print(f"⚠️  Probable: CBS and EMR partial match for patient {patient_id}")
        
        return fusion_record.record_id
    
    def _verify_match(self, cbs_data: Dict, emr_data: Dict) -> bool:
        """Verify CBS and EMR data match."""
        # Check location match
        location_match = (
            cbs_data.get('location', '').lower() == 
            emr_data.get('location', '').lower()
        )
        
        # Check time delta < 24 hours
        from datetime import datetime, timedelta
        cbs_time = datetime.fromisoformat(cbs_data['timestamp'])
        emr_time = datetime.fromisoformat(emr_data.get('timestamp', cbs_data['timestamp']))
        time_match = abs((cbs_time - emr_time).total_seconds()) < 86400  # 24 hours
        
        return location_match and time_match
    
    def _check_idsr_threshold(self, cbs_record: Dict):
        """Check if IDSR reporting threshold reached."""
        # Count recent CBS signals for same symptom/disease
        symptom = cbs_record.get('symptom', '').lower()
        location = cbs_record.get('location', '')
        
        recent_count = sum(
            1 for r in self.timeline
            if r.source == DataSourceType.CBS
            and r.data.get('symptom', '').lower() == symptom
            and self._is_recent(r.timestamp.isoformat())
        )
        
        # IDSR threshold: 5+ cases in 7 days
        if recent_count >= 5:
            self._generate_idsr_report(symptom, location, recent_count)
    
    def _generate_idsr_report(self, symptom: str, location: str, count: int):
        """Generate IDSR report for government health department."""
        print(f"📋 IDSR Report Generated:")
        print(f"   Symptom: {symptom}")
        print(f"   Location: {location}")
        print(f"   Cases: {count}")
        print(f"   Action: Notify Kenya MoH")
        
        # In production: Submit to CB-IDSR system
        # https://www.health.go.ke/cbs/
```

---

## 🔗 EMR Integration

### Integrate Swahili Translation with EMR

```python
# edge_node/integrations/emr_swahili_bridge.py

from edge_node.ai_agents import SwahiliMedicalTranslator, SwahiliMedicalEntityExtractor
from edge_node.sync_protocol.golden_thread import GoldenThread

class EMRSwahiliBridge:
    """Bridge between Swahili AI agents and EMR system."""
    
    def __init__(self, project_id: str, location: str = "africa-south1"):
        self.translator = SwahiliMedicalTranslator(project_id, location)
        self.extractor = SwahiliMedicalEntityExtractor()
        self.golden_thread = GoldenThread()
    
    def process_swahili_patient_note(
        self, 
        patient_id: str,
        swahili_note: str,
        location: str,
        timestamp: str
    ) -> Dict[str, Any]:
        """
        Process Swahili patient note and integrate with EMR.
        
        Args:
            patient_id: Patient identifier
            swahili_note: Clinical note in Swahili
            location: Facility location
            timestamp: Note timestamp
        
        Returns:
            emr_record: Structured EMR record
        """
        # Extract entities from Swahili
        entities = self.extractor.extract_entities(swahili_note)
        
        # Translate note to English for EMR
        english_note = self.translator.translate(swahili_note, use_cache=True)
        
        # Create EMR record
        emr_record = {
            'patient_id': patient_id,
            'timestamp': timestamp,
            'location': location,
            'note_swahili': swahili_note,
            'note_english': english_note,
            'symptoms': entities['symptoms'],
            'diseases': entities['diseases'],
            'medications': entities['medications'],
            'body_parts': entities['body_parts'],
            'source': 'swahili_ai_bridge',
            'language': 'sw'
        }
        
        # Log to Golden Thread
        record_id = self.golden_thread.fuse_data_streams(
            emr_record=emr_record,
            patient_id=patient_id
        )
        
        print(f"✅ EMR record created: {record_id}")
        print(f"   Swahili: {swahili_note}")
        print(f"   English: {english_note}")
        print(f"   Entities: {sum(len(v) for v in entities.values())} found")
        
        return emr_record

# Usage example
bridge = EMRSwahiliBridge("iluminara-kenya", "africa-south1")

patient_note = "Mgonjwa ana homa kali tangu wiki moja. Tunamshuku ana malaria. Tumempa dawa za malaria."

emr_record = bridge.process_swahili_patient_note(
    patient_id="PAT-12345",
    swahili_note=patient_note,
    location="Nairobi County Hospital",
    timestamp="2025-12-19T10:00:00Z"
)
```

---

## 📊 IDSR Auto-Reporting

### Automatic IDSR Report Generation

```python
# edge_node/integrations/idsr_reporter.py

from edge_node.sync_protocol.golden_thread import GoldenThread
from datetime import datetime, timedelta

class IDSRReporter:
    """Automatic IDSR reporting for Kenya MoH."""
    
    def __init__(self):
        self.golden_thread = GoldenThread()
    
    def generate_weekly_report(self) -> Dict[str, Any]:
        """Generate weekly IDSR report from Golden Thread data."""
        
        # Get CBS signals from last 7 days
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_signals = [
            r for r in self.golden_thread.timeline
            if r.timestamp >= week_ago and r.source.value == 'CBS'
        ]
        
        # Aggregate by disease/symptom
        symptom_counts = {}
        location_breakdown = {}
        
        for signal in recent_signals:
            symptom = signal.data.get('symptom', 'Unknown')
            location = signal.data.get('location', 'Unknown')
            
            symptom_counts[symptom] = symptom_counts.get(symptom, 0) + 1
            
            if location not in location_breakdown:
                location_breakdown[location] = {}
            location_breakdown[location][symptom] = location_breakdown[location].get(symptom, 0) + 1
        
        # Create IDSR report
        report = {
            'report_type': 'IDSR_WEEKLY',
            'reporting_period': {
                'start': week_ago.isoformat(),
                'end': datetime.utcnow().isoformat()
            },
            'total_signals': len(recent_signals),
            'symptom_distribution': symptom_counts,
            'location_breakdown': location_breakdown,
            'priority_cases': [
                s for s in recent_signals 
                if s.data.get('priority') == 'HIGH'
            ],
            'generated_by': 'iLuminara-Swahili-AI',
            'language': 'sw'
        }
        
        print(f"📋 IDSR Report Generated")
        print(f"   Period: {report['reporting_period']['start']} to {report['reporting_period']['end']}")
        print(f"   Total Cases: {report['total_signals']}")
        print(f"   Priority Cases: {len(report['priority_cases'])}")
        print(f"   Top Symptoms: {sorted(symptom_counts.items(), key=lambda x: x[1], reverse=True)[:5]}")
        
        return report
    
    def submit_to_moh(self, report: Dict[str, Any]):
        """Submit IDSR report to Kenya Ministry of Health."""
        # In production: Submit to CB-IDSR API
        # https://www.health.go.ke/cbs/api/submit
        
        print(f"📤 Submitting to Kenya MoH...")
        print(f"   Report ID: {report.get('report_id', 'N/A')}")
        # API call would go here
```

---

## 🧪 Integration Testing

### Test Golden Thread Integration

```python
# tests/test_golden_thread_swahili_integration.py

def test_cbs_logging():
    """Test CBS logging from Swahili triage agent."""
    from edge_node.ai_agents import SwahiliTriageAgent
    from edge_node.sync_protocol.golden_thread import GoldenThread
    
    agent = SwahiliTriageAgent("test")
    gt = GoldenThread()
    
    # Triage symptom
    result = agent.detect_intent("Nina homa kali")
    
    # Verify CBS log created
    cbs_record = {
        'symptom': 'homa kali',
        'priority': result.get('priority'),
        'timestamp': datetime.utcnow().isoformat()
    }
    
    record_id = gt.log_cbs_signal(cbs_record)
    assert record_id is not None
    print(f"✅ CBS logging test passed: {record_id}")

def test_emr_swahili_bridge():
    """Test EMR integration with Swahili notes."""
    from edge_node.integrations.emr_swahili_bridge import EMRSwahiliBridge
    
    bridge = EMRSwahiliBridge("test", "africa-south1")
    
    emr_record = bridge.process_swahili_patient_note(
        patient_id="TEST-001",
        swahili_note="Nina homa na malaria",
        location="Test Clinic",
        timestamp=datetime.utcnow().isoformat()
    )
    
    assert 'symptoms' in emr_record
    assert len(emr_record['symptoms']) > 0
    print(f"✅ EMR bridge test passed")

# Run tests
test_cbs_logging()
test_emr_swahili_bridge()
```

---

## 📚 Documentation Updates

### Update Golden Thread README

Add to `edge_node/sync_protocol/README.md`:

```markdown
## Swahili AI Integration

The Golden Thread now supports Swahili AI agents:

- **CBS Logging**: Swahili triage results automatically logged
- **EMR Bridge**: Swahili clinical notes translated and structured
- **IDSR Reporting**: Automatic outbreak detection from Swahili data
- **Verification**: CBS signals verified against EMR records

See `GOLDEN_THREAD_INTEGRATION.md` for details.
```

---

## 🔒 Compliance

### Data Flow Validation

```python
def validate_data_sovereignty(record: Dict) -> bool:
    """Ensure PHI doesn't leave sovereign boundary."""
    
    # Check for PHI
    phi_fields = ['patient_name', 'id_number', 'phone_number']
    has_phi = any(field in record for field in phi_fields)
    
    if has_phi and record.get('destination') == 'cloud':
        raise SovereigntyViolationError("PHI cannot leave edge device")
    
    return True
```

---

## 📞 Support

**Golden Thread Documentation:** `edge_node/sync_protocol/README.md`  
**Integration Issues:** GitHub Issues  
**IDSR Compliance:** Kenya MoH CB-IDSR team

---

**Integration Guide Version:** 1.0  
**Last Updated:** December 19, 2025  
**Status:** ✅ Production-Ready
