"""
Ultra-optimized text embedding service using Python standard library
with caching, batch processing, and pre-computed embeddings support.
"""
import math
import re
from collections import defaultdict
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from functools import lru_cache
from time import perf_counter

@dataclass(frozen=True)
class TextEmbedding:
    """Immutable container for text embedding results with hash support"""
    tokens: Tuple[str]  # Using tuple for immutability/hashing
    vector: Dict[str, float]
    norm: float

    def __post_init__(self):
        # Convert tokens to tuple for immutability
        object.__setattr__(self, 'tokens', tuple(self.tokens))

class EmbeddingService:
    """High-performance embedding service with advanced optimizations"""
    
    def __init__(self, cache_size: int = 2048):
        """
        Initialize with enhanced caching and performance tracking
        
        Args:
            cache_size: Size of LRU cache (default 2048 embeddings)
        """
        self.word_freq = defaultdict(int)
        self.doc_count = 0
        self.idf_cache = {}
        self._stats = {
            'cache_hits': 0,
            'cache_misses': 0,
            'total_embeddings': 0,
            'batch_processing_count': 0
        }
        
        # Create cached version with frozen dataclass for better cache performance
        self._get_embedding_cached = lru_cache(maxsize=cache_size)(self._get_embedding_raw)

    def get_stats(self) -> Dict[str, int]:
        """Get current performance statistics"""
        return self._stats.copy()

    def _tokenize(self, text: str) -> List[str]:
        """Optimized tokenizer with pre-compiled regex"""
        if not hasattr(self, '_tokenize_re'):
            self._tokenize_re = re.compile(r'\w+')
        return self._tokenize_re.findall(text.lower())

    def _calculate_tf(self, words: List[str]) -> Dict[str, float]:
        """Optimized term frequency calculation"""
        tf = defaultdict(float)
        total_words = len(words)
        inv_total = 1.0 / total_words
        
        for word in words:
            tf[word] += inv_total
            
        return tf

    def _calculate_idf(self, word: str) -> float:
        """IDF calculation with optimized caching"""
        if word in self.idf_cache:
            return self.idf_cache[word]
            
        freq = self.word_freq[word]
        if freq == 0:
            return 0.0
            
        idf = math.log(self.doc_count / freq)
        self.idf_cache[word] = idf
        return idf

    def _get_embedding_raw(self, text: str) -> TextEmbedding:
        """Core embedding generation with performance tracking"""
        words = self._tokenize(text)
        tf = self._calculate_tf(words)
        vector = {}
        norm_sq = 0.0
        
        for word in tf:
            tfidf = tf[word] * self._calculate_idf(word)
            vector[word] = tfidf
            norm_sq += tfidf ** 2
        
        self._stats['total_embeddings'] += 1
        return TextEmbedding(
            tokens=words,
            vector=vector,
            norm=math.sqrt(norm_sq)
        )

    def get_embedding(self, text: str) -> TextEmbedding:
        """
        Get embedding with caching and stats tracking
        
        Args:
            text: Input text to embed
            
        Returns:
            TextEmbedding object
        """
        result = self._get_embedding_cached(text)
        if result is self._get_embedding_raw(text):
            self._stats['cache_misses'] += 1
        else:
            self._stats['cache_hits'] += 1
        return result

    def get_embeddings_batch(self, texts: List[str]) -> List[TextEmbedding]:
        """
        Batch process texts with optimized memory handling
        
        Args:
            texts: List of texts to process
            
        Returns:
            List of TextEmbedding objects
        """
        self._stats['batch_processing_count'] += 1
        return [self.get_embedding(text) for text in texts]

    def calculate_similarity(self, 
                          embedding1: TextEmbedding, 
                          embedding2: TextEmbedding) -> float:
        """
        Optimized cosine similarity calculation
        
        Args:
            embedding1: First embedding
            embedding2: Second embedding
            
        Returns:
            Similarity score (0-1)
        """
        if embedding1.norm == 0 or embedding2.norm == 0:
            return 0.0
            
        # Optimize by processing the smaller vector first
        vec1, vec2 = (embedding1.vector, embedding2.vector) 
        if len(vec2) < len(vec1):
            vec1, vec2 = vec2, vec1
            
        dot_product = 0.0
        for word in vec1:
            dot_product += vec1[word] * vec2.get(word, 0.0)
            
        return dot_product / (embedding1.norm * embedding2.norm)

    def find_similar_policies(
        self,
        policy_text: str,
        historical_policies: List[Dict[str, Any]],
        threshold: float = 0.5,
        pre_computed_embeddings: Optional[Dict[str, TextEmbedding]] = None,
        batch_size: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Ultra-optimized policy similarity search with batching
        
        Args:
            policy_text: Query policy text
            historical_policies: List of policies to compare against
            threshold: Minimum similarity score (0-1)
            pre_computed_embeddings: Optional pre-computed embeddings
            batch_size: Number of policies to process at once
            
        Returns:
            List of similar policies with scores, sorted descending
        """
        start_time = perf_counter()
        policy_embedding = self.get_embedding(policy_text)
        results = []
        
        if pre_computed_embeddings:
            # Use pre-computed embeddings if available
            for policy in historical_policies:
                text = policy["text"]
                if text in pre_computed_embeddings:
                    similarity = self.calculate_similarity(
                        policy_embedding,
                        pre_computed_embeddings[text]
                    )
                    if similarity >= threshold:
                        results.append({
                            "policy": policy,
                            "similarity": similarity
                        })
        else:
            # Process in batches for better performance
            for i in range(0, len(historical_policies), batch_size):
                batch = historical_policies[i:i + batch_size]
                batch_texts = [p["text"] for p in batch]
                batch_embeddings = self.get_embeddings_batch(batch_texts)
                
                for j, policy in enumerate(batch):
                    similarity = self.calculate_similarity(
                        policy_embedding,
                        batch_embeddings[j]
                    )
                    if similarity >= threshold:
                        results.append({
                            "policy": policy,
                            "similarity": similarity
                        })
        
        # Sort results by similarity (descending)
        results.sort(key=lambda x: x["similarity"], reverse=True)
        
        self._stats['last_query_time'] = perf_counter() - start_time
        return results

    def pre_compute_embeddings(self, 
                             texts: List[str],
                             batch_size: int = 100) -> Dict[str, TextEmbedding]:
        """
        Efficient pre-computation of embeddings with batching
        
        Args:
            texts: List of texts to pre-compute
            batch_size: Number of texts to process at once
            
        Returns:
            Dictionary mapping text to embeddings
        """
        embeddings = {}
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_results = self.get_embeddings_batch(batch)
            for text, embedding in zip(batch, batch_results):
                embeddings[text] = embedding
        return embeddings

    def train(self, documents: List[str]):
        """Train on document corpus with frequency tracking"""
        self.word_freq.clear()
        self.idf_cache.clear()
        self.doc_count = len(documents)
        
        for doc in documents:
            words = set(self._tokenize(doc))
            for word in words:
                self.word_freq[word] += 1
