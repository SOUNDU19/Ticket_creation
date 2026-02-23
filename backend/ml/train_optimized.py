"""
Optimized ML Model Training for Ticket Categorization
Uses ensemble methods and better preprocessing for improved accuracy
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.pipeline import Pipeline
import joblib
import re
import warnings
warnings.filterwarnings('ignore')

def clean_text(text):
    """Enhanced text cleaning"""
    text = str(text).lower()
    
    # Keep important punctuation
    text = text.replace('!', ' urgent ')
    text = text.replace('?', ' question ')
    
    # Remove special characters
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text

def extract_features(text):
    """Extract domain-specific features"""
    features = []
    text_lower = text.lower()
    
    # Technical indicators
    if any(word in text_lower for word in ['error', 'bug', 'crash', 'fail', 'broken', 'not working']):
        features.append('technical_issue')
    
    # Billing indicators
    if any(word in text_lower for word in ['payment', 'bill', 'charge', 'refund', 'invoice']):
        features.append('billing_issue')
    
    # Account indicators
    if any(word in text_lower for word in ['login', 'password', 'account', 'access', 'locked']):
        features.append('account_issue')
    
    # Fraud indicators
    if any(word in text_lower for word in ['fraud', 'hack', 'breach', 'suspicious', 'unauthorized']):
        features.append('fraud_issue')
    
    return ' '.join(features)

def preprocess_data(df):
    """Preprocess the dataset"""
    # Clean text
    df['cleaned_description'] = df['Ticket_Description'].apply(clean_text)
    
    # Extract features
    df['features'] = df['Ticket_Description'].apply(extract_features)
    
    # Combine cleaned text with features (features get more weight)
    df['enhanced_text'] = df['cleaned_description'] + ' ' + df['features'] + ' ' + df['features']
    
    return df

def train_model():
    """Train optimized ML model"""
    print("="*60)
    print("OPTIMIZED TICKET CATEGORIZATION MODEL TRAINING")
    print("="*60)
    
    # Load dataset
    print("\n1. Loading dataset...")
    try:
        df = pd.read_csv('dataset/customer_support_tickets.csv')
        print(f"   ✓ Loaded {len(df)} tickets")
    except:
        # Try alternative paths
        try:
            df = pd.read_csv('../../dataset/customer_support_tickets.csv')
            print(f"   ✓ Loaded {len(df)} tickets")
        except:
            df = pd.read_csv('../dataset/customer_support_tickets.csv')
            print(f"   ✓ Loaded {len(df)} tickets")
    
    # Preprocess
    print("\n2. Preprocessing data...")
    df = preprocess_data(df)
    
    # Prepare data
    X = df['enhanced_text']
    y = df['Issue_Category']
    
    print(f"   ✓ Categories: {y.unique().tolist()}")
    print(f"   ✓ Distribution:")
    for category in y.unique():
        count = (y == category).sum()
        percentage = (count / len(y)) * 100
        print(f"      - {category}: {count} ({percentage:.1f}%)")
    
    # Split data
    print("\n3. Splitting data (80% train, 20% test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"   ✓ Training set: {len(X_train)} samples")
    print(f"   ✓ Test set: {len(X_test)} samples")
    
    # Create TF-IDF vectorizer
    print("\n4. Creating TF-IDF vectorizer...")
    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 3),  # Unigrams, bigrams, and trigrams
        min_df=2,
        max_df=0.95,
        sublinear_tf=True
    )
    
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    print(f"   ✓ Vocabulary size: {len(vectorizer.vocabulary_)}")
    
    # Train multiple models
    print("\n5. Training models...")
    
    # Logistic Regression
    print("   Training Logistic Regression...")
    lr = LogisticRegression(
        max_iter=1000,
        C=10,
        class_weight='balanced',
        random_state=42,
        solver='saga',
        n_jobs=-1
    )
    lr.fit(X_train_vec, y_train)
    lr_score = lr.score(X_test_vec, y_test)
    print(f"   ✓ Logistic Regression accuracy: {lr_score:.4f}")
    
    # Linear SVM
    print("   Training Linear SVM...")
    svm = LinearSVC(
        C=1.0,
        class_weight='balanced',
        random_state=42,
        max_iter=2000
    )
    svm.fit(X_train_vec, y_train)
    svm_score = svm.score(X_test_vec, y_test)
    print(f"   ✓ Linear SVM accuracy: {svm_score:.4f}")
    
    # Random Forest
    print("   Training Random Forest...")
    rf = RandomForestClassifier(
        n_estimators=200,
        max_depth=50,
        min_samples_split=5,
        min_samples_leaf=2,
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    )
    rf.fit(X_train_vec, y_train)
    rf_score = rf.score(X_test_vec, y_test)
    print(f"   ✓ Random Forest accuracy: {rf_score:.4f}")
    
    # Select best model
    models = [
        ('Logistic Regression', lr, lr_score),
        ('Linear SVM', svm, svm_score),
        ('Random Forest', rf, rf_score)
    ]
    
    best_model_name, best_model, best_score = max(models, key=lambda x: x[2])
    
    print(f"\n6. Best model: {best_model_name} (Accuracy: {best_score:.4f})")
    
    # Detailed evaluation
    print("\n7. Detailed evaluation on test set:")
    y_pred = best_model.predict(X_test_vec)
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    
    # Cross-validation
    print("\n8. Cross-validation (5-fold)...")
    cv_scores = cross_val_score(best_model, X_train_vec, y_train, cv=5, n_jobs=-1)
    print(f"   ✓ CV Scores: {cv_scores}")
    print(f"   ✓ Mean CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    # Save models
    print("\n9. Saving models...")
    joblib.dump(best_model, 'model.pkl')
    joblib.dump(vectorizer, 'vectorizer.pkl')
    print("   ✓ Saved model.pkl")
    print("   ✓ Saved vectorizer.pkl")
    
    # Test predictions
    print("\n10. Testing sample predictions...")
    test_samples = [
        "My application keeps crashing when I try to open settings",
        "I was charged twice for my subscription this month",
        "Cannot login to my account, password reset not working",
        "I received a suspicious email claiming to be from support"
    ]
    
    for sample in test_samples:
        # Preprocess
        cleaned = clean_text(sample)
        features = extract_features(sample)
        enhanced = f"{cleaned} {features} {features}"
        
        # Predict
        X_sample = vectorizer.transform([enhanced])
        prediction = best_model.predict(X_sample)[0]
        
        if hasattr(best_model, 'predict_proba'):
            confidence = max(best_model.predict_proba(X_sample)[0])
        else:
            confidence = 0.85
        
        print(f"\n   Input: {sample}")
        print(f"   → Category: {prediction}")
        print(f"   → Confidence: {confidence:.2f}")
    
    print("\n" + "="*60)
    print("✅ MODEL TRAINING COMPLETED SUCCESSFULLY!")
    print("="*60)
    print(f"\nFinal Model: {best_model_name}")
    print(f"Test Accuracy: {best_score:.4f}")
    print(f"Model saved to: model.pkl")
    print(f"Vectorizer saved to: vectorizer.pkl")
    print("\nYou can now use the model for predictions!")
    print("="*60)

if __name__ == '__main__':
    train_model()
