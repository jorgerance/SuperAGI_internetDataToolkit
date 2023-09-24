#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC
from typing import List

from superagi.tools.base_tool import BaseTool, BaseToolkit

from superagi.tools.external_tools.SuperAGI_internetDataToolkit.news_headlines import NewsHeadlinesTool
from superagi.tools.external_tools.SuperAGI_internetDataToolkit.search_internet import InternetSearchTool
from superagi.tools.external_tools.SuperAGI_internetDataToolkit.website_content import WebsiteContentTool
from superagi.tools.external_tools.SuperAGI_internetDataToolkit.check_file_existence import CheckFileExistenceTool


class InternetDataToolKit(BaseToolkit, ABC):
    """
    The InternetDataToolKit class represents a collection of tools designed for various internet-based operations.
    It includes tools for searching the internet, fetching news headlines, and extracting website content.
    """
    name: str = "Internet Data Toolkit"
    description: str = "A toolkit comprising tools for internet-based operations such as searching, fetching news headlines, and extracting website information."

    def get_tools(self) -> List[BaseTool]:
        """
        Retrieves a list of tool instances available in the Internet Data Toolkit.
        The tools included are for searching the internet, fetching news headlines, and extracting website content.

        Returns:
            List[BaseTool]: A list of tool instances available in the toolkit.
        """
        return [InternetSearchTool(), NewsHeadlinesTool(), WebsiteContentTool(), CheckFileExistenceTool()]

    def get_env_keys(self) -> List[str]:
        """
        Retrieves a list of environment keys that are used by the toolkit.
        These keys can be used to access environment-specific configurations or settings.

        Returns:
            List[str]: A list of environment keys used by the toolkit.
        """
        return []
