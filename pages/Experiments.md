# Experiments


## Testing the Viability of Using VLMs
There are several ways for a language model to gather information about a game state.
Ideally if the model is capable of decerning the game state from just an image, there wouldn't be a need for any API access given by the developers.

Before we get ahead of ourselves, we have to boil the problem down to it's bare necessities.
First and for most, the model has to be accurate; for if it isn't, the second guessing would defeat the purpose of integrating a model to a game as complex as factorio.
The prime metric is the model's ability to do visual question answering.

To test the viability of VLMs, I've opted to test 5 State of the art (as of June 2024) API models for their 0-shot accuracy and pre-prompted accuracy. and for one instance for Multi-shot accuracy (GPT-4o).
The reason that it doesn't require any additional performance load on the user, but it does incur financial costs.

Example Prompt:
How much wood do I have?
How much coal do I have?
How much stone do I have?
How many iron plates do I have?
How many copper plates do I have?

### 0-Shot Accuracy, Single Prompt

|                       | 1 Item   | 5 Items  | 13 Items  | 21 Items  | 33 Items  | Average Accuracy by Prompt |
|-----------------------|----------|----------|-----------|-----------|-----------|----------------------------|
| **GPT-4o**            | **100.00%** | **60.00%** | **60.00%**  | **20.00%**  | **0.00%**   | **48.00%**                 |
| **GPT-4**             | **100.00%** | **0.00%**  | **0.00%**   | **0.00%**   | **20.00%**  | **24.00%**                 |
| **Claude3 - Opus**    | **60.00%**  | **80.00%** | **0.00%**   | **0.00%**   | **20.00%**  | **32.00%**                 |
| **Gemini 1.5 Flash**  | **100.00%** | **0.00%**  | **60.00%**  | **0.00%**   | **20.00%**  | **36.00%**                 |
| **Gemini 1.5 Pro**    | **100.00%** | **60.00%** | **100.00%** | **20.00%**  | **20.00%**  | **60.00%**                 |

Contextual Prompt:
The following is the inventory screen for the game
please answer with 100% accuracy the following ques
How much wood do I have?
How much coal do I have?
How much stone do I have?
How many iron plates do I have?
How many copper plates do I have?

### Pre-prompted Context, Single Prompt

|                       | 1 Item   | 5 Items  | 13 Items  | 21 Items  | 33 Items  | Average Accuracy by Prompt |
|-----------------------|----------|----------|-----------|-----------|-----------|----------------------------|
| **GPT-4o**            | **100.00%** | **40.00%** | **20.00%**  | **40.00%**  | **20.00%**  | **44.00%**                 |
| **GPT-4**             | **100.00%** | **0.00%**  | **20.00%**  | **0.00%**   | **20.00%**  | **28.00%**                 |
| **Claude3 - Opus**    | **80.00%**  | **60.00%** | **0.00%**   | **0.00%**   | **0.00%**   | **28.00%**                 |
| **Gemini 1.5 Flash**  | **100.00%** | **80.00%** | **60.00%**  | **20.00%**  | **60.00%**  | **64.00%**                 |
| **Gemini 1.5 Pro**    | **100.00%** | **80.00%** | **80.00%**  | **40.00%**  | **40.00%**  | **68.00%**                 |


### Multi-shot, Single Prompt

|                       | 1 Item   | 5 Items  | 13 Items  | 21 Items  | 33 Items  | Average Accuracy by Prompt |
|-----------------------|----------|----------|-----------|-----------|-----------|----------------------------|
| **ChatGPT-4o**        | **100.00%** | **60.00%** | **80.00%**  | **80.00%**  | **60.00%**  | **76.00%**                 |

GPT-4o in Multi-shot managed to excel reaching up to 76%. However, could potentially be depended on the quality of the prompt, and the player's inventory can go up to 120 slots (vanilla), and with over 200+ items in game it would take more time (and the data) to finetune the model for simply the accurate reporting of what the player has.

- "Oh the first item is a single Wooden chest, the next is 10 Wood, 48 Coal, 44 Stone and 7 Iron Ore"
- "everything else is correct, but for stone, there are 6 stacks of 50 units and plus 2"
- "This time there are only 4 stacks of stone and plus 2 units, everything else is correct"

VLMs seemed feasible at first, but there are multiple things to consider
- Resource intensiveness.
- Size of input image/video.
- Noticable response time.

Not to mention, this will limit the model to when they can get a screenshot of the players inventory, where players can pick up items and have their inventory updated but never need to open up their inventory.

The world of VLMs also inherit the issues of image processing, resolution, image preprocessing, aspect ratio, compression and quality.

The accurate capturing a player's ever changing inventory in itself can already be challenging, and the amount of data required to report every item accurately simply to know the player's inventory isn't feasible.

Even the best VLMs according to HuggingFace's leaderboards only show the highest average scores of around 70%.
https://huggingface.co/spaces/opencompass/open_vlm_leaderboard
Which simply isn't good enough for our use case.
<!-- ![alt text](assets/images/main.py__Factorio.drawio.png "Python Flowchart") -->

The Idea should be that players can easily ask what they have without needing all the hassle and processing time.


## Choosing The Right Model

The right model has to satisfy the following:
• must be run locally.
• be open-sourced.
• have some basic knowledge about the game.
• be small enough to not affect performance.
• respond with low latency.
• be as accurate as possible.


## Goal and Motivation

(While) The overall goal isn't to replace useful knowledge resources like Reddit/Wiki/Youtube, the idea is that flow and immersion is broken when players have to stop and grow their knowledge base in order for the player to continue playing. Having to search up guides or an online tutorial while can be a fufilling activity on its own (growing self-competency), it breaks away from actually playing the game itself.

Factorio is a game about crafting and optimization, Players often have to press E to check their inventory every few seconds to check recipes or craft items for logistics. I don't know how many times I have to check how many Steel plates I have left to craft XYZ.

Often players take it for granted the motor skill required and the amount of actions per minute wasted on checking information we should "already know".


1) How effectively can LLMs be combined to create an AI
companion that understands the game state and responds
to player queries in real-time?
2) How can the AI companion be designed to learn along-
side the player and build a personalized knowledge base
that evolves with their progress?
3) How accurate can the AI companion be out of the box?
4) What are the limitations of using LLMs in this context?


## Understanding The Minimum Amount of Information required for Utility (for something to be useful)

The complexity for game state can vary between games.

Board games like Chess, Checkers, Go, or even Tic-Tac-Toe are games where all information is available to all players and there is no hidden information.

While games like FTL, Slay the Spire, Darkest Dungeon rely on their roguelike elements, Civilizaion VI, Stellaris, Starcraft 2, Dota 2 and League of Legends rely on fog of war as information by obscurity or enemy actors.

And thusly, the minimum information for each game may vary, and thus the model may need different information for each individual game. Like most RPG games would have an inventory(Player resource) or map(Positional information). To build a universal LLM model that could be run locally by the player would be a huge ask, either the size of the model will inevitably grow, or the model will have to lose functionality else where. And so it makes sense to have a specialized model for each individual game.

Factorio sits in an interesting position between perfect and imperfect information games. While it primarily operates as a perfect information game, there are some aspects that introduce elements of imperfect information:

### Perfect Information Aspects:

- Game World and Mechanics: All elements of the game, such as resources, factory layouts, and production chains, are fully visible and accessible to the player. The player has complete control over the environment and can plan and optimize their factory based on the visible resources and infrastructure.
- No Hidden Elements: There is no hidden information regarding enemy positions or resources. Everything is discoverable by exploring the map.

### Imperfect Information Aspects:

- Exploration: At the start of the game, the player does not know the layout of the map or the location of key resources. The need to explore introduces a temporary element of imperfect information.
- Enemy Attacks: While enemy bases are visible once discovered, their attack patterns and timing can introduce some unpredictability, especially early in the game.

In summary, Factorio is largely a perfect information game due to its transparency in mechanics and the player's ability to access and manipulate all game elements. However, the initial need for exploration and the unpredictability of certain events add a layer of imperfect information, particularly in the early stages of gameplay.

The player will always need to interact with their inventory and that knowledge is contingent on the games progression.

The Model will be able to obtain the necessary information via API, the game directly informing the model, this way it ensures abosolute accuracy without any of the guess work.


## Challenges and Limitations of LLMs

While LLMs can provide rich conversational interactions and near real-time guidance and support for the player's context, an optimization game like Factorio demands players to perform estimations and calculations for the production of items; and LLMs aren't particularly designed to solve logic or mathematical puzzles.

The task is such that the model should be able to accurately report how many the player can craft with the available inventory. 

Take for instance a wooden chest, it takes 2 pieces of woodto craft 1 wooden chest. 
The model is able to retrieve the player inventory (get inventory()) and calculate without any additional functions for how many the player can craft. 
TODO: maybe show some examples

Where the model struggles however, when a complex recipe like the inserter seen here in figure 5. Because all three ingredients required iron plates(TODO: add mini icons for item names) the model had issues with calculating the right result. As of time of writing (Factorio vanilla v.1.1.109) there are no provided API by the game that calculates the item based on the player’s inventory.

Several models were tested in their ability to solve complex recipes such as inserters.

| **Models**              | **#1**               | **#2**               | **#3**               |
|-------------------------|----------------------|----------------------|----------------------|
| **ChatGPT 4o**          | 0*                   | 1                    | 1                    |
| **Gemini Advanced**     | 1                    | 1                    | 1                    |
| **Gemma2 27B**          | 1                    | 1                    | 1                    |
| **Claude 3.5 Sonnet**   | 1                    | 1                    | 1                    |
| **Llama3.1-8B-I-Q8_0**  | 1                    | 0                    | 3                    |
*Attempted to craft all Iron Gear Wheels first, resulting in 0 Iron Plates left for Electronic Circuits.

Prompt 1:
Given that the player's inventory has: 10 Iron Plates and 2 Copper Plates.

The recipe for 1 Iron Gear Wheel is: 2 Iron Plates.
The recipe for 1 Electronic Circuit is: 1 Iron Plate and 3 Copper Cables.
The recipe for 2 Copper Cables is: 1 Copper Plate.
The recipe for 1 Inserter is: 1 Iron Plate, 1 Iron Gear Wheel, and 1 Electronic Circuit.

What is the maximum amount of Inserters the player can craft?

============================================================
Expected Response:
Able to craft 1 Inserter.
============================================================

| **Models**              | **#1**               | **#2**               | **#3**               |
|-------------------------|----------------------|----------------------|----------------------|
| **ChatGPT 4o**          | 300                  | 100                  | 400                  |
| **Gemini Advanced**     | 200                  | 200                  | 266                  |
| **Gemma2 27B**          | 133                  | 133                  | 133                  |
| **Claude 3.5 Sonnet**   | 133                  | 200                  | 200                  |
| **Llama3.1-8B-I-Q8_0**  | 100                  | 133                  | 133                  |

Prompt 2:
Given that the player's inventory has: 400 Iron Plates, 400 Copper Plates, 200 Iron Gear Wheels, and 200 Electronic Circuits.

The recipe for 1 Iron Gear Wheel is: 2 Iron Plates.
The recipe for 1 Electronic Circuit is: 1 Iron Plate and 3 Copper Cables.
The recipe for 2 Copper Cables is: 1 Copper Plate.
The recipe for 1 Inserter is: 1 Iron Plate, 1 Iron Gear Wheel, and 1 Electronic Circuit.

What is the maximum amount of Inserters the player can craft?

============================================================
Expected Response:
Able to craft 250 Inserter.
============================================================


In the Prompt #1, almost all models were able to decern that only 1 inserter could be crafted. Right as I was about to formally benchmark the models, GPT-4o decided to perform the heuristic wrong, but would have otherwise reported 1.

Where as all models failed in Prompt #2 when the player inventory had intemediary products.

Surprisingly, the heuristics for this optimization problem is simple; Craft how many inserters you can first, subtract that from the model, and review what intemediary product is needed.

For the example in prompt #2, once the player has crafted 200 initial inserters, they would be left with, 200 Iron Plates, 400 Copper Plates, 0 Iron Gear Wheels, and 0 Electronic Circuits; which is enough to craft an additional 50 inserters.

Seeing that even the SOTA models aren't able to solve these types of optimization constraint problems, with the ultimate goal of maintaining absolute accuracy to the player, several helper functions were written to supplement this.

Additionally, in the interest of added utility, the model is also given the helper function to calculate the theoretical requirements. E.g. "What would I need to craft 12 Lazer Turrets", despite not having enough batteries.

## Bridging Factorio With The LLM

Factorio is renown for it's modding community and support. (One modder even ended up becoming one of the devs implementing it as one of the core up and coming feature)

There are no direct connections via Python to access a player's game state.
So in order to do this, the work around is to utilize the MCRcon python library to send Remote Commands (RCON) to the player's game, and in order to receive an output from the game, the mod itself will output to a json file (Appdata/Factorio/script-output) to be read within the python environment.
While this solution is hardly ideal, I have yet to find a better solution.

TODO: add flowchat of how the Python environment interacts with Factorio via the mod and json.

The following are some functions readily (or indirectly) used by the model:

get_player_name()
- returns player name
get_inventory()
- returns player inventory
get_all_items_info()
- returns info on all items within that game instance
get_all_items()
- returns all items within that game instance
get_recipe(item_name)
- returns the recipe with the given item name

This gives the model enough information to answer player inqueries and perform calculations.

Naturally, it is also worth benchmarking the response time, for if the latency becomes too great, it becomes a bottleneck for the model's performace.


## API Benchmarks and Local Databases

| **CustomMod API calls**   | **Execution time for 1000 calls (s)** | **Factorio.db Equivalent**          | **Execution time for 1000 calls (s)** |
|---------------------------|---------------------------------------|-------------------------------------|---------------------------------------|
| get_player_name()          | 16.66                                 | -                                   | -                                     |
| get_inventory()            | 16.68                                 | -                                   | -                                     |
| get_all_items_info()       | 17.17                                 | -                                   | -                                     |
| get_all_items()            | 16.75                                 | list_all_item_names_from_db()       | 0.22                                  |
| get_recipe(item_name)      | 16.71                                 | get_recipe_from_db(item_name)       | 0.17                                  |

Here I highlight the use of databases versus calling directly to the game.

Some information are static (so long as the game instance is the same), like the player's name, item information or recipes.
Whereas a player's inventory may vary throughout the game, so it makes little sense to cache or store the information in the long term, since it could change by the second.

Whereever possible it is to minimize huge calls (over 200+ items) it makes sense to place it into a database for quick retrieval. As evident by the results of getting an item's recipe, it takes around 16.71 seconds for the API to make 1000 calls (which is really 0.01671 seconds per call on average), but only 0.17 seconds for the same 1000 call via the database solution (0.00017 seconds per call!) that's around 98.29 times faster (or 9829% faster if you like multiplying by 100).