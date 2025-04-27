# Summarize fetched news articles
import os 
# import torch
# from transformers import (
#     AutoTokenizer,
#     AutoModelForCausalLM,
#     pipeline,
# )
from llama_cpp import Llama

# Load the model and tokenizer
LOCAL_MODEL = os.getenv("SUMMARIZER_MODEL_PATH")

# tokenizer = AutoTokenizer.from_pretrained(LOCAL_MODEL)
# model = AutoModelForCausalLM.from_pretrained(
#     LOCAL_MODEL,
#     torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
#     device_map="auto",
#     low_cpu_mem_usage=True, 
# )

# generator = pipeline(
#     "text-generation",
#     model=model,
#     tokenizer=tokenizer,
#     max_new_tokens=512,
#     do_sample=True, # Determines if the model should sample or not
#     temperature=0.7, # Controls the randomness of predictions
# )

# initialize once
llm = Llama(
    model_path=LOCAL_MODEL,
    n_ctx=1024, # adjustable
    n_threads=os.cpu_count(), # tune for CPU
    n_batch=32,
    n_gpu_layers=30,
    low_cpu_mem_usage=True,
)

def summarize_article(text: str, max_length: int=100) -> str:
    """
    Summarize the text using a local model.
    Args:
        text (str): The text to summarize.
        max_length (int): The maximum length of the summary.
    Returns:
        str: The summarized text.
    """
    prompt = (
        "Summarize the following news content in 2-3 sentences:\n\n"
        f"{text}\n\nSummary:"
    )

    ## If using transformers
    # out = generator(
    #     prompt,
    #     max_length=max_length,
    #     truncation=True,
    # )
    # # Remove the prompt from the generated text
    # generated_text = out[0]['generated_text']
    # summary = generated_text.split("Summary:")[-1].strip()

    # Is using Llama
    resp = llm(
        prompt=prompt,
        max_tokens=max_length,
        echo=False,
    )
    # print(resp)
    return resp["choices"][0]["text"]

if __name__ == "__main__":
    # Example usage
    text = (
        "In a groundbreaking study, scientists have discovered a new species of "
        "dinosaur that roamed the Earth 100 million years ago. The fossilized "
        "remains were found in a remote area of Argentina, and researchers believe "
        "this species could provide new insights into the evolution of dinosaurs."
    )
    summary = summarize_article(text)
    print("Summary:", summary)
    