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

open http://127.0.0.1:5000/

using this ip we can open our website


safe email sample detection 
<img width="1758" height="988" alt="Screenshot 2026-10-21 150935" src="https://github.com/user-attachments/assets/d1bb3c46-f7ce-4e86-bcf1-4b7a1ef3c31b" />
<img width="1737" height="956" alt="Screenshot 2026-10-21 150943" src="https://github.com/user-attachments/assets/291f1c6b-9277-4b6f-8fe4-eff1d0dbc59c" />
phishing mail sample detection
<img width="1567" height="986" alt="Screenshot 2026-10-21 150952" src="https://github.com/user-attachments/assets/c35bdf24-d1c9-4dd4-97cf-4e59bbce2f29" />
<img width="1466" height="898" alt="Screenshot 2026-10-21 150959" src="https://github.com/user-attachments/assets/9a3b3f58-bc7b-47e6-b994-0976d9c484cf" />

