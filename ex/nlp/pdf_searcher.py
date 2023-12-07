import os
import re
import nltk
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

# # Download the NLTK stopwords if not already done
# nltk.download('stopwords')
# from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Get a list of English stopwords
# english_stop_words = set(stopwords.words('english'))


def load_stop_words(stop_word_file):
    with open(stop_word_file, 'r', encoding='utf-8') as f:
        stop_words = set([line.strip() for line in f.readlines()])
    return stop_words


# stop_words_file = './vocab.50K.en'
# # 载入停用词
# english_stop_words = load_stop_words(stop_words_file)
english_stop_words = set(ENGLISH_STOP_WORDS)
print(type(english_stop_words))
print(len(english_stop_words))
# Remove non-alphabetic characters from the filename and tokenize
def clean_and_tokenize_filename(filename):
    # Remove non-alphabetic characters
    filename = re.sub(r'[^a-zA-Z]', ' ', filename)
    # Convert to lowercase and tokenize
    words = word_tokenize(filename.lower())
    # Remove stopwords
    cleaned_words = [word for word in words if word not in english_stop_words]
    return frozenset(cleaned_words)

# Calculate the similarity between two sets of words
def calculate_similarity(set1, set2):
    return len(set1.intersection(set2)) / max(len(set1), len(set2))

# Find similar filenames
def find_similar_filenames(directory_path, similarity_threshold=0.8):
    file_tokens_dict = {}
    similar_files = []

    # Walk through the directory
    for root, _, files in os.walk(directory_path):
        for filename in files:
            if filename.lower().endswith('.pdf'):
                file_path = os.path.join(root, filename)
                # Clean and tokenize the filename
                tokens = clean_and_tokenize_filename(filename)
                # Add to the dictionary
                file_tokens_dict[file_path] = tokens
    
    # Compare files to find similar filenames
    paths = list(file_tokens_dict.keys())
    for i in range(len(paths)):
        for j in range(i + 1, len(paths)):
            similarity = calculate_similarity(file_tokens_dict[paths[i]], file_tokens_dict[paths[j]])
            if similarity >= similarity_threshold:
                similar_files.append((paths[i], paths[j]))
    
    return similar_files

directory_path = '/home/sha/Downloads/amule'

# Find similar PDF filenames
similar_filenames = find_similar_filenames(directory_path)

# Print the results
if similar_filenames:
    print("Pairs of similar filenames based on tokenized file names:")
    for file_pair in similar_filenames:
        print(file_pair[0], "<-->", file_pair[1])
else:
    print("No similar filenames found based on file names.")