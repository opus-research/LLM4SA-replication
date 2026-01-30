# Leveraging Large Language Models for Sentiment Analysis in GitHub Pull Request Discussions - Replication Package

This is the replication package for the paper that contains the scripts and data utilized for the execution of the work.

* The data folder provided the dataset utilized in this work.
* The output folder provided the output of all models executed for this work. The name for each file on this folder is comprised of the model name and the prompt engineering technique associated with the file (0shot = no examples, 1shot = 1 example, 3shot = 3 examples, cotshot = 3 examples + reasoning). The responses contained in the file are in the same order as the messages in the dataset.
* The .ipynb files in the root of the repository are the scripts for the collection, analysis processes and generating a sample (for coding) utilized in the work, and are named in order of execution.
* The coding folder, which contains sample used, codes associated with the sample, the codebook, and the scripts for analysis described in the paper (the notebook used to generate the sample is `03_generate_sample_for_coding.ipbny`).

## Requirements

1. Python (executed by the authors of the authors of the paper with version 3.12)
2. Jupyter (or any environment capable of running .ipynb files)
3. Ollama
4. An OpenAI key

> **Note:** In terms of hardware, the main limitation is the execution of ollama. For the models utilized, in terms of memory, the default ollama models usually utilizes from 50% to 66% of the number of paramaters of the models in gigabytes of memory. For example, Llama 3.1 70B requires 43GB of memory.

> **Note:** The study was executed with a laptop running Windows that has an Intel Core i9 13900HX, 32GB of DDR5 RAM, and a RTX 4090 Laptop with 16GB of VRAM.

## Memory and Storage Requirements

The following table lists the storage requirements for each of the local models utilized in this study. The memory requirement is roughly the same value (can combine RAM with VRAM).

| Model Name         | Memory/Storage Requirement |
|---------------------|----------------------------|
| gemma2:9b          | 5.4GB                      |
| gemma2:27b         | 16GB                       |
| llama3.1:8b        | 4.9GB                      |
| llama3.1:70b       | 43GB                       |
| mistral-nemo:12b   | 7.1GB                      |
| mistral-small:22b  | 13GB                       |
| deepseek-r1:8b     | 5.2GB                      |
| deepseek-r1:32b    | 20GB                       |

## Environment Setup

1. Install the dependencies in your python environent

```pip install -r requirements.txt```

> **Note:** If you plan to use a GPU for running transformer models, it is advisable to install PyTorch separately by following the official instructions at https://pytorch.org/get-started/locally/ to ensure compatibility with your GPU and drivers. This may provide better performance and compatibility than the default installation from `requirements.txt`.

2. Install the required models in ollama

```ollama pull model_name```

The names for the models utilized in this work are `gemma2:9b`, `gemma2:27b`, `llama3.1:8b`, `llama3.1:70b`, `mistral-nemo:12b`, `mistral-small:22b`, `deepseek-r1:8b`, and `deepseek-r1:32b`.

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

The following table lists all of the examples that were with the prompt engineering techniques, for the PRemo dataset. Examples 1, 4, and 7 were utilized for one-shot (one example per class), and all examples were utilized for few-shot and CoT.

| ID  | Sentiment  | Message                                                                                                                                                                                                                              | Reasoning (CoT)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
|-----|------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1   | Positive   | Thinking out loud I'm not sure whether a subclass would be a good way to go or not, but happy to discuss further. Thanks!                                                                                                           | Analyzing the tone of the message, we notice that the author is satisfied with what was implemented, and the use of 'thinking out loud' suggests a collaborative approach by openly exploring ideas; the phrase 'I'm not sure' shows openness to suggestions, and 'happy to discuss further' reveals a positive disposition for dialogue and adjustment, indicating that the author values feedback; finally, 'Thanks!' conveys gratitude and reinforces the tone of appreciation and cooperation. |
| 2   | Positive   | Thanks, Your contribution is now merged in with a polish commit.                                                                                                                                                                    | Observing the structure of the message, we notice that 'Thanks' establishes a tone of gratitude, and the expression 'Your contribution' emphasizes the value of the recipient’s participation, creating a sense of recognition; the word 'merged' suggests approval, since the work was integrated into the main project. These elements together reinforce a tone of approval and appreciation for the recipient's effort.                                                      |
| 3   | Positive   | I did polish it a bit more, thanks Eddu!                                                                                                                                                                                            | The 'thanks Eddu!' suggests camaraderie and gratitude, probably for feedback that was given in the pull request. By recognizing the importance of Eddu's feedback in a friendly way and acting on it, the author conveys a tone of cooperation and friendship.                                                                                                                                                                                                                                                               |
| 4   | Neutral    | Quick check using python awscli.                                                                                                                                                                                                   | Analyzing the phrase 'Quick check,' we see that it describes a brief verification without any quality or emotional judgment, suggesting an objective communication; 'Using python awscli' describes the tool and language used, keeping the focus on functionality; the tone is descriptive and informative, without emotional inclination, and the language is purely technical and direct, intended to share a detail without expecting a reaction.                                                                                 |
| 5   | Neutral    | Should this be `AsyncComponent` maybe?                                                                                                                                                                                             | The author of the message is providing, in a purely technical manner, feedback for a change that he believes should be done in the pull request.                                                                                                                                                                                                                                                                                                                                                                         |
| 6   | Neutral    | Can you please give a short update when do you think the next Guice release will be cut? Are there any plans?                                                                                                                       | Looking at the excerpt 'Can you please give a short update,' we see it is a polite and straightforward request, without emotional tone; the phrase 'when do you think the next Guice release will be cut?' seeks information without implying urgency or frustration, and 'Are there any plans?' reinforces the tone of curiosity and inquiry, keeping the focus on information. The choice of words indicates interest but without any emotional inclination.                                                             |
| 7   | Negative   | Sorry, test case was mistaken.                                                                                                                                                                                                     | Observing the use of 'Sorry,' we notice an expression of regret that suggests the author feels responsible for the error.                                                                                                                                                                                                                                                                                                                                                                                                |
| 8   | Negative   | Oh, you know what? I'm stupid. I'm actually using `http-server`. Please, accept my apologies.                                                                                                                                      | In this message, the author utilizes a self-deprecating expression ('I'm stupid') and then apologizes, likely to the reviewer.                                                                                                                                                                                                                                                                                                                                                                                           |
| 9   | Negative   | Hmm, ok that is unfortunate. I have split support into a separate pull request (#2071). If you want you can close this pull request here then, if you don't think there is any chance this will be integrated.                                                             | Analyzing 'unfortunate,' we notice an expression of disappointment with the situation; the phrase 'If you want you can close this pull request' suggests resignation, indicating that the author has low expectations about the integration of the original request; the phrase 'if you don't think there is any chance' emphasizes a pessimistic, almost resigned tone regarding the pull request's outcome.                                                                                                          |

---

### Gold Dataset Prompt Examples

The following table lists all of the examples used for the gold dataset prompts. These are used for one-shot (one example per class) and few-shot/CoT (all examples) settings.

| ID  | Sentiment  | Message                                                                                                                                                                                                                              | Reasoning (CoT)                                                                                                                                                                                                                       |
|-----|------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1   | Positive   | This is just to good to be true. I'm almost crying 'caus of joy. Thanks a lot, this makes life a lot easier!                                                                                   | Expresses joy and gratitude, with phrases like 'almost crying' indicating positive emotion.                                                                                                   |
| 2   | Positive   | Finally! Thanks for the fix!                                                                                                                                                                  | Shows satisfaction and appreciation (finally, thanks), indicating a positive reaction to the change.                                                                                          |
| 3   | Positive   | hehe yeah I first asked to myself, why we have to ask for defined? and not just initialize the value in the initializer. I started to delete that stuff and when I saw the initialize method I realize about the typo :). | Lighthearted tone (hehe, smiley) and amusement about the mistake; no anger, overall friendly/positive.                                                                                        |
| 4   | Neutral    | This is incorrectly placed. It should be under the method signature.                                                                                                                          | A factual correction about code structure with no praise, anger, or other emotional language.                                                                                                 |
| 5   | Neutral    | I'm not sure we need to do this based on checksums.  If somebody touches a file, we should probably send a notification of a change.  I think we should avoid the checksums unless there's a need. | Reasoned technical discussion and recommendation; uncertainty is about design choice, not an emotional reaction.                                                                              |
| 6   | Neutral    | `$return` will only have the last `$child`                                                                                                                                                    | A neutral observation about program behavior/bug (what the variable contains), stated without sentiment.                                                                                      |
| 7   | Negative   | This code again! Will this hack never tire of creating new issues.                                                                                                                            | Shows exasperation and blame ('hack', 'again'), expressing frustration/anger toward the code.                                                                                                |
| 8   | Negative   | Ahhh yes. Brain fail, sorry!                                                                                                                                                                  | Expresses self-frustration and apology (brain fail), which reflects negative affect rather than neutrality.                                                                                   |
| 9   | Negative   | Hate the double colons.  Bring back the old style!                                                                                                                                            | Explicitly conveys dislike ('hate') and a complaint about style, indicating negative sentiment.                                                                                               |

## Datasets

This replication package uses two datasets for sentiment analysis in GitHub pull request discussions:

### 1. PRemo Dataset

This is the primary dataset used in the study:

- **Source:** Coutinho, D., Cito, L., Lima, M. V., Arantes, B., Alves Pereira, J., Arriel, J., ... & Fonseca, B. (2024, June). "Looks Good To Me;-): Assessing Sentiment Analysis Tools for Pull Request Discussions." In Proceedings of the 28th International Conference on Evaluation and Assessment in Software Engineering (pp. 211-221).
- **File:** `data/dataset.json`
- **Format:** The schema for the JSON file is as follows:


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
    // "comp_only" and "neuro_and_comp" when only 2 experts agreed
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

See the comments in the JSON example above for detailed field descriptions.

**Citation:**

> Coutinho, D., Cito, L., Lima, M. V., Arantes, B., Alves Pereira, J., Arriel, J., ... & Fonseca, B. (2024, June). "Looks Good To Me;-): Assessing Sentiment Analysis Tools for Pull Request Discussions." In Proceedings of the 28th International Conference on Evaluation and Assessment in Software Engineering (pp. 211-221).

### 2. Gold Dataset (Gold Standard GitHub Dataset)

This dataset is used as an additional benchmark and is referred to as the "gold standard GitHub dataset" in the original paper.

- **Source:** Novielli, N., Calefato, F., Dongiovanni, D., Girardi, D., & Lanubile, F. (2020, June). Can we use se-specific sentiment analysis tools in a cross-platform setting?. In Proceedings of the 17th International Conference on Mining Software Repositories (pp. 158-168).
- **File:** `data/github_gold.csv`
- **Format:** The format and field descriptions for this dataset can be found in the file itself (`data/github_gold.csv`).

**Citation:**

> Novielli, N., Calefato, F., Dongiovanni, D., Girardi, D., & Lanubile, F. (2020, June). Can we use se-specific sentiment analysis tools in a cross-platform setting?. In Proceedings of the 17th International Conference on Mining Software Repositories (pp. 158-168).