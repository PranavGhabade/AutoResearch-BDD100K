# AutoResearch BDD100K Research Protocol

## Objective

Improve the performance of a baseline object detection model
on the BDD100K dataset through controlled autonomous experiments.

The primary objective is to improve the selected evaluation metric
without manipulating the evaluation process.

---

## Research Cycle

Each experiment follows this process:

1. Inspect the current implementation.
2. Identify a possible improvement.
3. Form a hypothesis.
4. Modify only permitted files.
5. Run the training experiment.
6. Evaluate the model using the fixed evaluation procedure.
7. Record the result.
8. Compare the result with the current baseline.
9. Keep the modification if the result improves.
10. Revert the modification if the result does not improve.
11. Move to the next experiment.

---

## Evaluation Integrity

The agent must never:

- modify ground-truth labels
- modify the validation dataset
- modify evaluation metrics
- modify evaluation code
- modify benchmark calculation
- remove difficult samples from evaluation
- report a result that was not actually obtained
- modify the guardrail system

The evaluation procedure must remain fixed across experiments.

---

## Experiment Requirements

Every experiment should contain:

- Experiment ID
- Hypothesis
- Description of the modification
- Files changed
- Training configuration
- Evaluation metric
- Result
- Comparison with the current baseline
- Decision: KEEP or REVERT

---

## Improvement Strategy

The agent should prefer experiments that have:

- a clear hypothesis
- a measurable expected effect
- a reasonable implementation cost
- reproducibility
- relevance to object detection

The agent should avoid making many unrelated changes
in a single experiment.

Whenever possible, change one major factor at a time.

---

## Baseline

The baseline model and evaluation configuration must be established
before autonomous experimentation begins.

The baseline result becomes the reference point for subsequent
experiments.