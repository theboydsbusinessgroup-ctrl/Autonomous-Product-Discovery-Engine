"""Product specification primitives used before production begins."""

from dataclasses import dataclass, field


@dataclass
class ProductSpec:
    name: str
    buyer: str
    problem: str
    promised_outcome: str
    format: str
    target_price: float
    marketplace: str
    differentiation: str
    components: list[str] = field(default_factory=list)
    support_risk: str = "low"
    rights_status: str = "original"

    def is_launchable(self) -> bool:
        """A spec is launchable only when core commercial facts are defined."""
        return all(
            [
                self.name.strip(),
                self.buyer.strip(),
                self.problem.strip(),
                self.promised_outcome.strip(),
                self.format.strip(),
                self.marketplace.strip(),
                self.differentiation.strip(),
            ]
        ) and self.target_price > 0 and self.rights_status == "original"
