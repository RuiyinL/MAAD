# Replication for the Paper: *MAAD: Automate Software Architecture Design through Knowledge-Driven Multi-Agent Collaboration*

This is the replication package for the paper: *MAAD: Automate Software Architecture Design through Knowledge-Driven Multi-Agent Collaboration*. This repository contains an introduction of MAAD framework, source code for the implementations of each agent, the dataset of several requirements cases, and MAAD's generations based on one requirements case.

## Introduction

The MAAD framework implements a knowledge‑driven, multi‑agent pipeline that autonomously transforms a Software Requirements Specification (SRS) into a complete architecture design, MAAD comprises four specialized agents, and each individual agent is equipped with perception, reasoning, and action capabilities.

After receiving the SRS, the `Analyst agent` examines its content, identifies key aspects of the requirements, and distills them into four decomposed requirement artifacts. Once the `Modeler agent` perceives the generated artifacts in the artifacts pools from the Analyst agent, it constructs the system's multi‑view representation according to the "4+1" architecture view models proposed by Philippe Kruchten. When the `Designer agent` perceives the artifacts by the Analyst and Modeler agents, it synthesizes the final architecture documentation. The documentation formulates system goals and detailed design specifications. Finally, the `Evaluator agent` assesses the generated architecture by comparing the architecture views against the original SRSs. It produces an ATAM evaluation report and a Mismatch Analysis report, pinpointing any deviations or trade‑offs. Overall, the four agents enact a cohesive, feedback‑driven workflow. Through iterative communication and artifact exchange, MAAD ensures that each agent's autonomous activities cumulatively yield a robust, traceable architecture design.

![image](https://github.com/RuiyinL/MAAD/blob/main/img/Overview.png)



---

## 📁 Repository Structure

```plaintext
├── scripts               # Source code of the MAAD framework
├── requirements          # Requirements dataset
├── Interview Protocol    # An interview protocol for evaluating the MAAD framework
├── MAAD artifacts        # Generated artifacts of the MAAD framework
│ ├── GPT-4o              # Generations of MAAD equipped with GPT-4o
│ │ ├── GPT-4o_RAG        # Generations of MAAD equipped with GPT-4o (using RAG)
│ │ └── GPT-4o_noRAG      # Generations of MAAD equipped with GPT-4o (without using RAG)
│ ├── Deepseek-R1         # Generations of MAAD equipped with Deepseek-R1
│ │ ├── DeepSeek-R1_RAG   # Generations of MAAD equipped with Deepseek-R1 (using RAG)
│ │ └── DeepSeek-R1_noRAG # Generations of MAAD equipped with Deepseek-R1 (without using RAG)
│ └── Llama3.3            # Generations of MAAD equipped with Llama3.3
│ ├── Llama3.3_RAG        # Generations of MAAD equipped with Llama3.3 (using RAG)
│ └── Llama3.3-noRAG      # Generations of MAAD equipped with Llama3.3 (without using RAG)
├── MetaGPT               # Comparative results with MetaGPT
└── README.md             # Description of this replication package
```

## 📝 Citation

```bibtex
@article{Li2025MAAD,
  author = {Li, Ruiyin and Zhang, Yiran and Zhou, Xiyu and Liang, Peng and Sun, Weisong and Xuan, Jifeng and Jin, Zhi and Liu, Yang},
  title = {{MAAD: Automate Software Architecture Design through Knowledge-Driven Multi-Agent Collaboration}},
  journal={arXiv preprint arXiv:2507.21382},
  year={2025}
}
```
