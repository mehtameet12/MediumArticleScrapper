import json
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

def combine_text_content(json_data):
    combined_text = ""
    for section in json_data['content']:
        for content in section['content']:
            if 'text' in content:
                combined_text += content['text'] + " "
    return combined_text.strip()

def analyze_sentiment(text, nlp):
    doc = nlp(text)
    polarity = doc._.polarity
    if polarity > 0:
        return "positive"
    elif polarity < 0:
        return "negative"
    else:
        return "neutral"

def transform_structure(json_data, nlp):
    transformed_data = {
        "article_title": json_data["title"],
        "article_url": json_data["url"],
        "author": json_data["author"],
        "published_date": json_data["date"],
        "content": combine_text_content(json_data),
        "comments": []
    }
    
    for comment in json_data["comments"]:
        sentiment = analyze_sentiment(comment["comment_text"], nlp)
        transformed_comment = {
            "author": comment["author"],
            "comment_text": comment["comment_text"],
            "likes": comment["likes"],
            "replies": 0,
            "sentiment": sentiment
        }
        transformed_data["comments"].append(transformed_comment)
    
    return transformed_data

def main():
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("spacytextblob")
    
    with open('raw_output.json', 'r') as file:
        data = json.load(file)
    
    transformed_data = transform_structure(data, nlp)
    
    with open('processed_output.json', 'w', encoding='utf-8') as file:
            json.dump(transformed_data, file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()