#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
import urllib.parse
from typing import Type

import requests
from pydantic import BaseModel, Field
from superagi.tools.base_tool import BaseTool


class InternetSearchInput(BaseModel):
    query: str = Field(..., description="The specific topic or subject to be researched on the internet.")
    limit: int = Field(..., description="The maximum number of results to be fetched in one cycle. Defaults to 5.")


class InternetSearchTool(BaseTool):
    """
    Perform an internet search using Google.

    Attributes:
        name : The name of the tool.
        description : A brief description of the tool's functionality.
        args_schema : The schema defining the input arguments for the tool.
    """
    name: str = "Internet Search Tool"
    args_schema: Type[BaseModel] = InternetSearchInput
    description: str = "Retrieve information on a specified topic from the internet."

    def _execute(self, query: str = "", limit: int = 5) -> str:
        """
        Execute the Internet Search Tool.

        Args:
            query : The specific topic or subject to be researched on the internet.
            limit : The maximum number of results to be fetched in one cycle. Defaults to 5.

        Returns:
            A JSON-formatted string containing an array of results with title, link, and snippet, or an error message if no results are found.
        """
        return self.search_google(query=query, limit=limit)

    def search_google(self, query: str = "", language: str = 'EN', serp_api_url: str = 'http://192.168.8.225:7000', limit: int = 5) -> str:
        """
        Query Google with the given query and return the search results.

        Args:
            query : The search query string.
            language : The language for the search results. Defaults to 'EN'.
            serp_api_url : The URL of the SERP API. Defaults to 'http://192.168.8.225:7000'.
            limit : The maximum number of search results to return. Defaults to 5.

        Returns:
            A JSON-formatted string containing the search results or an error message if no results are found.
        """
        # Define the set of characters to preserve in the search results
        _clean_charset = ''' !¡"#$%&'()*+,-0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~áàäçéèëíìïñóòöúùüÁÀÄÇÉÈËÍÌÏÑÓÒÖÚÙÜ«»‘’´“”·.‚'''

        def _remove_unwanted_characters(text: str, characters_to_preserve: str = _clean_charset) -> str:
            """Remove unwanted characters from a text."""
            pattern = f'[^{re.escape(characters_to_preserve)}]+'
            return re.sub(pattern, '', text)

        # Encode the query string and construct the endpoint URL
        url_encoded_query = urllib.parse.quote(query.strip().rstrip('?'))
        endpoint_url = f"{serp_api_url}/google/search?lang={language}&limit={limit}&text={url_encoded_query}"

        try:
            # Send a GET request to the SERP API and parse the JSON response
            response = requests.get(endpoint_url)
            response.raise_for_status()
            jresponse = response.json()
        except requests.RequestException as e:
            return json.dumps({"error": str(e), "query": query}, indent=1)

        # Process the search results and remove unwanted characters
        results_json = [
                {
                    'title': _remove_unwanted_characters(result['title']),
                    'link': result['url'],
                    'snippet': _remove_unwanted_characters(result['description'])
                } for result in jresponse
            ]

        # Construct the final JSON object containing the query and the processed results
        json_object = {'query': query, 'results': results_json}

        # Return the JSON-formatted string or an error message if no results are found
        if not results_json:
            return f"Google search returned no results for query \"{query}\""
        return json.dumps(json_object, indent=1)
