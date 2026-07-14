from __future__ import annotations

from typing import Any


FEATURE_KEYS = (
    "home",
    "console",
    "claims",
    "shop",
    "fleet",
    "team",
    "van",
    "portal_admin",
)


def default_features(user: dict[str, Any]) -> dict[str, bool]:
    role = str(user.get("role") or "").lower()
    is_admin = bool(user.get("is_admin"))
    is_supervisor = bool(user.get("is_supervisor"))
    has_tech = bool(user.get("tech_id"))
    out = {k: False for k in FEATURE_KEYS}
    out["home"] = True
    out["van"] = has_tech
    if is_admin:
        return {k: True for k in FEATURE_KEYS}
    if role in ("inventory", "fleet"):
        out["fleet"] = True
        out["home"] = True
        return out
    if is_supervisor:
        out["claims"] = True
        out["team"] = True
        out["van"] = has_tech
        return out
    return out


def merge_overrides(
    defaults: dict[str, bool], overrides: dict[str, bool] | None
) -> dict[str, bool]:
    if not overrides:
        return dict(defaults)
    merged = dict(defaults)
    for key, value in overrides.items():
        if key in FEATURE_KEYS:
            merged[key] = bool(value)
    return merged


def can_see_record(
    user: dict[str, Any],
    record_office: str,
    record_tech_id: int | None = None,
) -> bool:
    if user.get("is_admin"):
        return True
    allowed = {o.lower() for o in (user.get("offices") or []) if o}
    if allowed and str(record_office or "").lower() not in allowed:
        return False
    if user.get("tech_id") and record_tech_id is not None:
        return int(user["tech_id"]) == int(record_tech_id)
    return True


def resolve_user_access(user: dict[str, Any]) -> dict[str, Any]:
    defaults = default_features(user)
    features = merge_overrides(defaults, user.get("feature_overrides"))
    return {
        "user_id": user.get("id"),
        "features": features,
        "offices": list(user.get("offices") or []),
        "tech_id": user.get("tech_id"),
    }
