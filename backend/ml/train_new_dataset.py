"""
Train ML Model on New Customer Support Dataset
Dataset: dataset/customer_support_tickets.csv
Categories: Technical, Billing, Account, General Inquiry, Fraud
"""

import pandas as pd
import numpy as np
import joblib
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
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
    """Extract domain-specific keywords"""
    keywords = []
    text_lower = text.lower()
    
    # Technical keywords
    if any(w in text_lower for w in ['error', 'bug', 'crash', 'fail', 'broken', 'not working', 'loading', 'sync', 'settings']):
        keywords.append('technical_issue')
    
    # Billing keywords
    if any(w in text_lower for w in ['payment', 'bill', 'charge', 'refund', 'invoice', 'subscription', 'pricing', 'plan', 'upgrade']):
        keywords.append('billing_issue')
    
    # Account keywords
    if any(w in text_lower for w in ['login', 'password', 'account', 'access', 'locked', 'reset', 'username', '2fa', 'authentication']):
        keywords.append('account_issue')
    
    # General inquiry keywords
    if any(w in text_lower for w in ['how', 'where', 'when', 'what', 'information', 'help', 'support', 'question', 'inquiry']):
        keywords.append('general_inquiry')
    
    # Fraud/Security keywords
    if any(w in text_lower for w in ['fraud', 'security', 'hack', 'breach', 'suspicious', 'unauthorized', 'scam']):
        keywords.append('fraud_security')
    
    return ' '.join(keywords)

def enhance_text(subject, description):
    """Combine and enhance subject and description"""
    # Subject is usually more important, so give it more weight
    subject_clean = clean_text(subject)
    desc_clean = clean_text(description)
    keywords = extract_keywords(f"{subject} {description}")
    
    # Combine: subject (3x weight) + description + keywords (2x weight)
    enhanced = f"{subject_clean} {subject_clean} {subject_clean} {desc_clean} {keywords} {keywords}"
    
    return enhanced

def main():
    print("\n" + "="*70)
    print("NEXORAAI ML TRAINING - NEW CUSTOMER SUPPORT DATASET")
    print("="*70)
    
    # Load dataset
    print("\n📂 Loading dataset...")
    df = pd.read_csv('../../dataset/customer_support_tickets.csv')
    
    print(f"✓ Loaded {len(df)} tickets")
    print(f"\n📊 Dataset columns: {df.columns.tolist()}")
    
    # Check for required columns
    required_cols = ['Ticket_Subject', 'Ticket_Description', 'Issue_Category']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        print(f"\n❌ ERROR: Missing columns: {missing_cols}")
        return
    
    # Remove missing values
    df = df[required_cols].dropna()
    print(f"\n✓ After removing missing values: {len(df)} tickets")
    
    # Show category distribution
    print(f"\n📈 Category Distribution:")
    category_counts = df['Issue_Category'].value_counts()
    for category, count in category_counts.items():
        percentage = (count / len(df)) * 100
        print(f"   {category:20s}: {count:5d} ({percentage:5.2f}%)")
    
    # Balance categories (optional - limit max per category)
    max_per_category = 5000
    df_balanced = df.groupby('Issue_Category').apply(
        lambda x: x.sample(min(len(x), max_per_category), random_state=42)
    ).reset_index(drop=True)
    
    if len(df_balanced) < len(df):
        print(f"\n⚖️  Balanced to {len(df_balanced)} tickets (max {max_per_category} per category)")
        print(f"\n📈 Balanced Distribution:")
        for category, count in df_balanced['Issue_Category'].value_counts().items():
            percentage = (count / len(df_balanced)) * 100
            print(f"   {category:20s}: {count:5d} ({percentage:5.2f}%)")
    
    # Preprocess text
    print(f"\n🔄 Preprocessing text...")
    texts = []
    for idx, row in df_balanced.iterrows():
        if idx % 2000 == 0:
            print(f"   Processed {idx}/{len(df_balanced)} tickets...")
        enhanced = enhance_text(row['Ticket_Subject'], row['Ticket_Description'])
        texts.append(enhanced)
    
    categories = df_balanced['Issue_Category'].values
    print(f"✓ Preprocessing complete: {len(texts)} tickets")
    
    # Train-test split
    print(f"\n✂️  Splitting data...")
    X_train_text, X_test_text, y_train, y_test = train_test_split(
        texts, categories,
        test_size=0.2,
        random_state=42,
        stratify=categories
    )
    
    print(f"   Training set: {len(X_train_text)} tickets")
    print(f"   Testing set:  {len(X_test_text)} tickets")
    
    # TF-IDF Vectorization
    print(f"\n🔢 Creating TF-IDF features...")
    vectorizer = TfidfVectorizer(
        max_features=8000,      # More features for better accuracy
        ngram_range=(1, 3),     # Unigrams, bigrams, trigrams
        min_df=2,               # Ignore rare terms
        max_df=0.8,             # Ignore very common terms
        sublinear_tf=True,      # Use log scaling
        strip_accents='unicode'
    )
    
    X_train = vectorizer.fit_transform(X_train_text)
    X_test = vectorizer.transform(X_test_text)
    
    print(f"✓ Feature dimensions: {X_train.shape[1]}")
    print(f"✓ Vocabulary size: {len(vectorizer.vocabulary_)}")
    
    # Train model
    print(f"\n🤖 Training Logistic Regression model...")
    model = LogisticRegression(
        max_iter=2000,
        C=1.0,                  # Regularization strength
        class_weight='balanced', # Handle class imbalance
        solver='lbfgs',
        random_state=42,
        n_jobs=-1,              # Use all CPU cores
        verbose=0
    )
    
    model.fit(X_train, y_train)
    print(f"✓ Training complete!")
    
    # Evaluate on test set
    print(f"\n📊 Evaluating model...")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n{'='*70}")
    print(f"🎯 OVERALL ACCURACY: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"{'='*70}")
    
    # Detailed classification report
    print(f"\n📋 Classification Report:")
    print(classification_report(y_test, y_pred, digits=4))
    
    # Per-category accuracy
    print(f"\n📊 Per-Category Accuracy:")
    unique_categories = np.unique(y_test)
    for category in sorted(unique_categories):
        mask = y_test == category
        cat_accuracy = accuracy_score(y_test[mask], y_pred[mask])
        cat_count = mask.sum()
        print(f"   {category:20s}: {cat_accuracy:.4f} ({cat_accuracy*100:.2f}%) - {cat_count} samples")
    
    # Confusion matrix
    print(f"\n🔍 Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred, labels=sorted(unique_categories))
    print(f"\n   Categories: {sorted(unique_categories)}")
    print(cm)
    
    # Save model and vectorizer
    print(f"\n💾 Saving model...")
    joblib.dump(model, 'model.pkl')
    joblib.dump(vectorizer, 'vectorizer.pkl')
    
    print(f"\n{'='*70}")
    print(f"✅ TRAINING COMPLETE!")
    print(f"{'='*70}")
    print(f"✓ Model saved: model.pkl")
    print(f"✓ Vectorizer saved: vectorizer.pkl")
    print(f"✓ Final Accuracy: {accuracy*100:.2f}%")
    print(f"✓ Categories: {', '.join(sorted(unique_categories))}")
    print(f"{'='*70}\n")

if __name__ == '__main__':
    main()
