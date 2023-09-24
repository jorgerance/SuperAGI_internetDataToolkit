#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
from typing import Type

import requests
from pydantic import BaseModel, Field
from retry import retry
from superagi.tools.base_tool import BaseTool

class NewsHeadlinesInput(BaseModel):
    limit: int = Field(..., description="The maximum number of news headlines to retrieve in one cycle. Defaults to 8.")


class NewsHeadlinesTool(BaseTool):
    """
    Tool to fetch the latest news headlines.

    Attributes:
        name : The name of the tool.
        description : A brief description of the tool's functionality.
        args_schema : The schema defining the input arguments for the tool.
    """
    name: str = "News Headlines Tool"
    args_schema: Type[BaseModel] = NewsHeadlinesInput
    description: str = "Retrieve the latest news headlines in a markdown-formatted string."

    def _execute(self, limit: int = 8) -> str:
        """
        Execute the News Headlines Tool.

        Args:
            limit : The maximum number of news headlines to retrieve in one cycle. Defaults to 8.

        Returns:
            A markdown-formatted string containing an array of news headlines with title, link and source, or an error message if no headlines are found.
        """
        return self.news_headlines(limit=limit)

    @retry(tries=2, delay=4, backoff=4)
    def news_headlines(self, limit: int = 8, tag: str = 'news', format: str = 'json') -> str:
        # sourcery skip: assign-if-exp
        """
        Fetch and return the latest news headlines.

        Args:
            limit : The maximum number of news headlines to retrieve.
            tag : The tag representing the type of news to fetch. Defaults to 'news'.

        Returns:
            A JSON-formatted string containing the latest news headlines or an error message if no headlines are found.
        """
        def _decode_unicode_escape_sequences(input_string: str) -> str:
            """Decode Unicode escape sequences in a string."""
            return re.sub(r'\\u([0-9a-fA-F]{4})', lambda match: chr(int(match.group(1), 16)), input_string)

        def _remove_unwanted_characters(text: str) -> str:
            """Remove unwanted characters from a text."""
            characters_to_preserve = ''' !¡"#$%&'()*+,-0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~áàäçéèëíìïñóòöúùüÁÀÄÇÉÈËÍÌÏÑÓÒÖÚÙÜ«»‘’´“”·.‚'''
            pattern = f'[^{re.escape(characters_to_preserve)}]+'
            return re.sub(pattern, '', text)

        def _format_to_markdown(data_list: list) -> str:
            """
            Formats a list of dictionaries to a pretty-formatted Markdown string.

            :param data_list: List of dictionaries.
            :type data_list: list
            :return: Pretty-formatted Markdown string.
            :rtype: str
            """
            markdown_str = ""
            for i, data in enumerate(data_list, start=1):
                markdown_str += f"{i}. "
                for key, value in data.items():
                    markdown_str += f"**{key.capitalize()}:** {value}  \n"
                markdown_str += "\n"
            return markdown_str

        # Set headers and query parameters for the HTTP request
        headers = {
            'Accept': "application/json",
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,es;q=0.7,fr;q=0.6,de;q=0.5',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'X-Requested-With': 'XMLHttpRequest',
        }
        params = {
            'type': 'newest',
            'tag': tag,
            'extraIds[]': '',
            'sourcesNav': 'false',
            'search': '',
            'itemsPerPage': limit,
        }

        try:
            # Send a GET request to fetch the news
            response = requests.get('http://192.168.8.225:8888/', params=params, headers=headers, verify=False, timeout=20)
            response.raise_for_status()
            news = response.json()['entries']
        except requests.RequestException as e:
            return json.dumps({"error": str(e)}, indent=1)

        # Parse and process the news headlines
        headlines = [
            {
                "title": f"{_remove_unwanted_characters(_decode_unicode_escape_sequences(headline['title']))}",
                "link": f"{headline['link']}",
                "source": f"{headline['sourcetitle']}"
            }
            for idx, headline in enumerate(news) if idx < limit
        ]

        # Return the JSON-formatted / markdown-formatted string or an error message if no headlines are found or if an error occurs
        if headlines:
            if format == 'markdown':
                return _format_to_markdown(headlines)
            return json.dumps(headlines, indent=2)
        else:
            return "No news found."
