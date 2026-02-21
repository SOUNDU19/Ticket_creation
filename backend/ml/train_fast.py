import pandas as pd
import numpy as np
import joblib
import re
import glob
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
import warnings
warnings.filterwarnings('ignore')

def clean_text(text):
    """Simple text cleaning"""
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = ' '.join(text.split())
    return text

def load_and_prepare_data():
    """Load and prepare dataset"""
    print("\n" + "="*60)
    print("LOADING DATASET")
    print("="*60)
    
    dataset_files = glob.glob('../../datasets/*.csv')
    
    if not dataset_files:
        print("ERROR: No dataset files found!")
        return None, None
    
    print(f"Found {len(dataset_files)} dataset file(s)")
    
    # Load only one dataset for speed
    df = pd.read_csv(dataset_files[3])  # Use the 20k dataset
    print(f"Loaded: {dataset_files[3]} - {len(df)} rows")
    
    # Limit to 10k for fast training
    if len(df) > 10000:
        df = df.sample(n=10000, random_state=42)
        print(f"Sampled to: {len(df)} rows")
    
    # Use subject as text and type as category
    text_col = 'subject'
    category_col = 'type'
    
    df = df[[text_col, category_col]].dropna()
    
    print(f"\nAfter removing missing values: {len(df)} rows")
    print(f"\nCategory distribution:")
    print(df[category_col].value_counts())
    
    return df[text_col].values, df[category_col].values

def train_models(X_train, X_test, y_train, y_test):
    """Train models"""
    print("\n" + "="*60)
    print("TRAINING MODELS")
    print("="*60)
    
    # Use only Logistic Regression for speed
    print(f"\n--- Training Logistic Regression ---")
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1 Score:  {f1:.4f}")
    
    print("\n--- Classification Report ---")
    print(classification_report(y_test, y_pred))
    
    return model

def main():
    """Main training pipeline"""
    print("\n" + "="*60)
    print("NEXORAAI FAST ML TRAINING")
    print("="*60)
    
    # Load data
    texts, categories = load_and_prepare_data()
    
    if texts is None:
        return
    
    # Simple text cleaning
    print("\n" + "="*60)
    print("TEXT PREPROCESSING")
    print("="*60)
    print("Cleaning text...")
    
    processed_texts = [clean_text(text) for text in texts]
    print(f"Preprocessing complete: {len(processed_texts)} texts")
    
    # Train-test split
    print("\n" + "="*60)
    print("TRAIN-TEST SPLIT")
    print("="*60)
    X_train_text, X_test_text, y_train, y_test = train_test_split(
        processed_texts, categories, test_size=0.2, random_state=42, stratify=categories
    )
    print(f"Training samples: {len(X_train_text)}")
    print(f"Testing samples: {len(X_test_text)}")
    
    # TF-IDF Vectorization
    print("\n" + "="*60)
    print("TF-IDF VECTORIZATION")
    print("="*60)
    vectorizer = TfidfVectorizer(max_features=3000, ngram_range=(1, 2))
    X_train = vectorizer.fit_transform(X_train_text)
    X_test = vectorizer.transform(X_test_text)
    print(f"Feature dimensions: {X_train.shape[1]}")
    
    # Train model
    model = train_models(X_train, X_test, y_train, y_test)
    
    # Save model and vectorizer
    print("\n" + "="*60)
    print("SAVING MODEL")
    print("="*60)
    joblib.dump(model, 'model.pkl')
    joblib.dump(vectorizer, 'vectorizer.pkl')
    print("✓ Model saved: model.pkl")
    print("✓ Vectorizer saved: vectorizer.pkl")
    
    print("\n" + "="*60)
    print("TRAINING COMPLETE!")
    print("="*60)

if __name__ == '__main__':
    main()
