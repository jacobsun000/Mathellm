# Mathellm - Math Problem Generator with LLM

<img src="./asset/logo.gif" alt="Mathellm Logo" width="256" height="256" />

CSCI 5541 course project by Linguatech:

- [Jacob Sun](https://github.com/jacobsun000)
- [Chloe Chen](https://github.com/RichSomeday222)
- [Tong Liao](https://github.com/Humanlt)

## Introduction

Mathellm is a math problem generator with LLM (Language Model) that can generate math problems and their solutions in LaTeX format. It is designed to help teachers and students generate math problems and solutions easily and quickly. The user can specify the type of math problems to generate, the number of problems to generate, and the difficulty level of the problems. The generated problems and solutions can be exported to LaTeX files, which can be compiled to PDF files for printing or sharing.

## Implementation

...To be filled...

## Setup

- Linux
- Python 3.11
- Node.js
- npm/pnpm

Environment variable:

Create a `.env` file in the root directory with the following content:

```bash
export OPENAI_API_KEY="Your OpenAI API Key"
```

Then setup python environment:

```bash
pip install -r requirements.txt
```

Next setup React frontend:

```bash
cd frontend
pnpm install
```

## Usage

Run with following command:

```bash
./run.sh
```

## Demo

![Demo](./asset/demo.png)

## Example

Problem class: DiffConstant

- Problem name: Derivative of a Constant
- Description: Calculate the derivative of a constant with respect to a variable.
- Level: 1
- Difficulty: 3
- Tags: \['differentiation', 'basic', 'constant'\]
- Expression: $\frac{d}{d x} \left(- \frac{61}{5}\right)$
- Solution: \[$\frac{d}{d x} C = 0$\]
- Answer: {'symbolic': '0', 'numeric': None}
- Content: A botanist is studying the growth rate of a rare plant in a controlled environment. Surprisingly, after several weeks of monitoring, she finds that the height of the plant does not change and remains constant at $-(\frac{61}{5})$ centimeters. She decides to model the derivative of the plant's height with respect to time to confirm her observations. What is the derivative of the constant plant height with respect to time? $[ \frac{d}{d x} \left(- \frac{61}{5}\right)]$
