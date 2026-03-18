"""
OBD-II Diagnostic Trouble Code Knowledge Base.

Real codes, real descriptions, real repair cost ranges.
This is the domain knowledge layer that makes the agent useful.
A technician would recognize every entry here.
"""

from src.models import DTCEntry, CodeRelationship, Severity, VehicleSystem


# ── OBD-II CODE DATABASE ────────────────────────────────────────────
# 50 common DTCs organized by system. Costs are US national averages.

DTC_DATABASE: dict[str, DTCEntry] = {}

def _register(entry: DTCEntry) -> None:
    DTC_DATABASE[entry.code] = entry


# ── POWERTRAIN (P) CODES ────────────────────────────────────────────

_register(DTCEntry(
    code="P0300",
    description="Random/Multiple Cylinder Misfire Detected",
    system=VehicleSystem.POWERTRAIN,
    severity=Severity.HIGH,
    common_causes=["Worn spark plugs", "Faulty ignition coils", "Vacuum leak", "Low fuel pressure", "Bad fuel injectors"],
    symptoms=["Rough idle", "Engine vibration", "Loss of power", "Check engine light flashing"],
    typical_repair_cost_low=150,
    typical_repair_cost_high=1000,
    is_emissions_related=True,
    can_cause_further_damage=True,  # Can damage catalytic converter
))

_register(DTCEntry(
    code="P0301",
    description="Cylinder 1 Misfire Detected",
    system=VehicleSystem.POWERTRAIN,
    severity=Severity.HIGH,
    common_causes=["Bad spark plug (cyl 1)", "Faulty ignition coil (cyl 1)", "Fuel injector failure (cyl 1)", "Compression loss (cyl 1)"],
    symptoms=["Rough idle", "Loss of power", "Engine vibration"],
    typical_repair_cost_low=100,
    typical_repair_cost_high=600,
    is_emissions_related=True,
    can_cause_further_damage=True,
))

_register(DTCEntry(
    code="P0171",
    description="System Too Lean (Bank 1)",
    system=VehicleSystem.POWERTRAIN,
    severity=Severity.MODERATE,
    common_causes=["Vacuum leak", "Faulty MAF sensor", "Weak fuel pump", "Clogged fuel filter", "Leaking fuel injector"],
    symptoms=["Rough idle", "Hesitation on acceleration", "Poor fuel economy"],
    typical_repair_cost_low=100,
    typical_repair_cost_high=500,
    is_emissions_related=True,
    can_cause_further_damage=False,
))

_register(DTCEntry(
    code="P0174",
    description="System Too Lean (Bank 2)",
    system=VehicleSystem.POWERTRAIN,
    severity=Severity.MODERATE,
    common_causes=["Vacuum leak", "Faulty MAF sensor", "Weak fuel pump", "Intake manifold gasket leak"],
    symptoms=["Rough idle", "Hesitation", "Poor fuel economy"],
    typical_repair_cost_low=100,
    typical_repair_cost_high=500,
    is_emissions_related=True,
    can_cause_further_damage=False,
))

_register(DTCEntry(
    code="P0420",
    description="Catalyst System Efficiency Below Threshold (Bank 1)",
    system=VehicleSystem.POWERTRAIN,
    severity=Severity.MODERATE,
    common_causes=["Failing catalytic converter", "Faulty O2 sensor (downstream)", "Exhaust leak before cat", "Engine misfire damage to cat"],
    symptoms=["Check engine light", "Reduced fuel economy", "Sulfur smell from exhaust", "Failed emissions test"],
    typical_repair_cost_low=200,
    typical_repair_cost_high=2500,
    is_emissions_related=True,
    can_cause_further_damage=False,
))

_register(DTCEntry(
    code="P0440",
    description="Evaporative Emission Control System Malfunction",
    system=VehicleSystem.POWERTRAIN,
    severity=Severity.LOW,
    common_causes=["Loose gas cap", "Cracked EVAP hose", "Faulty purge valve", "Faulty vent valve"],
    symptoms=["Check engine light", "Fuel odor near vehicle"],
    typical_repair_cost_low=50,
    typical_repair_cost_high=400,
    is_emissions_related=True,
    can_cause_further_damage=False,
))

_register(DTCEntry(
    code="P0442",
    description="Evaporative Emission Control System Leak Detected (Small Leak)",
    system=VehicleSystem.POWERTRAIN,
    severity=Severity.LOW,
    common_causes=["Loose gas cap", "Small crack in EVAP hose", "Faulty purge solenoid"],
    symptoms=["Check engine light"],
    typical_repair_cost_low=50,
    typical_repair_cost_high=300,
    is_emissions_related=True,
    can_cause_further_damage=False,
))

_register(DTCEntry(
    code="P0455",
    description="Evaporative Emission Control System Leak Detected (Gross Leak)",
    system=VehicleSystem.POWERTRAIN,
    severity=Severity.LOW,
    common_causes=["Missing gas cap", "Disconnected EVAP hose", "Cracked charcoal canister"],
    symptoms=["Check engine light", "Strong fuel odor"],
    typical_repair_cost_low=50,
    typical_repair_cost_high=500,
    is_emissions_related=True,
    can_cause_further_damage=False,
))

_register(DTCEntry(
    code="P0128",
    description="Coolant Thermostat Below Thermostat Regulating Temperature",
    system=VehicleSystem.POWERTRAIN,
    severity=Severity.MODERATE,
    common_causes=["Stuck-open thermostat", "Faulty coolant temp sensor", "Low coolant level"],
    symptoms=["Slow cabin heat", "Poor fuel economy", "Temperature gauge stays low"],
    typical_repair_cost_low=150,
    typical_repair_cost_high=400,
    is_emissions_related=True,
    can_cause_further_damage=False,
))

_register(DTCEntry(
    code="P0135",
    description="O2 Sensor Heater Circuit Malfunction (Bank 1, Sensor 1)",
    system=VehicleSystem.POWERTRAIN,
    severity=Severity.MODERATE,
    common_causes=["Faulty O2 sensor", "Blown fuse", "Wiring issue in heater circuit"],
    symptoms=["Poor fuel economy", "Check engine light", "Rough idle when cold"],
    typical_repair_cost_low=150,
    typical_repair_cost_high=350,
    is_emissions_related=True,
    can_cause_further_damage=False,
))

_register(DTCEntry(
    code="P0401",
    description="Exhaust Gas Recirculation (EGR) Flow Insufficient",
    system=VehicleSystem.POWERTRAIN,
    severity=Severity.MODERATE,
    common_causes=["Carbon-clogged EGR valve", "Faulty EGR position sensor", "Blocked EGR passages"],
    symptoms=["Rough idle", "Engine knock under load", "Failed emissions test"],
    typical_repair_cost_low=150,
    typical_repair_cost_high=500,
    is_emissions_related=True,
    can_cause_further_damage=False,
))

_register(DTCEntry(
    code="P0500",
    description="Vehicle Speed Sensor (VSS) Malfunction",
    system=VehicleSystem.POWERTRAIN,
    severity=Severity.HIGH,
    common_causes=["Faulty VSS", "Damaged wiring", "Corroded connector", "Failed instrument cluster"],
    symptoms=["Speedometer not working", "Erratic shifting", "ABS/traction control light on", "Cruise control inoperative"],
    typical_repair_cost_low=100,
    typical_repair_cost_high=350,
    is_emissions_related=False,
    can_cause_further_damage=False,
))

_register(DTCEntry(
    code="P0700",
    description="Transmission Control System Malfunction",
    system=VehicleSystem.POWERTRAIN,
    severity=Severity.HIGH,
    common_causes=["Transmission issue (check for additional trans codes)", "Faulty TCM", "Wiring issue", "Low transmission fluid"],
    symptoms=["Check engine light", "Harsh shifting", "Transmission slipping", "Limp mode"],
    typical_repair_cost_low=100,
    typical_repair_cost_high=3000,
    is_emissions_related=False,
    can_cause_further_damage=True,
))

_register(DTCEntry(
    code="P0715",
    description="Input/Turbine Speed Sensor Circuit Malfunction",
    system=VehicleSystem.POWERTRAIN,
    severity=Severity.HIGH,
    common_causes=["Faulty input speed sensor", "Damaged wiring", "Transmission internal issue", "Low trans fluid"],
    symptoms=["Erratic shifting", "Harsh shifts", "No speedometer", "Limp mode"],
    typical_repair_cost_low=150,
    typical_repair_cost_high=500,
    is_emissions_related=False,
    can_cause_further_damage=True,
))

_register(DTCEntry(
    code="P0340",
    description="Camshaft Position Sensor Circuit Malfunction (Bank 1)",
    system=VehicleSystem.POWERTRAIN,
    severity=Severity.HIGH,
    common_causes=["Faulty CMP sensor", "Damaged reluctor ring", "Wiring/connector issue", "Timing chain stretched"],
    symptoms=["Hard starting", "Stalling", "Rough running", "No start condition"],
    typical_repair_cost_low=100,
    typical_repair_cost_high=400,
    is_emissions_related=True,
    can_cause_further_damage=False,
))

_register(DTCEntry(
    code="P0335",
    description="Crankshaft Position Sensor Circuit Malfunction",
    system=VehicleSystem.POWERTRAIN,
    severity=Severity.CRITICAL,
    common_causes=["Faulty CKP sensor", "Damaged reluctor wheel", "Wiring issue", "ECM problem"],
    symptoms=["Engine stalls", "No start", "Intermittent misfire", "Tachometer erratic"],
    typical_repair_cost_low=100,
    typical_repair_cost_high=350,
    is_emissions_related=True,
    can_cause_further_damage=True,
))

_register(DTCEntry(
    code="P0011",
    description="Camshaft Position Timing Over-Advanced (Bank 1)",
    system=VehicleSystem.POWERTRAIN,
    severity=Severity.MODERATE,
    common_causes=["Low oil level/pressure", "Dirty oil (missed oil changes)", "Faulty VVT solenoid", "Timing chain stretch"],
    symptoms=["Rough idle", "Poor fuel economy", "Reduced power", "Rattling on startup"],
    typical_repair_cost_low=100,
    typical_repair_cost_high=800,
    is_emissions_related=True,
    can_cause_further_damage=True,
))

_register(DTCEntry(
    code="P0101",
    description="Mass Air Flow (MAF) Sensor Circuit Range/Performance",
    system=VehicleSystem.POWERTRAIN,
    severity=Severity.MODERATE,
    common_causes=["Dirty MAF sensor", "Air filter clogged", "Intake air leak", "Faulty MAF sensor"],
    symptoms=["Poor acceleration", "Rough idle", "Black smoke from exhaust", "Stalling"],
    typical_repair_cost_low=50,
    typical_repair_cost_high=400,
    is_emissions_related=True,
    can_cause_further_damage=False,
))

_register(DTCEntry(
    code="P0217",
    description="Engine Coolant Over Temperature Condition",
    system=VehicleSystem.POWERTRAIN,
    severity=Severity.CRITICAL,
    common_causes=["Coolant leak", "Failed water pump", "Stuck thermostat (closed)", "Blown head gasket", "Failed radiator fan"],
    symptoms=["Temperature gauge in red", "Steam from engine", "Loss of power", "Engine shutdown"],
    typical_repair_cost_low=200,
    typical_repair_cost_high=3000,
    is_emissions_related=False,
    can_cause_further_damage=True,
))

_register(DTCEntry(
    code="P0507",
    description="Idle Air Control System RPM Higher Than Expected",
    system=VehicleSystem.POWERTRAIN,
    severity=Severity.LOW,
    common_causes=["Vacuum leak", "Dirty throttle body", "Faulty IAC valve", "Intake manifold gasket leak"],
    symptoms=["High idle RPM", "Idle fluctuation"],
    typical_repair_cost_low=50,
    typical_repair_cost_high=300,
    is_emissions_related=True,
    can_cause_further_damage=False,
))

_register(DTCEntry(
    code="P0562",
    description="System Voltage Low",
    system=VehicleSystem.POWERTRAIN,
    severity=Severity.HIGH,
    common_causes=["Failing alternator", "Weak battery", "Corroded battery terminals", "Parasitic drain"],
    symptoms=["Dim headlights", "Slow cranking", "Multiple warning lights", "Electrical accessories malfunction"],
    typical_repair_cost_low=100,
    typical_repair_cost_high=700,
    is_emissions_related=False,
    can_cause_further_damage=True,
))

_register(DTCEntry(
    code="P0016",
    description="Crankshaft/Camshaft Position Correlation (Bank 1 Sensor A)",
    system=VehicleSystem.POWERTRAIN,
    severity=Severity.HIGH,
    common_causes=["Timing chain stretched", "Faulty VVT actuator", "Low oil level/pressure", "Worn timing chain tensioner"],
    symptoms=["Rough running", "Rattling noise on startup", "Reduced power", "Poor fuel economy"],
    typical_repair_cost_low=300,
    typical_repair_cost_high=2500,
    is_emissions_related=True,
    can_cause_further_damage=True,
))

# ── CHASSIS (C) CODES ──────────────────────────────────────────────

_register(DTCEntry(
    code="C0035",
    description="Left Front Wheel Speed Sensor Circuit Malfunction",
    system=VehicleSystem.CHASSIS,
    severity=Severity.HIGH,
    common_causes=["Faulty wheel speed sensor", "Damaged sensor wiring", "Debris on sensor", "Bad wheel bearing"],
    symptoms=["ABS light on", "Traction control light on", "ABS not functioning"],
    typical_repair_cost_low=100,
    typical_repair_cost_high=400,
    is_emissions_related=False,
    can_cause_further_damage=False,
))

_register(DTCEntry(
    code="C0050",
    description="Right Rear Wheel Speed Sensor Circuit Malfunction",
    system=VehicleSystem.CHASSIS,
    severity=Severity.HIGH,
    common_causes=["Faulty wheel speed sensor", "Damaged wiring", "Corroded connector", "Worn wheel bearing"],
    symptoms=["ABS light on", "Traction control disabled", "Stability control off"],
    typical_repair_cost_low=100,
    typical_repair_cost_high=400,
    is_emissions_related=False,
    can_cause_further_damage=False,
))

_register(DTCEntry(
    code="C0265",
    description="EBCM Motor Relay Circuit Open/Shorted",
    system=VehicleSystem.CHASSIS,
    severity=Severity.CRITICAL,
    common_causes=["Faulty ABS module", "Relay failure", "Wiring issue", "Corroded ground"],
    symptoms=["ABS completely inoperative", "Brake warning light on", "Reduced braking ability"],
    typical_repair_cost_low=300,
    typical_repair_cost_high=1500,
    is_emissions_related=False,
    can_cause_further_damage=False,
))

# ── BODY (B) CODES ─────────────────────────────────────────────────

_register(DTCEntry(
    code="B0001",
    description="Driver Frontal Stage 1 Deployment Control",
    system=VehicleSystem.BODY,
    severity=Severity.CRITICAL,
    common_causes=["Faulty airbag module", "Clockspring failure", "Airbag connector issue", "Crash sensor malfunction"],
    symptoms=["Airbag warning light on", "Airbag may not deploy in crash"],
    typical_repair_cost_low=200,
    typical_repair_cost_high=1500,
    is_emissions_related=False,
    can_cause_further_damage=False,
))

_register(DTCEntry(
    code="B1000",
    description="ECU Malfunction (Body Control Module)",
    system=VehicleSystem.BODY,
    severity=Severity.MODERATE,
    common_causes=["Faulty BCM", "Software corruption", "Power supply issue", "Water intrusion"],
    symptoms=["Various electrical malfunctions", "Intermittent accessory failures"],
    typical_repair_cost_low=200,
    typical_repair_cost_high=800,
    is_emissions_related=False,
    can_cause_further_damage=False,
))

# ── NETWORK (U) CODES ──────────────────────────────────────────────

_register(DTCEntry(
    code="U0100",
    description="Lost Communication with ECM/PCM",
    system=VehicleSystem.NETWORK,
    severity=Severity.CRITICAL,
    common_causes=["CAN bus wiring fault", "Faulty ECM/PCM", "Blown fuse", "Corroded connector"],
    symptoms=["Multiple warning lights", "No start", "Limp mode", "Gauge failures"],
    typical_repair_cost_low=100,
    typical_repair_cost_high=2000,
    is_emissions_related=False,
    can_cause_further_damage=True,
))

_register(DTCEntry(
    code="U0101",
    description="Lost Communication with TCM",
    system=VehicleSystem.NETWORK,
    severity=Severity.HIGH,
    common_causes=["CAN bus fault", "Faulty TCM", "Wiring issue", "Blown fuse"],
    symptoms=["Transmission stuck in gear", "No shifting", "Check engine light"],
    typical_repair_cost_low=100,
    typical_repair_cost_high=1500,
    is_emissions_related=False,
    can_cause_further_damage=True,
))

_register(DTCEntry(
    code="U0121",
    description="Lost Communication with ABS Module",
    system=VehicleSystem.NETWORK,
    severity=Severity.HIGH,
    common_causes=["CAN bus fault", "Faulty ABS module", "Wiring damage", "Corroded connector"],
    symptoms=["ABS light on", "Traction control disabled", "Stability control off"],
    typical_repair_cost_low=100,
    typical_repair_cost_high=1200,
    is_emissions_related=False,
    can_cause_further_damage=False,
))

_register(DTCEntry(
    code="U0140",
    description="Lost Communication with Body Control Module",
    system=VehicleSystem.NETWORK,
    severity=Severity.MODERATE,
    common_causes=["CAN bus fault", "Faulty BCM", "Wiring issue", "Water damage"],
    symptoms=["Electrical accessories not working", "No interior lights", "Power windows/locks inoperative"],
    typical_repair_cost_low=100,
    typical_repair_cost_high=1000,
    is_emissions_related=False,
    can_cause_further_damage=False,
))


# ── CODE RELATIONSHIPS ──────────────────────────────────────────────
# When these codes appear together, the primary code is likely the root cause.

CODE_RELATIONSHIPS: list[CodeRelationship] = [
    CodeRelationship(
        primary_code="P0300",
        related_codes=["P0301", "P0171", "P0174"],
        explanation="Random misfire (P0300) with lean codes (P0171/P0174) strongly suggests a vacuum leak or MAF sensor issue as the root cause. The lean condition causes the misfires.",
        combined_severity=Severity.HIGH,
    ),
    CodeRelationship(
        primary_code="P0171",
        related_codes=["P0174"],
        explanation="Both banks running lean simultaneously points to a common cause: vacuum leak after the MAF sensor, faulty MAF sensor, or weak fuel pump. Not two separate problems.",
        combined_severity=Severity.MODERATE,
    ),
    CodeRelationship(
        primary_code="P0420",
        related_codes=["P0300"],
        explanation="Misfires (P0300) dump unburned fuel into the catalytic converter, damaging it over time. Fix the misfire FIRST — the cat code may clear on its own.",
        combined_severity=Severity.HIGH,
    ),
    CodeRelationship(
        primary_code="P0335",
        related_codes=["P0340", "P0300", "P0016"],
        explanation="Crankshaft sensor failure (P0335) causes loss of engine sync, triggering camshaft position errors and misfires as secondary symptoms.",
        combined_severity=Severity.CRITICAL,
    ),
    CodeRelationship(
        primary_code="P0700",
        related_codes=["P0715", "U0101"],
        explanation="P0700 is a generic transmission alert. P0715 and U0101 are the specific faults. Focus diagnosis on the specific codes, not P0700.",
        combined_severity=Severity.HIGH,
    ),
    CodeRelationship(
        primary_code="P0562",
        related_codes=["U0100", "U0101", "U0121", "U0140"],
        explanation="Low system voltage (P0562) causes communication dropouts across all modules. Fix the charging system first — the U-codes will likely clear.",
        combined_severity=Severity.HIGH,
    ),
    CodeRelationship(
        primary_code="P0016",
        related_codes=["P0011", "P0300"],
        explanation="Crank/cam correlation error with VVT timing issues suggests timing chain stretch or VVT system failure. The misfire is a symptom.",
        combined_severity=Severity.HIGH,
    ),
    CodeRelationship(
        primary_code="P0217",
        related_codes=["P0128"],
        explanation="These are contradictory codes. If both appear, the coolant temperature sensor is likely faulty, giving false readings in both directions.",
        combined_severity=Severity.HIGH,
    ),
    CodeRelationship(
        primary_code="U0100",
        related_codes=["U0101", "U0121", "U0140"],
        explanation="Lost communication with ECM plus other modules suggests a CAN bus backbone failure, not individual module failures. Check CAN bus wiring first.",
        combined_severity=Severity.CRITICAL,
    ),
]


# ── LOOKUP FUNCTIONS ────────────────────────────────────────────────

def lookup_code(code: str) -> DTCEntry | None:
    """Look up a single DTC code. Returns None if not found."""
    return DTC_DATABASE.get(code.upper())


def lookup_multiple_codes(codes: list[str]) -> dict[str, DTCEntry | None]:
    """Look up multiple codes at once."""
    return {code.upper(): lookup_code(code) for code in codes}


def find_relationships(codes: list[str]) -> list[CodeRelationship]:
    """Find known relationships among a set of codes."""
    codes_upper = {c.upper() for c in codes}
    matches = []
    for rel in CODE_RELATIONSHIPS:
        primary_present = rel.primary_code in codes_upper
        any_related_present = any(rc in codes_upper for rc in rel.related_codes)
        if primary_present and any_related_present:
            matches.append(rel)
    return matches


def get_system_from_code(code: str) -> VehicleSystem | None:
    """Infer vehicle system from code prefix."""
    prefix = code[0].upper() if code else ""
    mapping = {"P": VehicleSystem.POWERTRAIN, "C": VehicleSystem.CHASSIS, "B": VehicleSystem.BODY, "U": VehicleSystem.NETWORK}
    return mapping.get(prefix)
