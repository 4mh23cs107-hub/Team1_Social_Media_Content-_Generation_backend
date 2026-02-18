import os
import json
import requests
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
ENDPOINT = "https://models.github.ai/inference"
MODEL = "gpt-4o-mini"

client = None
if GITHUB_TOKEN:
    client = ChatCompletionsClient(
        endpoint=ENDPOINT,
        credential=AzureKeyCredential(GITHUB_TOKEN),
    )


def generate_image_content(prompt):
    """
    Generates an image using DALL-E 3 via GitHub Models API.
    """
    if not GITHUB_TOKEN:
        return None
        
    url = "https://models.github.ai/inference/images/generations"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()["data"][0]["url"]
        return None
    except Exception:
        return None

def generate_social_media_content(topic, platform, tone="professional", audience="general"):
    """
    Generates social media content based on topic, platform, and tone.
    Returns a dictionary with 'caption', 'hashtags', 'content_type', and 'image_url'.
    """
    if not client:
        return {"caption": "AI Service not configured (Missing GITHUB_TOKEN).", "hashtags": "", "content_type": "post", "image_url": None}

    system_prompt = (
        f"You are a professional social media manager and content creator. Generate high-quality, comprehensive content for {platform}. "
        "There is no length limit; feel free to provide long-form content if appropriate for the topic. "
        "You must respond in valid JSON format with three keys: 'caption', 'hashtags', and 'content_type' (e.g., Post, Article, Story, Thread). "
        "Return ONLY the JSON object. Do not include any explanations, markdown code blocks, or preamble."
    )
    user_prompt = f"Topic: {topic}\nPlatform: {platform}\nTone: {tone}\nAudience: {audience}\n\nPlease provide the main content (as 'caption'), relevant hashtags, and suggest a content type. Do not restrict the length of the response."

    output = {"caption": "", "hashtags": "", "content_type": "post", "image_url": None}

    try:
        response = client.complete(
            messages=[
                SystemMessage(content=system_prompt),
                UserMessage(content=user_prompt),
            ],
            model=MODEL,
            max_tokens=4096
        )
        content = response.choices[0].message.content
        
        # Clean the response in case it's wrapped in markdown code blocks
        if content.startswith("```json"):
            content = content.replace("```json", "", 1).rsplit("```", 1)[0].strip()
        elif content.startswith("```"):
            content = content.replace("```", "", 1).rsplit("```", 1)[0].strip()
            
        output.update(json.loads(content))
    except Exception as e:
        # Fallback
        try:
            content = response.choices[0].message.content
            if content.startswith("```json"):
                content = content.replace("```json", "", 1).rsplit("```", 1)[0].strip()
            elif content.startswith("```"):
                content = content.replace("```", "", 1).rsplit("```", 1)[0].strip()
            output.update(json.loads(content))
        except:
            output["caption"] = f"Error generating text: {str(e)}"

    # Generate Image
    image_prompt = f"A professional social media {output.get('content_type', 'post')} image about {topic}. Style: {tone}. Target Audience: {audience}."
    output["image_url"] = generate_image_content(image_prompt)
    
    return output
