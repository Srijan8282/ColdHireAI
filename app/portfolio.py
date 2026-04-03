import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class Portfolio:
    def __init__(self, file_path="app/resource/my_portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.vectorizer = TfidfVectorizer()
        self._fitted = False

    def load_portfolio(self):
        if not self._fitted:
            self.vectorizer.fit(self.data["Techstack"].fillna(""))
            self._fitted = True

    def query_links(self, skills):
        if not skills:
            return []
        skills = [str(s).strip() for s in skills if s and str(s).strip()]
        if not skills:
            return []
        query = " ".join(skills)
        query_vec = self.vectorizer.transform([query])
        corpus_vec = self.vectorizer.transform(self.data["Techstack"].fillna(""))
        scores = cosine_similarity(query_vec, corpus_vec)[0]
        top_indices = np.argsort(scores)[::-1][:2]
        links = [{"links": self.data.iloc[i]["Links"]} for i in top_indices]
        return [links]