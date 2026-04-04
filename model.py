from sklearn.linear_model import LogisticRegression


def train_model(data, features):
    model_data = data[features + ['Target_Buy']].dropna()

    X = model_data[features]
    y = model_data['Target_Buy']

    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)

    return model


def predict_top_stocks(model, data, features):
    latest_data = data.groupby('Stock').tail(1)

    latest_data = latest_data.dropna(subset=features)

    latest_data['Buy_Prob'] = model.predict_proba(
        latest_data[features]
    )[:, 1]

    return latest_data.sort_values(by='Buy_Prob', ascending=False)