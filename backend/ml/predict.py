import joblib
import re
import os
import numpy as np

# Load model and vectorizer
MODEL_PATH = 'ml/model.pkl'
VECTORIZER_PATH = 'ml/vectorizer.pkl'

model = None
vectorizer = None

def load_models():
    """Load ML models"""
    global model, vectorizer
    
    if model is None or vectorizer is None:
        try:
            model = joblib.load(MODEL_PATH)
            vectorizer = joblib.load(VECTORIZER_PATH)
            print("✓ ML models loaded successfully")
        except Exception as e:
            print(f"✗ Error loading models: {e}")
            raise

def clean_text(text):
    """Enhanced text cleaning"""
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
    """Extract domain-specific keywords for better categorization"""
    keywords = []
    
    text_lower = text.lower()
    
    # Technical keywords
    if any(word in text_lower for word in ['error', 'bug', 'crash', 'fail', 'broken', 'not working', 'issue', 'problem']):
        keywords.append('technical_issue')
    
    # Billing keywords
    if any(word in text_lower for word in ['payment', 'bill', 'charge', 'refund', 'invoice', 'subscription', 'pricing']):
        keywords.append('billing_issue')
    
    # Account keywords
    if any(word in text_lower for word in ['login', 'password', 'account', 'access', 'locked', 'reset', 'username']):
        keywords.append('account_issue')
    
    # Feature request keywords
    if any(word in text_lower for word in ['feature', 'request', 'add', 'new', 'enhancement', 'improve', 'suggestion']):
        keywords.append('feature_request')
    
    # Security keywords
    if any(word in text_lower for word in ['security', 'hack', 'breach', 'fraud', 'suspicious', 'unauthorized']):
        keywords.append('security_issue')
    
    return ' '.join(keywords)

def preprocess_text(text):
    """Preprocess text with basic tokenization"""
    # Simple stopwords list
    stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                 'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
                 'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 
                 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that'}
    
    # Tokenize and filter
    words = text.lower().split()
    tokens = [word for word in words if word not in stopwords and len(word) > 2]
    return ' '.join(tokens)

def extract_entities(text):
    """Extract named entities using enhanced pattern matching"""
    entities = {
        'emails': [],
        'phone_numbers': [],
        'error_codes': [],
        'urls': [],
        'amounts': [],
        'dates': []
    }
    
    # Extract emails
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    entities['emails'] = list(set(re.findall(email_pattern, text)))
    
    # Extract phone numbers
    phone_pattern = r'\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}'
    entities['phone_numbers'] = list(set(re.findall(phone_pattern, text)))
    
    # Extract error codes (various patterns)
    error_patterns = [
        r'\b[A-Z]{2,}\s?-?\s?\d{3,}\b',  # ERR-500, ERROR500
        r'\berror\s?\d+\b',  # error 404
        r'\b\d{3}\s?error\b',  # 500 error
        r'\bcode\s?\d+\b'  # code 123
    ]
    error_codes = []
    for pattern in error_patterns:
        error_codes.extend(re.findall(pattern, text, re.IGNORECASE))
    entities['error_codes'] = list(set(error_codes))
    
    # Extract URLs
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    entities['urls'] = list(set(re.findall(url_pattern, text)))
    
    # Extract monetary amounts
    amount_pattern = r'\$\s?\d+(?:,\d{3})*(?:\.\d{2})?|\d+(?:,\d{3})*(?:\.\d{2})?\s?(?:dollars?|USD|EUR|GBP)'
    entities['amounts'] = list(set(re.findall(amount_pattern, text, re.IGNORECASE)))
    
    # Extract dates (simple patterns)
    date_patterns = [
        r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}',  # 12/31/2024
        r'\d{4}[/-]\d{1,2}[/-]\d{1,2}',  # 2024-12-31
        r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}'  # January 1, 2024
    ]
    dates = []
    for pattern in date_patterns:
        dates.extend(re.findall(pattern, text, re.IGNORECASE))
    entities['dates'] = list(set(dates))
    
    # Remove empty lists
    entities = {k: v for k, v in entities.items() if v}
    
    return entities

def assign_priority(category, confidence, description=""):
    """
    Enhanced priority assignment matching the trained model
    Priority Levels: Critical, High, Medium, Low
    Categories: Technical, Billing, Account, General Inquiry, Fraud
    """
    description_lower = description.lower()
    category_lower = category.lower()
    
    # CRITICAL priority keywords (most urgent)
    critical_keywords = [
        'critical', 'emergency', 'urgent', 'asap', 'immediately',
        'down', 'outage', 'system down', 'complete failure',
        'data loss', 'security breach', 'hacked', 'breach',
        'cannot access', 'total failure', 'production down'
    ]
    
    # Check for critical keywords
    if any(keyword in description_lower for keyword in critical_keywords):
        return 'critical'
    
    # Fraud category is always high priority or critical
    if 'fraud' in category_lower:
        if any(word in description_lower for word in ['unauthorized', 'suspicious', 'breach', 'hack']):
            return 'critical'
        return 'high'
    
    # HIGH priority keywords
    high_priority_keywords = [
        'error', 'bug', 'crash', 'broken', 'not working',
        'failed', 'failure', 'issue', 'problem', 'stuck',
        'cannot', 'unable', 'locked out', 'blocked'
    ]
    
    # Technical issues with error keywords
    if 'technical' in category_lower:
        if any(keyword in description_lower for keyword in high_priority_keywords):
            return 'high'
        return 'medium'
    
    # Account issues (login, access problems)
    if 'account' in category_lower:
        if any(word in description_lower for word in ['locked', 'cannot login', 'access denied', 'blocked']):
            return 'high'
        return 'medium'
    
    # Billing issues
    if 'billing' in category_lower:
        if any(word in description_lower for word in ['charged', 'refund', 'wrong amount', 'overcharged']):
            return 'high'
        return 'medium'
    
    # General Inquiry - usually low priority
    if 'general' in category_lower or 'inquiry' in category_lower:
        if any(word in description_lower for word in ['urgent', 'asap', 'immediately']):
            return 'medium'
        return 'low'
    
    # Default based on confidence
    if confidence < 0.6:
        return 'medium'  # Uncertain predictions get medium priority
    
    # Default to low priority
    return 'low'

def predict_ticket(description):
    """Predict ticket category, priority, and extract entities with enhanced accuracy"""
    try:
        # Load models if not loaded
        if model is None or vectorizer is None:
            load_models()
        
        # Enhanced preprocessing
        cleaned = clean_text(description)
        keywords = extract_keywords(description)
        
        # Combine original text with extracted keywords (keywords get more weight)
        enhanced_text = f"{cleaned} {keywords} {keywords}"
        
        # Vectorize
        X = vectorizer.transform([enhanced_text])
        
        # Predict category
        category = model.predict(X)[0]
        
        # Get confidence score
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(X)[0]
            confidence = float(max(proba))
        elif hasattr(model, 'decision_function'):
            decision = model.decision_function(X)[0]
            if len(decision.shape) > 0 and decision.shape[0] > 1:
                # Multi-class
                confidence = float(1 / (1 + np.exp(-max(decision))))
            else:
                # Binary
                confidence = float(1 / (1 + np.exp(-abs(decision))))
        else:
            confidence = 0.85  # Default confidence
        
        # Boost confidence if keywords match category
        if keywords:
            if 'technical' in keywords and any(word in category.lower() for word in ['technical', 'bug', 'issue']):
                confidence = min(confidence + 0.1, 0.99)
            elif 'billing' in keywords and 'billing' in category.lower():
                confidence = min(confidence + 0.1, 0.99)
            elif 'account' in keywords and 'account' in category.lower():
                confidence = min(confidence + 0.1, 0.99)
            elif 'feature' in keywords and 'feature' in category.lower():
                confidence = min(confidence + 0.1, 0.99)
            elif 'security' in keywords and any(word in category.lower() for word in ['security', 'fraud']):
                confidence = min(confidence + 0.1, 0.99)
        
        # Assign priority based on category and keywords
        priority = assign_priority(category, confidence, description)
        
        # Extract entities
        entities = extract_entities(description)
        
        return {
            'category': category,
            'priority': priority,
            'confidence': round(confidence, 2),
            'entities': entities
        }
    
    except Exception as e:
        print(f"Prediction error: {e}")
        import traceback
        traceback.print_exc()
        # Return default prediction
        return {
            'category': 'General Inquiry',
            'priority': 'medium',
            'confidence': 0.50,
            'entities': {}
        }

# Initialize models on import
try:
    load_models()
except:
    print("Models not yet trained. Run train.py first.")
