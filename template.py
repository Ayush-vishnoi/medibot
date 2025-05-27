import os
from pathlib import Path
import logging
logging.basicConfig(level=logging.INFO,format='[%(asctime)s]: %(message)s:')

list_of_file=[
    "src/__init__.py",
    "src/helper.py",
    "src/prompt.py",
    ".env",
    "setup.py",
    "app.py",
    "research/trial.ipynb"
]
for filepath in list_of_file:
    filepath=Path(filepath)
    filedir,filenmae=os.path.split(filepath)

    if filedir!="":
        os.makedirs(filedir,exist_ok=True)
        logging.info(f"create directory {filedir} for the file:{filenmae}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath)==0):
        with open(filepath,"w") as f:
            pass
        logging.info(f"create empty file: {filepath}")
    else:
        logging.info(f"file {filepath} is already exist")