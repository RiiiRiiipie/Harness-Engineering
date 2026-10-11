"""
Core harness configuration classes.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from pathlib import Path
import yaml


@dataclass
class ModuleConfig:
    """Configuration for a single harness module."""
    type: str
    params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ObservabilityConfig:
    """Observability configuration."""
    tracing: Dict[str, Any] = field(default_factory=dict)
    logging: Dict[str, Any] = field(default_factory=dict)
    metrics: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BenchmarkConfig:
    """Benchmark integration configuration."""
    swe_bench: Dict[str, Any] = field(default_factory=dict)
    terminal_bench: Dict[str, Any] = field(default_factory=dict)
    custom: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HarnessConfig:
    """Main harness configuration."""
    name: str
    version: str
    description: str = ""
    modules: Dict[str, ModuleConfig] = field(default_factory=dict)
    plugins: Dict[str, Any] = field(default_factory=dict)
    observability: ObservabilityConfig = field(default_factory=ObservabilityConfig)
    benchmarks: BenchmarkConfig = field(default_factory=BenchmarkConfig)

    @classmethod
    def from_yaml(cls, path: str) -> "HarnessConfig":
        """Load configuration from YAML file."""
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        
        # Extract harness section
        harness_data = data.get('harness', data)
        
        # Convert module configs
        modules = {}
        for key, value in harness_data.get('modules', {}).items():
            modules[key] = ModuleConfig(
                type=value['type'],
                params=value.get('params', {})
            )
        
        return cls(
            name=harness_data.get('name', 'unnamed'),
            version=harness_data.get('version', '0.1.0'),
            description=harness_data.get('description', ''),
            modules=modules,
            plugins=harness_data.get('plugins', {}),
            observability=ObservabilityConfig(**harness_data.get('observability', {})),
            benchmarks=BenchmarkConfig(**harness_data.get('benchmarks', {}))
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "HarnessConfig":
        """Create configuration from dictionary."""
        harness_data = data.get('harness', data)
        return cls.from_yaml_string(yaml.dump(harness_data))

    @classmethod
    def from_yaml_string(cls, yaml_str: str) -> "HarnessConfig":
        """Create configuration from YAML string."""
        data = yaml.safe_load(yaml_str)
        modules = {}
        for key, value in data.get('modules', {}).items():
            modules[key] = ModuleConfig(
                type=value['type'],
                params=value.get('params', {})
            )
        return cls(
            name=data.get('name', 'unnamed'),
            version=data.get('version', '0.1.0'),
            description=data.get('description', ''),
            modules=modules,
            plugins=data.get('plugins', {}),
            observability=ObservabilityConfig(**data.get('observability', {})),
            benchmarks=BenchmarkConfig(**data.get('benchmarks', {}))
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'version': self.version,
            'description': self.description,
            'modules': {
                k: {'type': v.type, 'params': v.params}
                for k, v in self.modules.items()
            },
            'plugins': self.plugins,
            'observability': {
                'tracing': self.observability.tracing,
                'logging': self.observability.logging,
                'metrics': self.observability.metrics
            },
            'benchmarks': {
                'swe_bench': self.benchmarks.swe_bench,
                'terminal_bench': self.benchmarks.terminal_bench,
                'custom': self.benchmarks.custom
            }
        }

    def save(self, path: str) -> None:
        """Save configuration to YAML file."""
        with open(path, 'w') as f:
            yaml.dump({'harness': self.to_dict()}, f, default_flow_style=False)