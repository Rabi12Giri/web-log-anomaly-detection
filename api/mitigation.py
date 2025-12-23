# mitigation.py
# Rule-based mitigation recommendation engine (human-in-the-loop)

def assess_severity(anomaly):
    """
    Assigns a severity level based on anomaly indicators.
    """
    if anomaly.get("error_rate", 0) > 0.4 or anomaly.get("total_requests", 0) > 1500:
        return "HIGH"
    if anomaly.get("error_rate", 0) > 0.2 or anomaly.get("total_requests", 0) > 700:
        return "MEDIUM"
    return "LOW"


def suggest_mitigation(anomaly):
    """
    Generates mitigation recommendations for detected anomalies.
    """
    actions = []

    if anomaly.get("total_requests", 0) > 1000:
        actions.append("Apply rate limiting or temporary IP throttling")

    if anomaly.get("error_rate", 0) > 0.3:
        actions.append("Investigate HTTP errors – possible probing or exploit attempts")

    if anomaly.get("unique_urls", 0) > 200:
        actions.append("Inspect for automated crawling or brute-force behavior")

    if not actions:
        actions.append("Monitor activity – no immediate mitigation required")

    return actions
