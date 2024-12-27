from setfit import SetFitModel, Trainer, TrainingArguments
from pprint import pprint
from datasets import load_dataset, Dataset
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    accuracy_score,
)
import os

from huggingface_hub import login
login(token=os.getenv("HF_TOKEN"))


class Train:
    def __init__(self, model_name: str, dataset_path: str):
        self.model_name = model_name
        self.model = SetFitModel.from_pretrained(self.model_name)
        self.dataset = load_dataset("csv", data_files=dataset_path)

    def compute_metrics(self, y_pred, y_test):
        if hasattr(y_pred, "cpu"):
            y_pred = y_pred.cpu().numpy()
        if hasattr(y_test, "cpu"):
            y_test = y_test.cpu().numpy()

        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average="binary")
        recall = recall_score(y_test, y_pred, average="binary")
        f1 = f1_score(y_test, y_pred, average="binary")
        return {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1,
        }

    def split_data(self):
        dataset = self.dataset["train"].class_encode_column("label")
        transformed_dataset = dataset.train_test_split(
            test_size=0.2, stratify_by_column="label"
        )
        train_dataset = transformed_dataset["train"]

        transformed_dataset = transformed_dataset["test"].train_test_split(
            test_size=0.5, stratify_by_column="label"
        )
        validation_dataset = transformed_dataset["train"]
        test_dataset = transformed_dataset["test"]
        return train_dataset, validation_dataset, test_dataset

    def train(self, train_dataset: Dataset, eval_dataset: Dataset) -> None:
        training_args = TrainingArguments(
            output_dir="checkpoints",
            sampling_strategy="unique",
            logging_strategy="steps",
            eval_strategy="steps",
            save_strategy="steps",
            load_best_model_at_end=True,
            logging_steps=20,
        )
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            metric=self.compute_metrics,
        )
        trainer.train()

        # Evaluate
        pprint(trainer.evaluate())

        # Push to the hub
        self.model.push_to_hub(repo_id='sharukat/adersim-dem-hse')

    def hyperparameter_tune(self):
        pass
