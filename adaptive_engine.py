def detect_anomaly(distance, mean, std):
    return distance > (mean + 2 * std)