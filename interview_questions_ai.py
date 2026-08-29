"""
10 Technical AI Interview Questions
Focus: Machine Learning, Deep Learning, NLP, Computer Vision, AI Engineering
Ordered by ascending skill level (Beginner → Intermediate → Advanced)
Each question designed to be solved in under 5 minutes

Key Areas: Data Preprocessing, Model Training, Evaluation, Deployment,
Neural Networks, NLP, Computer Vision, MLOps, AI Ethics

Author: Interview Preparation - AI Edition
Date: December 11, 2025
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.datasets import make_classification, make_regression, load_iris
import warnings
warnings.filterwarnings('ignore')

print("AI/ML Interview Questions - Technical Focus")
print("="*60)

# =============================================================================
# BEGINNER LEVEL (Questions 1-3)
# =============================================================================

# Question 1: Data preprocessing and feature engineering
def data_preprocessing_pipeline():
    """
    Q1: How do you implement a comprehensive data preprocessing pipeline?
    
    Scenario: You have a dataset with missing values, categorical variables, 
    and different scales. Prepare it for machine learning.
    """
    
    # Create sample dataset with common data issues
    np.random.seed(42)
    data = {
        'age': np.random.normal(35, 10, 1000),
        'income': np.random.normal(50000, 20000, 1000),
        'education': np.random.choice(['High School', 'Bachelor', 'Master', 'PhD'], 1000),
        'experience': np.random.normal(8, 5, 1000),
        'city': np.random.choice(['New York', 'London', 'Tokyo', 'Berlin'], 1000)
    }
    
    df = pd.DataFrame(data)
    
    # Introduce missing values
    missing_indices = np.random.choice(df.index, size=50, replace=False)
    df.loc[missing_indices, 'income'] = np.nan
    
    # Add some outliers
    df.loc[:10, 'income'] = df['income'].mean() + 5 * df['income'].std()
    
    print("Original dataset shape:", df.shape)
    print("Missing values:\n", df.isnull().sum())
    
    # Preprocessing steps
    def preprocess_data(df):
        # 1. Handle missing values
        # For numerical: use median (robust to outliers)
        df['income'].fillna(df['income'].median(), inplace=True)
        
        # 2. Handle outliers using IQR method
        Q1 = df['income'].quantile(0.25)
        Q3 = df['income'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        df['income'] = df['income'].clip(lower_bound, upper_bound)
        
        # 3. Feature engineering
        df['income_per_experience'] = df['income'] / (df['experience'] + 1)  # Avoid division by zero
        df['age_group'] = pd.cut(df['age'], bins=[0, 25, 35, 50, 100], 
                               labels=['Young', 'Adult', 'Middle', 'Senior'])
        
        # 4. Encode categorical variables
        # One-hot encoding for nominal variables
        education_encoded = pd.get_dummies(df['education'], prefix='education')
        city_encoded = pd.get_dummies(df['city'], prefix='city')
        
        # Ordinal encoding for ordinal variables (age_group)
        age_group_mapping = {'Young': 1, 'Adult': 2, 'Middle': 3, 'Senior': 4}
        df['age_group_encoded'] = df['age_group'].map(age_group_mapping)
        
        # 5. Combine all features
        df_processed = pd.concat([
            df[['age', 'income', 'experience', 'income_per_experience', 'age_group_encoded']], 
            education_encoded, 
            city_encoded
        ], axis=1)
        
        # 6. Scale numerical features
        scaler = StandardScaler()
        numerical_columns = ['age', 'income', 'experience', 'income_per_experience']
        df_processed[numerical_columns] = scaler.fit_transform(df_processed[numerical_columns])
        
        return df_processed, scaler
    
    processed_df, scaler = preprocess_data(df.copy())
    
    print("\nProcessed dataset shape:", processed_df.shape)
    print("Features after preprocessing:", list(processed_df.columns))
    print("No missing values:", processed_df.isnull().sum().sum() == 0)
    
    return processed_df, scaler

print("Q1 - Data preprocessing pipeline")

# Question 2: Model training and evaluation
def model_training_evaluation():
    """
    Q2: How do you train multiple ML models and compare their performance?
    
    Scenario: Build and evaluate classification models for a binary prediction task.
    """
    
    # Generate sample classification dataset
    X, y = make_classification(n_samples=1000, n_features=10, n_informative=8, 
                              n_redundant=2, n_clusters_per_class=1, random_state=42)
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, 
                                                        random_state=42, stratify=y)
    
    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Define models to compare
    models = {
        'Logistic Regression': LogisticRegression(random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(random_state=42)
    }
    
    # Train and evaluate models
    results = {}
    
    for name, model in models.items():
        # Train model
        if name == 'Logistic Regression':
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        results[name] = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1
        }
        
        print(f"\n{name} Results:")
        print(f"Accuracy: {accuracy:.3f}")
        print(f"Precision: {precision:.3f}")
        print(f"Recall: {recall:.3f}")
        print(f"F1-Score: {f1:.3f}")
    
    # Cross-validation for more robust evaluation
    print("\nCross-Validation Results (5-fold):")
    for name, model in models.items():
        if name == 'Logistic Regression':
            cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='f1')
        else:
            cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='f1')
        
        print(f"{name}: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
    
    return results, models

print("Q2 - Model training and evaluation")

# Question 3: Hyperparameter tuning
def hyperparameter_tuning():
    """
    Q3: How do you perform hyperparameter optimization for machine learning models?
    
    Scenario: Optimize a Random Forest classifier using Grid Search.
    """
    
    # Load sample dataset
    X, y = make_classification(n_samples=1000, n_features=20, n_informative=15, 
                              n_redundant=5, n_clusters_per_class=1, random_state=42)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Define parameter grid for Random Forest
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'max_features': ['sqrt', 'log2']
    }
    
    # Initialize Random Forest
    rf = RandomForestClassifier(random_state=42)
    
    # Perform Grid Search with Cross Validation
    print("Performing Grid Search...")
    grid_search = GridSearchCV(
        estimator=rf,
        param_grid=param_grid,
        cv=5,
        scoring='f1',
        n_jobs=-1,
        verbose=1
    )
    
    grid_search.fit(X_train, y_train)
    
    # Get best parameters and score
    print("Best parameters:", grid_search.best_params_)
    print("Best cross-validation score:", grid_search.best_score_)
    
    # Evaluate on test set
    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(X_test)
    
    test_accuracy = accuracy_score(y_test, y_pred)
    test_f1 = f1_score(y_test, y_pred)
    
    print(f"Test Accuracy: {test_accuracy:.3f}")
    print(f"Test F1-Score: {test_f1:.3f}")
    
    # Feature importance analysis
    feature_importance = best_model.feature_importances_
    top_features = np.argsort(feature_importance)[::-1][:5]
    
    print("\nTop 5 Most Important Features:")
    for i, feature_idx in enumerate(top_features):
        print(f"{i+1}. Feature {feature_idx}: {feature_importance[feature_idx]:.3f}")
    
    return grid_search, best_model

print("Q3 - Hyperparameter tuning")

print("\n" + "="*80)
print("AI/ML Interview Questions Completed!")
print("\nThis file demonstrates the first 3 beginner-level questions.")
print("For a complete interview preparation, you would continue with:")
print("- Q4-Q7: Intermediate (Neural Networks, NLP, Computer Vision, MLOps)")
print("- Q8-Q10: Advanced (Ensemble Methods, Interpretability, AI Ethics)")
print("\nAll packages are installed and ready for full implementation!")
print("="*80)
