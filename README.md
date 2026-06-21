# TakeMeter: NBA Discourse Quality Classifier

## Project Overview

TakeMeter is a text classification project that evaluates the quality and style of online community discourse. For this project, I built a classifier for NBA discussion comments using four labels: `analysis`, `hot_take`, `reaction`, and `question`.

The goal is not just to train a model, but to understand how well a machine learning classifier can learn messy human discourse categories. This project includes a custom label taxonomy, an annotated dataset, a fine-tuned transformer model, a zero-shot LLM baseline comparison, and an evaluation of where the model succeeds and fails.

## Community Choice

I chose NBA online discussion comments because basketball communities contain many different types of discourse. Fans post statistical arguments, emotional reactions, bold unsupported claims, and genuine questions about teams, players, trades, and games.

This community is a strong fit for TakeMeter because the distinction between a thoughtful argument and a low-support take matters to people who participate in sports discussions.

## Label Taxonomy

I used four mutually exclusive labels.

### `analysis`

A comment is labeled `analysis` when it makes a structured basketball argument using evidence, reasoning, statistics, comparisons, tactical observations, or specific examples.

**Examples:**

* “The Nuggets are harder to guard when Jokic catches the ball at the elbow because it forces the defense to choose between helping on cutters or staying home on shooters.”
* “Shai’s scoring jump makes sense because his free throw rate has increased and he is getting to his spots more consistently in the midrange.”

### `hot_take`

A comment is labeled `hot_take` when it makes a strong or confident basketball claim with little, weak, or no supporting evidence.

**Examples:**

* “Tatum is never winning a championship as the best player. He just does not have it.”
* “This rookie is already better than half the All-Stars in the league.”

### `reaction`

A comment is labeled `reaction` when it mainly expresses an immediate emotional response to a game, player, trade, injury, highlight, or news event without trying to build an argument.

**Examples:**

* “That dunk was insane. I still cannot believe he finished that.”
* “I am sick. We really blew a 20-point lead again.”

### `question`

A comment is labeled `question` when its main purpose is to ask for clarification, explanation, prediction, or other people’s opinions.

**Examples:**

* “Why do teams keep switching smaller guards onto Jokic instead of sending an early double?”
* “Who do you think has the better long-term ceiling, Anthony Edwards or Shai?”

## Dataset

The dataset is stored in:

`data/takemeter_dataset.csv`

The CSV contains three columns:

| Column  | Description                                               |
| ------- | --------------------------------------------------------- |
| `text`  | The NBA discussion comment                                |
| `label` | One of `analysis`, `hot_take`, `reaction`, or `question`  |
| `notes` | Optional annotation notes, especially for difficult cases |

### Data Collection Source

I collected public NBA discussion comments from public online basketball discussion spaces.

### Labeling Process

Each example was labeled manually using the definitions in `planning.md`. For ambiguous examples, I used the decision rules from the planning document to choose exactly one label.

### Label Distribution

| Label      | Count |
| ---------- | ----: |
| `analysis` |  TODO |
| `hot_take` |  TODO |
| `reaction` |  TODO |
| `question` |  TODO |
| **Total**  |  TODO |

### Difficult-to-Label Examples

| Example | Possible Labels | Final Label | Reason |
| ------- | --------------- | ----------- | ------ |
| TODO    | TODO            | TODO        | TODO   |
| TODO    | TODO            | TODO        | TODO   |
| TODO    | TODO            | TODO        | TODO   |

## Model and Fine-Tuning Approach

The fine-tuned model used for this project is:

`distilbert-base-uncased`

I used the starter Colab notebook to split the dataset into train, validation, and test sets, tokenize the text, fine-tune the model, and evaluate performance.

Initial training setup:

| Setting       | Value                               |
| ------------- | ----------------------------------- |
| Base model    | `distilbert-base-uncased`           |
| Epochs        | 3                                   |
| Learning rate | 2e-5                                |
| Batch size    | 16                                  |
| Split         | 70% train, 15% validation, 15% test |

I used these settings because they are reasonable defaults for fine-tuning a small transformer model on a relatively small labeled dataset.

## Baseline Comparison

I compared the fine-tuned model against a zero-shot Groq baseline using:

`llama-3.3-70b-versatile`

The baseline prompt included the four label definitions and instructed the model to output only one label name.

### Baseline Prompt

TODO: Paste final baseline prompt here.

## Evaluation Results

Both models were evaluated on the same test set.

### Overall Accuracy

| Model                       | Accuracy |
| --------------------------- | -------: |
| Zero-shot Groq baseline     |     TODO |
| Fine-tuned DistilBERT model |     TODO |

### Per-Class Metrics

#### Zero-Shot Groq Baseline

| Label      | Precision | Recall | F1-score |
| ---------- | --------: | -----: | -------: |
| `analysis` |      TODO |   TODO |     TODO |
| `hot_take` |      TODO |   TODO |     TODO |
| `reaction` |      TODO |   TODO |     TODO |
| `question` |      TODO |   TODO |     TODO |

#### Fine-Tuned DistilBERT Model

| Label      | Precision | Recall | F1-score |
| ---------- | --------: | -----: | -------: |
| `analysis` |      TODO |   TODO |     TODO |
| `hot_take` |      TODO |   TODO |     TODO |
| `reaction` |      TODO |   TODO |     TODO |
| `question` |      TODO |   TODO |     TODO |

### Confusion Matrix

Rows represent true labels. Columns represent predicted labels.

| True \ Predicted | `analysis` | `hot_take` | `reaction` | `question` |
| ---------------- | ---------: | ---------: | ---------: | ---------: |
| `analysis`       |       TODO |       TODO |       TODO |       TODO |
| `hot_take`       |       TODO |       TODO |       TODO |       TODO |
| `reaction`       |       TODO |       TODO |       TODO |       TODO |
| `question`       |       TODO |       TODO |       TODO |       TODO |

## Wrong Prediction Analysis

### Wrong Prediction 1

**Text:** TODO
**True label:** TODO
**Predicted label:** TODO
**Analysis:** TODO

### Wrong Prediction 2

**Text:** TODO
**True label:** TODO
**Predicted label:** TODO
**Analysis:** TODO

### Wrong Prediction 3

**Text:** TODO
**True label:** TODO
**Predicted label:** TODO
**Analysis:** TODO

## Sample Classifications

| Text | Predicted Label | Confidence | Notes |
| ---- | --------------- | ---------: | ----- |
| TODO | TODO            |       TODO | TODO  |
| TODO | TODO            |       TODO | TODO  |
| TODO | TODO            |       TODO | TODO  |
| TODO | TODO            |       TODO | TODO  |
| TODO | TODO            |       TODO | TODO  |

## Reflection: What the Model Learned vs. What I Intended

TODO: Explain what the model actually appeared to learn compared with the intended label definitions.

## Spec Reflection

### One way the spec helped

TODO

### One way the implementation diverged from the spec

TODO

## AI Usage

I used AI tools to support the project, but I reviewed and made the final decisions myself.

### AI Use 1: Label Stress-Testing

TODO: Describe how AI was used to test ambiguous label boundaries.

### AI Use 2: Failure Analysis

TODO: Describe how AI was used to identify patterns in wrong predictions.

### Annotation Assistance Disclosure

TODO: State whether AI was used to pre-label any examples. If yes, explain that every label was manually reviewed and corrected.

## Demo Video

TODO: Add demo video link here.

The demo shows:

* 3–5 comments being classified by the fine-tuned model
* One correct prediction with explanation
* One incorrect prediction with explanation
* A brief walkthrough of the evaluation report

## Repository Contents

```text
AI201-PROJECT3-TAKEMETER/
  data/
    takemeter_dataset.csv
  planning.md
  README.md
  evaluation_results.json
  confusion_matrix.png
```

