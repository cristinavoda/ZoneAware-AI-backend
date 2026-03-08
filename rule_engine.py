def evaluate_rules(distance, outside_zone, battery, reachable):
    if not reachable:
        return "critical"
    if outside_zone:
        return "high"
    if battery < 15 and distance > 5:
        return "critical"
    if distance > 6:
        return "medium"
    return "low"