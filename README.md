# League of Legends Match Prediction (Phase 1)

## Introduction
League of Legends (LoL) is a very popular MOBA (Multiplayer Online Battle Arena) video game. In this project, we will analyze a dataset of ranked games to predict the outcome of a match based on team performance during the first 10 minutes.

Two teams of 5 players face off: the Blue team (bottom left of the map) and the Red team (top right).

To win, a team must destroy the opposing Nexus, which is the "heart" of the enemy base. In your dataset, the blueWins column simply indicates whether the blue team successfully destroyed the red Nexus (1) or not (0).

## The Map and Roles (Context)
The map is divided into 3 main paths called "lanes", and a wild area between them called "jungle".

Top lane: Often solitary and resilient fighters.

Mid lane: Often mages or assassins dealing high damage.

Bot lane: A duo consisting of a marksman (for ranged damage) and a support (to help the team).

Jungle: A player who does not stay in a lane but moves through the wild area to surprise enemies and capture neutral objectives.

## Resources (Dataset Features)
To become stronger and destroy the Nexus, players must accumulate resources. This is where the dataset features come into play. They measure the team's efficiency during the first 10 minutes, a crucial phase called "Early Game".

1. Gold
This is the game's currency. It allows players to buy equipment (swords, armor, boots) to become more powerful.

Sources of gold: Killing minions, monsters, destroying towers, or killing opposing players.

Impact: The more gold a team has (blueTotalGold), the stronger they are supposed to be compared to the opponent.

2. Experience and Levels (Experience & Level)
By staying close to fights, characters (Champions) gain experience (XP).

Levels: Players start at level 1. With each level gained (up to 18), they improve their skills (spells).

Dataset link: blueAvgLevel indicates the average level of the team. If the blue team averages level 7 and the red team level 5, the blue team has a huge advantage (more powerful spells).

3. Combat (Kills & Deaths)
Kills: Number of times the team has killed an opponent. This grants a lot of gold and XP, and temporarily removes the opponent from the game (they must wait to respawn).

Deaths: Number of times team members have died.

Assist: Helping to kill an enemy without dealing the fatal blow.

4. Minions and Monsters (Minions & Jungle)
Minions: Small harmless robot soldiers that advance automatically in the lanes. Killing them (blueTotalMinionsKilled) is the main source of stable income.

Jungle Minions: Neutral monsters in the forest. Usually, only the "Jungler" kills them (blueTotalJungleMinionsKilled).

## Strategic Objectives (Elite Monsters & Structures)
Beyond simple fighting, capturing objectives provides decisive permanent or temporary advantages.

Towers: Defensive turrets that shoot at enemies. They must be destroyed to advance toward the enemy base. Destroying a tower early (blueTowersDestroyed) grants a lot of gold to the whole team and opens up the map.

Dragons: Large neutral monsters. Killing a dragon gives a permanent bonus to the entire team (e.g., +5% damage for the whole match). It is a highly contested objective (blueDragons).

Herald (Rift Herald): A unique monster available early in the game. The team that kills it can summon it to charge and destroy an enemy tower in one hit. This is a huge strategic advantage (blueHeralds).

Vision (Wards)
Warding Totem: The fog of war hides enemies. Players place "Wards" to light up a dark area and see enemy movements.

blueWardsPlaced or blueWardsDestroyed measures map control. A team that sees better can avoid traps and attack better.

## Problem Statement
In this project, you will try to answer questions like: "If the blue team has killed X minions, Y enemies, destroyed Z towers, and has N more gold than the red team after 10 minutes, what is its probability of winning the match at the end (often 20-30 minutes later)?"

The first 10 minutes are often decisive because the advantage gained ("snowball" effect) allows buying better items faster and dominating the rest of the game.

## Dataset

The dataset used is `high_diamond_ranked_10min.csv`, which contains approximately 10,000 ranked games from high ELO (Diamond I to Master).

- **Target**: `blueWins` (1 if Blue team wins, 0 otherwise).
- **Features**: 38 features (19 per team) including kills, gold, experience, etc.

## Project Structure

- `lol_prediction_phase1.ipynb`: The main Jupyter Notebook containing the analysis and modeling.
- `high_diamond_ranked_10min.csv`: The dataset file.
- `requirements.txt`: List of Python dependencies.

## Getting Started

### Prerequisites

Ensure you have Python installed. It is recommended to use a virtual environment.

### Installation

1.  Clone the repository or download the files.
2.  Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

### Usage

1.  Launch Jupyter Notebook:

    ```bash
    jupyter notebook
    ```

2.  Open `lol_prediction_phase1.ipynb` and run the cells to reproduce the analysis and models.

## Analysis Overview

The notebook covers the following steps:

1.  **EDA**: Exploratory Data Analysis to understand feature distributions and correlations.
2.  **Unsupervised Learning**: PCA to visualize the data structure.
3.  **Preprocessing**: Data splitting and scaling.
4.  **Baseline Modeling**: Training Logistic Regression and Random Forest models to establish a baseline performance.

## Results

Baseline models achieve decent accuracy, with Gold and Experience differences being the most significant predictors.