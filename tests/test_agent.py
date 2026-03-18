"""
Tests for the Vehicle Diagnostics Agent.
These test the knowledge base and tools WITHOUT hitting the OpenAI API.
"""

import pytest
from src.obd_database import (
    lookup_code,
    lookup_multiple_codes,
    find_relationships,
    get_system_from_code,
    DTC_DATABASE,
)
from src.models import Severity, VehicleSystem


class TestOBDDatabase:
    """Tests for the OBD-II knowledge base."""
    
    def test_database_has_entries(self):
        assert len(DTC_DATABASE) >= 30, "Database should have at least 30 codes"
    
    def test_lookup_known_code(self):
        entry = lookup_code("P0300")
        assert entry is not None
        assert entry.description == "Random/Multiple Cylinder Misfire Detected"
        assert entry.severity == Severity.HIGH
        assert entry.system == VehicleSystem.POWERTRAIN
    
    def test_lookup_unknown_code(self):
        entry = lookup_code("P9999")
        assert entry is None
    
    def test_lookup_case_insensitive(self):
        entry = lookup_code("p0300")
        assert entry is not None
    
    def test_multiple_lookup(self):
        results = lookup_multiple_codes(["P0300", "P0171", "FAKE1"])
        assert results["P0300"] is not None
        assert results["P0171"] is not None
        assert results["FAKE1"] is None
    
    def test_cost_range_string(self):
        entry = lookup_code("P0300")
        assert entry is not None
        cost = entry.cost_range_str()
        assert "$" in cost
        assert "-" in cost


class TestCodeRelationships:
    """Tests for the root cause / symptom detection."""
    
    def test_misfire_lean_relationship(self):
        rels = find_relationships(["P0300", "P0171", "P0174"])
        assert len(rels) > 0
        # Should find the lean-causes-misfire relationship
        primary_codes = [r.primary_code for r in rels]
        assert any(code in primary_codes for code in ["P0300", "P0171"])
    
    def test_no_relationship(self):
        rels = find_relationships(["P0440", "C0035"])
        assert len(rels) == 0
    
    def test_electrical_cascade(self):
        rels = find_relationships(["P0562", "U0100", "U0101"])
        assert len(rels) > 0
        # P0562 should be identified as root cause
        assert any(r.primary_code == "P0562" for r in rels)
    
    def test_single_code_no_relationship(self):
        rels = find_relationships(["P0300"])
        assert len(rels) == 0


class TestSystemInference:
    """Tests for system identification from code prefix."""
    
    def test_powertrain(self):
        assert get_system_from_code("P0300") == VehicleSystem.POWERTRAIN
    
    def test_chassis(self):
        assert get_system_from_code("C0035") == VehicleSystem.CHASSIS
    
    def test_body(self):
        assert get_system_from_code("B0001") == VehicleSystem.BODY
    
    def test_network(self):
        assert get_system_from_code("U0100") == VehicleSystem.NETWORK
    
    def test_unknown(self):
        assert get_system_from_code("X1234") is None


class TestSeverityClassification:
    """Tests that critical codes are properly classified."""
    
    def test_critical_codes_exist(self):
        critical_codes = [
            code for code, entry in DTC_DATABASE.items()
            if entry.severity == Severity.CRITICAL
        ]
        assert len(critical_codes) >= 3, "Should have at least 3 critical codes"
    
    def test_overheating_is_critical(self):
        entry = lookup_code("P0217")
        assert entry is not None
        assert entry.severity == Severity.CRITICAL
        assert entry.can_cause_further_damage is True
    
    def test_loose_gas_cap_is_low(self):
        entry = lookup_code("P0440")
        assert entry is not None
        assert entry.severity == Severity.LOW
    
    def test_airbag_is_critical(self):
        entry = lookup_code("B0001")
        assert entry is not None
        assert entry.severity == Severity.CRITICAL


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
