"""
Data models for the Vehicle Diagnostics Agent.
Demonstrates: dataclasses, Pydantic models, inheritance, enums.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ── Enums ──────────────────────────────────────────────────────────

class Severity(str, Enum):
    """OBD-II code severity levels."""
    CRITICAL = "critical"       # Stop driving immediately
    HIGH = "high"               # Schedule repair within days
    MODERATE = "moderate"       # Schedule within 2 weeks
    LOW = "low"                 # Monitor, fix at next service
    INFORMATIONAL = "info"      # No action needed


class VehicleSystem(str, Enum):
    """Major vehicle systems mapped to OBD-II code prefixes."""
    POWERTRAIN = "powertrain"       # P codes
    CHASSIS = "chassis"             # C codes
    BODY = "body"                   # B codes
    NETWORK = "network"             # U codes


class UrgencyLevel(str, Enum):
    """Final urgency classification for the vehicle owner."""
    STOP_DRIVING = "Stop driving. Tow to shop immediately."
    SHOP_WITHIN_48H = "Drive cautiously. Get to a shop within 48 hours."
    SCHEDULE_SOON = "Schedule a repair within 1-2 weeks."
    NEXT_SERVICE = "Address at your next scheduled service."
    MONITOR = "Monitor for recurrence. No immediate action needed."


# ── Dataclasses (OBD-II Knowledge Base entries) ─────────────────────

@dataclass
class DTCEntry:
    """
    A single Diagnostic Trouble Code entry in our knowledge base.
    This is what a technician would look up in a repair manual.
    """
    code: str                               # e.g., "P0300"
    description: str                        # e.g., "Random/Multiple Cylinder Misfire Detected"
    system: VehicleSystem
    severity: Severity
    common_causes: list[str] = field(default_factory=list)
    symptoms: list[str] = field(default_factory=list)
    typical_repair_cost_low: int = 0        # USD
    typical_repair_cost_high: int = 0       # USD
    is_emissions_related: bool = False
    can_cause_further_damage: bool = False

    def cost_range_str(self) -> str:
        return f"${self.typical_repair_cost_low} - ${self.typical_repair_cost_high}"


@dataclass
class CodeRelationship:
    """
    Defines known relationships between codes.
    When codes appear together, they often share a root cause.
    """
    primary_code: str           # The likely root cause code
    related_codes: list[str]    # Codes that are symptoms of the primary
    explanation: str            # Why these are related
    combined_severity: Severity # Severity when they appear together


# ── Pydantic Models (Structured Agent Output) ──────────────────────

class VehicleInfo(BaseModel):
    """Vehicle information provided by the user."""
    make: str = Field(description="Vehicle manufacturer (e.g., Toyota)")
    model: str = Field(description="Vehicle model (e.g., Camry)")
    year: int = Field(description="Model year")
    mileage: Optional[int] = Field(default=None, description="Current odometer reading")


class SingleCodeAnalysis(BaseModel):
    """Analysis of a single DTC code."""
    code: str = Field(description="The OBD-II diagnostic trouble code")
    description: str = Field(description="What this code means")
    system: str = Field(description="Which vehicle system is affected")
    severity: str = Field(description="Severity: critical, high, moderate, low, or info")
    likely_causes: list[str] = Field(description="Most probable causes, ordered by likelihood")
    recommended_action: str = Field(description="What the vehicle owner should do")
    estimated_cost_range: str = Field(description="Estimated repair cost range in USD")
    is_root_cause: bool = Field(description="True if this is likely a root cause, False if it is a symptom of another code")


class DiagnosticReport(BaseModel):
    """
    The complete diagnostic report output by the agent.
    This is the structured deliverable.
    """
    vehicle: VehicleInfo
    codes_analyzed: list[SingleCodeAnalysis]
    root_cause_summary: str = Field(
        description="Plain-English summary of the most likely root cause(s)"
    )
    prioritized_repair_sequence: list[str] = Field(
        description="Ordered list: fix these in this sequence for maximum efficiency"
    )
    total_estimated_cost_low: int = Field(description="Low end of total repair cost estimate")
    total_estimated_cost_high: int = Field(description="High end of total repair cost estimate")
    urgency: str = Field(description="Overall urgency classification")
    safe_to_drive: bool = Field(description="Is it safe to continue driving?")
    plain_english_summary: str = Field(
        description="Explain the entire diagnosis as if talking to someone who knows nothing about cars"
    )
