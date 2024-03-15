import gradio as gr
from transformers import pipeline

def summarize_text(text):
    # Load pre-trained summarization pipeline
    summarization_pipeline = pipeline("summarization")

    # Generate summary
    summary = summarization_pipeline(text, max_length=100, min_length=20, do_sample=False)

    # Extract summarized text
    summarized_text = summary[0]['summary_text']

    return summarized_text

sample_text = """
Bert: Bidirectional Encoder Representations from Transformers.

In recent years, natural language processing (NLP) has seen many remarkable advancements, 
thanks to deep learning techniques. One such technique that has gained significant attention is
 the Transformer architecture. Introduced by Vaswani et al. in 2017, the Transformer model has become the foundation
   for various state-of-the-art NLP models.
One of the groundbreaking applications of the Transformer architecture is BERT
 (Bidirectional Encoder Representations from Transformers). Developed by researchers
   at Google, BERT has set new benchmarks in a wide range of NLP tasks, including
     text classification, named entity recognition, question answering, and more.
BERT's key innovation lies in its ability 
to capture bidirectional contextual information 
of words in a sentence. Unlike traditional models that process text sequentially, BERT considers the entire context of a word by leveraging attention mechanisms. This bidirectional understanding enables BERT to grasp the nuances and complexities of natural language with remarkable accuracy.
Furthermore, BERT is pre-trained on massive corpora of text data, allowing it to learn rich representations of language. Through pre-training tasks like masked language modeling and next sentence prediction, BERT acquires a deep understanding of semantic relationships within sentences.

Thanks to its effectiveness and versatility, BERT has been widely adopted in both academia and industry. Its open-source nature has led to the development of various BERT-based models tailored to specific NLP tasks and domains. Moreover, pre-trained BERT models are readily available, empowering researchers and developers to leverage state-of-the-art NLP capabilities without the need for extensive computational resources.

In conclusion, BERT represents a significant milestone in the field of natural language processing. Its bidirectional architecture, coupled with extensive pre-training, has revolutionized the way we approach NLP tasks, enabling breakthroughs in understanding, generating, and processing human language.
"""

# Summarize the sample text
summary_text = summarize_text(sample_text)

# Print the summary
print("Summary:")
print(summary_text)
