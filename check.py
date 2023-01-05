# Scikit Learn
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np 
#com docs
documents = []
documents.append("Alpine snow winter boots. hello hey")
documents.append("Alpine snow winter boots.")
documents.append("Snow winter jacket.")

#com1 docs
documents1 = []
documents1.append("Alpine snow")
documents1.append("Alpine snow winter boots.")
documents1.append("Snow winter jacket.")
documents1.append("Snow skii jet race")

# Create the Document Term Matrix
count_vectorizer = CountVectorizer(stop_words='english')
count_vectorizer = CountVectorizer()
sparse_matrix = count_vectorizer.fit_transform(documents)

# Similarity between the first document (“Alpine snow winter boots”) with each of the other documents of the set:
matrix=cosine_similarity(sparse_matrix, sparse_matrix)
print(matrix)
matrix = np.asarray(matrix)
avg = matrix.mean()
print(avg)