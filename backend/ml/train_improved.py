"""
Improved ML Training - Fast and Accurate
Focus on category prediction with balanced approach
"""

import pandas as pd
import numpy as np
import joblib
import re
import glob
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import warnings
warnings.filterwarnings('ignore')

def clean_text(text):
    """Enhanced text cleaning"""
    if pd.isna(text):
        return ""
    
    text = str(text).lower()
    
    # Keep important indicators
    text = text.replace('!', ' urgent ')
    text = text.replace('?', ' question ')
    
    # Remove special characters
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = ' '.join(text.split())
    
    return text

def extract_keywords(text):
    """Extract domain keywords"""
    keywords = []
    text_lower = text.lower()
    
    if any(w in text_lower for w in ['error', 'bug', 'crash', 'fail', 'broken', 'not working']):
        keywords.append('technical_issue')
    if any(w in text_lower for w in ['payment', 'bill', 'charge', 'refund', 'invoice']):
        keywords.append('billing_issue')
    if any(w in text_lower for w in ['login', 'password', 'account', 'access', 'locked']):
        keywords.append('account_issue')
    if any(w in text_lower for w in ['feature', 'request', 'add', 'new', 'enhancement']):
        keywords.append('feature_request')
    
    return ' '.join(keywords)

def enhance_text(text):
    """Enhance text with keywords"""
    cleaned = clean_text(text)
    keywords = extract_keywords(text)
    return f"{cleaned} {keywords} {keywords}"

def main():
    print("\n" + "="*60)
    print("NEXORAAI IMPROVED ML TRAINING")
    print("="*60)
    
    # Load dataset
    print("\nLoading dataset...")
    dataset_files = glob.glob('../../datasets/*.csv')
    df = pd.read_csv(dataset_files[3])  # Multi-lang 20k dataset
    
    df = df[['subject', 'type']].dropna()
    print(f"Loaded {len(df)} samples")
    print(f"\nCategories: {df['type'].value_counts().to_dict()}")
    
    # Balance categories
    min_samples = 100
    category_counts = df['type'].value_counts()
    valid_categories = category_counts[category_counts >= min_samples].index
    df = df[df['type'].isin(valid_categories)]
    
    # Limit per category for speed
    max_per_category = 2000
    df = df.groupby('type').apply(
        lambda x: x.sample(min(len(x), max_per_category), random_state=42)
    ).reset_index(drop=True)
    
    print(f"\nBalanced to {len(df)} samples")
    print(f"Categories: {df['type'].value_counts().to_dict()}")
    
    # Preprocess
    print("\nPreprocessing...")
    texts = [enhance_text(text) for text in df['subject'].values]
    categories = df['type'].values
    
    # Split
    X_train_text, X_test_text, y_train, y_test = train_test_split(
        texts, categories, test_size=0.2, random_state=42, stratify=categories
    )
    
    print(f"Train: {len(X_train_text)}, Test: {len(X_test_text)}")
    
    # Vectorize
    print("\nVectorizing...")
    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 3),
        min_df=2,
        max_df=0.8,
        sublinear_tf=True
    )
    
    X_train = vectorizer.fit_transform(X_train_text)
    X_test = vectorizer.transform(X_test_text)
    
    print(f"Features: {X_train.shape[1]}")
    
    # Train
    print("\nTraining Logistic Regression...")
    model = LogisticRegression(
        max_iter=2000,
        C=1.0,
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n{'='*60}")
    print(f"ACCURACY: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"{'='*60}")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Per-category accuracy
    print("\nPer-Category Accuracy:")
    for category in np.unique(y_test):
        mask = y_test == category
        cat_acc = accuracy_score(y_test[mask], y_pred[mask])
        print(f"  {category}: {cat_acc:.4f} ({cat_acc*100:.2f}%)")
    
    # Save
    print("\nSaving model...")
    joblib.dump(model, 'model.pkl')
    joblib.dump(vectorizer, 'vectorizer.pkl')
    
    print("\n" + "="*60)
    print("✓ TRAINING COMPLETE!")
    print("✓ Model saved: model.pkl")
    print("✓ Vectorizer saved: vectorizer.pkl")
    print(f"✓ Final Accuracy: {accuracy*100:.2f}%")
    print("="*60)

if __name__ == '__main__':
    main()
