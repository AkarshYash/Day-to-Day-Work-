# phishing_detector.py

import pandas as pd
import re, tldextract, joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def extract_features(url):
    features = {}
    features['url_length'] = len(url)
    features['has_ip'] = 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0
    features['has_https'] = 1 if 'https' in url else 0
    features['has_at'] = 1 if '@' in url else 0
    ext = tldextract.extract(url)
    features['subdomain_count'] = len(ext.subdomain.split('.')) if ext.subdomain else 0
    return list(features.values())

def train_model():
    print("Training model...")
    data = pd.DataFrame({
        'url': [
            'http://example.com',
            'https://paypal.com',
            'http://192.168.0.1/login',
            'http://bit.ly/scam',
            'https://secure-login.com@evil.com'
        ],
        'label': [0, 0, 1, 1, 1]
    })
    data['features'] = data['url'].apply(extract_features)
    X = list(data['features'])
    y = data['label']
    model = RandomForestClassifier()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model.fit(X_train, y_train)
    print("Model accuracy:", model.score(X_test, y_test))
    return model

def main():
    model = train_model()
    while True:
        url = input("\n🔗 Enter URL to check (or 'exit'): ").strip()
        if url.lower() == "exit":
            break
        features = extract_features(url)
        result = model.predict([features])[0]
        print("⚠️ Phishing!" if result == 1 else "✅ Legit URL")

if __name__ == "__main__":
    main()
