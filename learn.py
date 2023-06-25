from transformers import AutoTokenizer, DataCollatorWithPadding, AutoModelForSequenceClassification, \
    TrainingArguments, Trainer
from datasets import load_dataset, ClassLabel, load_metric
import numpy as np

c2l = ClassLabel(names=[
                     "INTJ", "INTP", "ENTJ", "ENTP", 
                     "INFJ", "INFP", "ENFJ", "ENFP",
                     "ISTJ", "ISFJ", "ESTJ", "ESFJ",
                     "ISTP", "ISFP", "ESTP", "ESFP"])

dataset_file = "dataset.csv"

dataset = load_dataset("csv", data_files=dataset_file)['train']
dataset = dataset.train_test_split(test_size=0.2)
print(dataset)

tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")


def preprocess_function(batch):
    # clean text
    tokenized = tokenizer(batch["posts"], truncation=True)
    tokenized["label"] = c2l.str2int(batch["type"])
    return tokenized


tokenized_set = dataset.map(preprocess_function, batched=True)

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=len(c2l.names))

metric = load_metric("accuracy")


def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)


training_args = TrainingArguments(
    output_dir="./results",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=5,
    weight_decay=0.01,
    save_strategy="no"
)

print(tokenized_set['train'][0])
print(tokenized_set['test'][0])

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_set["train"],
    eval_dataset=tokenized_set["test"],
    tokenizer=tokenizer,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)

trainer.train()
print("Training done")
trainer.save_model("model")
print("Model saved")
trainer.evaluate()
print("Evaluation done")
