import requests
import os
from typing import Dict, Any

class LinkedInService:
    @property
    def client_id(self):
        return os.getenv("LINKEDIN_CLIENT_ID")

    @property
    def client_secret(self):
        return os.getenv("LINKEDIN_CLIENT_SECRET")

    @property
    def redirect_uri(self):
        return os.getenv("LINKEDIN_REDIRECT_URI", "http://localhost:3000/linkedin-callback.html")

    def get_authorization_url(self) -> str:
        url = "https://www.linkedin.com/oauth/v2/authorization"
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": "w_member_social profile email openid",
        }
        return f"{url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"

    def get_access_token(self, code: str) -> Dict[str, Any]:
        url = "https://www.linkedin.com/oauth/v2/accessToken"
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
        }
        response = requests.post(url, data=data)
        return response.json()

    def get_user_profile(self, access_token: str) -> Dict[str, Any]:
        url = "https://api.linkedin.com/v2/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        return response.json()

    def post_content(self, access_token: str, linkedin_id: str, text: str, image_url: str = None) -> Dict[str, Any]:
        url = "https://api.linkedin.com/v2/ugcPosts"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        
        post_data = {
            "author": f"urn:li:person:{linkedin_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }

        # If image is provided, we'd need to upload it first which is a 3-step process.
        # For simplicity in this initial version, we will post only text.
        # LinkedIn Image Upload requires: 1. Register Upload, 2. Upload, 3. Complete Upload.
        
        response = requests.post(url, headers=headers, json=post_data)
        return response.json()

linkedin_service = LinkedInService()
