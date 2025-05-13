"""
Simplified similarity engine using only Python standard library
"""
import math
import re
from collections import defaultdict
from typing import List, Dict, Any

class SimilarityEngine:
    """Text similarity service using TF-IDF and cosine similarity"""
    
    def __init__(self):
        self.word_freq = defaultdict(int)
        self.doc_count = 0
        self.idf_cache = {}
    
    def _tokenize(self, text: str) -> List[str]:
        """Basic tokenizer - splits text into lowercase words"""
        words = re.findall(r'\w+', text.lower())
        return words
    
    def _calculate_tf(self, words: List[str]) -> Dict[str, float]:
        """Calculate term frequency for a document"""
        tf = defaultdict(float)
        total_words = len(words)
        
        for word in words:
            tf[word] += 1.0 / total_words
            
        return tf
    
    def _calculate_idf(self, word: str) -> float:
        """Calculate inverse document frequency for a word"""
        if word in self.idf_cache:
            return self.idf_cache[word]
            
        if self.word_freq[word] == 0:
            return 0.0
            
        idf = math.log(self.doc_count / self.word_freq[word])
        self.idf_cache[word] = idf
        return idf
    
    def _calculate_tfidf_vector(self, text: str) -> Dict[str, float]:
        """Calculate TF-IDF vector for a document"""
        words = self._tokenize(text)
        tf = self._calculate_tf(words)
        vector = {}
        
        for word in tf:
            vector[word] = tf[word] * self._calculate_idf(word)
            
        return vector
    
    def _cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """Calculate cosine similarity between two vectors"""
        dot_product = 0.0
        norm1 = 0.0
        norm2 = 0.0
        
        # Calculate dot product and norms
        all_words = set(vec1.keys()).union(set(vec2.keys()))
        for word in all_words:
            v1 = vec1.get(word, 0.0)
            v2 = vec2.get(word, 0.0)
            dot_product += v1 * v2
            norm1 += v1 ** 2
            norm2 += v2 ** 2
            
        norm1 = math.sqrt(norm1)
        norm2 = math.sqrt(norm2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
            
        return dot_product / (norm1 * norm2)
    
    def train(self, documents: List[str]):
        """Train the engine on a corpus of documents"""
        self.word_freq.clear()
        self.idf_cache.clear()
        self.doc_count = len(documents)
        
        for doc in documents:
            words = set(self._tokenize(doc))
            for word in words:
                self.word_freq[word] += 1
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts (0-1 scale)"""
        vec1 = self._calculate_tfidf_vector(text1)
        vec2 = self._calculate_tfidf_vector(text2)
        return self._cosine_similarity(vec1, vec2)
    
    def find_similar_policies(
        self,
        policy_text: str,
        historical_policies: List[Dict[str, Any]],
        threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """Find similar historical policies above threshold"""
        policy_vec = self._calculate_tfidf_vector(policy_text)
        results = []
        
        for policy in historical_policies:
            hist_vec = self._calculate_tfidf_vector(policy["text"])
            similarity = self._cosine_similarity(policy_vec, hist_vec)
            
            if similarity >= threshold:
                results.append({
                    "policy": policy,
                    "similarity": similarity
                })
        
        # Sort by similarity (descending)
        return sorted(results, key=lambda x: x["similarity"], reverse=True)
