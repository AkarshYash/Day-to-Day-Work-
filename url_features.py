import tldextract
import re

def extract_features(url):
    features = {}
    features['url_length'] = len(url)
    features['has_ip'] = 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0
    features['has_https'] = 1 if 'https' in url else 0
    features['has_at'] = 1 if '@' in url else 0
    ext = tldextract.extract(url)
    features['subdomain_count'] = len(ext.subdomain.split('.')) if ext.subdomain else 0
    return list(features.values())
