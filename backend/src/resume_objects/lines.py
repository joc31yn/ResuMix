"""
The Lines Class

This class is used to represent a line in a resume.
It contains the information stored about the line, and related functions to parse it.
"""

import re
import ast
from ..general_helper.isa_bot import AIBot


class Line:
    """
    Functions needed:
    - gen_score: have AI cook
    - adj_score: adjust score by general input in learning phase
    - gen_keyword: generate keywords with AI: just rip it off gen_score
    - strip: generate the string only content for stuff such as gpt
    - to_dict: get the dictionary version to store into db
    Variables needed:
    - contents: lstr
    - content_str: str
    - sect_score (possibly, for gpt parsing): dict
    - keywords: listof(str)
    """

    def __init__(self, class_dict: dict = None) -> None:
        """
        Takes the info from storage to build the class
        OR create an empty class if info is None
        """
        self.content = r""  # content is latex code segment
        self.cate_score = {}  # dict of str: int
        # This stands for category score
        self.content_str = ""  # content_str is pure string
        self.keywords = []  # list of pure strings
        self.aux_info = {}
        self.bot = AIBot()  # AI bot for generating scores

        self.score: int = None  # Used for optimization

        # getter and setters are not needed
        if class_dict is not None:
            if "aux_info" not in class_dict:
                raise ValueError("Missing 'aux_info', should not happen in prod")
            if (
                "type" not in class_dict["aux_info"]
                or class_dict["aux_info"]["type"] != "lines"
            ):
                raise ValueError("Invalid input: 'type' must be 'lines'")
            # At this point, info is a Lines class
            self.content = class_dict["content"] if "content" in class_dict else r""
            self.content_str = (
                class_dict["content_str"] if "content_str" in class_dict else ""
            )
            self.keywords = class_dict["keywords"] if "keywords" in class_dict else []
            self.aux_info = class_dict["aux_info"]

    def content_flatten(self) -> None:
        """
        Modifies self.content_str
        """
        # Remove LaTeX commands and extract plain text
        # Handle hyperlinks: extract the second argument if present, otherwise the first
        self.content = re.sub(r"\\href\{[^}]*\}\{([^}]*)\}", r"\1", self.content)
        self.content_str = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", self.content)
        self.content_str = re.sub(r"\\[a-zA-Z]+\s*", "", self.content_str)
        self.content_str = re.sub(r"\{([^}]*)\}", r"\1", self.content_str)
        self.content_str = re.sub(r"\s+", " ", self.content_str).strip()
        # This should be useless if the frontend works as expected

    def gen_score(self, forced: bool = False, industry: str = "software") -> bool:
        """
        Generate a set of scores for this line
        WILL OVERWRITE EXISTING
        Effect: modify self.cate_score
        """
        print("DEBUG: CATE_SCORE SHOULD BE DEPRECATED")
        return False

    def to_dict(self) -> dict:
        """
        Compile the class into a dict for storage
        """
        result = {}
        if self.aux_info:
            result["aux_info"] = self.aux_info
        else:
            result["aux_info"] = {"type": "lines"}
        result["content"] = self.content
        result["content_str"] = self.content_str
        return result

    # def __get_dict(self, prompt: str, retries: int) -> tuple[bool, dict]:
    #     """
    #     Gets the dictionary according to the prompt (mainly to fill the cate_score)
    #     DOES NOT DIRECTLY MODIFY CATE_SCORE
    #     the boolean represents whether a valid response is generated
    #     the dict represents the result
    #     This method is RECURSIVE, when retries hits 0 it returns failure
    #     """
    #     prompt_instruction = "When you are asked a question, first analyze it, then output ONLY a python dictionary that contains the answer. Sample output: {'something': 1, 'your_answer': 1}. Note: the dictionary should contain keys of type string and values of type int Do not output anything else. Also, whenever giving something a score, make it out of 3"
    #     if retries <= 0:
    #         return False, {}

    #     try:
    #         response = self.bot.response_instruction(prompt, prompt_instruction)
    #         print(response)  # Debugging output
    #         # Extract the dictionary from the response
    #         match = re.search(r"\s*(\{.*\})", response, re.DOTALL)
    #         if match:

    #             result_dict = ast.literal_eval(
    #                 match.group(1)
    #             )  # Safely convert string to dictionary
    #             # Convert the values of the dictionary to integers
    #             result_dict = {
    #                 k: int(v) for k, v in result_dict.items() if str(v).isdigit()
    #             }
    #         if isinstance(result_dict, dict):
    #             return True, result_dict
    #     except Exception as e:
    #         print(f"Error occurred: {e}")
    #         pass

    #     return self.__get_dict(prompt, retries - 1)

    def total_tokens(self) -> int:
        """
        Returns the total number of tokens used in the cate_score generation
        """
        return self.bot.total_tokens
