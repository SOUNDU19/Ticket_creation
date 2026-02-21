import pandas as pd
import numpy as np
import spacy
import joblib
import re
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import warnings
warnings.filterwarnings('ignore')

# Load spaCy model
print("Loading spaCy model...")
nlp = spacy.load('en_core_web_sm')

def clean_text(text):
    """Clean and preprocess text"""
    if pd.isna(text):
        return ""
    
    # Convert to lowercase
    text = str(text).lower()
    
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text

def preprocess_text(text):
    """Preprocess text using spaCy"""
    doc = nlp(text)
    
    # Lemmatize and remove stopwords
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and len(token.text) > 2]
    
    return ' '.join(tokens)

def load_and_prepare_data():
    """Load and prepare dataset"""
    print("\n" + "="*60)
    print("LOADING DATASET")
    print("="*60)
    
    # Try to load datasets from the datasets folder
    import os
    import glob
    
    dataset_files = glob.glob('../../datasets/*.csv')
    
    if not dataset_files:
        print("ERROR: No dataset files found in datasets folder!")
        return None, None
    
    print(f"Found {len(dataset_files)} dataset file(s)")
    
    # Load all datasets and combine
    dfs = []
    for file in dataset_files:
        try:
            df = pd.read_csv(file)
            print(f"Loaded: {file} - {len(df)} rows")
            dfs.append(df)
        except Exception as e:
            print(f"Error loading {file}: {e}")
    
    if not dfs:
        print("ERROR: Could not load any datasets!")
        return None, None
    
    # Combine all datasets
    df = pd.concat(dfs, ignore_index=True)
    print(f"\nTotal combined rows: {len(df)}")
    
    # Limit to 40k samples for faster training
    if len(df) > 40000:
        df = df.sample(n=40000, random_state=42)
        print(f"Sampled down to: {len(df)} rows for faster training")
    
    print(f"Columns: {df.columns.tolist()}")
    
    # Identify text and category columns
    text_col = None
    category_col = None
    
    # Common column name patterns
    text_patterns = ['description', 'text', 'issue', 'ticket', 'message', 'content', 'body', 'subject']
    category_patterns = ['category', 'label', 'class', 'type', 'queue']
    
    for col in df.columns:
        col_lower = col.lower()
        if not text_col and any(pattern in col_lower for pattern in text_patterns):
            text_col = col
        if not category_col and any(pattern in col_lower for pattern in category_patterns):
            category_col = col
    
    if not text_col or not category_col:
        print(f"\nERROR: Could not identify text and category columns!")
        print(f"Available columns: {df.columns.tolist()}")
        print("\nUsing first two columns as fallback...")
        text_col = df.columns[0]
        category_col = df.columns[1]
    
    print(f"\nUsing columns:")
    print(f"  Text: {text_col}")
    print(f"  Category: {category_col}")
    
    # Remove missing values
    df = df[[text_col, category_col]].dropna()
    
    print(f"\nAfter removing missing values: {len(df)} rows")
    print(f"\nCategory distribution:")
    print(df[category_col].value_counts())
    
    return df[text_col].values, df[category_col].values

def train_models(X_train, X_test, y_train, y_test):
    """Train multiple models and select the best"""
    print("\n" + "="*60)
    print("TRAINING MODELS")
    print("="*60)
    
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Linear SVM': LinearSVC(max_iter=2000, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42)
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
        
        print(f"Accuracy:  {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall:    {recall:.4f}")
        print(f"F1 Score:  {f1:.4f}")
        
        results.append({
            'model': name,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1
        })
        
        # Track best model
        if accuracy > best_score:
            best_score = accuracy
            best_model = model
            best_name = name
    
    print("\n" + "="*60)
    print("BEST MODEL SELECTION")
    print("="*60)
    print(f"Best Model: {best_name}")
    print(f"Accuracy: {best_score:.4f}")
    
    # Detailed evaluation of best model
    y_pred_best = best_model.predict(X_test)
    
    print("\n--- Classification Report ---")
    print(classification_report(y_test, y_pred_best))
    
    print("\n--- Confusion Matrix ---")
    cm = confusion_matrix(y_test, y_pred_best)
    print(cm)
    
    return best_model, results

def main():
    """Main training pipeline"""
    print("\n" + "="*60)
    print("NEXORAAI ML TRAINING PIPELINE")
    print("="*60)
    
    # Load data
    texts, categories = load_and_prepare_data()
    
    if texts is None:
        return
    
    # Text preprocessing
    print("\n" + "="*60)
    print("TEXT PREPROCESSING")
    print("="*60)
    print("Cleaning and preprocessing text...")
    
    processed_texts = []
    for i, text in enumerate(texts):
        if i % 1000 == 0:
            print(f"Processed {i}/{len(texts)} texts...")
        cleaned = clean_text(text)
        processed = preprocess_text(cleaned)
        processed_texts.append(processed)
    
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
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    X_train = vectorizer.fit_transform(X_train_text)
    X_test = vectorizer.transform(X_test_text)
    print(f"Feature dimensions: {X_train.shape[1]}")
    
    # Train models
    best_model, results = train_models(X_train, X_test, y_train, y_test)
    
    # Save model and vectorizer
    print("\n" + "="*60)
    print("SAVING MODEL")
    print("="*60)
    joblib.dump(best_model, 'model.pkl')
    joblib.dump(vectorizer, 'vectorizer.pkl')
    print("✓ Model saved: model.pkl")
    print("✓ Vectorizer saved: vectorizer.pkl")
    
    # Summary
    print("\n" + "="*60)
    print("TRAINING SUMMARY")
    print("="*60)
    for result in results:
        print(f"\n{result['model']}:")
        print(f"  Accuracy:  {result['accuracy']:.4f}")
        print(f"  Precision: {result['precision']:.4f}")
        print(f"  Recall:    {result['recall']:.4f}")
        print(f"  F1 Score:  {result['f1']:.4f}")
    
    print("\n" + "="*60)
    print("TRAINING COMPLETE!")
    print("="*60)

if __name__ == '__main__':
    main()
