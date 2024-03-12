import pandas as pd
import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense, AdditiveAttention

# Load data
train_df = pd.read_csv("train1.csv")
test_df = pd.read_csv("test1.csv")
val_df = pd.read_csv("validation1.csv")

# Concatenate train, test, and validation datasets for preprocessing
full_df = pd.concat([train_df, test_df, val_df], ignore_index=True)

# Tokenization for input text
tokenizer_input = Tokenizer()
tokenizer_input.fit_on_texts(full_df['article'])

# Tokenization for target summaries
tokenizer_target = Tokenizer()
tokenizer_target.fit_on_texts(train_df['highlights'])

# Pad sequences for input text
max_len_input = 121  # adjust this based on your text length distribution
train_sequences_input = tokenizer_input.texts_to_sequences(train_df['article'])
train_padded_input = pad_sequences(train_sequences_input, maxlen=max_len_input, padding='post')

# Pad sequences for target summaries
max_len_target = max(len(seq) for seq in tokenizer_target.texts_to_sequences(train_df['highlights']))
train_sequences_target = tokenizer_target.texts_to_sequences(train_df['highlights'])
train_padded_target = pad_sequences(train_sequences_target, maxlen=max_len_target, padding='post')

# Define model
model = Sequential()
model.add(Embedding(input_dim=len(tokenizer_input.word_index) + 1, output_dim=100, input_length=max_len_input))
model.add(LSTM(100, return_sequences=True))

# Output layer with the correct activation function
# Output layer with the correct activation function
model.add(Dense(len(tokenizer_target.word_index) + 1, activation='softmax'))

# Compile model with appropriate loss function
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
# Train model
model.fit(train_padded_input, train_padded_target, epochs=10, batch_size=64, validation_split=0.2)

def generate_summary(new_text):
    new_text_sequence = tokenizer_input.texts_to_sequences([new_text])
    new_text_padded = pad_sequences(new_text_sequence, maxlen=max_len_input, padding='post')
    predicted_summary_probs = model.predict(new_text_padded)[0]  # Get predictions for the first sequence in the batch
    predicted_summary_indices = [np.argmax(prob) for prob in predicted_summary_probs]
    predicted_summary_words = [word for word, index in tokenizer_target.word_index.items() if index in predicted_summary_indices]
    predicted_summary = ' '.join(predicted_summary_words)
    return predicted_summary

# Example usage
new_text = "your text goes here..."
predicted_summary = generate_summary(new_text)
print(predicted_summary)
