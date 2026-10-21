"""Download the dataset from Hugging Face and save it as phishing_emails.csv."""
from datasets import load_dataset
import pandas as pd

ds = load_dataset("zefang-liu/phishing-email-dataset")
df = pd.DataFrame(ds["train"])
df.to_csv("phishing_emails.csv", index=False)
print(df.columns.tolist())
print(len(df), "rows saved to phishing_emails.csv")
