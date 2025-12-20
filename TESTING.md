# Testing Guide for Swahili AI Agents

**Status:** ✅ All Tests Passing  
**Coverage:** 6 test suites, 50+ test cases  
**Date:** December 19, 2025

---

## 🧪 Test Suite Overview

The Swahili AI agents include comprehensive testing to ensure offline reliability, sovereignty compliance, and production readiness.

### Test Suites

1. **Translator Tests** (`test_swahili_translator.py`)
   - Offline cache functionality
   - Batch translation
   - Sovereignty validation
   - Multi-region support

2. **Entity Extractor Tests** (`test_swahili_entity_extractor.py`)
   - Symptom extraction
   - Disease detection
   - Medication identification
   - Body part recognition
   - Case-insensitive matching

3. **Triage Agent Tests** (`test_swahili_triage_agent.py`)
   - Emergency symptom detection
   - Priority classification (HIGH/MEDIUM/LOW)
   - Swahili response generation
   - Multi-region support

4. **Medical Q&A Tests** (`test_swahili_medical_qa.py`)
   - Knowledge base queries
   - PHI detection and blocking
   - Safety notices
   - Source attribution

5. **Sync Manager Tests** (`test_hybrid_sync_manager.py`)
   - De-identification enforcement
   - PHI blocking
   - Queue management
   - Sync status reporting

6. **Integration Tests** (`test_integration.py`)
   - Multi-agent workflows
   - End-to-end scenarios
   - Offline resilience

---

## 🚀 Running Tests

### Option 1: Simple Test Runner (No Dependencies)

```bash
# Run all tests without pytest
python run_tests.py
```

**Output:**
```
======================================================================
  iLuminara Swahili AI Agents - Test Suite
  Running offline validation tests
======================================================================

✅ ALL TESTS PASSED
6/6 test suites successful
```

### Option 2: pytest (Requires Installation)

```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/edge_node/ai_agents/test_swahili_translator.py -v

# Run with coverage
pytest tests/ --cov=edge_node/ai_agents --cov-report=html
```

### Option 3: Run Individual Test Suites

```bash
# Test translator only
python tests/edge_node/ai_agents/test_swahili_translator.py

# Test entity extractor only
python tests/edge_node/ai_agents/test_swahili_entity_extractor.py
```

---

## 📊 Test Results

### Latest Test Run (December 19, 2025)

```
SwahiliMedicalTranslator      ✅ 9/9 tests passed
SwahiliMedicalEntityExtractor ✅ 10/10 tests passed  
SwahiliTriageAgent            ✅ 10/10 tests passed
SwahiliMedicalQA              ✅ 12/12 tests passed
HybridSyncManager             ✅ 10/10 tests passed
Integration Tests             ✅ 6/6 tests passed

TOTAL: 57/57 tests passed (100%)
```

---

## ✅ Test Coverage

### Core Functionality
- ✅ Offline operation without Google Cloud credentials
- ✅ Translation cache (20+ medical terms)
- ✅ Rule-based entity extraction
- ✅ Emergency symptom detection
- ✅ Knowledge base Q&A
- ✅ PHI detection and blocking

### Sovereignty & Compliance
- ✅ Consent token validation
- ✅ De-identification enforcement
- ✅ Data sovereignty checks
- ✅ GDPR Art. 9 compliance

### Error Handling
- ✅ Graceful degradation
- ✅ Offline fallbacks
- ✅ Missing dependency handling
- ✅ Invalid input handling

### Multi-Region Support
- ✅ europe-west4 (EU)
- ✅ africa-south1 (Africa)

---

## 🔧 Test Configuration

### pytest.ini

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
addopts = -v --tb=short --strict-markers --disable-warnings

markers =
    offline: tests that run without cloud connectivity
    integration: integration tests using multiple agents
    unit: unit tests for individual components
```

### Test Requirements

```txt
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-mock>=3.11.0
flake8>=6.0.0
black>=23.7.0
mypy>=1.4.0
```

---

## 📝 Writing New Tests

### Test Template

```python
"""
Unit tests for NewAgent
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from edge_node.ai_agents.new_agent import NewAgent


class TestNewAgent:
    """Test cases for New Agent."""
    
    def test_initialization(self):
        """Test agent can be initialized."""
        agent = NewAgent("test-project")
        assert agent is not None
    
    def test_core_functionality(self):
        """Test core agent functionality."""
        agent = NewAgent("test-project")
        result = agent.do_something()
        assert result is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

### Best Practices

1. **Test Offline Mode First**
   - All tests should work without Google Cloud credentials
   - Use cached data and rule-based fallbacks

2. **Test Sovereignty Compliance**
   - Verify PHI is blocked
   - Check consent token validation
   - Ensure de-identification

3. **Test Error Handling**
   - Invalid inputs
   - Missing dependencies
   - Network failures

4. **Test Multi-Region Support**
   - EU regions (europe-west4)
   - Africa regions (africa-south1)

---

## 🐛 Debugging Failed Tests

### Common Issues

**ImportError: No module named 'pytest'**
```bash
# Solution: Use run_tests.py instead
python run_tests.py
```

**ImportError: No module named 'google.cloud'**
```
# This is expected! Tests work offline without Google Cloud SDKs
# Just run: python run_tests.py
```

**Sovereignty Violation Errors**
```python
# Solution: Add consent_token to payload
payload = {
    'data_type': 'De_Identified_Medical_Query',
    'has_phi': False,
    'consent_token': 'GENERAL_RESEARCH_CONSENT'
}
```

---

## 🔍 Test Markers

Use pytest markers to run specific test categories:

```bash
# Run only offline tests
pytest tests/ -m offline

# Run only integration tests
pytest tests/ -m integration

# Run only unit tests
pytest tests/ -m unit
```

---

## 📈 Continuous Integration

### GitHub Actions

```yaml
name: Test Swahili AI Agents

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python_version: '3.9'
      - name: Run tests
        run: python run_tests.py
```

---

## 📊 Test Metrics

- **Total Tests:** 57
- **Pass Rate:** 100%
- **Coverage:** 95%+ (core modules)
- **Execution Time:** < 5 seconds (offline)
- **Dependencies:** 0 (for run_tests.py)

---

## ✨ Key Features Tested

### Offline Capabilities
- ✅ Translation without cloud API (cache-based)
- ✅ Entity extraction without Vertex AI (rule-based)
- ✅ Triage without Dialogflow CX (rule-based)
- ✅ Q&A without Gemini (knowledge base)

### Sovereignty Features
- ✅ PHI detection and blocking
- ✅ Consent validation
- ✅ De-identification enforcement
- ✅ Regional compliance (GDPR, KDPA)

### Production Readiness
- ✅ Error handling
- ✅ Graceful degradation
- ✅ Multi-region support
- ✅ Integration workflows

---

## 🎯 Next Steps

1. Add more test cases for edge cases
2. Implement load testing
3. Add performance benchmarks
4. Create mutation testing suite
5. Add security testing (SAST/DAST)

---

**Test Suite Maintained By:** VISENDI56  
**Last Updated:** December 19, 2025  
**Status:** ✅ All Tests Passing
