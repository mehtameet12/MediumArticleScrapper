import os
import json
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_content_with_gpt(content):
    """
    Summarize the article content using OpenAI's GPT model.
    
    Args:
        content (str): The full article content.
    
    Returns:
        str: The summarized content.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes articles."},
                {"role": "user", "content": f"Summarize the following article in 3 sentences:\n\n{content}"}
            ],
            max_tokens=150,
            temperature=0.5
        )
        summary = response.choices[0].message["content"].strip()
        return summary
    except Exception as e:
        print(f"Error summarizing content with GPT: {e}")
        return None

def analyze_comments_with_gpt(comments):
    """
    Analyze comments using OpenAI's GPT model to detect frequent concerns, highly liked comments, and sentiment trends.
    
    Args:
        comments (list): List of comment dictionaries.
    
    Returns:
        str: Analysis results.
    """
    try:
        comments_text = "\n".join([f"{comment['author']}: {comment['comment_text']} (Likes: {comment['likes']}, Sentiment: {comment['sentiment']})" for comment in comments])
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes comments."},
                {"role": "user", "content": f"Analyze the following comments and provide insights on frequent concerns, highly liked comments, and sentiment trends:\n\n{comments_text}"}
            ],
            max_tokens=300,
            temperature=0.5
        )
        analysis = response.choices[0].message["content"].strip()
        return analysis
    except Exception as e:
        print(f"Error analyzing comments with GPT: {e}")
        return None

def update_json_with_summary_and_analysis(input_path, summary, analysis):
    """
    Update the processed_output.json file with the summary and commentary_analysis.
    
    Args:
        input_path (str): Path to the processed JSON file.
        summary (str): The summarized content.
        analysis (str): The comment analysis results.
    """
    try:
        with open(input_path, "r") as file:
            data = json.load(file)
        
        data["summary"] = summary
        data["commentary_analysis"] = analysis
        
        with open(input_path, "w") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        
        print(f"Updated {input_path} with summary and commentary_analysis.")
    except Exception as e:
        print(f"Error updating JSON file: {e}")

def main(input_path="processed_output.json"):
    """
    Main function to summarize content and analyze comments using OpenAI's GPT model.
    
    Args:
        input_path (str): Path to the processed JSON file.
    """
    with open(input_path, "r") as file:
        data = json.load(file)
    
    summary = summarize_content_with_gpt(data["content"])
    if not summary:
        print("Failed to summarize content.")
        return
    
    analysis = analyze_comments_with_gpt(data["comments"])
    if not analysis:
        print("Failed to analyze comments.")
        return
    
    update_json_with_summary_and_analysis(input_path, summary, analysis)

if __name__ == "__main__":
    main()