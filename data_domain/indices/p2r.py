"""
Price-to-Rent ratio calculation.
"""
from typing import Optional

def calculate_p2r(price: float, annual_rent: float) -> Optional[float]:
    """
    Calculate Price-to-Rent ratio.

    Args:
        price: Property price.
        annual_rent: Annual rent.

    Returns:
        P2R ratio, or None if invalid.

    >>> calculate_p2r(1000000, 50000)
    20.0
    >>> calculate_p2r(1000000, 0) is None
    True
    """
    if annual_rent <= 0:
        return None
    return price / annual_rent