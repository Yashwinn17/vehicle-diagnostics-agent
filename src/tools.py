"""
LangChain tools for the Vehicle Diagnostics Agent.

Each tool wraps domain logic and exposes it to the LLM via function calling.
The agent decides WHEN and HOW to use these tools based on the user's input.
"""

from langchain_core.tools import tool

from src.obd_database import (
    lookup_code,
    lookup_multiple_codes,
    find_relationships,
    get_system_from_code,
    DTC_DATABASE,
)
from src.models import Severity


@tool
def lookup_codes(codes: list[str]) -> str:
    """Look up OBD-II diagnostic trouble codes and return detailed information.
    
    Use this tool FIRST for every diagnosis. Pass ALL codes the user provides.
    Returns: description, severity, common causes, symptoms, and repair costs for each code.
    
    Args:
        codes: List of OBD-II codes like ["P0300", "P0171", "P0420"]
    """
    results = lookup_multiple_codes(codes)
    output_parts = []
    
    for code, entry in results.items():
        if entry is None:
            # Code not in our database — still provide what we can infer
            system = get_system_from_code(code)
            system_str = system.value if system else "unknown"
            output_parts.append(
                f"**{code}**: Not in local database. System: {system_str}. "
                f"Use your automotive knowledge to analyze this code. "
                f"It may be a manufacturer-specific code."
            )
        else:
            causes = ", ".join(entry.common_causes[:4])
            symptoms = ", ".join(entry.symptoms[:3])
            output_parts.append(
                f"**{code}**: {entry.description}\n"
                f"  System: {entry.system.value}\n"
                f"  Severity: {entry.severity.value}\n"
                f"  Common causes: {causes}\n"
                f"  Symptoms: {symptoms}\n"
                f"  Cost range: {entry.cost_range_str()}\n"
                f"  Emissions related: {'Yes' if entry.is_emissions_related else 'No'}\n"
                f"  Can cause further damage: {'YES - fix soon' if entry.can_cause_further_damage else 'No'}"
            )
    
    return "\n\n".join(output_parts)


@tool
def find_code_relationships(codes: list[str]) -> str:
    """Analyze relationships between multiple OBD-II codes to find root causes.
    
    ALWAYS use this tool when the user provides 2+ codes. It reveals which codes
    are root causes and which are symptoms, preventing unnecessary repairs.
    
    Args:
        codes: List of OBD-II codes to analyze relationships between
    """
    relationships = find_relationships(codes)
    
    if not relationships:
        return (
            "No known relationships found between these specific codes in the database. "
            "Analyze each code independently, but use your automotive knowledge to check "
            "if they could share a common cause (e.g., vacuum leak, electrical issue, etc.)."
        )
    
    output_parts = ["**Known Code Relationships Found:**\n"]
    for rel in relationships:
        related_present = [rc for rc in rel.related_codes if rc.upper() in {c.upper() for c in codes}]
        output_parts.append(
            f"ROOT CAUSE: {rel.primary_code} → triggers: {', '.join(related_present)}\n"
            f"  Explanation: {rel.explanation}\n"
            f"  Combined severity: {rel.combined_severity.value}\n"
            f"  ACTION: Fix {rel.primary_code} first. {', '.join(related_present)} may clear on their own."
        )
    
    return "\n\n".join(output_parts)


@tool
def estimate_repair(codes: list[str], vehicle_year: int = 2020) -> str:
    """Estimate total repair costs and generate a prioritized repair sequence.
    
    Use this tool AFTER analyzing codes and relationships. It calculates costs
    and provides the optimal repair order.
    
    Args:
        codes: List of OBD-II codes to estimate costs for
        vehicle_year: Vehicle model year (older vehicles may cost more due to parts availability)
    """
    results = lookup_multiple_codes(codes)
    relationships = find_relationships(codes)
    
    # Identify root causes vs symptoms
    symptom_codes = set()
    for rel in relationships:
        for rc in rel.related_codes:
            if rc.upper() in {c.upper() for c in codes}:
                symptom_codes.add(rc.upper())
    
    # Age multiplier (older cars = slightly higher costs)
    import datetime
    car_age = datetime.datetime.now().year - vehicle_year
    age_multiplier = 1.0 + max(0, (car_age - 5)) * 0.03  # 3% increase per year over 5 years old
    age_multiplier = min(age_multiplier, 1.5)  # Cap at 50% increase
    
    # Build prioritized repair sequence
    severity_order = {
        Severity.CRITICAL: 0,
        Severity.HIGH: 1,
        Severity.MODERATE: 2,
        Severity.LOW: 3,
        Severity.INFORMATIONAL: 4,
    }
    
    repair_items = []
    total_low = 0
    total_high = 0
    
    # Sort by: root causes first, then by severity
    for code, entry in sorted(
        results.items(),
        key=lambda x: (
            x[0] in symptom_codes,  # Root causes first (False < True)
            severity_order.get(x[1].severity, 5) if x[1] else 5,
        ),
    ):
        if entry is None:
            repair_items.append(f"  {code}: Unknown code — requires manual diagnosis ($100-$200 diagnostic fee)")
            total_low += 100
            total_high += 200
            continue
        
        adj_low = int(entry.typical_repair_cost_low * age_multiplier)
        adj_high = int(entry.typical_repair_cost_high * age_multiplier)
        
        is_symptom = code in symptom_codes
        note = " (SYMPTOM — may resolve after root cause fix)" if is_symptom else " (ROOT CAUSE — fix this first)"
        
        repair_items.append(
            f"  {code}: {entry.description}\n"
            f"    Priority: {entry.severity.value.upper()}{note}\n"
            f"    Estimated cost: ${adj_low} - ${adj_high}"
        )
        
        if not is_symptom:  # Only count root cause costs
            total_low += adj_low
            total_high += adj_high
    
    # Determine overall safety
    safety_critical = any(
        entry and entry.severity == Severity.CRITICAL
        for entry in results.values()
    )
    damage_risk = any(
        entry and entry.can_cause_further_damage
        for entry in results.values()
    )
    
    safety_note = ""
    if safety_critical:
        safety_note = "⚠️ SAFETY CRITICAL: Do NOT drive this vehicle. Tow to repair facility."
    elif damage_risk:
        safety_note = "⚠️ DAMAGE RISK: Continued driving may cause additional expensive damage. Repair within 48 hours."
    
    return (
        f"**Repair Estimate for {vehicle_year} vehicle:**\n\n"
        f"**Prioritized Repair Sequence:**\n"
        + "\n\n".join(repair_items)
        + f"\n\n**Total Estimated Cost (root cause repairs): ${total_low} - ${total_high}**\n"
        f"Note: Symptom codes may resolve without separate repair. Re-scan after root cause fixes.\n"
        f"Vehicle age adjustment: {car_age} years ({age_multiplier:.0%} of base cost)\n"
        f"\n{safety_note}"
    )


# Export all tools as a list for the agent
ALL_TOOLS = [lookup_codes, find_code_relationships, estimate_repair]
