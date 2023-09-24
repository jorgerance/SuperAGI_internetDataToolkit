#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
from typing import Type

import trafilatura
from pydantic import BaseModel, Field
from superagi.tools.base_tool import BaseTool


class WebsiteContentInput(BaseModel):
    url: str = Field(..., description="The URL of the website to be fetched in plain text.")


class WebsiteContentTool(BaseTool):
    """
    Tool to fetch a website content in plain text.

    Attributes:
        name : The name of the tool.
        description : A brief description of the tool's functionality.
        args_schema : The schema defining the input arguments for the tool.
    """
    name: str = "Website Content Tool"
    args_schema: Type[BaseModel] = WebsiteContentInput
    description: str = "Fetch website content in plain text returning a JSON-formatted string."

    def _execute(self, url: str = "") -> str:
        """
        Execute the Website Content Tool.

        Args:
            url: The URL of the website to be fetched in plain text.

        Returns:
            A JSON object containing the URL and its corresponding plain text content, or an error message if the content could not be fetched.
        """
        return self.fetch_website_content(url=url)

    def fetch_website_content(self, url: str) -> str:
        """
        Fetch the content of the specified website in plain text.

        Args:
            url: The URL of the website whose content is to be fetched.

        Returns:
            A JSON-formatted string containing the URL and its corresponding plain text content.
        """
        try:
            plaintext_content = trafilatura.extract(trafilatura.fetch_url(url)) or requests.get(url).text
            json_content = {
                "url": url,
                "plaintext_content": plaintext_content
            } if plaintext_content else {"error": "Failed to extract content from the website.", "url": url}
            return json.dumps(json_content)
        except Exception as e:
            return json.dumps({"error": str(e), "url": url}, indent=1)



#if __name__ == "__main__":
#    url = 'https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT'
#    c = trafilatura.extract(trafilatura.fetch_url(url))
#    if not c:
#        c = requests.get(url).text
