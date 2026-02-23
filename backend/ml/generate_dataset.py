"""
Generate 10,000 additional realistic support ticket samples
"""
import pandas as pd
import random
from datetime import datetime, timedelta

# Ticket templates by category
TICKET_TEMPLATES = {
    'Technical': [
        "The {feature} is not working properly. Getting {error_type} error.",
        "Application crashes when I try to {action}. Please help urgently.",
        "Cannot {action} due to {error_type}. This is blocking my work.",
        "Getting error code {error_code} when attempting to {action}.",
        "The {feature} keeps freezing and I have to restart the app.",
        "API endpoint {endpoint} is returning {error_type}. Need immediate fix.",
        "Dashboard not loading, just showing {error_type}.",
        "Unable to {action} - system shows {error_type}.",
        "Performance issue: {feature} is extremely slow, taking {time} to load.",
        "Integration with {software} is broken. Getting {error_type}.",
        "Mobile app crashes on {device} when I {action}.",
        "Cannot upload {file_type} files. Error: {error_type}.",
        "Search functionality not working. Returns {error_type}.",
        "Export feature failing with {error_type}.",
        "Sync between devices not working. Data from {time} is missing.",
        "Notification system broken. Not receiving any {notification_type}.",
        "Cannot connect to {service}. Connection timeout error.",
        "Database query failing with {error_type}.",
        "SSL certificate error when accessing {feature}.",
        "Browser compatibility issue with {browser}. {feature} not working."
    ],
    'Billing': [
        "I was charged {amount} but my plan should be {amount}. Please refund the difference.",
        "Double charged for {service} on {date}. Need immediate refund.",
        "Subscription renewed but I cancelled it {time} ago.",
        "Cannot update payment method. Card keeps getting declined.",
        "Invoice #{invoice_number} shows wrong amount. Should be {amount} not {amount}.",
        "Charged for {service} I never subscribed to. Please investigate.",
        "Refund requested {time} ago but still not received.",
        "Billing cycle changed without notification. Why was I charged on {date}?",
        "Promo code {promo_code} not applied. Should get {discount}% discount.",
        "Upgrade to {plan} plan but still being charged for {plan} plan.",
        "Payment failed but service was suspended. I have sufficient funds.",
        "Tax calculation seems incorrect. Charged {amount} tax on {amount} purchase.",
        "Cannot download invoice for {date}. Getting {error_type}.",
        "Recurring charge of {amount} appearing but I cancelled subscription.",
        "Credit card charged {amount} more than quoted price.",
        "Annual plan charged monthly. Need to fix billing cycle.",
        "Discount not reflected in invoice. Should be {amount} not {amount}.",
        "Payment gateway error. Transaction ID: {transaction_id}.",
        "Subscription downgrade not reflected in billing.",
        "Charged in wrong currency. Should be {currency} not {currency}."
    ],
    'Account': [
        "Cannot login to my account. Password reset not working.",
        "Account locked after {number} failed login attempts. Please unlock.",
        "Two-factor authentication not working. Not receiving {method} codes.",
        "Email address change request submitted {time} ago but not processed.",
        "Profile picture not updating. Tried {number} times.",
        "Cannot delete my account. Delete button not working.",
        "Account shows as inactive but I'm actively using it.",
        "Username already taken error but that's my old username.",
        "Cannot link {social_media} account. Getting {error_type}.",
        "Password reset email not arriving. Checked spam folder.",
        "Account verification pending for {time}. When will it be completed?",
        "Cannot change email from {email} to {email}.",
        "Lost access to {method} device. Cannot pass 2FA.",
        "Account compromised. Seeing unauthorized {activity} from {location}.",
        "Cannot update phone number. System says it's already in use.",
        "Profile data not syncing across devices.",
        "Account merge request - have {number} duplicate accounts.",
        "Cannot access account settings. Page shows {error_type}.",
        "Security question reset not working.",
        "Account recovery process failing at step {number}."
    ],
    'General Inquiry': [
        "What are your support hours? Need to know for {timezone}.",
        "How do I {action}? Cannot find it in documentation.",
        "Is there a {feature} feature available?",
        "Do you offer {discount_type} discounts?",
        "What's the difference between {plan} and {plan} plans?",
        "Can I {action} without {requirement}?",
        "Where is your {location} office located?",
        "How long does {process} usually take?",
        "Is {feature} available in {region}?",
        "Can you provide a demo of {feature}?",
        "What's your refund policy for {service}?",
        "Do you integrate with {software}?",
        "Is there a mobile app for {platform}?",
        "How do I export my data to {format}?",
        "What's the maximum {limit} allowed?",
        "Can I upgrade from {plan} to {plan} mid-cycle?",
        "Do you offer training for {feature}?",
        "What's your data retention policy?",
        "Is {feature} GDPR compliant?",
        "Can I get a quote for {number} users?"
    ],
    'Fraud': [
        "Suspicious login from {location} at {time}. I didn't authorize this.",
        "Received phishing email claiming to be from support. Subject: {subject}.",
        "Unauthorized transaction of {amount} on {date}. Please investigate.",
        "Account showing activity I didn't perform. Someone accessed my {feature}.",
        "Credit card details compromised. Need to secure my account immediately.",
        "Suspicious charge from {merchant}. I never made this purchase.",
        "Someone changed my password without my knowledge.",
        "Received suspicious SMS asking for {sensitive_info}.",
        "Account accessed from {number} different locations simultaneously.",
        "Unauthorized API calls detected. IP: {ip_address}.",
        "Fake support call claiming to be from your company.",
        "Suspicious email with attachment asking to {action}.",
        "Account showing purchases I never made totaling {amount}.",
        "Someone added their payment method to my account.",
        "Received invoice for services I never ordered.",
        "Suspicious activity: {number} failed login attempts from {location}.",
        "Phishing website mimicking your login page: {url}.",
        "Unauthorized access to my {sensitive_data}.",
        "Someone is using my account to {malicious_activity}.",
        "Received call asking for verification code. Is this legitimate?"
    ]
}

# Replacement values
FEATURES = ['dashboard', 'settings', 'profile', 'reports', 'analytics', 'export', 'import', 'search', 'filter', 'notifications']
ERROR_TYPES = ['500 Internal Server Error', '404 Not Found', '403 Forbidden', 'timeout', 'connection refused', 'null pointer exception', 'undefined error']
ACTIONS = ['save changes', 'upload file', 'download report', 'export data', 'import contacts', 'share document', 'delete item', 'update profile']
ERROR_CODES = ['ERR-500', 'ERR-404', 'ERR-403', 'CODE-1001', 'ERROR-2345', 'SYS-999']
ENDPOINTS = ['/api/users', '/api/tickets', '/api/reports', '/api/analytics', '/api/export']
SOFTWARE = ['Salesforce', 'Slack', 'Microsoft Teams', 'Google Workspace', 'Zoom', 'Jira']
DEVICES = ['iPhone 14', 'Samsung Galaxy', 'iPad Pro', 'Android tablet']
FILE_TYPES = ['PDF', 'CSV', 'Excel', 'image', 'video']
SERVICES = ['Premium', 'Pro', 'Enterprise', 'Basic', 'Standard']
BROWSERS = ['Chrome', 'Firefox', 'Safari', 'Edge']
AMOUNTS = ['$9.99', '$19.99', '$49.99', '$99.99', '$199.99', '$29.99']
PLANS = ['Basic', 'Pro', 'Premium', 'Enterprise', 'Starter']
CURRENCIES = ['USD', 'EUR', 'GBP', 'CAD', 'AUD']
SOCIAL_MEDIA = ['Google', 'Facebook', 'LinkedIn', 'Twitter']
LOCATIONS = ['New York', 'London', 'Tokyo', 'Sydney', 'Mumbai', 'Berlin']
PLATFORMS = ['iOS', 'Android', 'Windows', 'Mac', 'Linux']
FORMATS = ['CSV', 'JSON', 'XML', 'PDF', 'Excel']
TIMEZONES = ['EST', 'PST', 'GMT', 'IST', 'AEST']

# Priority distribution
PRIORITY_DIST = {
    'Technical': {'Critical': 0.15, 'High': 0.35, 'Medium': 0.35, 'Low': 0.15},
    'Billing': {'Critical': 0.05, 'High': 0.30, 'Medium': 0.45, 'Low': 0.20},
    'Account': {'Critical': 0.10, 'High': 0.30, 'Medium': 0.40, 'Low': 0.20},
    'General Inquiry': {'Critical': 0.02, 'High': 0.08, 'Medium': 0.30, 'Low': 0.60},
    'Fraud': {'Critical': 0.60, 'High': 0.30, 'Medium': 0.08, 'Low': 0.02}
}

CHANNELS = ['Email', 'Chat', 'Web Form', 'Phone']
AGENTS = ['David Kim', 'Elena Rodriguez', 'Anya Sharma', 'Ben Carter', 'Chloe Adams']

def generate_ticket_description(category):
    """Generate realistic ticket description"""
    template = random.choice(TICKET_TEMPLATES[category])
    
    # Replace placeholders
    description = template
    description = description.replace('{feature}', random.choice(FEATURES))
    description = description.replace('{error_type}', random.choice(ERROR_TYPES))
    description = description.replace('{action}', random.choice(ACTIONS))
    description = description.replace('{error_code}', random.choice(ERROR_CODES))
    description = description.replace('{endpoint}', random.choice(ENDPOINTS))
    description = description.replace('{software}', random.choice(SOFTWARE))
    description = description.replace('{device}', random.choice(DEVICES))
    description = description.replace('{file_type}', random.choice(FILE_TYPES))
    description = description.replace('{service}', random.choice(SERVICES))
    description = description.replace('{browser}', random.choice(BROWSERS))
    description = description.replace('{amount}', random.choice(AMOUNTS))
    description = description.replace('{plan}', random.choice(PLANS))
    description = description.replace('{currency}', random.choice(CURRENCIES))
    description = description.replace('{social_media}', random.choice(SOCIAL_MEDIA))
    description = description.replace('{location}', random.choice(LOCATIONS))
    description = description.replace('{platform}', random.choice(PLATFORMS))
    description = description.replace('{format}', random.choice(FORMATS))
    description = description.replace('{timezone}', random.choice(TIMEZONES))
    description = description.replace('{time}', f"{random.randint(1, 48)} hours")
    description = description.replace('{date}', f"{random.randint(1, 28)}/{random.randint(1, 12)}/2024")
    description = description.replace('{number}', str(random.randint(2, 10)))
    description = description.replace('{invoice_number}', f"INV-{random.randint(10000, 99999)}")
    description = description.replace('{promo_code}', f"PROMO{random.randint(100, 999)}")
    description = description.replace('{discount}', str(random.choice([10, 15, 20, 25, 30])))
    description = description.replace('{transaction_id}', f"TXN-{random.randint(100000, 999999)}")
    description = description.replace('{email}', f"user{random.randint(1, 999)}@example.com")
    description = description.replace('{method}', random.choice(['SMS', 'email', 'authenticator app']))
    description = description.replace('{activity}', random.choice(['logins', 'purchases', 'changes']))
    description = description.replace('{requirement}', random.choice(['admin access', 'premium plan', 'verification']))
    description = description.replace('{limit}', random.choice(['users', 'storage', 'API calls']))
    description = description.replace('{subject}', f"Urgent: {random.choice(['Verify Account', 'Security Alert', 'Payment Issue'])}")
    description = description.replace('{sensitive_info}', random.choice(['password', 'credit card', 'SSN', 'verification code']))
    description = description.replace('{ip_address}', f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}")
    description = description.replace('{url}', f"https://fake-site-{random.randint(1000, 9999)}.com")
    description = description.replace('{sensitive_data}', random.choice(['contacts', 'documents', 'payment info', 'personal data']))
    description = description.replace('{malicious_activity}', random.choice(['spam', 'phishing', 'unauthorized purchases']))
    description = description.replace('{notification_type}', random.choice(['emails', 'push notifications', 'SMS alerts']))
    description = description.replace('{discount_type}', random.choice(['student', 'non-profit', 'bulk', 'annual']))
    description = description.replace('{region}', random.choice(['US', 'EU', 'Asia', 'Australia']))
    description = description.replace('{process}', random.choice(['verification', 'approval', 'processing', 'review']))
    
    return description

def generate_priority(category):
    """Generate priority based on category distribution"""
    priorities = list(PRIORITY_DIST[category].keys())
    weights = list(PRIORITY_DIST[category].values())
    return random.choices(priorities, weights=weights)[0]

def generate_tickets(num_tickets=10000):
    """Generate specified number of tickets"""
    print(f"Generating {num_tickets} new support tickets...")
    
    tickets = []
    categories = list(TICKET_TEMPLATES.keys())
    
    # Category distribution (matching existing dataset)
    category_weights = [0.30, 0.25, 0.20, 0.20, 0.05]  # Technical, Billing, Account, General, Fraud
    
    for i in range(num_tickets):
        if (i + 1) % 1000 == 0:
            print(f"  Generated {i + 1}/{num_tickets} tickets...")
        
        # Select category
        category = random.choices(categories, weights=category_weights)[0]
        
        # Generate ticket data
        ticket_id = f"TKT-{200000 + i}"
        customer_name = f"Customer {random.randint(1, 9999)}"
        customer_email = f"customer{random.randint(1, 9999)}@example.com"
        
        # Generate subject (first 50 chars of description)
        description = generate_ticket_description(category)
        subject = description[:50] + "..." if len(description) > 50 else description
        
        priority = generate_priority(category)
        channel = random.choice(CHANNELS)
        
        # Generate date (last 365 days)
        days_ago = random.randint(0, 365)
        submission_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        
        # Resolution time based on priority
        if priority == 'Critical':
            resolution_hours = random.randint(1, 12)
        elif priority == 'High':
            resolution_hours = random.randint(6, 48)
        elif priority == 'Medium':
            resolution_hours = random.randint(24, 96)
        else:
            resolution_hours = random.randint(48, 120)
        
        assigned_agent = random.choice(AGENTS)
        satisfaction_score = random.choices([1, 2, 3, 4, 5], weights=[0.05, 0.10, 0.15, 0.30, 0.40])[0]
        
        ticket = {
            'Ticket_ID': ticket_id,
            'Customer_Name': customer_name,
            'Customer_Email': customer_email,
            'Ticket_Subject': subject,
            'Ticket_Description': description,
            'Issue_Category': category,
            'Priority_Level': priority,
            'Ticket_Channel': channel,
            'Submission_Date': submission_date,
            'Resolution_Time_Hours': resolution_hours,
            'Assigned_Agent': assigned_agent,
            'Satisfaction_Score': satisfaction_score
        }
        
        tickets.append(ticket)
    
    return pd.DataFrame(tickets)

def main():
    """Main function to generate and append tickets"""
    print("="*60)
    print("GENERATING ADDITIONAL SUPPORT TICKETS")
    print("="*60)
    
    # Load existing dataset
    print("\n1. Loading existing dataset...")
    try:
        existing_df = pd.read_csv('../../dataset/customer_support_tickets.csv')
        print(f"   ✓ Loaded {len(existing_df)} existing tickets")
    except:
        try:
            existing_df = pd.read_csv('../dataset/customer_support_tickets.csv')
            print(f"   ✓ Loaded {len(existing_df)} existing tickets")
        except:
            existing_df = pd.read_csv('dataset/customer_support_tickets.csv')
            print(f"   ✓ Loaded {len(existing_df)} existing tickets")
    
    # Generate new tickets
    print("\n2. Generating 10,000 new tickets...")
    new_df = generate_tickets(10000)
    print(f"   ✓ Generated {len(new_df)} new tickets")
    
    # Combine datasets
    print("\n3. Combining datasets...")
    combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    print(f"   ✓ Total tickets: {len(combined_df)}")
    
    # Show distribution
    print("\n4. Category distribution:")
    for category in combined_df['Issue_Category'].unique():
        count = (combined_df['Issue_Category'] == category).sum()
        percentage = (count / len(combined_df)) * 100
        print(f"   - {category}: {count} ({percentage:.1f}%)")
    
    # Save combined dataset
    print("\n5. Saving combined dataset...")
    try:
        combined_df.to_csv('../../dataset/customer_support_tickets.csv', index=False)
        print("   ✓ Saved to ../../dataset/customer_support_tickets.csv")
    except:
        try:
            combined_df.to_csv('../dataset/customer_support_tickets.csv', index=False)
            print("   ✓ Saved to ../dataset/customer_support_tickets.csv")
        except:
            combined_df.to_csv('dataset/customer_support_tickets.csv', index=False)
            print("   ✓ Saved to dataset/customer_support_tickets.csv")
    
    print("\n" + "="*60)
    print("✅ DATASET EXPANSION COMPLETED!")
    print("="*60)
    print(f"\nOriginal size: {len(existing_df)} tickets")
    print(f"New tickets: {len(new_df)} tickets")
    print(f"Total size: {len(combined_df)} tickets")
    print("\nNext step: Retrain the model with the expanded dataset")
    print("Run: python train_optimized.py")
    print("="*60)

if __name__ == '__main__':
    main()
