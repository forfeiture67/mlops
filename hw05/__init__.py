"""Manual and automatic experiment tracking with MLflow."""

import os

# This homework records experiments locally and does not need usage telemetry.
os.environ["MLFLOW_DISABLE_TELEMETRY"] = "true"
