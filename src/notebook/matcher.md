---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.17.3
kernelspec:
  name: csplab-base
  display_name: CSPLab Base (pandas, numpy, matplotlib)
  language: python
---

```{code-cell} ipython3
from dotenv import load_dotenv
import os
from functools import lru_cache
import requests
import numpy as np
```

```{code-cell} ipython3
class Matcher:
    def __init__(self, model="text-embedding-3-small", cache_size=1000):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = model
        self.base_url = "https://api.openai.com/v1"

        if not self.api_key:
            raise ValueError("OpenAI API key required")

        # Cache with configurable size
        self._get_embedding = lru_cache(maxsize=cache_size)(self._get_embedding_uncached)

    def _get_embedding_uncached(self, text):
        """Get embedding from OpenRouter API (without cache)"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model,
            "input": text
        }

        response = requests.post(
            f"{self.base_url}/embeddings",
            headers=headers,
            json=data
        )

        if response.status_code == 200:
            return response.json()["data"][0]["embedding"]
        else:
            raise Exception(f"API Error: {response.status_code} - {response.text}")

    def get_embedding(self, text):
        """Get embedding (with cache)"""
        return self._get_embedding(text)

    @staticmethod
    def cosine_similarity(a, b):
        """Calculate cosine similarity between two vectors"""
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def semantic_match(self, text1, text2, start_word = None, threshold=0.8):
        """
        Compare two texts semantically

        Args:
            text1, text2: Texts to compare
            threshold: Similarity threshold (0-1)

        Returns:
            bool: True if similarity >= threshold
        """
        try:
            emb1 = self.get_embedding(text1)
            if start_word:
                text2_clean = text2.split(start_word)[-1]
                emb2 = self.get_embedding(text2_clean)
            else:
                emb2 = self.get_embedding(text2)
            similarity = self.cosine_similarity(emb1, emb2)
            return similarity >= threshold
        except Exception as e:
            print(f"Embedding error: {e}")
            return False

    def get_similarity_score(self, text1, text2, start_word = None):
        """Return similarity score (0-1)"""
        try:
            emb1 = self.get_embedding(text1)
            if start_word:
                text2_clean = text2.split(start_word)[-1]
                emb2 = self.get_embedding(text2_clean)
            else:
                emb2 = self.get_embedding(text2)
            return self.cosine_similarity(emb1, emb2)
        except Exception as e:
            print(f"Embedding error: {e}")
            return 0.0

    def sliding_window_match(self, first_chain, second_chain, threshold=0.85, window_overlap=0.5):
        """
        Find the best matching substring in descriptif using sliding window
        """
        first_words = first_chain.split()
        second_words = second_chain.split()
        window_size = len(first_words)
        best_similarity = 0.0

        for i in range(0, len(second_words) - window_size + 1):
            window_text = " ".join(second_words[i:i + window_size])
            similarity = self.get_similarity_score(first_chain, window_text)
            best_similarity = max(best_similarity, similarity)
            if best_similarity >= threshold:
                return True

        return best_similarity >= threshold

    def levenshtein_distance(self, s1, s2):
        """
        Calculate Levenshtein distance between two strings
        """
        if len(s1) < len(s2):
            return self.levenshtein_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = list(range(len(s2) + 1))
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    def levenshtein_similarity(self, s1, s2):
        """
        Calculate similarity ratio (0-1) based on Levenshtein distance
        """
        distance = self.levenshtein_distance(s1.lower(), s2.lower())
        max_len = max(len(s1), len(s2))
        if max_len == 0:
            return 1.0
        return 1 - (distance / max_len)

    def levenshtein_match(self, s1, s2, threshold=0.6):
        """
        Check if two strings match using Levenshtein similarity
        """
        return self.levenshtein_similarity(s1, s2) >= threshold

    def contains_with_levenshtein(self, s1, s2, threshold=0.7):
        """
        Check if corps_libelle is contained in descriptif using Levenshtein
        """
        # Direct comparison first
        if self.levenshtein_match(s1, s2, threshold):
            return True

        # Try sliding window with Levenshtein
        s1_words = s1.split()
        s2_words = s2.split()

        window_size = len(s1)
        best_similarity = 0.0

        for i in range(len(s2_words) - window_size + 1):
            window_text = " ".join(s2_words[i:i + window_size])
            similarity = self.levenshtein_similarity(s1, window_text)
            best_similarity = max(best_similarity, similarity)

            if best_similarity >= threshold:
                return True

        return False

    def clear_cache(self):
        """Clear the cache"""
        self._get_embedding.cache_clear()

    def cache_info(self):
        """Get cache information"""
        return self._get_embedding.cache_info()
```

```{code-cell} ipython3
matcher = Matcher()
```

```{code-cell} ipython3
corps_libelle = "agents de catégorie a des services déconcentrés de la direction générale de la concurrence, de la consommation et de la répression des fraudes"
descriptif = "Décret n° 2007-119 du 30 janvier 2007 portant statut des agents de catégorie A des services déconcentrés de la direction générale de la concurrence de la consommation et de la répression des fraudes"
matcher.get_similarity_score(corps_libelle, descriptif), matcher.get_similarity_score(corps_libelle, descriptif, "statut"), matcher.levenshtein_similarity(corps_libelle, descriptif)
```

```{code-cell} ipython3

```
