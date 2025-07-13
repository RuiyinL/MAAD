from metagpt.actions import Action
from pathlib import Path
from metagpt.roles import Role
import asyncio
from metagpt.logs import logger
from metagpt.schema import Message
import json
import os
import time

class AnalyzeRequirement(Action):
    #Generate ASR
    PROMPT_TEMPLATE1: str = """"
    Given the software requirements below\n
    {requirements_document}\n
    Generate Architecturally Significant Requirements (ASRs) from the provided requirements. For each ASR, the criteria are: influence system architectural decisions, involves critical quality attributes, require cross-component coordination. 
    Structure your outputs as follows:\n
    "The ASRs are:\n
    1. [ASR-001]:\n
    - [Original text of ASR1]\n
    - [Related quality attribute(s)]\n
    - [Architectural Impact]\n
    2. [ASR-002]:
    ..."

    An example is here:
    1. ASR-001
    - Original text of ASR1: The system must support 100,000 concurrent requests per second
    - [Related quality attribute(s)]: Scalability, Availability, Performance efficiency, Fault Tolerance
    - Architectural Impact: Distributed architecture design is required
    - Related Components: API Gateway, Load Balancer
    ...
    """

    #Generate FR
    PROMPT_TEMPLATE2: str = """
    Here is a provided software requirements \n
    {requirements_document}\n
    Provide a concise summary of the functional requirements (FR). Specifically, identify the features and tasks outlined in the document. Structure your outputs as follows:\n
    "The functional requirements are:\n
    1. [FR-001]  
    1.1 [Task 1]
    1.2 [Task 2]
    …
    2. [FR-002]
    2.1 [Task 1]
    ..."
    """

    #Genertae non-functional requirements
    PROMPT_TEMPLATE3: str = """
    Here is a provided software requirements specification\n
    {requirements_document}\n  
    Based on the provided software requirements specification, please summarize all Non-functional Requirements (NFR). Structure your outputs as follows:\n
    "The Non-functional Requirements are:\n
    1. [NFR-001]:\n
    - [Original text of NFR-001]\n
    - [Related quality attribute(s)]\n
    2. [NFR-002]:
    ..."
    """

    PROMPT_TEMPLATE4: str = """"
    Here is a provided software requirements specification\n
    {requirements_document}\n  
    Based on the provided software requirements specification, please generate the Design Constraints (DC). Structure your outputs as follows:\n
    "The Design Constraints are:\n
    1. DC-001: XXXX
    2. DC-002: XXXX
    ..."
    """
    name: str = "AnalyzeRequirement"
    
    requirement_root : Path = Path("output//Analyst")

    @classmethod
    def set_output_root(cls, requirement_root: Path):
        cls.requirement_root = requirement_root

    async def run(self, requirement_document: str):
        prompt1 = self.PROMPT_TEMPLATE1.format(requirements_document=requirement_document)
        rsp = ""
        rsp = await self._aask(prompt1)
        file_path = self.file_name("ASR")
        with file_path.open("w", encoding='utf-8') as f:
            f.write(rsp)
        prompt2 = self.PROMPT_TEMPLATE2.format(requirements_document=requirement_document)
        rsp = await self._aask(prompt2)
        file_path = self.file_name("FR")
        with file_path.open("w", encoding='utf-8') as f:
            f.write(rsp)
        prompt3 = self.PROMPT_TEMPLATE3.format(requirements_document=requirement_document)
        rsp = await self._aask(prompt3)
        file_path = self.file_name("NFR")
        with file_path.open("w", encoding='utf-8') as f:
            f.write(rsp)
        prompt4 = self.PROMPT_TEMPLATE4.format(requirements_document=requirement_document)
        rsp = await self._aask(prompt4)
        file_path = self.file_name("DC")
        with file_path.open("w", encoding='utf-8') as f:
            f.write(rsp)

    @classmethod
    def file_name(cls, name : str) -> str:
        output_dir = cls.requirement_root
        output_dir.mkdir(parents=True, exist_ok=True)
        if name == "ASR":
            file_name = f"ASR.txt"
            file_path = output_dir / file_name
        elif name == "FR":
            file_name = f"FR.txt"
            file_path = output_dir / file_name
        elif name == "NFR":
            file_name = f"NFR.txt"
            file_path = output_dir / file_name
        elif name == "DC":
            file_name = f"DC.txt"
            file_path = output_dir / file_name
        return file_path

class Analyst(Role):
    name: str = "Agent1"
    profile: str = "Analyst"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([AnalyzeRequirement])

    async def _act(self):
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo  # todo will be SimpleWriteCode()

        msg = self.get_memories(k=1)[0]  # find the most recent messages
        await todo.run(msg.content)

async def main():
    with open("config.json", "r", encoding='utf-8') as f:
        config = json.load(f)
    input_file = config["input_file"]
    # read requirements
    with open(input_file, "r", encoding='utf-8') as f:
        requirement = f.read()
    role = Analyst()
    file_name = os.path.basename(input_file)
    requirement_root = Path("output//" + file_name.split(".")[0] + "//Analyst")
    AnalyzeRequirement.set_output_root(requirement_root)
    result = await role.run(requirement)
    logger.info(result)

asyncio.run(main())