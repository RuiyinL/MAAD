import subprocess

scripts = [
    "agents/analyst.py",
    "agents/modeler.py",
    "agents/designer.py",
    "agents/evaluator.py",
]

for script in scripts:
    print(f"Running {script}...")
    subprocess.run(["python", script])
    print(f"Finished running {script}.")
    print("-" * 40)