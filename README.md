# Leveraging Large Language Models for Sentiment Analysis in GitHub Pull Request Discussions - Replication Package

This is the replication package for the paper that contains the scripts and data utilized for the execution of the work.

* The data folder provided the dataset utilized in this work.
* The output folder provided the output of all models executed for this work. The name for each file on this folder is comprised of the model name and the prompt engineering technique associated with the file (0shot = no examples, 1shot = 1 example, 3shot = 3 examples, cotshot = 3 examples + reasoning).
* The two .ipynb files in the root of the repository are the scripts for the collection and analysis processes utilized in the work, and are named in order of execution)

## Requirements

1. Python (executed by the authors of the authors of the paper with version 3.12)
2. Jupyter (or any environment capable of running .ipynb files)
3. Ollama
4. An OpenAI key

In terms of hardware, the main limitation is the execution of ollama. For the models utilized, in terms of memory, the default ollama models usually utilizes from 50% to 66% of the number of paramaters of the models in gigabytes of memory. For example, Llama 3.1 70B requires 43GB of memory.

The study was executed with a laptop running Windows that has an Intel Core i9 13900HX, 32GB of DDR5 RAM, and a RTX 4090 Laptop with 16GB of VRAM.

## Environment Setup

1. Install the dependencies in your python environent

```pip install -r requirements.txt```

2. Install the required models in ollama

```ollama pull model_name```

The names for the models utilized in this work are `gemma2:9b`, `gemma2:27b`, `llama3.1:8b`, `llama3.1:70b`, `mistral-nemo:12b`, and `mistral-small:22b`.

3. Create a `.env` file in the root of the repository with the OpenAI key, utilizing the following format.

``` OPENAI_API_KEY=YOUR_KEY_HERE ```

4. After the previous steps, you should be ready to execute the jupyter notebooks utilizing your environment. The documents provide comments that explain what each part of the code is doing.

## Prompt

All of the prompts utilized in this work are variations of the following base prompt.

```
You are a bot that classifies messages from Github pull requests. Classify the message as one of three types of sentiment: positive, neutral, and negative.

For classification purposes, we consider love and joy (and related emotions) positive, anger, sadness, and fear, negative, surprise can be positive or negative depending on the context, and neutral is considered the absense of any emotions.

Return the result one of the following JSONs: {{"sentiment": "positive"}}, {{"sentiment": "negative"}} OR {{"sentiment": "neutral"}}.
                
Message: "{message}"
```

This prompt, especially the second line, was tailor-made to reflect the emotion model that was followed by the creators of the dataset (the reference can be found on the paper).

For the prompt engineering techniques, we appended examples utilizing the following format (reasoning was only included for the chain of thought technique).

```
Here are some examples to help you get started:

Example 1: "Oh, you know what? I'm stupid. I'm actually using `http-server`. Please, accept my apologies"
Reasoning 1: "In this message, the author utilizes a self deprecating expression (I'm stupid) and then apologizes, likely to the reviewer."
Response for Example 1: {"sentiment": "negative"}
```

## Dataset

The schema for the json file provided in this replication package is as follows. 

```json
 {
    // Raw contents of each message.
    "raw_message": "#651 ",
    // URL to the original message on GitHub
    "message_url": "https://github.com/plotly/plotly.py/pull/650#issuecomment-270786907",
    "part2_aggregate": {
      // Polarity of the message, obtained via manual labeling
      "polarity": "neutral",
      // Avg. confidence for the 3 experts that labeled the message
      "avg_confidence": 4.666666666666667,
      // Type of agreement between experts: "all", "comp_only", "neuro_and_comp", "undefined"
      // "all" when 3 experts agreed
      // "comp_only" and "neuro_and_comp" when only 2 expers agreed
      // "undefined" when none of the experts agreed. In these cases there is an additional field "discussion_polarity" in the root of the object, which is the polarity of the messages that was agreed by the experts in the post-labeling discussions, as described in the paper.
      "agreement_type": "all"
    },
    // The evaluation done by the paper that published this dataset of sentiment analysis tools from the literature
    "tools": {
      "SentiStrength": "neutral",
      "SentiStrengthSE": "neutral",
      "SentiCR": "neutral",
      "DEVA": "neutral",
      "Senti4SD": "neutral"
    }
  }
```
