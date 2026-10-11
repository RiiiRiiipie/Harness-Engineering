"""
Harness Engineering - A modular framework for configurable software engineering harnesses.

This package provides a composable architecture for building and customizing
testing/evaluation harnesses tailored to specific use cases.
"""

__version__ = "0.1.0"
__author__ = "Rishabh Pandey"
__email__ = "rishi@example.com"
__license__ = "MIT"

from .core.harness import Harness
from .core.config import HarnessConfig
from .modules.base import Module, ModuleType

__all__ = [
    "Harness",
    "HarnessConfig",
    "Module",
    "ModuleType",
]