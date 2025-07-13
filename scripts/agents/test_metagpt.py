from metagpt.software_company import generate_repo
from metagpt.utils.project_repo import ProjectRepo
import os
import json
from pathlib import Path

with open("config.json", "r", encoding='utf-8') as f:
    config = json.load(f)
input_file = config["input_file"]
file_name = os.path.basename(input_file).split(".")[0]
output_root = Path("output//" + file_name.split(".")[0] + "//MetaGPT")
with open(input_file, "r", encoding='utf-8') as f:
    input_text = f.read()
repo: ProjectRepo = generate_repo(input_text)
print(repo)  # it will print the repo structure with files