import time
import joblib
import pandas as pd
from elasticsearch import Elasticsearch
from datetime import datetime

# --- CONFIGURATION ---
ES_HOST = "http://10.0.2.5:9200"  # Your Ubuntu IP
CHECK_INTERVAL = 5                # Check every 5 seconds

# 1. Load the AI Brain (Model + Vectorizer)
print("🧠 Loading AI Model...")
try:
    model = joblib.load('random_forest_model.pkl')
    vectorizer = joblib.load('tfidf_vectorizer.pkl')
    print("✅ AI Model Loaded Successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    print("Did you run the training notebook first?")
    exit()

# 2. Connect to Database
es = Elasticsearch(ES_HOST)
if es.ping():
    print(f"✅ Connected to SIEM at {ES_HOST}")
else:
    print("❌ Could not connect to SIEM. Check IP.")
    exit()

print("\n🛡️  FORENSECURECHAIN AI ENGINE IS ACTIVE")
print("🔎  Monitoring for threats... (Press Ctrl+C to stop)")

# 3. The Infinite Loop (The Heartbeat)
processed_ids = set() # Keep track of logs we've already seen

while True:
    try:
        # Ask for logs from the last 10 seconds
        query_body = {
            "query": {
                "bool": {
                    "must": [
                        {"exists": {"field": "process.command_line"}},
                        {"range": {"@timestamp": {"gte": "now-10s"}}} 
                    ]
                }
            }
        }

        # Execute Search
        response = es.search(index="winlogbeat-*", body=query_body)
        hits = response['hits']['hits']

        if len(hits) > 0:
            for hit in hits:
                log_id = hit['_id']
                
                # Skip if we already analyzed this specific log
                if log_id in processed_ids:
                    continue
                
                processed_ids.add(log_id)
                
                # Extract the command line
                cmd = hit['_source'].get('process', {}).get('command_line', "")
                
                if cmd:
                    # -- AI PREDICTION --
                    # 1. Convert text to math
                    vec = vectorizer.transform([cmd])
                    # 2. Predict (0 = Safe, 1 = Malicious)
                    pred = model.predict(vec)[0]
                    # 3. Confidence Score (Probability)
                    prob = model.predict_proba(vec).max() * 100

                    if pred == 1:
                        print("\n" + "!"*50)
                        print(f"🚨 MALWARE DETECTED! (Confidence: {prob:.1f}%)")
                        print(f"💀 Command: {cmd}")
                        print("!"*50 + "\n")
                    else:
                        # Optional: Print safe logs just so you know it's working
                        print(f"✅ Safe: {cmd[:50]}...")

        # Sleep before checking again
        time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        print("\n🛑 Stopping Engine.")
        break
    except Exception as e:
        print(f"⚠️ Error: {e}")
        time.sleep(CHECK_INTERVAL)