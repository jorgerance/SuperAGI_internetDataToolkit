import unittest

from InternetDataTool.internetdata_toolkit import InternetDataToolKit
from InternetDataTool.news_headlines import NewsHeadlinesTool
from InternetDataTool.search_internet import InternetSearchTool
from InternetDataTool.website_content import WebsiteContentTool


class InternetDataToolkitTests(unittest.TestCase):
    def setUp(self):
        self.toolkit = InternetDataToolKit()

    def test_get_tools_returns_list_of_tools(self):
        tools = self.toolkit.get_tools()
        self.assertIsInstance(tools, list)
        self.assertTrue(all(isinstance(tool, (NewsHeadlinesTool, InternetSearchTool, WebsiteContentTool)) for tool in tools))

    def test_get_env_keys_returns_list_of_strings(self):
        env_keys = self.toolkit.get_env_keys()
        self.assertIsInstance(env_keys, list)
        self.assertTrue(all(isinstance(key, str) for key in env_keys))

    def test_toolkit_has_name_and_description(self):
        self.assertEqual(self.toolkit.name, "Internet Data Toolkit")
        self.assertEqual(self.toolkit.description, "A toolkit comprising tools for internet-based operations such as searching, fetching news headlines, and extracting website information.")


if __name__ == '__main__':
    unittest.main()
