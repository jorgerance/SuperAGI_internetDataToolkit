#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from typing import Type
from pydantic import BaseModel, Field
from superagi.tools.base_tool import BaseTool

class CheckFileExistenceInput(BaseModel):
    file_path: str = Field(..., description="The path of the file to check for existence.")

class CheckFileExistenceTool(BaseTool):
    """
    Tool to check if a given file path exists.

    Attributes:
        name : The name of the tool.
        description : A brief description of the tool's functionality.
        args_schema : The schema defining the input arguments for the tool.
    """
    name: str = "File Existence Tool"
    args_schema: Type[BaseModel] = CheckFileExistenceInput
    description: str = "Check if a given file path exists."

    def _execute(self, file_path: str) -> str:
        """
        Execute the File Existence Tool.

        Args:
            file_path : The path of the file to check for existence.

        Returns:
            A message indicating whether the file exists or not.
        """
        if os.path.exists(file_path):
            return f"The file {file_path} exists."
        else:
            return f"The file {file_path} does not exist."