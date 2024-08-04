from transformers import AutoModel, AutoTokenizer, AutoModelForCausalLM, LlamaForCausalLM, LlamaTokenizerFast
from peft import PeftModel
import os
from parse_news import get_finnhub_news


def load_model_and_tokenizer(base_model, peft_model):
    # Load the tokenizer and model
    tokenizer = LlamaTokenizerFast.from_pretrained(base_model, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    model = LlamaForCausalLM.from_pretrained(base_model, trust_remote_code=True, device_map="cuda:0", load_in_8bit=True)
    model = PeftModel.from_pretrained(model, peft_model)
    model = model.eval()
    return model, tokenizer


def analyze_sentiment(model, tokenizer, text, ticker):
    # Prepare the input prompt
    prompt = f'''Instruction: What is the sentiment of this news about this ticker: {ticker}? Please choose an answer from {{negative/neutral/positive}}
Input: {text}
Answer: '''

    # Tokenize the input text
    tokens = tokenizer(prompt, return_tensors='pt', padding=True, max_length=1000)

    # Generate the response from the model
    res = model.to('cuda').generate(**tokens, max_length=1000)

    # Decode and extract the sentiment
    res_sentences = tokenizer.decode(res[0])
    sentiment = res_sentences.split("Answer: ")[1].strip()

    return sentiment


def get_finnhub_news_sentiment(ticker):
    news_info_and_sentiments = []
    base_model = "NousResearch/Llama-2-13b-hf"
    peft_model = "FinGPT/fingpt-sentiment_llama2-13b_lora"

    # Load the model and tokenizer once
    model, tokenizer = load_model_and_tokenizer(base_model, peft_model)

    # Example texts to analyze
    latest_news = get_finnhub_news(ticker)

    for news in latest_news:
        news_info_and_sentiments.append({
            'headline': news['headline'],
            'summary': news['summary'],
            'sentiment': analyze_sentiment(model, tokenizer, news['headline'] + ' ' + news['summary'], news['related'])
        })

    return news_info_and_sentiments


if __name__ == "__main__":
    print(get_finnhub_news_sentiment("AMD"))
