import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib

print("🔥 STARTING AGGRESSIVE TRAINING...")

# 1. The Curriculum
# Safe stuff (Background noise)
safe_commands = [
    "C:\\Windows\\System32\\RuntimeBroker.exe -Embedding",
    "C:\\Windows\\system32\\SearchFilterHost.exe 0 824 828",
    "C:\\Windows\\system32\\svchost.exe -k netsvcs -p",
    "C:\\Windows\\system32\\conhost.exe 0xffffffff -ForceV1",
    "C:\\Program Files\\Windows Defender\\MsMpEng.exe",
    "taskhostw.exe",
    "lsass.exe",
    "services.exe",
    "python detection_engine.py",
    "C:\\Windows\\System32\\smartscreen.exe -Embedding"
]

# Evil stuff (Attacks)
attack_commands = [
    "whoami /priv",
    "whoami /groups",
    "whoami",
    "powershell.exe -w hidden -c",
    "powershell -nop -noni -enc",
    "net user administrator",
    "net localgroup administrators",
    "certutil -urlcache -split -f",
    "vssadmin delete shadows /all",
    "wbadmin delete catalog -quiet"
]

# 2. Build the Dataset
df_safe = pd.DataFrame({'command_line': safe_commands, 'label': 0})
df_attack = pd.DataFrame({'command_line': attack_commands, 'label': 1})

# 3. MASSIVE OVERSAMPLING
# We duplicate the attack list 100 TIMES to force the AI to respect it.
df_attack_boosted = pd.concat([df_attack] * 100, ignore_index=True)
df = pd.concat([df_safe, df_attack_boosted])

# 4. Train
print(f"📚 Training on {len(df)} examples...")
vectorizer = TfidfVectorizer(lowercase=True)
X = vectorizer.fit_transform(df['command_line'])
y = df['label']

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# 5. Save the new brain
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')
joblib.dump(model, 'random_forest_model.pkl')
print("✅ NEW BRAIN SAVED! 'whoami' is now flagged as Threat Level 1.")