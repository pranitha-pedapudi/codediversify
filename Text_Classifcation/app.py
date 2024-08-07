from flask import Flask, request, render_template_string
import pickle
import re

app = Flask(__name__)

# Load the model and vectorizer
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('vectorizer.pkl', 'rb') as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

def remove_profanities(text):
    """
    Removes profanities from a given string.
    """
    profanities = ["damn", "fuck", "shit", "bitch", "asshole"]
    for profanity in profanities:
        text = re.sub(profanity, "*" * len(profanity), text)
    return text

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sentiment of Sentence</title>
        <style>
            body {
                background: url('https://img.freepik.com/free-photo/sunset-fog-lake_395237-229.jpg?t=st=1716014581~exp=1716018181~hmac=1b891f817458642743841545035d7fb724ac4d351a04071af4a1a35f1db8f367&w=1380') no-repeat center center fixed;
                background-size: cover;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                font-family: Arial, sans-serif;
                color: #333;
            }
            .container {
                background: rgba(255, 255, 255, 0.9);
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
                text-align: center;
            }
            h1 {
                margin-bottom: 20px;
                font-size: 24px;
            }
            form {
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            input[type="text"] {
                padding: 10px;
                margin-bottom: 15px;
                width: 300px;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 16px;
            }
            button {
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                background-color: #28a745;
                color: white;
                font-size: 16px;
                cursor: pointer;
            }
            button:hover {
                background-color: #218838;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Sentiment of Sentence</h1>
            <form action="/check" method="post">
                <label for="inputText">Enter Text:</label>
                <input type="text" id="inputText" name="inputText" required>
                <button type="submit">Check</button>
            </form>
        </div>
    </body>
    </html>
    ''')

@app.route('/check', methods=['POST'])
def check():
    input_text = request.form['inputText']

    # Preprocess the input text
    input_text = input_text.lower()
    input_text = re.sub('[^\w\s]', '', input_text)
    input_text = ' '.join([word for word in input_text.split() if word not in [
        'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", 
        "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 
        'him', 'his'
    ]])
    input_text = remove_profanities(input_text)

    # Vectorize the input text
    input_vec = vectorizer.transform([input_text])

    # Predict the classification
    prediction = model.predict(input_vec)[0]

    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sentiment of Sentence</title>
        <style>
            body {
                background: url('https://img.freepik.com/free-photo/sunset-fog-lake_395237-229.jpg?t=st=1716014581~exp=1716018181~hmac=1b891f817458642743841545035d7fb724ac4d351a04071af4a1a35f1db8f367&w=1380') no-repeat center center fixed;
                background-size: cover;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                font-family: Arial, sans-serif;
                color: #333;
            }
            .container {
                background: rgba(255, 255, 255, 0.9);
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
                text-align: center;
            }
            h1 {
                margin-bottom: 20px;
                font-size: 24px;
            }
            p {
                font-size: 18px;
            }
            a {
                display: inline-block;
                margin-top: 20px;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                background-color: #007bff;
                color: white;
                text-decoration: none;
                font-size: 16px;
                cursor: pointer;
            }
            a:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Sentiment of Sentence</h1>
            <p>The text "<strong>{{ input_text }}</strong>" is classified as: <strong>{{ prediction }}</strong></p>
            <a href="/">Go back</a>
        </div>
    </body>
    </html>
    ''', input_text=input_text, prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
