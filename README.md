# Autonomous AI Game Agent (Clash of Clans)

*Note: This project was originally developed as a collaborative team project. This repository contains my personal version, focusing on my contributions, adaptations, and code presentation.*

## 📌 Project Overview
This project is a fully autonomous AI agent built in Python capable of playing Clash of Clans. It integrates **Computer Vision**, **OCR**, and a **rule-based decision system** to perceive the environment, extract relevant data, and make real-time decisions, demonstrating an end-to-end AI pipeline from perception to action in a dynamic environment.

### ⚙️ How it works:
1. **Perception:** Uses **YOLOv8** for real-time object detection on the screen to identify game structures and elements.
2. **Data Extraction:** Implements **PaddleOCR** to read and extract numerical data (available resources).
3. **Decision & Automation:** Processes the extracted data through a rule-based decision system to evaluate targets in real-time. It autonomously executes system-level mouse clicks via **PyAutoGUI** to interact with the game, eliminating the need for manual interaction.

### 🚀 Technologies
- **Python**
- **YOLOv8** (Ultralytics)
- **PaddleOCR**
- **OpenCV**
- **PyAutoGUI**

This project demonstrates practical experience in building agentic workflows, integrating AI models, handling real-time data extraction, and managing system stability under low-latency constraints.

---
 
## 🔧 Setting Up the Virtual Environment

Follow these steps to create and activate a virtual environment, then install the dependencies:

### 1. Create a virtual environment

```bash
python -m venv venv
```

### 2. Activate the virtual environment

- **Windows (Command Prompt):**  
  `venv\Scripts\activate`

- **Windows (PowerShell):**  
  `.\venv\Scripts\Activate.ps1`

- **macOS / Linux:**  
  `source venv/bin/activate`

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## ▶️ Running the Program

The project includes a script launcher that allows you to choose which functionality to execute from the terminal menu.

### To run the launcher:

```bash
python main.py
```


### Alternatively To Run Scripts Individually

You can also run each script directly using Python’s `-m` flag:

> Resource collector

```bash
python -m script.resource_collector
```

> Attack Overlay

```bash
python -m script.overlay_attack
```

> Pre Attack Resource Analysis
```bash
python -m script.pre_attack_resources
```
