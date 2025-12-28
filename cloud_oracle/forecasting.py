# Abstracted model training logic for multi-cloud portability

class ModelTrainer:
    def train(self, data, config):
        raise NotImplementedError

class MLflowTrainer(ModelTrainer):
    def train(self, data, config):
        # Portable ML training using MLflow
        import mlflow
        with mlflow.start_run():
            # ...training logic...
            mlflow.log_params(config)
            mlflow.log_artifact("model.pkl")
        return "mlflow://run/model"

# Usage:
# trainer = MLflowTrainer()
# model_uri = trainer.train(data, config)
