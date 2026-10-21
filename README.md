# PhishGuard: Phishing Email Detector

Scikit-learn model (TF-IDF + URL/keyword features + Logistic Regression) with a
Flask backend and an HTML/CSS/JS frontend.

## Project structure
```
app.py               Flask backend (loads model, /api/check)
features.py          URL / keyword features, red flags, advice
train_model.py       trains the model, prints accuracy, saves confusion matrix
download_data.py     downloads the dataset from Hugging Face
templates/index.html frontend (website)
requirements.txt     packages to run the website
requirements-train.txt  extra packages to train the model
```

## Run
```bash
pip install -r requirements.txt -r requirements-train.txt
python download_data.py      # creates phishing_emails.csv
python train_model.py        # creates phishing_model.pkl + tfidf.pkl
python app.py                # open http://127.0.0.1:5000
```

## Dataset
[zefang-liu/phishing-email-dataset](https://huggingface.co/datasets/zefang-liu/phishing-email-dataset)
(not included in the repo).

## Results
Add accuracy and `confusion_matrix.png` here.

Learning project only. Not 100% accurate. Never click unknown links.
