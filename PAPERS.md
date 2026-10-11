# Research Papers & References

This document catalogs the key research papers that inform and inspire the Harness Engineering framework. Papers are organized by relevance and theme.

---

## Core Foundational Papers

### 1. HERMES: Harness Engineering for Software Engineering via Modular Executable Dev-Primitives
- **arXiv**: [2610.07832](https://arxiv.org/abs/2610.07832)
- **Authors**: Haibo Jin, Xinjie Li, Peng Kuang, Haohan Wang
- **Date**: October 2026
- **Categories**: cs.SE, cs.AI, cs.CL, cs.MA
- **Relevance**: **Directly foundational** — Introduces "Harness Engineering" as a discipline, proposes Dev-Primitives (modular executable abstractions), and the HERMES framework with dependency-aware dynamic activation and bug diagnosis mechanisms.
- **Key Concepts**: Dev-Primitives, modular harness design, dynamic activation, execution evidence mapping, repository-scale instantiation

### 2. MESH-Harness: Self-Improving Agent Harnesses via Bandit-Guided Compositional Evolution
- **arXiv**: [2610.05300](https://arxiv.org/abs/2610.05300)
- **Authors**: Zhiwei Shang, Yu Huo, Mingrong Gong, An Yan, Zikun Qu, Junhao Dong, Bryan Kian Hsiang Low, Chenglin Wu, Zhongxiang Dai
- **Date**: October 2026
- **Categories**: cs.AI
- **Relevance**: **Highly relevant** — Proposes compositional harness optimization using functional modules with explicit interfaces, bandit-guided search (LinUCB), and iterative self-improvement. Directly aligns with our modular/composable architecture.
- **Key Concepts**: Module-level design reuse, compositional evolution, bandit-guided search, mixed-start coordinate ascent, role-specific module pools

### 3. What Does a Harness Repair? A Preregistered Study of Visibility, Baseline Adequacy and Evaluation Defects
- **arXiv**: [2610.05533](https://arxiv.org/abs/2610.05533)
- **Authors**: Bowen Xu, Boyu Chen
- **Date**: October 2026
- **Categories**: cs.SE, cs.AI
- **Relevance**: **Critical for evaluation design** — Preregistered study analyzing where harness improvements actually come from (parser visibility, weak comparisons, evaluation defects). Informs our evaluation engine design and defect detection.
- **Key Concepts**: Harness search, evaluation defects, parser visibility, baseline adequacy, GEPA search, replication studies

---

## Agent Harness & Observability

### 4. AgentSpy: Making AI Agent Behavior Observable
- **arXiv**: [2610.06001](https://arxiv.org/abs/2610.06001)
- **Authors**: Christoph Bühler, Matteo Biagiola, Luca Di Grazia, Guido Salvaneschi
- **Date**: October 2026
- **Categories**: cs.SE, cs.AI
- **Relevance**: **High** — External observation harness for AI agents using isolated environments, system call monitoring, and network traffic recording. Informs our runtime adapter and observability modules.
- **Key Concepts**: Declarative environment specification, conformance analysis, safety analysis, system call monitoring, reliability/security analysis

### 5. TestPrism: Rethinking Test Evaluation Beyond a Single Reference
- **arXiv**: [2610.12289](https://arxiv.org/abs/2610.12289)
- **Authors**: Han Li, Lingxiang Hu, Jiacheng Huang, Ziqian Jiang, Jingkai Luo, Wei Gao, Yunfan Tan, Zun Wang, Jiaheng Liu
- **Date**: October 2026
- **Categories**: cs.SE
- **Relevance**: **High** — Introduces multi-reference test evaluation (Joint Success Function) and TestHelix for test synthesis with peer validation. Relevant for our evaluation engine's multi-criteria assessment.
- **Key Concepts**: Joint Success Function, multi-reference evaluation, TestHelix, heterogeneous synthesis, recursive self-improvement

---

## Evaluation & Benchmarking

### 6. DSV-Mem: Evaluating Multimodal Memory in Professional Workflows for MLLM Agents
- **arXiv**: [2610.08102](https://arxiv.org/abs/2610.08102)
- **Authors**: Jike Zhong, Ritwick Chaudhry, Xuanbai Chen, Tianchen Zhao, Linghan Xu, Yifan Xing, Nishant Sankaran
- **Date**: October 2026
- **Categories**: cs.AI
- **Relevance**: **Moderate** — Introduces a generation harness for evaluation suite creation by decoupling state-transition synthesis from conversation filling. Relevant for benchmark harness design.
- **Key Concepts**: Dense stateful visual memory, generation harness, state-transition synthesis, professional workflow evaluation

---

## Related Work (Broader Context)

### 7. SWE-bench: Can Language Models Resolve Real-World GitHub Issues?
- **arXiv**: [2310.06770](https://arxiv.org/abs/2310.06770) (and follow-ups)
- **Authors**: Carlos E. Jimenez, John Yang, Alexander Wettig, et al.
- **Relevance**: Primary benchmark for SE harness evaluation; our framework targets compatibility

### 8. Terminal-Bench: Evaluating LLMs as Terminal Users
- **arXiv**: [2402.15725](https://arxiv.org/abs/2402.15725)
- **Relevance**: Benchmark for terminal-based agent harnesses; informs our tool coordinator design

### 9. ReAct: Synergizing Reasoning and Acting in Language Models
- **arXiv**: [2210.03629](https://arxiv.org/abs/2210.03629)
- **Authors**: Shunyu Yao, Jeffrey Zhao, Dian Yu, et al.
- **Relevance**: Foundational agent architecture; harnesses must support ReAct-style loops

### 10. AutoGPT / BabyAGI / AgentBench Literature
- Various agent frameworks and benchmarks that motivate the need for configurable harnesses

---

## Thematic Clusters

### Harness Architecture & Modularity
| Paper | Key Contribution |
|-------|------------------|
| HERMES (2610.07832) | Dev-Primitives, dynamic activation, bug diagnosis |
| MESH-Harness (2610.05300) | Compositional evolution, bandit-guided module recombination |
| AgentSpy (2610.06001) | External observation, declarative env spec, system call monitoring |

### Harness Evaluation & Defects
| Paper | Key Contribution |
|-------|------------------|
| What Does a Harness Repair? (2610.05533) | Preregistered study of harness gain sources, evaluation defects |
| TestPrism (2610.12289) | Multi-reference evaluation, Joint Success Function |

### Benchmark Harness Generation
| Paper | Key Contribution |
|-------|------------------|
| DSV-Mem (2610.08102) | Generation harness decoupling state synthesis from conversation |

---

## How These Papers Inform Our Design

| Our Component | Inspired By | Key Insight Adopted |
|---------------|-------------|---------------------|
| **Module Interfaces** | HERMES, MESH-Harness | Explicit role-specific interfaces for composability |
| **Dynamic Activation** | HERMES | Dependency-aware module instantiation |
| **Compositional Search** | MESH-Harness | Bandit-guided module recombination |
| **Evaluation Engine** | TestPrism, Xu & Chen | Multi-criteria evaluation, defect detection |
| **Observability** | AgentSpy | External monitoring, declarative spec, conformance/safety |
| **Benchmark Harness** | DSV-Mem | Decoupled state-transition synthesis |

---

## Tracking New Research

This list will be updated as new relevant papers appear. Watch these venues:
- **arXiv categories**: cs.SE, cs.AI, cs.CL, cs.LG
- **Conferences**: ICSE, FSE, ASE, ICML, NeurIPS, ICLR, PLDI, OOPSLA
- **Keywords**: "harness", "agent evaluation", "test harness", "evaluation framework", "modular agent", "compositional"

### Search Alerts (suggested)
```
("harness" OR "test harness") AND ("modular" OR "configurable" OR "composable") AND ("agent" OR "LLM" OR "software engineering")
("evaluation framework" OR "benchmark harness") AND ("self-improving" OR "evolution" OR "optimization")
```

---

## Contribution

To add a paper:
1. Add entry in appropriate section above
2. Include: Title, arXiv/link, Authors, Date, Categories, Relevance, Key Concepts
3. Update the "How These Papers Inform Our Design" table if applicable
4. Submit PR

---

*Last updated: October 2026*
*Maintainer: Rishabh Pandey (@RiiiRiiipie)*