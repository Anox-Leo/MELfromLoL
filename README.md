# League of Legends Match Prediction

## Authors

- **Léo JOLY-JEHENNE** 
- **Quentin LE GOFF**  

_IMT Atlantique - A3 - Machine Learning Project_

---

## Project Overview

This project aims to predict the outcome of ranked League of Legends matches based on early-game statistics (first 10 minutes). We use machine learning techniques to determine if the Blue team will win based on performance indicators collected during the "early game" phase.

### Main Notebook

📓 **`ML_Project_JOLY--JEHENNE_Leo_LE_GOFF_Quentin.ipynb`**

This comprehensive notebook contains the complete analysis pipeline:

- Exploratory Data Analysis (EDA)
- Feature Engineering
- Baseline Models (Logistic Regression, Random Forest)
- Enhanced Models (XGBoost, LightGBM, CatBoost)
- Hyperparameter Tuning
- Ensemble Learning (Voting, Stacking)
- Model Interpretability (SHAP values)

### Key Results

- **Best Model**: CatBoost
- **Test Accuracy**: 72.7%
- **Test AUC-ROC**: 0.8085
- **Most Important Features**: `blueGoldDiff`, `blueExperienceDiff`, `blueDragons`

## Dataset

### Original Source

**Kaggle Dataset**: [League of Legends Diamond Ranked Games (10 min)](https://www.kaggle.com/datasets/bobbyscience/league-of-legends-diamond-ranked-games-10-min/data)

- **Author**: BobbyScience
- **Size**: ~10,000 ranked games
- **ELO Range**: Diamond I to Master
- **File**: `high_diamond_ranked_10min.csv`

### Dataset Description

- **Target**: `blueWins` (1 if Blue team wins, 0 otherwise)
- **Features**: 39 features (19 per team) including:
  - Gold and experience metrics
  - Kills, deaths, assists
  - Objectives (dragons, heralds, towers)
  - Vision (wards placed/destroyed)

## Game Context

League of Legends (LoL) is a popular MOBA where two teams of 5 players compete. The Blue team starts at the bottom-left of the map, and the Red team at the top-right. To win, a team must destroy the opposing Nexus.

### Key Resources

| Resource       | Description                    | Impact                                    |
| -------------- | ------------------------------ | ----------------------------------------- |
| **Gold**       | In-game currency for equipment | More gold = stronger items                |
| **Experience** | Levels up champions (1-18)     | Higher level = more powerful abilities    |
| **Kills**      | Eliminating opponents          | Grants gold/XP, removes enemy temporarily |
| **Objectives** | Dragons, Herald, Towers        | Permanent bonuses and map control         |

## Installation

### Prerequisites

- Python 3.10+
- Virtual environment recommended

### Setup

```bash
# Clone the repository
git clone https://github.com/Anox-Leo/MELfromLoL.git
cd MELfromLoL

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Dependencies

```
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
scikit-learn>=1.3.0
xgboost>=2.0.0
lightgbm>=4.0.0
catboost>=1.2.0
shap>=0.42.0
jupyter>=1.0.0
```

## Usage

### Running the Notebook

```bash
# Launch Jupyter
jupyter notebook ML_Project_JOLY--JEHENNE_Léo_LE_GOFF_Quentin.ipynb

# Or run directly with VS Code
code ML_Project_JOLY--JEHENNE_Léo_LE_GOFF_Quentin.ipynb
```

### Data Access

The dataset can be loaded in two ways:

1. **Local file** (if present in repository):

```python
df = pd.read_csv('high_diamond_ranked_10min.csv')
```

2. **From GitHub Raw** (recommended for reproducibility):

```python
url = "https://raw.githubusercontent.com/Anox-Leo/MELfromLoL/main/high_diamond_ranked_10min.csv"
df = pd.read_csv(url)
```

## Project Structure

```
MELfromLoL/
├── README.md
├── requirements.txt
├── high_diamond_ranked_10min.csv                      # Dataset
└── ML_Project_JOLY--JEHENNE_Léo_LE_GOFF_Quentin.ipynb # Main notebook (complete analysis)
```

## Methodology

### Workflow

1. **EDA**: Metadata analysis, missing values, distributions, correlations
2. **Clustering**: K-Means to identify match archetypes
3. **Baseline Models**: Logistic Regression, Random Forest, Gradient Boosting
4. **Enhanced Models**: XGBoost, LightGBM, CatBoost with hyperparameter tuning
5. **Ensemble Learning**: Manual Voting and Stacking classifiers
6. **Interpretability**: SHAP values for feature importance explanation

### Model Comparison

| Model               | Val Accuracy | Val AUC   | Test AUC  |
| ------------------- | ------------ | --------- | --------- |
| Logistic Regression | 72.5%        | 0.800     | -         |
| Random Forest       | 71.8%        | 0.797     | -         |
| XGBoost             | 71.9%        | 0.811     | 0.807     |
| LightGBM            | 72.0%        | 0.811     | 0.807     |
| **CatBoost**        | **72.1%**    | **0.813** | **0.809** |
| Voting Ensemble     | 72.0%        | 0.799     | 0.808     |

## License

This project is for educational purposes. Dataset credit goes to BobbyScience on Kaggle.

## Acknowledgments

- Dataset: [BobbyScience - Kaggle](https://www.kaggle.com/datasets/bobbyscience/league-of-legends-diamond-ranked-games-10-min/data)
- Riot Games for League of Legends
