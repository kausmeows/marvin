import os, sys, toml
from dotenv import load_dotenv

load_dotenv()

FILE_NAME = os.path.abspath(os.path.dirname(sys.argv[0])) + '/cliGPT.toml'

DEFAULT_CONFIG = {
  "OPENAI_API_KEY": os.getenv('OPENAI_API_KEY'),
  "HISTORY_FILE_NAME": ".cliGPT-history",
  "DEBUG": True
}

def load_file():
  if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w+") as file:
      file.write(toml.dumps(DEFAULT_CONFIG))
    return DEFAULT_CONFIG
  else:
    return toml.load(FILE_NAME)

def get(var):
  return load_file()[var]

def set(var, value):
  data = load_file()
  data[var] = value
  with open(FILE_NAME, "w") as file:
    file.write(toml.dumps(data))