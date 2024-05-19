from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pandas as pd

def prepare_data(earthquakes):
    df = pd.DataFrame(earthquakes)
    df['timestamp'] = pd.to_datetime(df['time'])
    df['timestamp'] = df['timestamp'].astype(int) / 10**9
    return df[['latitude', 'longitude', 'timestamp', 'magnitude']]

def train_model(df):
    X = df[['latitude', 'longitude', 'timestamp']]
    y = df['magnitude']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

def predict(model, latitude, longitude, timestamp):
    return model.predict([[latitude, longitude, timestamp]])
