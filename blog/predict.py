import os
import joblib
import pandas as pd
from django.conf import settings
# from prml_helper.processor import Preprocessor


class SVC_Model():
    def __init__(self):
        MODEL_FILE = os.path.join(settings.MODELS, "final_svc_2may.joblib")
        print("Loading Model...")
        self.model = joblib.load(MODEL_FILE)
        print("Loaded Model")

    def predict(self, comment_text):
        text = pd.DataFrame([comment_text], columns=["comment_text"])
        prediction = self.model.predict(text)
        return prediction
