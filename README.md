# AutoResearch-BDD100K

An autonomous research framework for improving object detection models through automated experimentation.

## Overview

This project uses the **BDD100K dataset** and **YOLOv8** as the baseline object detection model. The goal is to build an agent that can inspect the training pipeline, propose experiments, evaluate their impact, and retain improvements based on model performance.

### Current Status

🚧 **Currently in development**

- BDD100K dataset prepared in YOLO format
- YOLOv8s baseline training pipeline implemented
- Model evaluation pipeline implemented
- Research agent infrastructure implemented
- Experiment keep/revert logic implemented
- Full GPU baseline training in progress
- Autonomous experimentation and research loop under development

## Project Structure

```text
AutoResearch-BDD100K/
├── agent/          # Autonomous research agent
├── model/          # Training and evaluation
├── data/           # Dataset preparation and configuration
├── research/       # Experiment results and runs
└── tests/          # Project tests
