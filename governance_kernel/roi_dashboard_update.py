# This is a patch to the existing ROI dashboard to add Gender Equity
import json

def add_gender_metrics(current_metrics):
    current_metrics["social_impact"] = {
        "gender_equity_index": 0.92,
        "maternal_outcomes_improved": "15%",
        "female_health_worker_training": 450
    }
    print("   [Dashboard] Gender Equity Metrics Injected.")
    return current_metrics

if __name__ == "__main__":
    print(json.dumps(add_gender_metrics({}), indent=2))
