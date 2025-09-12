# =============================
# Fixion AI Malware Detection Engine
# =============================

import json
from typing import List, Dict, Callable, Any

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.callbacks import Callback
import joblib
import tensorflow as tf
import os

# --------------------------
# Rule Representation Module
# --------------------------
class Rule:
    def __init__(self, name: str, condition: Callable[[Dict], bool], weight: float, action: str):
        self.name = name
        self.condition = condition
        self.weight = weight
        self.action = action

    def evaluate(self, features: Dict[str, Any]) -> Dict[str, Any]:
        matched = self.condition(features)
        return {
            'rule': self.name,
            'matched': matched,
            'weight': self.weight if matched else 0.0,
            'action': self.action if matched else None
        }

# ----------------------
# Rule Engine Management
# ----------------------
class RuleEngine:
    def __init__(self):
        self.rules: List[Rule] = []

    def add_rule(self, rule: Rule):
        self.rules.append(rule)

    def evaluate_all(self, features: Dict[str, Any]) -> Dict[str, Any]:
        results = [rule.evaluate(features) for rule in self.rules]
        total_weight = sum(r['weight'] for r in results if r['matched'])
        top_actions = list({r['action'] for r in results if r['matched'] and r['action']})
        return {
            'total_score': total_weight,
            'actions': top_actions,
            'rule_hits': [r for r in results if r['matched']]
        }

# ------------------
# Rule Definitions
# ------------------
def get_default_rules() -> List[Rule]:
    return [
        Rule("Known Malicious Hash", lambda f: f.get("file_hash") in f.get("malicious_hashes", []), 1.0, "quarantine"),
        Rule("Executes from Temp", lambda f: "temp" in f.get("file_path", "").lower(), 0.6, "sandbox"),
        Rule("Accesses System32", lambda f: "system32" in f.get("file_path", "").lower(), 0.8, "alert"),
        Rule("Uses Suspicious Port", lambda f: f.get("port") in [4444, 1337, 6666, 23, 135, 1900], 0.7, "alert"),
        Rule("Unsigned Executable", lambda f: not f.get("is_signed", True), 0.5, "alert"),
        Rule("Unusual CPU Usage", lambda f: f.get("cpu_usage", 0) > 80, 0.6, "monitor"),
        Rule("High Memory Usage", lambda f: f.get("memory_usage", 0) > 1024, 0.7, "sandbox"),
        Rule("Self Replication Detected", lambda f: f.get("creates_copies", False), 1.0, "quarantine"),
        Rule("Network Beaconing Pattern", lambda f: f.get("beaconing", False), 1.0, "alert"),
        Rule("Keylogger Behavior", lambda f: f.get("accesses_keyboard", False), 1.0, "quarantine"),
        Rule("Modifies Registry", lambda f: f.get("modifies_registry", False), 0.8, "alert"),
        Rule("Anti-Debugging Tricks Detected", lambda f: f.get("anti_debug", False), 1.0, "sandbox")
    ]

# ------------------------
# DSS Decision Module
# ------------------------
def rule_engine_decision_support(results: Dict[str, Any]) -> str:
    score = results['total_score']
    if score >= 2.0:
        return "quarantine"
    elif score >= 1.5:
        return "sandbox"
    elif score >= 1.0:
        return "alert"
    else:
        return "allow"

# ------------------------
# Autoencoder DSS Based on Anomaly and Confidence
# ------------------------
def decision_support_system(anomaly_score, confidence):
    if anomaly_score > 0.05 and confidence < 0.8:
        action = "Quarantine"
    elif anomaly_score > 0.1:
        action = "Delete"
    elif confidence > 0.95:
        action = "Log as known malware"
    else:
        action = "Monitor"
    print(f"[DSS] Action based on analysis: {action}")
    return action

# ------------------------
# Callback for AE Training
# ------------------------
class TrainingProgress(Callback):
    def on_epoch_end(self, epoch, logs=None):
        print(f"Epoch {epoch + 1}: Loss = {logs['loss']:.4f}")

# ------------------------
# Data Preparation
# ------------------------
def load_and_prepare_dataset(csv_path):
    df = pd.read_csv(csv_path)
    df = df.drop(columns=['hash'], errors='ignore')
    df['classification'] = df['classification'].astype('category').cat.codes
    X = df.drop('classification', axis=1).values
    y = df['classification'].values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return train_test_split(X_scaled, y, test_size=0.2, random_state=42), scaler

# ------------------------
# Supervised Model
# ------------------------
def train_supervised_model(X_train, y_train, X_test, y_test):
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    preds = clf.predict(X_test)
    print("\n--- Supervised Training Results ---")
    print("Accuracy:", accuracy_score(y_test, preds))
    print(classification_report(y_test, preds))
    joblib.dump(clf, "rf_hash_model.pkl")
    return clf

# ------------------------
# Autoencoder Model
# ------------------------
def create_autoencoder(input_dim):
    inp = Input(shape=(input_dim,))
    encoded = Dense(64, activation='relu')(inp)
    encoded = Dense(32, activation='relu')(encoded)
    decoded = Dense(64, activation='relu')(encoded)
    out = Dense(input_dim, activation='sigmoid')(decoded)
    model = Model(inputs=inp, outputs=out)
    model.compile(optimizer='adam', loss='mse')
    return model

def train_autoencoder_model(X_all):
    print("\n--- Training Autoencoder ---")
    autoencoder = create_autoencoder(X_all.shape[1])
    autoencoder.fit(X_all, X_all, epochs=20, batch_size=32, shuffle=True, callbacks=[TrainingProgress()])
    autoencoder.save("unsupervised_autoencoder.keras")
    return autoencoder

# ------------------------
# Main Integration
# ------------------------
def main():
    csv_path = "C:/Users/NINJA/Desktop/fixion/FixionServer/training_data/malware_dataset.csv"
    if not os.path.exists(csv_path):
        print("ERROR: Dataset not found.")
        return

    (X_train, X_test, y_train, y_test), scaler = load_and_prepare_dataset(csv_path)
    clf = train_supervised_model(X_train, y_train, X_test, y_test)
    X_all = np.vstack((X_train, X_test))
    ae = train_autoencoder_model(X_all)
    joblib.dump(scaler, "scaler.pkl")
    print("\n✅ Models and scaler saved.")

    # Rule engine setup
    engine = RuleEngine()
    for rule in get_default_rules():
        engine.add_rule(rule)

    # Simulate a test input
    test_sample = X_test[0].reshape(1, -1)
    pred = clf.predict(test_sample)[0]
    confidence = clf.predict_proba(test_sample).max()
    reconstruction = ae.predict(test_sample)
    anomaly_score = np.mean(np.power(test_sample - reconstruction, 2))
    print(f"\n[Test Sample] Prediction: {pred}, Confidence: {confidence:.2f}, Anomaly Score: {anomaly_score:.4f}")

    # DSS + Rule Engine
    decision_support_system(anomaly_score, confidence)

    # Simulated behavioral rule test input
    sample_features = {
        "file_hash": "abc123",
        "malicious_hashes": ["abc123", "def456"],
        "file_path": "C:/Users/Temp/malware.exe",
        "port": 4444,
        "is_signed": False,
        "cpu_usage": 90,
        "memory_usage": 2048,
        "creates_copies": True,
        "beaconing": True,
        "accesses_keyboard": True,
        "modifies_registry": True,
        "anti_debug": True
    }
    rule_results = engine.evaluate_all(sample_features)
    rule_action = rule_engine_decision_support(rule_results)
    print("[Rule Engine] Recommended Action:", rule_action)
    print("[Matched Rules]:")
    for hit in rule_results['rule_hits']:
        print(f" - {hit['rule']} → {hit['action']} (Weight: {hit['weight']})")

if __name__ == "__main__":
    main()
