import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import xgboost as xgb
import lightgbm as lgb
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

def load_and_preprocess(filepath):
    print("--- Loading Data ---")
    df = pd.read_csv(filepath)
    
    # Drop ID column if exists
    if 'gameId' in df.columns:
        df = df.drop('gameId', axis=1)
    
    print(f"Dataset shape: {df.shape}")
    
    # Target
    target = 'blueWins'
    
    # Feature Engineering (Simplistic for now, keeping original features)
    # Handling categorical 'dragonSoul'
    if 'dragonSoul' in df.columns:
        # Check if it has values
        print(f"Unique Dragon Souls: {df['dragonSoul'].unique()}")
        # One-hot encoding
        df = pd.get_dummies(df, columns=['dragonSoul'], drop_first=True)
    
    return df, target

def unsupervised_exploration(df, target_col):
    print("\n--- Unsupervised Exploration: Clustering ---")
    # Drop target for clustering
    X = df.drop(target_col, axis=1)
    
    # Scale data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # KMeans
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)
    
    df['cluster'] = clusters
    
    # Analyze correlation with target
    print("Cluster distribution vs Target (Win Rate per Cluster):")
    print(df.groupby('cluster')[target_col].mean())
    
    # Visualize
    # PCA for 2D visualization (optional, implemented in Phase 1 but useful here)
    from sklearn.decomposition import PCA
    pca = PCA(n_components=2)
    components = pca.fit_transform(X_scaled)
    
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=components[:,0], y=components[:,1], hue=df['cluster'], palette='viridis', alpha=0.5)
    plt.title('Clusters Visualization (PCA)')
    plt.savefig('clusters.png') # Saving instead of showing
    print("Cluster visualization saved to 'clusters.png'")
    
    return df

def train_and_optimize(df, target_col):
    print("\n--- Modeling & Optimization ---")
    X = df.drop([target_col, 'cluster'], axis=1) # Drop cluster used for analysis
    y = df[target_col]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 1. XGBoost with RandomSearch
    print("Optimizing XGBoost...")
    xgb_clf = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
    
    param_dist = {
        'n_estimators': [100, 200, 300],
        'learning_rate': [0.01, 0.05, 0.1, 0.2],
        'max_depth': [3, 5, 7],
        'subsample': [0.8, 1.0],
        'colsample_bytree': [0.8, 1.0]
    }
    
    random_search = RandomizedSearchCV(xgb_clf, param_distributions=param_dist, n_iter=10, cv=3, verbose=1, n_jobs=-1, random_state=42)
    random_search.fit(X_train_scaled, y_train)
    
    best_xgb = random_search.best_estimator_
    print(f"Best XGB Params: {random_search.best_params_}")
    
    # 2. LightGBM
    print("Training LightGBM...")
    lgb_clf = lgb.LGBMClassifier(random_state=42)
    lgb_clf.fit(X_train_scaled, y_train)
    
    # 3. Ensemble (Voting)
    print("Building Ensemble...")
    # Using Logistic Regression as a base linear model
    lr_clf = LogisticRegression(random_state=42)
    
    voting_clf = VotingClassifier(
        estimators=[('xgb', best_xgb), ('lgb', lgb_clf), ('lr', lr_clf)],
        voting='soft'
    )
    
    voting_clf.fit(X_train_scaled, y_train)
    
    # Evaluation
    print("\n--- Evaluation (Ensemble) ---")
    y_pred = voting_clf.predict(X_test_scaled)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(classification_report(y_test, y_pred))
    
    return voting_clf

if __name__ == "__main__":
    file_path = "high_diamond_ranked_10min.csv"
    
    try:
        df, target = load_and_preprocess(file_path)
        df = unsupervised_exploration(df, target)
        model = train_and_optimize(df, target)
        print("\nPhase 2 Analysis Complete.")
    except Exception as e:
        print(f"An error occurred: {e}")
