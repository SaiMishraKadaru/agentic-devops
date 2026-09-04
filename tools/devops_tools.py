def get_deployment_status():
    """Return the current status of the payment-api deployment."""

    return {
        "deployment": "payment-api",
        "status": "failed",
        "pod": "payment-api-7d8f9c",
        "reason": "CrashLoopBackOff"

        }

def get_deployment_logs():
    """Return simulated logs from the payment-api deployment."""

    return {
        "deployment": "payment-api",
        "pod": "payment-api-7d8f9c",
        "logs": [
            "Starting payment-api...",
            "Loading configuration...",
            "Connecting to database...",
            "ERROR: connection refused to database at db.internal:5432",
            "Application terminated."
        ]
    }
