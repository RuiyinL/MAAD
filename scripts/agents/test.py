import asyncio

from metagpt.rag.engines import SimpleEngine
from metagpt.const import EXAMPLE_DATA_PATH


DOC_PATH = "C:\\Research\\MAAD\\demo\\demo_v4\\agents\\rag\\software-architecture-in-practice-4th-edition.pdf"

async def main():
    engine = SimpleEngine.from_docs(input_files=[DOC_PATH])
    answer = await engine.aquery("What does Bob like?")
    print(answer)

if __name__ == "__main__":
    asyncio.run(main())