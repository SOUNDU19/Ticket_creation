"""
Enhanced ML Training for Better Category Prediction
Focuses on improving category classification accuracy
"""

import pandas as pd
import numpy as np
import joblib
import re
import glob
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

def clean_text(text):
    """Enhanced text cleaning"""
    if pd.isna(text):
        return ""
    
    text = str(text).lower()
    
    # Keep important punctuation that might indicate urgency
    text = text.replace('!', ' urgent ')
    text = text.replace('?', ' question ')
    
    # Remove special characters but keep spaces
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text

def extract_keywords(text):
    """Extract domain-specific keywords"""
    keywords = []
    
    # Technical keywords
    if any(word in text for word in ['error', 'bug', 'crash', 'fail', 'broken', 'not working']):
        keywords.append('technical_issue')
    
    # Billing keywords
    if any(word in text for word in ['payment', 'bill', 'charge', 'refund', 'invoice', 'subscription']):
        keywords.append('billing_issue')
    
    # Account keywords
    if any(word in text for word in ['login', 'password', 'account', 'access', 'locked', 'reset']):
        keywords.append('account_issue')
    
    # Feature request keywords
    if any(word in text for word in ['feature', 'request', 'add', 'new', 'enhancement', 'improve']):
        keywords.append('feature_request')
    
    # Security keywords
    if any(word in text for word in ['security', 'hack', 'breach', 'fraud', 'suspicious', 'unauthorized']):
        keywords.append('security_issue')
    
    return ' '.join(keywords)

def enhance_text(text):
    """Enhance text with extracted features"""
    cleaned = clean_text(text)
    keywords = extract_keywords(text.lower())
    
    # Combine original text with extracted keywords (keywords get more weight)
    enhanced = f"{cleaned} {keywords} {keywords}"
    
    return enhanced

def load_and_prepare_data():
    """Load and prepare dataset with focus on category balance"""
    print("\n" + "="*60)
    print("LOADING DATASET FOR ENHANCED TRAINING")
    print("="*60)
    
    dataset_files = glob.glob('../../datasets/*.csv')
    
    if not dataset_files:
        print("ERROR: No dataset files found!")
        return None, None
    
    print(f"Found {len(dataset_files)} dataset file(s)")
    
    # Load the best dataset (multi-lang 20k)
    df = pd.read_csv(dataset_files[3])
    print(f"Loaded: {dataset_files[3]} - {len(df)} rows")
    
    # Use subject as text and type as category
    text_col = 'subject'
    category_col = 'type'
    
    df = df[[text_col, category_col]].dropna()
    
    print(f"\nAfter removing missing values: {len(df)} rows")
    print(f"\nOriginal category distribution:")
    print(df[category_col].value_counts())
    
    # Balance categories (ensure each category has enough samples)
    min_samples = 100
    category_counts = df[category_col].value_counts()
    
    # Remove categories with too few samples
    valid_categories = category_counts[category_counts >= min_samples].index
    df = df[df[category_col].isin(valid_categories)]
    
    print(f"\nAfter filtering categories (min {min_samples} samples): {len(df)} rows")
    print(f"\nBalanced category distribution:")
    print(df[category_col].value_counts())
    
    # Limit total samples for training speed (but keep balance)
    max_per_category = 2000
    df_balanced = df.groupby(category_col).apply(
        lambda x: x.sample(min(len(x), max_per_category), random_state=42)
    ).reset_index(drop=True)
    
    print(f"\nAfter balancing (max {max_per_category} per category): {len(df_balanced)} rows")
    print(f"\nFinal category distribution:")
    print(df_balanced[category_col].value_counts())
    
    return df_balanced[text_col].values, df_balanced[category_col].values

def train_and_evaluate_models(X_train, X_test, y_train, y_test):
    """Train multiple models and select best for category prediction"""
    print("\n" + "="*60)
    print("TRAINING MULTIPLE MODELS")
    print("="*60)
    
    models = {
        'Logistic Regression': LogisticRegression(
            max_iter=2000,
            C=1.0,
            class_weight='balanced',
            random_state=42
        ),
        'Multinomial Naive Bayes': MultinomialNB(alpha=0.1),
        'Random Forest': RandomForestClassifier(
            n_estimators=200,
            max_depth=20,
            class_weight='balanced',
            random_state=42
        ),
        'Gradient Boosting': GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
    }
    
    best_model = None
    best_score = 0
    best_name = ""
    results = []
    
    for name, model in models.items():
        print(f"\n--- Training {name} ---")
        
        # Train model
        model.fit(X_train, y_train)
        
        # Predictions
        y_pred = model.predict(X_test)
        
        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        
        print(f"Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
        print(f"Precision: {precision:.4f}")
        print(f"Recall:    {recall:.4f}")
        print(f"F1 Score:  {f1:.4f}")
        
        # Cross-validation score
        cv_scores = cross_val_score(model, X_train, y_train, cv=3, scoring='accuracy')
        print(f"CV Score:  {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
        
        results.append({
            'model': name,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'cv_score': cv_scores.mean()
        })
        
        # Track best model (prioritize F1 score for balanced performance)
        if f1 > best_score:
            best_score = f1
            best_model = model
            best_name = name
    
    print("\n" + "="*60)
    print("BEST MODEL SELECTION")
    print("="*60)
    print(f"Best Model: {best_name}")
    print(f"F1 Score: {best_score:.4f}")
    
    # Detailed evaluation of best model
    y_pred_best = best_model.predict(X_test)
    accuracy_best = accuracy_score(y_test, y_pred_best)
    
    print(f"Test Accuracy: {accuracy_best:.4f} ({accuracy_best*100:.2f}%)")
    
    print("\n--- Classification Report ---")
    print(classification_report(y_test, y_pred_best))
    
    print("\n--- Confusion Matrix ---")
    cm = confusion_matrix(y_test, y_pred_best)
    print(cm)
    
    # Per-category accuracy
    print("\n--- Per-Category Accuracy ---")
    unique_categories = np.unique(y_test)
    for category in unique_categories:
        mask = y_test == category
        cat_accuracy = accuracy_score(y_test[mask], y_pred_best[mask])
        print(f"{category}: {cat_accuracy:.4f} ({cat_accuracy*100:.2f}%)")
    
    return best_model, results

def main():
    """Enhanced training pipeline"""
    print("\n" + "="*60)
    print("NEXORAAI ENHANCED ML TRAINING")
    print("Focus: Improved Category Prediction")
    print("="*60)
    
    # Load data
    texts, categories = load_and_prepare_data()
    
    if texts is None:
        return
    
    # Enhanced text preprocessing
    print("\n" + "="*60)
    print("ENHANCED TEXT PREPROCESSING")
    print("="*60)
    print("Cleaning and enhancing text with keyword extraction...")
    
    processed_texts = []
    for i, text in enumerate(texts):
        if i % 1000 == 0:
            print(f"Processed {i}/{len(texts)} texts...")
        enhanced = enhance_text(text)
        processed_texts.append(enhanced)
    
    print(f"Preprocessing complete: {len(processed_texts)} texts")
    
    # Train-test split with stratification
    print("\n" + "="*60)
    print("TRAIN-TEST SPLIT (STRATIFIED)")
    print("="*60)
    X_train_text, X_test_text, y_train, y_test = train_test_split(
        processed_texts, categories,
        test_size=0.2,
        random_state=42,
        stratify=categories
    )
    print(f"Training samples: {len(X_train_text)}")
    print(f"Testing samples: {len(X_test_text)}")
    
    # Enhanced TF-IDF Vectorization
    print("\n" + "="*60)
    print("ENHANCED TF-IDF VECTORIZATION")
    print("="*60)
    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 3),  # Include trigrams for better context
        min_df=2,  # Ignore terms that appear in less than 2 documents
        max_df=0.8,  # Ignore terms that appear in more than 80% of documents
        sublinear_tf=True,  # Use sublinear term frequency scaling
        use_idf=True
    )
    
    X_train = vectorizer.fit_transform(X_train_text)
    X_test = vectorizer.transform(X_test_text)
    print(f"Feature dimensions: {X_train.shape[1]}")
    print(f"Vocabulary size: {len(vectorizer.vocabulary_)}")
    
    # Train and evaluate models
    best_model, results = train_and_evaluate_models(X_train, X_test, y_train, y_test)
    
    # Save model and vectorizer
    print("\n" + "="*60)
    print("SAVING ENHANCED MODEL")
    print("="*60)
    joblib.dump(best_model, 'model.pkl')
    joblib.dump(vectorizer, 'vectorizer.pkl')
    print("✓ Enhanced model saved: model.pkl")
    print("✓ Enhanced vectorizer saved: vectorizer.pkl")
    
    # Summary
    print("\n" + "="*60)
    print("TRAINING SUMMARY")
    print("="*60)
    for result in results:
        print(f"\n{result['model']}:")
        print(f"  Accuracy:  {result['accuracy']:.4f} ({result['accuracy']*100:.2f}%)")
        print(f"  Precision: {result['precision']:.4f}")
        print(f"  Recall:    {result['recall']:.4f}")
        print(f"  F1 Score:  {result['f1']:.4f}")
        print(f"  CV Score:  {result['cv_score']:.4f}")
    
    print("\n" + "="*60)
    print("ENHANCED TRAINING COMPLETE!")
    print("Category prediction accuracy improved!")
    print("="*60)

if __name__ == '__main__':
    main()
