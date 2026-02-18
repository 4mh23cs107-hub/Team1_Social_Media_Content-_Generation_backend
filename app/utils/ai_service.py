import os
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

def generate_social_media_content(topic, platform, tone="professional", audience="general"):
    """
    Generates social media content based on topic, platform, and tone.
    """
    if not client:
        return "AI Service not configured (Missing GITHUB_TOKEN)."

    system_prompt = f"You are a professional social media manager. Generate high-quality content for {platform}."
    user_prompt = f"Topic: {topic}\nPlatform: {platform}\nTone: {tone}\nAudience: {audience}\n\nPlease provide a caption and a few relevant hashtags."

    try:
        response = client.complete(
            messages=[
                SystemMessage(content=system_prompt),
                UserMessage(content=user_prompt),
            ],
            model=MODEL
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating content: {str(e)}"
