# Helm chart placeholder template
HELM_TEMPLATE = """
apiVersion: v2
name: iluminaracore
description: iLuminara-Core deployment chart
type: application
"""
with open("deployment/Chart.yaml","w") as f:
    f.write(HELM_TEMPLATE)
