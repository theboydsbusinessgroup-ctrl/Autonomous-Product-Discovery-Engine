"""Guardrails used before an opportunity can advance."""

BLOCKED_REASON_CODES = {
    "regulated_or_high_stakes",
    "unclear_ip_rights",
    "copyright_or_trademark_dependency",
    "questionable_plr_mrr_rights",
    "custom_service_heavy",
    "material_upfront_commitment",
}


def is_eligible(*, ip_risk: float, blocked_reasons: set[str] | None = None) -> bool:
    """Return whether an opportunity is eligible for automated advancement.

    IP risk is a 0-100 score where higher is safer. Any explicit blocked reason
    prevents advancement regardless of the numeric opportunity score.
    """
    reasons = blocked_reasons or set()
    if reasons & BLOCKED_REASON_CODES:
        return False
    return float(ip_risk) >= 60
