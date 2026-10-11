# Harness Engineering

> A modular, configurable framework for building and customizing software engineering harnesses tailored to specific use cases.

## Overview

Harness Engineering is a system designed to enable users to create, modify, and extend testing and evaluation harnesses based on their specific requirements. Rather than providing a one-size-fits-all solution, this framework adopts a modular architecture where harness components can be composed, replaced, and configured to match diverse workflows—from AI agent evaluation to traditional software testing.

## Motivation

Modern software engineering involves increasingly complex workflows:
- **AI/LLM Agents** requiring custom evaluation harnesses
- **Long-horizon tasks** needing stateful, observable execution environments
- **Diverse benchmarks** with varying evaluation criteria
- **Cost/performance tradeoffs** requiring configurable harness parameters

Existing harnesses are often rigid, monolithic, or tied to specific benchmarks. This project aims to provide a **composable harness framework** where users can:
- Select and combine functional modules (context management, tool coordination, state tracking, parsing)
- Swap implementations for specific roles (e.g., different parsers, different state backends)
- Configure harness behavior declaratively
- Extend with custom modules for domain-specific needs

## Key Features

- **Modular Architecture**: Harness decomposed into role-specific modules with explicit interfaces
- **Composable Configurations**: Mix-and-match module implementations via declarative specs
- **Extensible Plugin System**: Add custom modules without modifying core framework
- **Declarative Configuration**: YAML/JSON-based harness definitions
- **Observability Built-in**: Integrated tracing, logging, and metric collection
- **Benchmark Agnostic**: Works with SWE-bench, Terminal-Bench, custom benchmarks, etc.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Harness Core                           │
├─────────────┬─────────────┬─────────────┬───────────────────┤
│  Context    │   State     │   Tool      │    Evaluation     │
│  Manager    │   Tracker   │  Coordinator│    Engine         │
├─────────────┼─────────────┼─────────────┼───────────────────┤
│  Parser     │  Runtime    │  Plugin     │    Config         │
│  Registry   │  Adapter    │  Loader     │    Resolver       │
└─────────────┴─────────────┴─────────────┴───────────────────┘
```

Each module defines a clear interface, allowing alternative implementations to be swapped in based on use case.

## Installation

```bash
# Clone the repository
git clone https://github.com/RiiiRiiipie/Harness-Engineering.git
cd Harness-Engineering

# Install dependencies (TBD)
# pip install -e .
```

## Quick Start

```python
from harness_engineering import Harness, HarnessConfig

# Define a custom harness configuration
config = HarnessConfig(
    context_manager="sliding_window",
    state_tracker="sqlite",
    tool_coordinator="async_subprocess",
    parser="structured_output",
    evaluator="test_based"
)

# Build and run
harness = Harness.from_config(config)
result = harness.run(task="fix_bug_in_module_x")
```

## Configuration

Harnesses are configured via YAML:

```yaml
# config/harness.yaml
harness:
  name: "custom-se-harness"
  version: "1.0.0"
  
modules:
  context_manager:
    type: "sliding_window"
    params:
      window_size: 8192
      strategy: "relevance_weighted"
  
  state_tracker:
    type: "sqlite"
    params:
      path: "./harness_state.db"
  
  tool_coordinator:
    type: "async_subprocess"
    params:
      timeout: 300
      max_parallel: 4
  
  parser:
    type: "structured_output"
    params:
      schema: "custom_schema.json"
  
  evaluator:
    type: "test_based"
    params:
      test_command: "pytest -xvs"
      coverage_threshold: 0.8

plugins:
  - "my_custom_plugin"
```

## Research Foundations

This work builds on several key research papers. See [PAPERS.md](PAPERS.md) for a curated list of foundational and related work.

## Project Structure

```
Harness-Engineering/
├── src/
│   └── harness_engineering/
│       ├── core/           # Core harness framework
│       ├── modules/        # Built-in module implementations
│       ├── plugins/        # Plugin system
│       ├── config/         # Configuration loading/validation
│       └── cli/            # Command-line interface
├── config/                 # Example configurations
├── tests/                  # Test suite
├── docs/                   # Documentation
├── examples/               # Example harnesses
└── PAPERS.md              # Research paper references
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Roadmap

- [ ] Core harness framework with module interfaces
- [ ] Built-in modules (context, state, tools, parsing, evaluation)
- [ ] Plugin system for custom extensions
- [ ] Configuration schema and validation
- [ ] CLI for harness management
- [ ] Example harnesses for common use cases
- [ ] Integration with major benchmarks (SWE-bench, Terminal-Bench)
- [ ] Documentation and tutorials

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## Citation

If you use this framework in your research, please cite the foundational papers listed in [PAPERS.md](PAPERS.md) and this repository:

```bibtex
@software{harness_engineering,
  title = {Harness Engineering: A Modular Framework for Configurable Software Engineering Harnesses},
  author = {Rishabh Pandey},
  year = {2026},
  url = {https://github.com/RiiiRiiipie/Harness-Engineering}
}
```

## Acknowledgments

This project draws inspiration from and builds upon the research listed in [PAPERS.md](PAPERS.md). Special thanks to the authors of HERMES, MESH-Harness, TestPrism, and related work for advancing the field of harness engineering.