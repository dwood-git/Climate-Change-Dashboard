"""
Components package for the wildfire climate change visualization dashboard.

This package contains all UI components and callback functions.
"""

from .layout import get_main_layout
from .callbacks import register_callbacks
from .dashboard_components import (
    create_historical_trends_section,
    create_vegetation_section,
    create_correlations_section
)
from .footer import get_footer

__all__ = [
    'get_main_layout',
    'register_callbacks',
    'create_historical_trends_section',
    'create_vegetation_section',
    'create_correlations_section',
    'get_footer'
] 