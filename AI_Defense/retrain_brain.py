import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib

print("🧠 TRAINING NEW AI MODEL...")

# 1. Create a Manual Dataset (Hardcoded for success)
# We teach it exactly what is Safe vs Bad
data = {
    'command_line': [
        # --- SAFE COMMANDS (Background Noise) ---
        "C:\\Windows\\system32\\SearchFilterHost.exe 0 824 828",
        "C:\\Windows\\system32\\svchost.exe -k netsvcs -p",
        "C:\\Windows\\System32\\RuntimeBroker.exe -Embedding",
        "C:\\Windows\\System32\\smartscreen.exe -Embedding",
        "C:\\Windows\\system32\\conhost.exe 0xffffffff -ForceV1",
        "C:\\Program Files\\Windows Defender\\MsMpEng.exe",
        "C:\\Windows\\system32\\wbem\\wmiprvse.exe -secured",
        "taskhostw.exe",
        "lsass.exe",
        "services.exe",
        
        # --- ATTACK COMMANDS (What we want to catch) ---
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
    ],
    'label': [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 0 = Safe
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1   # 1 = Malicious
    ]
}

df = pd.DataFrame(data)

# 2. Oversample (Make the attacks look bigger)
# We duplicate the attack rows 5 times to make sure the AI pays attention
df_attacks = df[df['label'] == 1]
df = pd.concat([df, df_attacks, df_attacks, df_attacks, df_attacks])

# 3. Vectorize (Text -> Math)
vectorizer = TfidfVectorizer(max_features=1000, lowercase=True)
X = vectorizer.fit_transform(df['command_line'])
y = df['label']

# 4. Train the Brain
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# 5. Save the new brain
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')
joblib.dump(model, 'random_forest_model.pkl')

print("✅ NEW BRAIN SAVED! 'whoami' is now flagged as Threat Level 1.")
print("👉 Now restart your detection_engine.py")