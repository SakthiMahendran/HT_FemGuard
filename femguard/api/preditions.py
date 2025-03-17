import torch
import numpy as np
import random
import torch.nn as nn
import joblib
from sklearn.preprocessing import StandardScaler, LabelEncoder
import warnings

# Suppress version mismatch warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Try to load preprocessing objects, but if missing, create them
try:
    scaler = joblib.load("scaler.pkl")
    label_encoders = joblib.load("label_encoders.pkl")
    y_encoder = joblib.load("y_encoder.pkl")
    print("Loaded existing scaler and encoders.")
except:
    print("Warning: Scaler or encoders not found! Creating new ones dynamically.")
    scaler = StandardScaler()
    label_encoders = {}
    y_encoder = LabelEncoder()

# Define Neural Network Model
class RiskSafetyNN(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(RiskSafetyNN, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.dropout1 = nn.Dropout(0.3)
        self.fc2 = nn.Linear(128, 64)
        self.dropout2 = nn.Dropout(0.3)
        self.fc3 = nn.Linear(64, 32)
        self.dropout3 = nn.Dropout(0.3)
        self.fc4 = nn.Linear(32, output_dim)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.dropout1(x)
        x = self.relu(self.fc2(x))
        x = self.dropout2(x)
        x = self.relu(self.fc3(x))
        x = self.dropout3(x)
        x = self.fc4(x)
        return x

# Load trained model
model_path = "risk_safety_nn.pth"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

checkpoint = torch.load(model_path, map_location=device)

# Adjust input/output dimensions dynamically
input_dim = checkpoint["fc1.weight"].shape[1]
output_dim = checkpoint["fc4.weight"].shape[0]

model = RiskSafetyNN(input_dim, output_dim).to(device)
model.load_state_dict(checkpoint)
model.eval()

class RiskSafetyPredictor:
    def __init__(self, model, scaler, label_encoders, y_encoder, device):
        self.model = model
        self.scaler = scaler
        self.label_encoders = label_encoders
        self.y_encoder = y_encoder
        self.device = device

    def _generate_random_features(self, expected_count):
        """Generate random values if not enough features are provided."""
        return [random.uniform(-1, 1) for _ in range(expected_count)]

    def predict(self, latitude, longitude):
        """Predict safety rating based on latitude, longitude, and missing features filled randomly."""
        # Construct feature array
        features = [latitude, longitude]

        # Ensure the feature length matches expected count
        expected_features = scaler.n_features_in_ if hasattr(scaler, "n_features_in_") else input_dim
        missing_count = expected_features - len(features)

        if missing_count > 0:
            print(f"Warning: Missing {missing_count} features, filling with random values.")
            features.extend(self._generate_random_features(missing_count))
        elif missing_count < 0:
            print(f"Warning: Too many features provided! Truncating extra {abs(missing_count)} features.")
            features = features[:expected_features]

        # Standardize numerical features
        features = np.array([features])
        features = scaler.transform(features)
        features_tensor = torch.tensor(features, dtype=torch.float32).to(self.device)

        # Make prediction
        with torch.no_grad():
            outputs = self.model(features_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1).cpu().numpy()
            predicted_class = np.argmax(probabilities, axis=1)[0]
            confidence_score = np.max(probabilities, axis=1)[0]

        # Decode prediction
        predicted_label = self.y_encoder.inverse_transform([predicted_class])[0] if hasattr(y_encoder, "inverse_transform") else str(predicted_class)

        return {
            "Predicted Safety Rating": predicted_label,
            "Confidence Score": confidence_score
        }

# Initialize predictor
predictor = RiskSafetyPredictor(model, scaler, label_encoders, y_encoder, device)

# # Example prediction
# test_latitude = 12.9716
# test_longitude = 77.5946
# prediction = predictor.predict(test_latitude, test_longitude)
# print("Prediction:", prediction)
