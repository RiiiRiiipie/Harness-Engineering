"""
Base module classes and types for the harness framework.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, Optional
from dataclasses import dataclass
import logging


class ModuleType(Enum):
    """Types of harness modules."""
    CONTEXT_MANAGER = "context_manager"
    STATE_TRACKER = "state_tracker"
    TOOL_COORDINATOR = "tool_coordinator"
    PARSER = "parser"
    EVALUATOR = "evaluator"
    RUNTIME_ADAPTER = "runtime_adapter"
    CUSTOM = "custom"


@dataclass
class ModuleResult:
    """Result of a module execution."""
    success: bool
    data: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class Module(ABC):
    """Base class for all harness modules."""
    
    def __init__(self, config: Dict[str, Any], logger: Optional[logging.Logger] = None):
        self.config = config
        self.logger = logger or logging.getLogger(self.__class__.__name__)
        self._initialized = False
    
    @property
    @abstractmethod
    def module_type(self) -> ModuleType:
        """Return the type of this module."""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name/identifier of this module implementation."""
        pass
    
    def initialize(self) -> ModuleResult:
        """Initialize the module. Called once before use."""
        if self._initialized:
            return ModuleResult(success=True, data="Already initialized")
        try:
            self._initialize()
            self._initialized = True
            return ModuleResult(success=True, data="Initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize {self.name}: {e}")
            return ModuleResult(success=False, error=str(e))
    
    @abstractmethod
    def _initialize(self) -> None:
        """Internal initialization logic."""
        pass
    
    @abstractmethod
    def execute(self, *args, **kwargs) -> ModuleResult:
        """Execute the module's main functionality."""
        pass
    
    def shutdown(self) -> ModuleResult:
        """Clean up resources. Called when harness shuts down."""
        try:
            self._shutdown()
            self._initialized = False
            return ModuleResult(success=True, data="Shutdown complete")
        except Exception as e:
            self.logger.error(f"Failed to shutdown {self.name}: {e}")
            return ModuleResult(success=False, error=str(e))
    
    def _shutdown(self) -> None:
        """Internal shutdown logic. Override if needed."""
        pass
    
    def health_check(self) -> ModuleResult:
        """Check if module is healthy."""
        return ModuleResult(
            success=self._initialized,
            data={"initialized": self._initialized, "name": self.name}
        )


class ContextManagerModule(Module):
    """Base class for context management modules."""
    
    @property
    def module_type(self) -> ModuleType:
        return ModuleType.CONTEXT_MANAGER


class StateTrackerModule(Module):
    """Base class for state tracking modules."""
    
    @property
    def module_type(self) -> ModuleType:
        return ModuleType.STATE_TRACKER


class ToolCoordinatorModule(Module):
    """Base class for tool coordination modules."""
    
    @property
    def module_type(self) -> ModuleType:
        return ModuleType.TOOL_COORDINATOR


class ParserModule(Module):
    """Base class for parser modules."""
    
    @property
    def module_type(self) -> ModuleType:
        return ModuleType.PARSER


class EvaluatorModule(Module):
    """Base class for evaluator modules."""
    
    @property
    def module_type(self) -> ModuleType:
        return ModuleType.EVALUATOR


class RuntimeAdapterModule(Module):
    """Base class for runtime adapter modules."""
    
    @property
    def module_type(self) -> ModuleType:
        return ModuleType.RUNTIME_ADAPTER