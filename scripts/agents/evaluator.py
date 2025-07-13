from metagpt.actions import Action
from pathlib import Path
from metagpt.roles import Role
import asyncio
from metagpt.logs import logger
from metagpt.schema import Message
import re
import json
import os
import time

class Evaluating(Action):
    PROMPT_TEMPLATE1: str = """"
    According to the provided requirements and UML diagrams (recorded in PlantUML syntax), please generate a Mismatch Analysis Report. \n
    1. Requirement: {requirement_document}\n
    2. Architectural views: {AV}\n
    3. Architectural documentation: {AD}\n
    Your report should identify any discrepancies, inconsistencies, or gaps between the system requirements and the architectural design. Structure your outputs as follows:\n
    [mismatch 1]
    - Description: A brief explanation of the mismatch.
    - Impact: An analysis of the potential impact on the system.
    - Recommendation: Suggestions or steps to resolve or mitigate the issue.
    [mismatch 2]
    - Description: A brief explanation of the mismatch.
    - Impact: An analysis of the potential impact on the system.
    - Recommendation: Suggestions or steps to resolve or mitigate the issue
    ……
    """

    #Generate ATAM report
    PROMPT_TEMPLATE2: str = """
    According to the provided requirements and UML diagrams, please generate an architecture evaluation report based on the ATAM method.\n
    1. Requirement: {requirement_document}\n
    2. UML views: {AV}\n
    Your report should include the following content:
    1. A concise presentation of the architecture: an architectural presentation that is both concise and, usually, understandable.
    2. Articulation of the business goals: the business goals presented in the ATAM exercise are being seen by some of the assembled participants for the first time and these are captured in the outputs.
    3. Prioritized quality attribute requirements expressed as quality attribute scenarios: uses prioritized quality attribute scenarios as the basis for evaluating the architecture.
    4. A set of risks and non-risks: An architectural risk is a decision that may lead to undesirable consequences in light of stated quality attribute requirements. Similarly, an architectural non-risk is a decision that, upon analysis, is deemed safe.
    5. A set of risk themes: When the analysis is complete, the evaluation team examines the full set of discovered risks to look for overarching themes that identify systemic weaknesses in the architecture or even in the architecture process and team. If left untreated, these risk themes will threaten the project’s business goals.
    6. Mapping of architectural decisions to quality requirements: Architectural decisions can be interpreted in terms of the drivers that they support or hinder.
    7. A set of identified sensitivity points and tradeoff points: Sensitivity points are architectural decisions that have a marked effect on a quality attribute response. Tradeoffs occur when two or more quality attribute responses are sensitive to the same architectural decision, but one of them improves while the other degrades—hence the tradeoff.
    """

    name: str = "Evaluating"
    output_root : Path = Path("output//Designer")

    @classmethod
    def set_output_root(cls, output_root: Path):
        cls.output_root = output_root    
    
    async def run(self, requirement_document: str, AV: str, AD: str, file_name: str):
        prompt1 = self.PROMPT_TEMPLATE1.format(requirement_document=requirement_document, AV=AV, AD=AD)    
        rsp = ""
        rsp = await self._aask(prompt1)
        mismatch_count = self.count_mismatch(rsp)
        with open(".\\output\\" + file_name + "\\Analyst\\FR.txt", "r", encoding='utf-8') as f:
            fr_text = f.read()
        with open(".\\output\\" + file_name + "\\Analyst\\NFR.txt", "r", encoding='utf-8') as f:
            nfr_text = f.read()
        functional_requirements_count = self.count_functional_requirements(fr_text)
        non_functional_requirements_count = self.count_non_functional_requirements(nfr_text)
        requirement_count = functional_requirements_count + non_functional_requirements_count
        mismatch_rate = mismatch_count/requirement_count
        file_path = self.file_name("MAR")
        with file_path.open("w", encoding='utf-8') as f:
            f.write(rsp)
            f.write(f"\nMismatch count: {mismatch_count}")
            f.write(f"\nRequirement count: {requirement_count}")
            f.write(f"\nMismatch rate: {mismatch_rate}")
        prompt2 = self.PROMPT_TEMPLATE2.format(requirement_document=requirement_document, AV=AV)  
        rsp = ""
        while not rsp:
            rsp = await self._aask(prompt2)
        file_path = self.file_name("ATAM")
        with file_path.open("w", encoding='utf-8') as f:
            f.write(rsp)
    
    @classmethod
    def file_name(cls, name : str) -> str:
        output_dir = cls.output_root
        output_dir.mkdir(parents=True, exist_ok=True)
        if name == "MAR":
            file_name = f"MAR.txt"
            file_path = output_dir / file_name
        elif name == "ATAM":
            file_name = f"ATAM.txt"
            file_path = output_dir / file_name
        elif name == "RS":
            file_name = f"RS.txt"
            file_path = output_dir / file_name
        elif name == "ER":
            file_name = f"ER.txt"
            file_path = output_dir / file_name
        return file_path

    @classmethod
    def count_requirement(cls, rsp_total: str):
        match = re.search(r'\d+', rsp_total)
        if match:
            return int(match.group())
        else:
            return None

    @staticmethod
    def count_mismatch(rsp):
        mismatches = re.findall(r'Mismatch \d+', rsp)
        return len(mismatches)
    @staticmethod
    def count_functional_requirements(rsp):
        functional_requirements = re.findall(r"\d+\.\d+", rsp)
        return len(functional_requirements)
    @staticmethod
    def count_non_functional_requirements(rsp):
        non_functional_requirements = re.findall(r"\[NFR-\d+\]", rsp)
        return len(non_functional_requirements)

class Evaluator(Role):
    name: str = "Agent4"
    profile: str = "Evaluator"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([Evaluating])

    async def _act(self):
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo  # todo will be SimpleWriteCode()
        msg = self.get_memories(k=1)[0]  # find the most recent messages
        json_dict = eval(msg.content)
        await todo.run(json_dict["requirement_document"], json_dict["AV"], json_dict["AD"], json_dict["FileName"])

async def main():
    with open("config.json", "r", encoding='utf-8') as f:
        config = json.load(f)
    input_file = config["input_file"]
    file_name = os.path.basename(input_file).split(".")[0]
    output_root = Path("output//" + file_name.split(".")[0] + "//Evaluator")
    Evaluating.set_output_root(output_root)
    with open(input_file, "r", encoding='utf-8') as f:
        requirement_document = f.read()
    with open(".\\output\\" + file_name.split(".")[0] + "\\Modeler\\AV.txt", encoding='utf-8') as f:
        AV = f.read()
    with open(".\\output\\" + file_name.split(".")[0] + "\\Designer\\AD.txt", encoding='utf-8') as f:
        AD = f.read()
    json_msg = {"requirement_document":requirement_document, "AV":AV, "AD":AD, "FileName":file_name.split(".")[0]}
    json_str = str(json_msg)
    role = Evaluator()
    result = await role.run(json_str)
    logger.info(result)

asyncio.run(main())