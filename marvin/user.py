import inquirer, subprocess, readline
from inquirer.themes import GreenPassion
from .fine_tune_data import FineTuneData
from . import config

class User:
  def __init__(self, txt_input, history_path_name = None):
    self.txt_input = txt_input
    self.FineTuneData = FineTuneData(history_path_name) if history_path_name else FineTuneData()
  
  def init(self):
    errors = []
    if(self.get_input()):

      error = self.FineTuneData.error()
      if(error):
        errors.append(error)

      if(len(config.get('OPENAI_API_KEY')) == 0):
        errors.append('OpenAI API key has not been configured. Please run the command:\n    marvin --add-openai-key <key>')

      if(errors):
        return errors
      else:
        return True
    else:
      return False
  
  def get_input(self):
    if(len(self.txt_input) <= 1):
      return False

    txt_input = ""
    for i, word in enumerate(self.txt_input[1:], start=0):
      txt_input += ' ' + word

    return txt_input.strip()
  
  def set_feedback(self):
    answers = inquirer.prompt([
      inquirer.List(
        "action",
        message="Your choice",
        choices=["Run command", "Tweak the command", "Quit"],
      ),
    ], theme=GreenPassion())
    return answers and answers['action']
  
  def run_command(self, bash_command):
    bash_command = bash_command.strip()

    print(' [ Run command ] $ ' + bash_command)
    result = subprocess.run(bash_command.split(), stdout=subprocess.PIPE)
    print(result.stdout.decode('utf-8').strip())

    self.FineTuneData.save(self.get_input(), bash_command)
    
    if(result.stderr):
      print(' [ error ] ')
      print(result.stderr)

  def tweak_the_command(self, placeholder):
    
    def rlinput(self, prefill=''):
      readline.set_startup_hook(lambda: readline.insert_text(prefill))
      try:
        return input(self)
      finally:
        readline.set_startup_hook()

    correction = rlinput(' [ Tweak the command ] $ ', placeholder)
    return correction