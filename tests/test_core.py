"""
Basic tests for the Harness Engineering framework.
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock

from harness_engineering.core.config import HarnessConfig, ModuleConfig
from harness_engineering.core.harness import Harness
from harness_engineering.modules.base import ModuleType, Module, ModuleResult


class DummyModule(Module):
    """Dummy module for testing."""
    
    def __init__(self, config, logger=None):
        super().__init__(config, logger)
        self.module_type_value = ModuleType.CUSTOM
        self.module_name = "dummy"
    
    @property
    def module_type(self):
        return self.module_type_value
    
    @property
    def name(self):
        return self.module_name
    
    def _initialize(self):
        pass
    
    def execute(self, *args, **kwargs):
        return ModuleResult(success=True, data="dummy result")
    
    def _shutdown(self):
        pass


class TestHarnessConfig:
    """Tests for HarnessConfig."""
    
    def test_create_from_dict(self):
        config = HarnessConfig(
            name="test-harness",
            version="1.0.0",
            description="Test harness",
            modules={
                "context_manager": ModuleConfig(type="sliding_window", params={"window_size": 4096})
            }
        )
        assert config.name == "test-harness"
        assert config.version == "1.0.0"
        assert "context_manager" in config.modules
    
    def test_to_dict(self):
        config = HarnessConfig(
            name="test-harness",
            version="1.0.0",
            modules={
                "context_manager": ModuleConfig(type="sliding_window", params={"window_size": 4096})
            }
        )
        data = config.to_dict()
        assert data["name"] == "test-harness"
        assert data["modules"]["context_manager"]["type"] == "sliding_window"
        assert data["modules"]["context_manager"]["params"]["window_size"] == 4096
    
    def test_save_and_load_yaml(self):
        config = HarnessConfig(
            name="test-harness",
            version="1.0.0",
            modules={
                "context_manager": ModuleConfig(type="sliding_window", params={"window_size": 4096})
            }
        )
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            temp_path = f.name
        
        try:
            config.save(temp_path)
            loaded = HarnessConfig.from_yaml(temp_path)
            assert loaded.name == "test-harness"
            assert loaded.modules["context_manager"].type == "sliding_window"
            assert loaded.modules["context_manager"].params["window_size"] == 4096
        finally:
            os.unlink(temp_path)


class TestHarness:
    """Tests for Harness class."""
    
    def test_harness_creation(self):
        config = HarnessConfig(
            name="test-harness",
            version="1.0.0",
            modules={}
        )
        harness = Harness(config)
        assert harness.config.name == "test-harness"
        assert not harness._initialized
    
    def test_register_module(self):
        Harness.register_module(ModuleType.CUSTOM, "dummy", DummyModule)
        assert "dummy" in Harness._module_registry[ModuleType.CUSTOM]
    
    def test_harness_with_dummy_module(self):
        # Register dummy module
        Harness.register_module(ModuleType.CUSTOM, "dummy", DummyModule)
        
        config = HarnessConfig(
            name="test-harness",
            version="1.0.0",
            modules={
                "custom": ModuleConfig(type="dummy", params={})
            }
        )
        
        harness = Harness.from_config(config)
        assert harness._initialized
        assert ModuleType.CUSTOM in harness.modules
        
        # Test health check
        health = harness.health_check()
        assert health["harness_initialized"] is True
        assert "custom" in health["modules"]
        
        harness.shutdown()

    @pytest.mark.parametrize(
        "module_type",
        [ModuleType.RUNTIME_ADAPTER, ModuleType.EVALUATOR],
    )
    def test_run_fails_when_runtime_or_evaluator_fails(self, module_type):
        harness = Harness(HarnessConfig(name="test-harness", version="1.0.0"))
        harness._initialized = True
        failing_module = Mock()
        failing_module.execute.return_value = ModuleResult(success=False, error="module failed")
        harness.modules[module_type] = failing_module

        result = harness.run(task="test task", task_id="test-id")

        assert not result.success
        assert result.error == "module failed"
        assert result.task_id == "test-id"


class TestModuleBase:
    """Tests for base Module class."""
    
    def test_module_lifecycle(self):
        module = DummyModule({})
        assert not module._initialized
        
        result = module.initialize()
        assert result.success
        assert module._initialized
        
        result = module.execute()
        assert result.success
        assert result.data == "dummy result"
        
        health = module.health_check()
        assert health.success
        assert health.data["initialized"] is True
        
        result = module.shutdown()
        assert result.success
        assert not module._initialized


if __name__ == "__main__":
    pytest.main([__file__, "-v"])