def to_amount(value: str) -> float:
    """Convert a currency string like "$1,234.56" to a float.
    Strips dollar signs, commas, and surrounding whitespace.
    """
    return float(value.replace("$", "").replace(",", "").strip())

__all__ = ["to_amount"]
