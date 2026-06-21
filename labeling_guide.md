# TakeMeter Labeling Guide

This guide explains how to label NBA discussion comments for the TakeMeter classifier.

Each comment must receive exactly one label:

- analysis
- hot_take
- reaction
- question

The goal is to label the structure and purpose of the comment, not whether I personally agree with it.

---

## Label 1: analysis

Use analysis when the comment makes a basketball argument using reasoning, evidence, statistics, comparisons, tactics, or specific examples.

### Key signals

- Explains why something happened
- Uses basketball concepts or strategy
- Mentions stats, trends, matchups, spacing, defense, efficiency, rotations, or player development
- Gives support for the claim

### Examples

- Jokic creates easy shots because his passing forces weak-side defenders to choose between helping and staying attached to shooters.
- The Knicks offense looks better with Brunson attacking early because it prevents the defense from loading up in the half court.

---

## Label 2: hot_take

Use hot_take when the comment makes a strong or confident claim with little, weak, or no support.

### Key signals

- Big claim without explanation
- Player or team judgment stated as fact
- Overconfident prediction
- Dramatic ranking or legacy claim
- Little evidence beyond opinion

### Examples

- Tatum will never be the best player on a real championship team.
- Wemby is already better than every center except Jokic.

---

## Label 3: reaction

Use reaction when the comment mainly expresses emotion in response to a game, play, trade, injury, highlight, or news event.

### Key signals

- Excitement, anger, disbelief, sadness, celebration, frustration
- Immediate response to something that just happened
- Does not try to build an argument
- Often short and emotional

### Examples

- That dunk was ridiculous. I cannot believe he finished that.
- I am sick. We really blew another fourth-quarter lead.

---

## Label 4: question

Use question when the main purpose of the comment is to ask for explanation, clarification, prediction, or other people’s opinions.

### Key signals

- Genuine question
- Asking why, how, who, or what
- Invites discussion
- Does not mainly argue a position

### Examples

- Why did the Lakers stop attacking the paint in the fourth quarter?
- Who has the better long-term ceiling, Anthony Edwards or Shai?

---

## Decision Rules for Ambiguous Comments

### analysis vs. hot_take

If the comment gives a specific basketball reason that supports the claim, label it analysis.

If the comment only makes a bold claim with weak or no support, label it hot_take.

### reaction vs. hot_take

If the comment is mostly emotional and tied to a specific moment, label it reaction.

If the comment makes a broad judgment about a player or team, label it hot_take.

### question vs. analysis

If the comment asks a genuine question, label it question.

If the question is rhetorical and the comment is really making an argument, label it analysis or hot_take depending on the support.

### reaction vs. question

If the question is mainly emotional frustration, label it reaction.

If the question is genuinely asking for an answer, label it question.

---

## Annotation Notes

When labeling difficult examples, write a short note explaining the decision.

A good note should answer:

- What labels were possible?
- Why did I choose the final label?
- What part of the comment was most important for the decision?

Example note:

Possible analysis/hot_take. I chose analysis because the comment gives a specific basketball reason instead of only making a broad claim.
