# FactorIA

**Enhancing the Factorio experience by leveraging the strengths of Large Language Models for real-time intelligent assistance.**

FactorIA is an innovative project that combines the automation and factory-building gameplay of Factorio with the advanced capabilities of a Large Language Model (LLM). This repository aims to enhance the Factorio experience by providing intelligent assistance, accurate crafting calculations, optimization suggestions, and interactive support through natural language processing.

# TODO List
## Intelligent Assistant Features
- [X] **Retrieve and Accurately Report Player's Inventory:** Automatically fetch and display the contents of the player's inventory.
- [X] **Calculate Maximum Craft for Any Item with Player's Inventory:** Determine the maximum number of any item that can be crafted using the current inventory.
- [X] **Calculate Crafts for Items *Not* in Player's Inventory:** Estimate crafting requirements for items that are not currently in the player's inventory.
- [X] **Natural Language Support:** Ask questions and get answers within the game using Text-to-speech and Speech-to-text to converse with the model with the wake word "Listen".
- [ ] **Real-Time Optimization Tips:** Receive suggestions on how to improve efficiency in real-time as you build and manage your factory.
- [ ] Reminders and TO-DO.
      
## Documentation
- [ ] Create a detailed user guide on installation and usage.
- [ ] Add API reference documentation for Mod.

## FactorIA.db
- [X] Items table to store item information.
- [X] Recipes table to store recipes.

## FactorIA Mod API
- [X] Send and receive commands using rcon
- [X] Get player name.
- [X] Get player inventory.
- [X] Get all items in game.
- [X] Get all item info.
- [X] Get recipe.
- [X] Get player's unlocked technology.
- [X] Get technology info.
- [X] Get all technologies in game.

## Additional Unplanned Features
- [ ] Track player's entities.
- [ ] Report Resource Depletion.
- [ ] Report Idle Miners.
### Production Events
- [ ] Report Factory Bottlenecks.
- [ ] Report Overproduction/Underproduction.
- [ ] Report Idle Assemblers.
### Logistics Events
- [ ] Report Train Status, state and fuel.
- [ ] Report Train Schedule Issues.
- [ ] Report Belt Blockages.
- [ ] Construction Bot Idle Time.
### Power Management Events
- [ ] Report Power Shortages.
- [ ] Report Power Surplus.
- [ ] Report Accumulator Levels.
### Defense Events
- [ ] Report Turret Ammo Levels.
- [ ] Report Wall Breaches.
### Research and Technology Events
- [ ] Report Research Bottlenecks.
### Player Actions and Advisories
- [ ] Report Efficiency Reports.
- [ ] Report Resource Planning.
- [ ] Report Pollution Levels.
