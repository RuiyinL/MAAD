from metagpt.actions import Action
from pathlib import Path
from metagpt.roles import Role
import asyncio
from metagpt.logs import logger
from metagpt.schema import Message
import json
import os
import time
import os
from langchain_community.vectorstores import LanceDB
from langchain_openai import OpenAIEmbeddings
import lancedb

os.environ["OPENAI_API_KEY"] = "[OpenAI API Key]"
embedding_function = OpenAIEmbeddings()
db = lancedb.connect("~/langchain")
table = db.open_table("vectorstore")

class Modeling(Action):
    #architectural views
    PROMPT_TEMPLATE1: str = """"
    Here are: \n
    (1) architecturally significant requirements: {ASR}\n
    (2) functional requirements: {FR}\n
    (3) non-functional requirements: {NFR}\n
    (4) design constraints: {DC}\n
    (5) reference knowledge: {RK}\n

    Based on the provided requirements, please generate "Logic View" using PlantUML syntax. Ensure that your PlantUML syntax is correct and that the diagrams are clear and informative.
    Logical Views:\n
        (1) Class Diagram: Focus on defining classes, their attributes, methods, and relationships such as inheritance, associations, compositions, and aggregations. Use appropriate visibility modifiers (+, -, #) and ensure that the diagram captures key object-oriented principles.
        (2) Object Diagram: Show objects and their concrete values, along with relationships between objects based on a given scenario. Ensure that instances of classes are properly labeled and connected to demonstrate how objects interact in a particular state.
        (3) State Diagram: represent the different states of an object in the system and the transitions between these states. Include entry/exit points, guard conditions, and state transitions triggered by events. Ensure the diagram clearly illustrates the lifecycle of an object.

    Tips:
    (1) When defining object instances in PlantUML, avoid specifying the type by appending : className to the object name. For example, instead of writing object ivm1 : InputValidationModule, just use object ivm1 and list only the methods associated with that object. Do not include the class name in the object definition.\n
    (2) When you want to define a "container", use "artifact" instead.\n
    (3) In Collaboration Diagram, if you want to define a "object", use "participant" instead.\n
    (4) Ensure that all UML diagrams clearly illustrate the specified concepts and relationships. Additionally, any provided UML representations must be syntactically correct according to PlantUML conventions.\n

    Structure your outputs as follows:
    Logical View:
    1 Class Diagram
    [PlantUML]
    2 Object Diagram
    [PlantUML]
    3 State Diagram
    [PlantUML]
    """

    PROMPT_TEMPLATE2: str = """"
    Here are: \n
    (1) architecturally significant requirements: {ASR}\n
    (2) functional requirements: {FR}\n
    (3) non-functional requirements: {NFR}\n
    (4) design constraints: {DC}\n
    (5) reference knowledge: {RK}\n

    Based on the provided requirements, please generate "Development View" using PlantUML syntax. Ensure that your PlantUML syntax is correct and that the diagrams are clear and informative.
    Development View:\n
        (1) Package Diagram: represent the modular structure of the system. Show the organization of code into packages, their dependencies, and hierarchical relationships. Use appropriate visibility settings for package components and ensure a clear representation of the software’s structure.
        (2) Component Diagram: illustrate the high-level software components and their dependencies. Show how different components interact, including provided and required interfaces, to depict the system’s modularity and reusability.

    Tips:
    (1) When defining object instances in PlantUML, avoid specifying the type by appending : className to the object name. For example, instead of writing object ivm1 : InputValidationModule, just use object ivm1 and list only the methods associated with that object. Do not include the class name in the object definition.\n
    (2) When you want to define a "container", use "artifact" instead.\n
    (3) In Collaboration Diagram, if you want to define a "object", use "participant" instead.\n
    (4) Ensure that all UML diagrams clearly illustrate the specified concepts and relationships. Additionally, any provided UML representations must be syntactically correct according to PlantUML conventions.\n

    Structure your outputs as follows:
    Development View:
    1 Package Diagram
    [PlantUML]
    2 Component Diagram
    [PlantUML]
    """

    PROMPT_TEMPLATE3: str = """"
    Here are: \n
    (1) architecturally significant requirements: {ASR}\n
    (2) functional requirements: {FR}\n
    (3) non-functional requirements: {NFR}\n
    (4) design constraints: {DC}\n
    (5) reference knowledge: {RK}\n

    Based on the provided requirements, please generate "Process View" using PlantUML syntax. Ensure that your PlantUML syntax is correct and that the diagrams are clear and informative.
    Process View:\n
        (1) Activity Diagram: represent a dynamic workflow or business process within the system. Use start and end nodes, actions, decisions, and control flows to illustrate a specific process execution path.
        (2) Sequence Diagram: depict the interaction between system components over time. Show lifelines, messages, and activation boxes to illustrate how objects communicate during a particular scenario.
        (3) Collaboration Diagram: represent the structural organization of objects interacting within a system. Focus on object roles, their communication, and how messages are exchanged among them.

    Tips:
    (1) When defining object instances in PlantUML, avoid specifying the type by appending : className to the object name. For example, instead of writing object ivm1 : InputValidationModule, just use object ivm1 and list only the methods associated with that object. Do not include the class name in the object definition.\n
    (2) When you want to define a "container", use "artifact" instead.\n
    (3) In Collaboration Diagram, if you want to define a "object", use "participant" instead.\n
    (4) Instead of using "repeat", you should use "loop" to wrap the loop and use "alt" to handle conditional checks inside the loop. "loop" represents the iteration process, while "alt" is used to evaluate conditions and handle branching, ensuring clear and controlled condition checking.\n
    (5) Ensure that all UML diagrams clearly illustrate the specified concepts and relationships. Additionally, any provided UML representations must be syntactically correct according to PlantUML conventions.\n

    Structure your outputs as follows:
    Process View:
    1 Activity Diagram
    [PlantUML]
    2 Sequence Diagram
    [PlantUML]
    3 Collaboration Diagram
    [PlantUML]
    """

    PROMPT_TEMPLATE4: str = """"
        Here are: \n
    (1) architecturally significant requirements: {ASR}\n
    (2) functional requirements: {FR}\n
    (3) non-functional requirements: {NFR}\n
    (4) design constraints: {DC}\n
    (5) reference knowledge: {RK}\n

    Based on the provided requirements, please generate "Physical View" using PlantUML syntax. Ensure that your PlantUML syntax is correct and that the diagrams are clear and informative.
    Physical View:\n
        (1) Deployment Diagram: model the physical deployment of system components across hardware nodes. Show servers, devices, execution environments, and their communication links.
        (2) Container Diagram: represent the high-level software architecture, including applications, databases, APIs, and their interactions. Illustrate how containers (e.g., microservices, web servers) are structured within the system.

    Tips:
    (1) When defining object instances in PlantUML, avoid specifying the type by appending : className to the object name. For example, instead of writing object ivm1 : InputValidationModule, just use object ivm1 and list only the methods associated with that object. Do not include the class name in the object definition.\n
    (2) When you want to define a "container", use "artifact" instead.\n
    (3) In Collaboration Diagram, if you want to define a "object", use "participant" instead.\n
    (4) Ensure that all UML diagrams clearly illustrate the specified concepts and relationships. Additionally, any provided UML representations must be syntactically correct according to PlantUML conventions.\n

    Structure your outputs as follows:
    Physical View:
    1 Deployment Diagram
    [PlantUML]
    2 Container Diagram
    [PlantUML]
    """

    PROMPT_TEMPLATE5: str = """"
    Here are: \n
    (1) architecturally significant requirements: {ASR}\n
    (2) functional requirements: {FR}\n
    (3) non-functional requirements: {NFR}\n
    (4) design constraints: {DC}\n
    (5) reference knowledge: {RK}\n

    Based on the provided requirements, please generate "Scenario View" using PlantUML syntax. Ensure that your PlantUML syntax is correct and that the diagrams are clear and informative.
    Scenario View:\n
        (1) Use Case Diagram: illustrate how users interact with the system. Include actors, use cases, and relationships such as includes, extends, and associations to represent system functionality from a user perspective.
    
    Tips:
    (1) When defining object instances in PlantUML, avoid specifying the type by appending : className to the object name. For example, instead of writing object ivm1 : InputValidationModule, just use object ivm1 and list only the methods associated with that object. Do not include the class name in the object definition.\n
    (2) When you want to define a "container", use "artifact" instead.\n
    (3) In Collaboration Diagram, if you want to define a "object", use "participant" instead.\n
    (4) Ensure that all UML diagrams clearly illustrate the specified concepts and relationships. Additionally, any provided UML representations must be syntactically correct according to PlantUML conventions.\n

    Structure your outputs as follows:
    Scenario View:
    1 Use Case Diagram
    [PlantUML]
    """

    PROMPT_TEMPLATE6: str = """"
    Here are: \n
    (1) architecturally significant requirements: {ASR}\n
    (2) functional requirements: {FR}\n
    (3) non-functional requirements: {NFR}\n
    (4) design constraints: {DC}\n
    (5) reference knowledge: {RK}\n

    Based on the provided requirements, please record the architectural decisions (Record key architectural decisions, selected alternatives and their trade-offs, helping the team understand the reasons behind the decisions and providing reference for possible subsequent adjustments) to explain the design choices made in response to the provided requirements and constraints.
    
    Structure your outputs as follows:
    Architectural Decisions:xxx
    """

    name: str = "Modeling"

    output_root : Path = Path("output//Modeler")

    @classmethod
    def set_output_root(cls, output_root: Path):
        cls.output_root = output_root

    async def run(self, ASR: str, FR: str, NFR: str, DC: str):
        prompt1 = self.PROMPT_TEMPLATE1.format(ASR = ASR, FR = FR, NFR = NFR, DC = DC, RK = "")
        prompt2 = self.PROMPT_TEMPLATE2.format(ASR = ASR, FR = FR, NFR = NFR, DC = DC, RK = "")
        prompt3 = self.PROMPT_TEMPLATE3.format(ASR = ASR, FR = FR, NFR = NFR, DC = DC, RK = "")
        prompt4 = self.PROMPT_TEMPLATE4.format(ASR = ASR, FR = FR, NFR = NFR, DC = DC, RK = "")
        prompt5 = self.PROMPT_TEMPLATE5.format(ASR = ASR, FR = FR, NFR = NFR, DC = DC, RK = "")
        prompt6 = self.PROMPT_TEMPLATE6.format(ASR = ASR, FR = FR, NFR = NFR, DC = DC, RK = "")
        rsp1 = ""
        while not rsp1:
            query = embedding_function.embed_query(prompt1)
            docs = table.search(query, query_type="vector").limit(3).to_pandas()["text"].to_list()
            reference_knowledge = " ".join(docs)
            prompt1 = self.PROMPT_TEMPLATE1.format(ASR = ASR, FR = FR, NFR = NFR, DC = DC, RK = reference_knowledge)
            rsp1 = await self._aask(prompt1)
        rsp2 = ""
        while not rsp2:
            query = embedding_function.embed_query(prompt2)
            docs = table.search(query, query_type="vector").limit(3).to_pandas()["text"].to_list()
            reference_knowledge = " ".join(docs)
            prompt2 = self.PROMPT_TEMPLATE2.format(ASR = ASR, FR = FR, NFR = NFR, DC = DC, RK = reference_knowledge)
            rsp2 = await self._aask(prompt2)
        rsp3 = ""
        while not rsp3:
            query = embedding_function.embed_query(prompt3)
            docs = table.search(query, query_type="vector").limit(3).to_pandas()["text"].to_list()
            reference_knowledge = " ".join(docs)
            prompt3 = self.PROMPT_TEMPLATE3.format(ASR = ASR, FR = FR, NFR = NFR, DC = DC, RK = reference_knowledge)
            rsp3 = await self._aask(prompt3)
        rsp4 = ""
        while not rsp4:
            query = embedding_function.embed_query(prompt4)
            docs = table.search(query, query_type="vector").limit(3).to_pandas()["text"].to_list()
            reference_knowledge = " ".join(docs)
            prompt4 = self.PROMPT_TEMPLATE4.format(ASR = ASR, FR = FR, NFR = NFR, DC = DC, RK = reference_knowledge)
            rsp4 = await self._aask(prompt4)
        rsp5 = ""
        while not rsp5:
            query = embedding_function.embed_query(prompt5)
            docs = table.search(query, query_type="vector").limit(3).to_pandas()["text"].to_list()
            reference_knowledge = " ".join(docs)
            prompt5 = self.PROMPT_TEMPLATE5.format(ASR = ASR, FR = FR, NFR = NFR, DC = DC, RK = reference_knowledge)
            rsp5 = await self._aask(prompt5)
        
        rsp6 = ""
        while not rsp6:
            query = embedding_function.embed_query(prompt6)
            docs = table.search(query, query_type="vector").limit(3).to_pandas()["text"].to_list()
            reference_knowledge = " ".join(docs)
            prompt6 = self.PROMPT_TEMPLATE6.format(ASR = ASR, FR = FR, NFR = NFR, DC = DC, RK = reference_knowledge)
            rsp6 = await self._aask(prompt6)
        file_path = self.file_name("AV")
        with file_path.open("w", encoding='utf-8') as f:
            f.write(rsp1+rsp2+rsp3+rsp4+rsp5+rsp6)

    
    @classmethod
    def file_name(cls, name : str) -> str:
        output_dir = cls.output_root
        output_dir.mkdir(parents=True, exist_ok=True)
        if name == "AV":
            file_name = f"AV.txt"
            file_path = output_dir / file_name
        elif name == "Verified_AV":
            file_name = f"Verified_AV.txt"
            file_path = output_dir / file_name
        return file_path

class Modeler(Role):
    name: str = "Agent2"
    profile: str = "Modeler"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_actions([Modeling])

    async def _act(self):
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo  # todo will be SimpleWriteCode()
        msg = self.get_memories(k=1)[0]  # find the most recent messages
        json_dict = eval(msg.content)
        await todo.run(json_dict["ASR"], json_dict["FR"], json_dict["NFR"], json_dict["DC"])

async def main():
    with open("config.json", "r", encoding='utf-8') as f:
        config = json.load(f)
    input_file = config["input_file"]
    file_name = os.path.basename(input_file).split(".")[0]
    output_root = Path("output//" + file_name.split(".")[0] + "//Modeler")
    Modeling.set_output_root(output_root)
    path = ".\\output" + "\\" + file_name + "\\Analyst"
    with open(path+"\\ASR.txt", encoding='utf-8') as f:
        ASR = f.read()
    with open(path + "\\FR.txt", encoding='utf-8') as f:
        FR = f.read()
    with open(path + "\\NFR.txt", encoding='utf-8') as f:
        NFR = f.read()
    with open(path + "\\DC.txt", encoding='utf-8') as f:
        DC = f.read()
    json_mag = {"ASR":ASR, "FR":FR, "NFR":NFR, "DC":DC}
    json_str = str(json_mag)
    role = Modeler()
    result = await role.run(json_str)
    logger.info(result)

asyncio.run(main())