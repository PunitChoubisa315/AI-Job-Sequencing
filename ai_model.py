import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# Historical data
data = pd.read_csv("data.csv")

# AI input
X = data[["M1", "M2"]]

# AI target
y = data["Total_Time"]

# Create AI model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

# Train model
model.fit(X, y)


def predict_job_score(m1, m2):

    input_data = pd.DataFrame(
        [[m1, m2]],
        columns=["M1", "M2"]
    )

    prediction = model.predict(input_data)

    return round(prediction[0], 2)


print("AI Model trained successfully!")

print(
    "Test Prediction:",
    predict_job_score(6, 5)
)