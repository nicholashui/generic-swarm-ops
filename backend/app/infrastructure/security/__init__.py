"""Security helpers — domain isolation, allow-list invariants (Wave 4)."""

from app.infrastructure.security.domain_isolation import (
    allowlists_equal,
    domain_prefix,
    is_cross_namespace_tool,
)

__all__ = [
    "allowlists_equal",
    "domain_prefix",
    "is_cross_namespace_tool",
]
