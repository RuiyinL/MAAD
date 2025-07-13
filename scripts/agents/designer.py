from metagpt.actions import Action
from pathlib import Path
from metagpt.roles import Role
import asyncio
from metagpt.logs import logger
from metagpt.schema import Message
import json
import os
from langchain_community.vectorstores import LanceDB
from langchain_openai import OpenAIEmbeddings
import lancedb

os.environ["OPENAI_API_KEY"] = "[OpenAI API Key]"
embedding_function = OpenAIEmbeddings()
db = lancedb.connect("~/langchain")
table = db.open_table("vectorstore")

class Designinng(Action):
    PROMPT_TEMPLATE1: str = """"
    Act as a software architect. Based on the following inputs: \n
    (1) architecturally significant requirements: {ASR}\n
    (2) functional requirements: {FR}\n
    (3) non-functional requirements: {NFR}\n
    (4) design constraints: {DC}\n
    (5) architectural views: {AV}\n
    (6) reference knowledge: {RK}\n

    Generate the following outputs in a structured technical document:
    1.Goals: Define the primary objectives that the architecture aims to achieve.
    2.Detailed Architecture Design: A detailed design document that specifies the system’s components and modules, outlining their interactions and interfaces.
    3.Component & Connector Specifications: Describe communication protocols (e.g., REST API contracts, event-driven messaging formats) and include error-handling mechanisms and performance thresholds.
    4.Key Technologies: Propose infrastructure configuration (e.g., resource allocation), and highlight scalability/fault-tradeoffs.
    5.Design Decisions: A clear explanation of design decisions, including chosen design patterns, technology selections, and the rationale behind key architectural choices.
    6.Design Decision Rationale: Justify technology choices, or explain pattern adoption.
    7.Executable Prototype Skeleton: Generate code scaffolding for critical modules.
    """
    
    name: str = "Designinng"
    
    output_root : Path = Path("output//Designer")

    @classmethod
    def set_output_root(cls, output_root: Path):
        cls.output_root = output_root

    async def run(self, ASR: str, FR: str, NFR: str, DC: str, AV: str):
        prompt1 = self.PROMPT_TEMPLATE1.format(ASR=ASR, FR=FR, NFR=NFR, DC=DC, AV=AV, RK="")
        query = embedding_function.embed_query(prompt1)
        docs = table.search(query, query_type="vector").limit(3).to_pandas()["text"].to_list()
        reference_knowledge = " ".join(docs)
        prompt1 = self.PROMPT_TEMPLATE1.format(ASR=ASR, FR=FR, NFR=NFR, DC=DC, AV=AV, RK=reference_knowledge)
        # print(prompt1)
        rsp = await self._aask(prompt1)
        file_path = self.file_name("AD")
        with file_path.open("w", encoding='utf-8') as f:
            f.write(rsp)
    
    @classmethod
    def file_name(cls,name:str) -> str:
        output_dir = cls.output_root
        output_dir.mkdir(parents=True, exist_ok=True)
        if name == "AD":
            file_name = f"AD.txt"
            file_path = output_dir / file_name
        return file_path

class Desiner(Role):
    name: str = "Agent3"
    profile: str = "Designer"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([Designinng])

    async def _act(self):
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo  # todo will be SimpleWriteCode()
        msg = self.get_memories(k=1)[0]  # find the most recent messages
        json_dict = eval(msg.content)
        await todo.run(json_dict["ASR"], json_dict["FR"], json_dict["NFR"], json_dict["DC"], json_dict["AV"])

async def main():
    with open("config.json", "r", encoding='utf-8') as f:
        config = json.load(f)
    input_file = config["input_file"]
    file_name = os.path.basename(input_file).split(".")[0]
    output_root = Path("output//" + file_name.split(".")[0] + "//Designer")
    Designinng.set_output_root(output_root)
    with open(".\\output\\" + file_name.split(".")[0] + "\\Analyst\\ASR.txt", 'r', encoding='utf-8') as f:
        ASR = f.read()
    with open(".\\output\\" + file_name.split(".")[0] + "\\Analyst\\FR.txt", 'r', encoding='utf-8') as f:
        FR = f.read()
    with open(".\\output\\" + file_name.split(".")[0] + "\\Analyst\\NFR.txt", 'r', encoding='utf-8') as f:
        NFR = f.read()
    with open(".\\output\\" + file_name.split(".")[0] + "\\Analyst\\DC.txt", 'r', encoding='utf-8') as f:
        DC = f.read()
    with open(".\\output\\" + file_name.split(".")[0] + "\\Modeler\\AV.txt", 'r', encoding='utf-8') as f:
        AV = f.read()
    json_dict = {"ASR":ASR, "FR":FR, "NFR":NFR, "DC":DC, "AV": AV}
    json_str = str(json_dict)
    role = Desiner()
    result = await role.run(json_str)
    logger.info(result)

asyncio.run(main())