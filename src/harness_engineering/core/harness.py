"""
Core Harness class - the main entry point for the framework.
"""

from typing import Dict, Any, Optional, List, Type
from dataclasses import dataclass, field
import logging
import importlib

from .config import HarnessConfig, ModuleConfig
from ..modules.base import (
    Module, ModuleType, ModuleResult,
    ContextManagerModule, StateTrackerModule, ToolCoordinatorModule,
    ParserModule, EvaluatorModule, RuntimeAdapterModule
)


# Module type to base class mapping
MODULE_BASE_CLASSES = {
    ModuleType.CONTEXT_MANAGER: ContextManagerModule,
    ModuleType.STATE_TRACKER: StateTrackerModule,
    ModuleType.TOOL_COORDINATOR: ToolCoordinatorModule,
    ModuleType.PARSER: ParserModule,
    ModuleType.EVALUATOR: EvaluatorModule,
    ModuleType.RUNTIME_ADAPTER: RuntimeAdapterModule,
    ModuleType.CUSTOM: Module,  # Base Module class for custom modules
}


@dataclass
class HarnessResult:
    """Result of a harness execution."""
    success: bool
    task_id: str
    output: Any = None
    error: Optional[str] = None
    metrics: Dict[str, Any] = field(default_factory=dict)
    trace: List[Dict[str, Any]] = field(default_factory=list)


class Harness:
    """
    Main Harness class that orchestrates all modules.
    
    The harness is configured declaratively via HarnessConfig and
    dynamically loads/instantiates the appropriate module implementations.
    """
    
    # Registry of available module implementations
    _module_registry: Dict[ModuleType, Dict[str, Type[Module]]] = {
        ModuleType.CONTEXT_MANAGER: {},
        ModuleType.STATE_TRACKER: {},
        ModuleType.TOOL_COORDINATOR: {},
        ModuleType.PARSER: {},
        ModuleType.EVALUATOR: {},
        ModuleType.RUNTIME_ADAPTER: {},
        ModuleType.CUSTOM: {},
    }
    
    def __init__(self, config: HarnessConfig, logger: Optional[logging.Logger] = None):
        self.config = config
        self.logger = logger or logging.getLogger("harness_engineering")
        self.modules: Dict[ModuleType, Module] = {}
        self._initialized = False
    
    @classmethod
    def register_module(cls, module_type: ModuleType, name: str, module_class: Type[Module]) -> None:
        """Register a module implementation."""
        if not issubclass(module_class, MODULE_BASE_CLASSES[module_type]):
            raise ValueError(f"Module class must inherit from {MODULE_BASE_CLASSES[module_type]}")
        cls._module_registry[module_type][name] = module_class
        cls._module_registry[module_type][module_class.__name__] = module_class
    
    @classmethod
    def from_config(cls, config: HarnessConfig) -> "Harness":
        """Create a Harness instance from configuration."""
        harness = cls(config)
        harness._load_modules()
        return harness
    
    @classmethod
    def from_yaml(cls, path: str) -> "Harness":
        """Create a Harness instance from YAML configuration file."""
        config = HarnessConfig.from_yaml(path)
        return cls.from_config(config)
    
    def _load_modules(self) -> None:
        """Load and instantiate all configured modules."""
        for module_key, module_config in self.config.modules.items():
            module_type = self._key_to_module_type(module_key)
            if module_type is None:
                self.logger.warning(f"Unknown module key: {module_key}")
                continue
            
            module_class = self._module_registry[module_type].get(module_config.type)
            if module_class is None:
                # Try to auto-discover from built-in modules
                module_class = self._discover_module(module_type, module_config.type)
            
            if module_class is None:
                raise ValueError(
                    f"No module implementation found for {module_type.value}: {module_config.type}"
                )
            
            module = module_class(module_config.params, self.logger)
            result = module.initialize()
            if not result.success:
                raise RuntimeError(f"Failed to initialize {module_key}: {result.error}")
            
            self.modules[module_type] = module
            self.logger.info(f"Loaded {module_key}: {module_config.type} ({module.name})")
        
        self._initialized = True
    
    def _key_to_module_type(self, key: str) -> Optional[ModuleType]:
        """Map config key to ModuleType."""
        mapping = {
            'context_manager': ModuleType.CONTEXT_MANAGER,
            'state_tracker': ModuleType.STATE_TRACKER,
            'tool_coordinator': ModuleType.TOOL_COORDINATOR,
            'parser': ModuleType.PARSER,
            'evaluator': ModuleType.EVALUATOR,
            'runtime_adapter': ModuleType.RUNTIME_ADAPTER,
            'custom': ModuleType.CUSTOM,
        }
        return mapping.get(key)
    
    def _discover_module(self, module_type: ModuleType, name: str) -> Optional[Type[Module]]:
        """Attempt to discover a module from built-in implementations."""
        # Map of known built-in modules
        builtin_modules = {
            ModuleType.CONTEXT_MANAGER: {
                'sliding_window': 'harness_engineering.modules.context.sliding_window.SlidingWindowContextManager',
                'hierarchical': 'harness_engineering.modules.context.hierarchical.HierarchicalContextManager',
                'relevance_weighted': 'harness_engineering.modules.context.relevance.RelevanceWeightedContextManager',
            },
            ModuleType.STATE_TRACKER: {
                'sqlite': 'harness_engineering.modules.state.sqlite.SQLiteStateTracker',
                'memory': 'harness_engineering.modules.state.memory.MemoryStateTracker',
            },
            ModuleType.TOOL_COORDINATOR: {
                'async_subprocess': 'harness_engineering.modules.tools.async_subprocess.AsyncSubprocessCoordinator',
                'sync_subprocess': 'harness_engineering.modules.tools.sync_subprocess.SyncSubprocessCoordinator',
            },
            ModuleType.PARSER: {
                'structured_output': 'harness_engineering.modules.parsers.structured.StructuredOutputParser',
                'regex': 'harness_engineering.modules.parsers.regex.RegexParser',
            },
            ModuleType.EVALUATOR: {
                'test_based': 'harness_engineering.modules.evaluators.test_based.TestBasedEvaluator',
                'metric_based': 'harness_engineering.modules.evaluators.metric_based.MetricBasedEvaluator',
            },
            ModuleType.RUNTIME_ADAPTER: {
                'local': 'harness_engineering.modules.runtime.local.LocalRuntimeAdapter',
                'docker': 'harness_engineering.modules.runtime.docker.DockerRuntimeAdapter',
            },
        }
        
        module_path = builtin_modules.get(module_type, {}).get(name)
        if module_path:
            try:
                module_name, class_name = module_path.rsplit('.', 1)
                module = importlib.import_module(module_name)
                return getattr(module, class_name)
            except (ImportError, AttributeError) as e:
                self.logger.warning(f"Failed to import built-in module {module_path}: {e}")
        
        return None
    
    def run(self, task: str, task_id: Optional[str] = None, **kwargs) -> HarnessResult:
        """
        Execute a task using the configured harness.
        
        Args:
            task: The task description or identifier
            task_id: Optional unique identifier for this run
            **kwargs: Additional task-specific parameters
            
        Returns:
            HarnessResult with execution outcome
        """
        if not self._initialized:
            raise RuntimeError("Harness not initialized. Call _load_modules() first.")
        
        import uuid
        task_id = task_id or str(uuid.uuid4())[:8]
        trace = []
        
        self.logger.info(f"Starting task {task_id}: {task}")
        
        try:
            # 1. Initialize context
            context_mgr = self.modules.get(ModuleType.CONTEXT_MANAGER)
            if context_mgr:
                ctx_result = context_mgr.execute(task=task, task_id=task_id, **kwargs)
                trace.append({"step": "context_init", "result": ctx_result.__dict__})
                if not ctx_result.success:
                    return HarnessResult(
                        success=False, task_id=task_id, error=ctx_result.error, trace=trace
                    )
            
            # 2. Initialize runtime
            runtime = self.modules.get(ModuleType.RUNTIME_ADAPTER)
            if runtime:
                rt_result = runtime.execute(task=task, task_id=task_id, **kwargs)
                trace.append({"step": "runtime_init", "result": rt_result.__dict__})
            
            # 3. Main execution loop (simplified)
            # In practice, this would coordinate context, tools, parsing, state
            tool_coord = self.modules.get(ModuleType.TOOL_COORDINATOR)
            parser = self.modules.get(ModuleType.PARSER)
            state_tracker = self.modules.get(ModuleType.STATE_TRACKER)
            
            # Placeholder for actual execution logic
            output = f"Executed task: {task}"
            
            # 4. Evaluate results
            evaluator = self.modules.get(ModuleType.EVALUATOR)
            metrics = {}
            if evaluator:
                eval_result = evaluator.execute(task=task, output=output, **kwargs)
                trace.append({"step": "evaluation", "result": eval_result.__dict__})
                metrics = eval_result.data or {}
            
            return HarnessResult(
                success=True,
                task_id=task_id,
                output=output,
                metrics=metrics,
                trace=trace
            )
            
        except Exception as e:
            self.logger.error(f"Task {task_id} failed: {e}")
            return HarnessResult(
                success=False,
                task_id=task_id,
                error=str(e),
                trace=trace
            )
    
    def shutdown(self) -> None:
        """Shutdown all modules cleanly."""
        for module_type, module in self.modules.items():
            result = module.shutdown()
            if not result.success:
                self.logger.warning(f"Module {module_type.value} shutdown failed: {result.error}")
        self._initialized = False
        self.logger.info("Harness shutdown complete")
    
    def get_module(self, module_type: ModuleType) -> Optional[Module]:
        """Get a module by type."""
        return self.modules.get(module_type)
    
    def health_check(self) -> Dict[str, Any]:
        """Check health of all modules."""
        return {
            "harness_initialized": self._initialized,
            "modules": {
                mt.value: module.health_check().__dict__
                for mt, module in self.modules.items()
            }
        }