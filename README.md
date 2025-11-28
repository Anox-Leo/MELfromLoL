# MELfromLoL - Machine Learning from League of Legends

## Project Overview

This project analyzes League of Legends Diamond ranked games data to predict game outcomes based on the first 10 minutes of gameplay using various machine learning algorithms.

## Dataset

**Source:** [League of Legends Diamond Ranked Games (10 min)](https://www.kaggle.com/datasets/bobbyscience/league-of-legends-diamond-ranked-games-10-min)

The dataset contains approximately 10,000 ranked games from high Diamond tier players, with features collected at the 10-minute mark of each game.

### Dataset Access

1. **Manual Download:**
   - Visit the Kaggle dataset page
   - Download `high_diamond_ranked_10min.csv`
   - Place it in the project root directory

2. **Using Kaggle API:**
   ```bash
   pip install kaggle
   kaggle datasets download -d bobbyscience/league-of-legends-diamond-ranked-games-10-min
   unzip league-of-legends-diamond-ranked-games-10-min.zip
   ```

## Project Components

- **Data Loading & Exploration:** Load and understand the dataset structure
- **Data Visualization:** Visualize distributions, correlations, and patterns
- **Feature Engineering:** Create derived features (K/D ratio, KDA, gold per minute, etc.)
- **ML Pipeline:** Train and evaluate multiple classification models:
  - Logistic Regression
  - Decision Tree
  - Random Forest
  - Gradient Boosting

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd MELfromLoL
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download the dataset** (see Dataset Access section above)

4. **Run the notebook:**
   ```bash
   jupyter notebook lol_analysis.ipynb
   ```

## Requirements

- Python 3.8+
- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- jupyter

See `requirements.txt` for specific versions.

## Project Structure

```
MELfromLoL/
├── README.md                          # Project documentation
├── lol_analysis.ipynb                 # Main analysis notebook
├── requirements.txt                   # Python dependencies
├── high_diamond_ranked_10min.csv      # Dataset (not included in repo)
├── best_lol_model.pkl                 # Saved best model (generated)
└── feature_scaler.pkl                 # Saved feature scaler (generated)
```

## Results & Insights

The notebook demonstrates:
- Comprehensive exploratory data analysis
- Multiple visualization techniques
- Comparison of 4 different ML algorithms
- Model evaluation using accuracy, precision, recall, F1-score, and ROC-AUC
- Feature importance analysis
- Cross-validation for model stability

Models achieve **>70% accuracy** in predicting game outcomes based solely on 10-minute statistics.

## Author

**Submission Date:** November 2025

## License

This project is for educational purposes.