# Experiments


## Testing the Viability of Using VLMs
There are several ways for a language model to gather information about a game state.
Ideally if the model is capable of decerning the game state from just an image, there wouldn't be a need for any API access given by the developers.

Before we get ahead of ourselves, we have to boil the problem down to it's bare necessities.
First and for most, the model has to be accurate; for if it isn't, the second guessing would defeat the purpose of integrating a model to a game as complex as factorio.
The prime metric is the model's ability to do visual question answering.

To test the viability of VLMs, I've opted to test 5 State of the art online models for their 0-shot accuracy and pre-prompted accuracy. and for one instance for Multi-shot accuracy (GPT-4o).
The reason that it doesn't require any additional performance load on the user, but it does incur financial costs.

0-Shot Accuracy, Single Prompt

|                       | 1 Item   | 5 Items  | 13 Items  | 21 Items  | 33 Items  | Average Accuracy by Prompt |
|-----------------------|----------|----------|-----------|-----------|-----------|----------------------------|
| **GPT-4o**            | **100.00%** | **60.00%** | **60.00%**  | **20.00%**  | **0.00%**   | **48.00%**                 |
| **GPT-4**             | **100.00%** | **0.00%**  | **0.00%**   | **0.00%**   | **20.00%**  | **24.00%**                 |
| **Claude3 - Opus**    | **60.00%**  | **80.00%** | **0.00%**   | **0.00%**   | **20.00%**  | **32.00%**                 |
| **Gemini 1.5 Flash**  | **100.00%** | **0.00%**  | **60.00%**  | **0.00%**   | **20.00%**  | **36.00%**                 |
| **Gemini 1.5 Pro**    | **100.00%** | **60.00%** | **100.00%** | **20.00%**  | **20.00%**  | **60.00%**                 |



Pre-prompted Context, Single Prompt

|                       | 1 Item   | 5 Items  | 13 Items  | 21 Items  | 33 Items  | Average Accuracy by Prompt |
|-----------------------|----------|----------|-----------|-----------|-----------|----------------------------|
| **GPT-4o**            | **100.00%** | **40.00%** | **20.00%**  | **40.00%**  | **20.00%**  | **44.00%**                 |
| **GPT-4**             | **100.00%** | **0.00%**  | **20.00%**  | **0.00%**   | **20.00%**  | **28.00%**                 |
| **Claude3 - Opus**    | **80.00%**  | **60.00%** | **0.00%**   | **0.00%**   | **0.00%**   | **28.00%**                 |
| **Gemini 1.5 Flash**  | **100.00%** | **80.00%** | **60.00%**  | **20.00%**  | **60.00%**  | **64.00%**                 |
| **Gemini 1.5 Pro**    | **100.00%** | **80.00%** | **80.00%**  | **40.00%**  | **40.00%**  | **68.00%**                 |



Multi-shot, Single Prompt

|                       | 1 Item   | 5 Items  | 13 Items  | 21 Items  | 33 Items  | Average Accuracy by Prompt |
|-----------------------|----------|----------|-----------|-----------|-----------|----------------------------|
| **ChatGPT-4o**        | **100.00%** | **60.00%** | **80.00%**  | **80.00%**  | **60.00%**  | **76.00%**                 |






https://huggingface.co/spaces/opencompass/open_vlm_leaderboard
<!-- ![alt text](assets/images/main.py__Factorio.drawio.png "Python Flowchart") -->