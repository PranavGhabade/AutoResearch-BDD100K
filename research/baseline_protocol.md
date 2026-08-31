# BDD100K Baseline Protocol

## 1. Research Objective

Establish a reproducible object detection baseline on the BDD100K
dataset that will later be used as the reference point for the
AutoResearch agent.

The AutoResearch agent must improve model performance without
modifying the evaluation procedure or benchmark data.

---

## 2. Reference Paper

Title:

"Z-YOLOv8s-based approach for road object recognition in complex
traffic scenarios"

Journal:

Alexandria Engineering Journal, Volume 106, 2024

DOI:

10.1016/j.aej.2024.07.011

The paper uses YOLOv8s as the baseline and proposes Z-YOLOv8s
through several architectural modifications.

---

## 3. Dataset

Dataset: BDD100K

Task: Object Detection

### Original BDD100K classes

The original BDD100K detection annotations contain:

1. pedestrian
2. rider
3. car
4. truck
5. bus
6. train
7. motorcycle
8. bicycle
9. traffic light
10. traffic sign

### Class reassignment used by the reference paper

The paper performs category reassignment:

Car:

- bike
- car
- bus
- truck
- train
- motorcycle

Pedestrian:

- person
- rider

Traffic Sign:

- traffic sign

Traffic Light:

- traffic light

Therefore the final detection task contains four classes:

1. car
2. pedestrian
3. traffic sign
4. traffic light

---

## 4. Dataset Split

The paper uses a:

7:1:2

train / validation / test split.

The validation and test data must remain fixed throughout
autonomous experimentation.

Ground-truth annotations must not be modified by the agent.

---

## 5. Baseline Model

Model:

YOLOv8s

Framework:

Ultralytics YOLOv8

Reference version:

Ultralytics 8.0.25

Pretrained weights:

No

The paper states that its ablation experiments and model comparisons
were performed without pretrained weights.

---

## 6. Training Configuration

Input image size:

640 × 640

Batch size:

8

Training epochs:

300

Random seed:

To be explicitly recorded for our reproduction.

GPU:

Reference experiment:

NVIDIA GeForce RTX 4090, 24 GB VRAM

CPU:

Intel Core i9-13900K

RAM:

60 GB

Software environment reported by the paper:

PyTorch 1.8.1

Torchvision 0.9.1

Ultralytics 8.0.25

---

## 7. Evaluation Metrics

Primary metric:

mAP@0.5:0.95

Secondary metric:

mAP@0.5

Additional metrics:

- Precision
- Recall
- FPS
- Parameter count

The evaluation procedure must remain unchanged across
experiments.

---

## 8. Published YOLOv8s Baseline

The paper reports the following YOLOv8s BDD100K baseline:

mAP@0.5:

67.9%

mAP@0.5:0.95:

35.2%

Precision:

74.6%

Recall:

60.8%

FPS:

136.25

Parameters:

11.1M

These values are the reference published results.

Our reproduced baseline does not need to exactly match these numbers.
Hardware, software versions, randomness, preprocessing and other
implementation differences must be documented.

---

## 9. AutoResearch Objective

The objective of our AutoResearch system is:

Starting from the reproducible YOLOv8s baseline, automatically search
for model or training modifications that improve the selected
evaluation metric on BDD100K.

The agent should independently generate hypotheses and experiments.

Known improvements from the reference Z-YOLOv8s model should not be
automatically provided to the agent during the initial search.

---

## 10. Permitted Experiment Areas

The agent may investigate:

- Model architecture
- Training hyperparameters
- Data augmentation
- Optimizer configuration
- Learning-rate scheduling
- Loss configuration
- Feature extraction
- Small-object detection improvements
- Other explicitly permitted model/training components

Each experiment should preferably change one major factor at a time.

---

## 11. Protected Components

The agent must never modify:

- Ground-truth annotations
- Validation dataset
- Test dataset
- Evaluation code
- Evaluation metrics
- Benchmark calculation
- Previous experiment results
- Guardrail code

The agent must not remove difficult samples or manipulate labels
to improve the reported metric.

---

## 12. Experiment Decision

Every experiment is compared against the current best valid result.

If the selected metric improves:

KEEP

If the selected metric does not improve:

REVERT

Every experiment must record:

- Experiment ID
- Hypothesis
- Modification
- Files changed
- Training configuration
- Evaluation metrics
- Baseline metric
- New metric
- Decision
- Training time
- Hardware used

---

## 13. Scientific Integrity

The agent must never report an improvement unless the result was
actually produced by the training and evaluation pipeline.

Every reported result must be reproducible from the recorded
experiment configuration and code state.