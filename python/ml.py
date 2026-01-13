from sklearn.ensemble import IsolationForest

model = IsolationForest(contamination=0.05)

features = [
    [12, 1.0, 1],  # req/min, fail ratio, ua count
    [2, 0.0, 3]
]

model.fit(features)

scores = model.predict(features)