import pandas as pd
import re
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Load the data
df = pd.read_csv('Multeway.csv')

# Remove duplicates based on the 'Text' column
df = df.drop_duplicates(subset='Text')

# Print or save the list of removed duplicates (optional)
removed_duplicates = df.drop(df.index[df.duplicated(subset='Text')])
print("Removed duplicates:")
print(removed_duplicates)

# Convert all text to lowercase
df['Text'] = df['Text'].str.lower()

# Remove punctuation
df['Text'] = df['Text'].str.replace('[^\w\s]', '', regex=True)

# Remove stop words
stop_words = [
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", 
    "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 
    'him', 'his'
]
df['Text'] = df['Text'].apply(lambda x: ' '.join([word for word in x.split() if word not in stop_words]))

df = df.drop_duplicates()

# Remove profanities
def remove_profanities(text):
    """
    Removes profanities from a given string.
    """
    profanities = ["damn", "fuck", "shit", "bitch", "asshole"]
    for profanity in profanities:
        text = re.sub(profanity, "*" * len(profanity), text)
    return text

df['Text'] = df['Text'].apply(remove_profanities)

# Create a new column to mark records with nonsensical or incomplete text
df['Text_Quality'] = 'Good'

# Identify records with specific criteria
# Adjust the criteria to ensure sufficient data remains
df.loc[df['Text'].str.len() < 10, 'Text_Quality'] = 'Bad'

# Check the resulting counts
print(f"Total samples: {len(df)}")
print(f"Good quality samples: {len(df[df['Text_Quality'] == 'Good'])}")
print(f"Bad quality samples: {len(df[df['Text_Quality'] == 'Bad'])}")

# Separate features and target
X = df[df['Text_Quality'] == 'Good']['Text']
y = df[df['Text_Quality'] == 'Good']['Classification']

# Print the sizes of X and y
print(f"Size of X: {X.shape}")
print(f"Size of y: {y.shape}")

# Ensure X and y are not empty before splitting
if len(X) == 0 or len(y) == 0:
    raise ValueError("No data available after filtering. Please adjust your filtering criteria.")

# Split the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Vectorize the text data
vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train a Logistic Regression model
model = LogisticRegression()
model.fit(X_train_vec, y_train)

# Predict on the test set
y_pred = model.predict(X_test_vec)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

# Save the model and vectorizer
with open('model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)

with open('vectorizer.pkl', 'wb') as vectorizer_file:
    pickle.dump(vectorizer, vectorizer_file)
