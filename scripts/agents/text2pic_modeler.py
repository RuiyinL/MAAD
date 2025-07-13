from plantweb.render import render
import re
import os
import json
import time

if __name__ == '__main__':
    with open("config.json", "r") as f:
        config = json.load(f)
    input_file = config["input_file"]
    file_name = os.path.basename(input_file).split(".")[0]
    diagrams_name = {"Logic_View":["Class Diagram", "Object Diagram", "State Diagram"],
                    "Development_View":["Package Diagram", "Component Diagram"],
                    "Process_View":["Activity Diagram", "Sequence Diagram", "Collaboration Diagram"],
                    "Physical_View":["Deployment Diagram", "Container Diagram"],
                    "Scenario_View":["Use Case Diagram"]}
    with open("C:\\Research\\MAAD\\demo\\demo_v4\\output\\" + file_name +"\\Modeler\\AV.txt",encoding='utf-8') as f:
        content = f.read()
    uml_matches = re.findall(r"@startuml(.*?)@enduml",  content, re.DOTALL)
    expected_diagram_count = sum(len(v) for v in diagrams_name.values())
    if len(uml_matches) != expected_diagram_count:
        print(f"Warning: Expected {expected_diagram_count} diagrams, but found {len(uml_matches)}.")
    index = 0
    for view, diagrams in diagrams_name.items():
        for diagram in diagrams:
            uml_content = f"@startuml{uml_matches[index]}@enduml"
            try:
                output = render(
                    uml_content,
                    engine='plantuml',
                    format='svg',
                    cacheopts={
                        'use_cache': False
                    })
            except Exception as e:
                index = index + 1
                print(f"Error rendering diagram {view} - {diagram}: {e}")
                continue
            rootname = os.path.join(
                r"C:\\Research\\MAAD\\demo\\demo_v4\\output\\",
                file_name.split(".")[0],
                "Modeler",
                f"{view}_{diagram.replace(' ', '_')}.svg"
            )
            print(rootname)
            time.sleep(1)
            os.makedirs(os.path.dirname(rootname), exist_ok=True)
            with open(rootname, "wb") as f:
                f.write(output[0])
            index = index + 1