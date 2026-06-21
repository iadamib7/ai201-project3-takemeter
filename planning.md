# TakeMeter Planning Document

## Project Overview

TakeMeter is a text classification project that evaluates the quality and style of online community discourse. For this project, I will build a classifier that labels online discussion posts into clear “take” categories, fine-tune a model on my own annotated dataset, compare it against a zero-shot LLM baseline, and analyze where the model succeeds or fails.

## Community Choice

I chose NBA online discussion comments as my community. NBA communities are a strong fit for this classification task because fans constantly post different kinds of takes: statistical analysis, emotional reactions, bold unsupported claims, and genuine questions. The discourse is active, text-heavy, and varied enough to make classification meaningful.

This community is also useful because the difference between a strong basketball argument and a weak reaction matters to actual participants. Fans often distinguish between posts that use evidence, posts that are just hot takes, posts that react emotionally to a game, and posts that ask for clarification or discussion.

## Label Taxonomy

I will use four labels: `analysis`, `hot_take`, `reaction`, and `question`.

### 1. `analysis`

A post is labeled `analysis` when it makes a structured basketball argument using evidence, reasoning, statistics, comparisons, tactical observations, or specific examples.

**Clear examples:**

* “The Nuggets are harder to guard when Jokic catches the ball at the elbow because it forces the defense to choose between helping on cutters or staying home on shooters.”
* “Shai’s scoring jump makes sense because his free throw rate has increased and he is getting to his spots more consistently in the midrange.”

### 2. `hot_take`

A post is labeled `hot_take` when it makes a strong or confident basketball claim with little, weak, or no supporting evidence.

**Clear examples:**

* “Tatum is never winning a championship as the best player. He just does not have it.”
* “This rookie is already better than half the All-Stars in the league.”

### 3. `reaction`

A post is labeled `reaction` when it mainly expresses an immediate emotional response to a game, player, trade, injury, highlight, or news event without trying to build an argument.

**Clear examples:**

* “That dunk was insane. I still cannot believe he finished that.”
* “I am sick. We really blew a 20-point lead again.”

### 4. `question`

A post is labeled `question` when its main purpose is to ask for clarification, explanation, prediction, or other people’s opinions.

**Clear examples:**

* “Why do teams keep switching smaller guards onto Jokic instead of sending an early double?”
* “Who do you think has the better long-term ceiling, Anthony Edwards or Shai?”

## Hard Edge Cases and Decision Rules

Some NBA comments may sit between two labels. I will use the following decision rules to keep annotation consistent.

### Edge Case 1: `analysis` vs. `hot_take`

A post may make a bold claim and include one statistic. If the statistic is part of a real explanation, I will label it `analysis`. If the statistic feels decorative, cherry-picked, or unsupported by further reasoning, I will label it `hot_take`.

**Example:**

“LeBron is overrated because his playoff record against top-seeded teams is not that good.”

This could seem analytical because it references a record, but it does not explain context, era, teammates, opponents, or why that stat proves the claim. I would label this as `hot_take`.

### Edge Case 2: `reaction` vs. `hot_take`

A post may be emotional and also make a claim. If the main purpose is immediate emotion, I will label it `reaction`. If the main purpose is a broad judgment about a player or team, I will label it `hot_take`.

**Example:**

“Trade everyone. This team is embarrassing.”

This is emotional and dramatic, but it is mainly reacting to a bad performance in the moment. I would label this as `reaction`.

### Edge Case 3: `question` vs. `analysis`

Some posts ask a question but also include reasoning. If the main purpose is to invite answers from others, I will label it `question`. If the question is mostly rhetorical and the post is making an argument, I will label it `analysis` or `hot_take` depending on the quality of support.

**Example:**

“Why does everyone ignore how good Brunson has been in the playoffs? His footwork, pace, and midrange control have carried the Knicks offense.”

This is phrased as a question, but it is really making an argument with specific support. I would label this as `analysis`.

## Data Collection Plan

I will collect at least 200 public NBA discussion posts or comments. I plan to collect examples from public NBA discussion spaces such as Reddit NBA threads, public basketball forums, or public comment sections related to NBA games, trades, rankings, and player discussions.

The dataset will be saved as a single CSV file at:

`data/takemeter_dataset.csv`

The CSV will contain at least these columns:

* `text`: the post or comment text
* `label`: one of `analysis`, `hot_take`, `reaction`, or `question`
* `notes`: optional notes for difficult or ambiguous examples

I will aim for a balanced dataset, with each label making up at least 20% of the examples if possible. Since the dataset must contain at least 200 examples, my target distribution is approximately:

* `analysis`: 50 examples
* `hot_take`: 50 examples
* `reaction`: 50 examples
* `question`: 50 examples

If one label is underrepresented after collecting 200 examples, I will collect additional examples that better represent that label. If one label becomes more than 70% of the dataset, I will treat that as an imbalance problem and collect more examples from the smaller labels before training.

## Annotation Process

I will label each example manually using the definitions in this planning document. I will not label only by skimming. For each post, I will read the full text and assign exactly one label.

For difficult examples, I will use the decision rules above and write a short note explaining the choice. I will document at least three difficult-to-label examples in the final README.

If I use an AI tool to pre-label examples, I will still review and correct every label myself. I will disclose that process in the AI usage section of the README.

## Evaluation Metrics

I will evaluate both the fine-tuned model and the zero-shot Groq baseline on the same test set.

I will report:

* Overall accuracy
* Per-class precision, recall, and F1-score
* A confusion matrix
* At least three wrong predictions with analysis

Accuracy is useful because it gives a simple overall measure of performance, but it is not enough by itself. Since this is a multi-class classification task, I need per-class metrics to see whether the model performs well across all labels or only learns the most common label.

F1-score is especially important because it balances precision and recall. For example, if the model predicts `reaction` too often, accuracy might look acceptable while the model is actually failing to distinguish emotional posts from hot takes. The confusion matrix will help show which labels the model confuses most often.

## Baseline Plan

I will compare my fine-tuned model against a zero-shot Groq baseline using `llama-3.3-70b-versatile`. The baseline prompt will include my label definitions and instruct the model to output only one label name.

This comparison is important because it shows whether fine-tuning actually improves performance over a powerful general-purpose language model that has not been trained on my specific labeled dataset.

## Fine-Tuning Plan

I plan to fine-tune `distilbert-base-uncased` using the starter Colab notebook. The notebook will handle the train, validation, and test split automatically.

My initial training setup will use the default hyperparameters unless the results suggest a problem:

* Base model: `distilbert-base-uncased`
* Epochs: 3
* Learning rate: 2e-5
* Batch size: 16
* Dataset split: 70% train, 15% validation, 15% test

I will document any hyperparameter changes in the README.

## Definition of Success

A successful model should perform meaningfully better than the zero-shot baseline or show clearer behavior on the specific community labels.

For this project, I will consider the classifier useful if:

* Overall accuracy is at least 70%
* Each major label has a reasonable F1-score, ideally at least 0.65
* The model does not collapse into predicting only one label
* The confusion matrix shows understandable errors rather than random failure
* The wrong predictions reveal clear patterns that can be explained and improved

For real deployment in a community tool, I would want stronger performance, especially on `analysis` and `hot_take`, because confusing those two labels could make the tool unfair or misleading.

## AI Tool Plan

### Label Stress-Testing

Before finalizing the dataset, I will use an AI tool to generate boundary examples between labels such as `analysis` vs. `hot_take`, `reaction` vs. `hot_take`, and `question` vs. `analysis`. If the generated examples are difficult to classify, I will revise the label definitions or decision rules before annotating the full dataset.

### Annotation Assistance

I may use an LLM to pre-label some examples, but I will manually review every label before including it in the final dataset. If I use pre-labeling, I will disclose it in the README and explain how I corrected or overrode the AI’s suggestions.

### Failure Analysis

After evaluating the fine-tuned model, I will use an AI tool to help identify patterns in the wrong predictions. I will provide the misclassified examples and ask the tool to look for common patterns such as sarcasm, short posts, vague wording, or confusion between specific label pairs. I will verify those patterns myself before including them in the final evaluation report.

## Clean Project Practices

To avoid the problems from my previous project, I will keep this project clean and readable.

I will avoid:

* Dead code after return statements
* Duplicate implementations of the same function
* Old starter-code stubs left inside completed files
* Unused files
* API keys committed to GitHub
* Fake or placeholder evaluation results
* Vague labels that cannot be applied consistently

Before each major commit, I will review the changed files and run:

`git status`

Then I will commit only the files that belong in the final project.
