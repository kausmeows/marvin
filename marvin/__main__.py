import sys
from .user import User
from . import gpt, config
from utils import logs

def main():
  if(len(sys.argv) > 1 and sys.argv[1] == '--add-openai-key'):
    add_openai_key(sys.argv)
  else:
    run(sys.argv)

def run(argv):
  logs.debug('[Debug mode]')

  user = User(argv)
  status = user.init()
  if(status == True):
    user_input = user.get_input()

    bash_result = gpt.generate_bash(user_input)

    if(bash_result):
      print('\n$ ' + bash_result + '\n')
      feedback = user.set_feedback()

      if (feedback == 'Run command'):
        user.run_command(bash_result)
      elif (feedback == 'Tweak the command'):
        user.run_command(user.tweak_the_command(bash_result))
      elif (feedback == 'Quit'):
        pass
    else:
      print('\nUsage: marvin --add-openai-key <key>\n')
  elif(status == False):
    logs.error['arg']('Please provide an input, ex: python marvin.py turn off the bluetooth')
  else:
    logs.error['config'](status)

def add_openai_key(argv):
  if len(argv) <= 2:
    logs.error['arg']('No key provided.')
  else:
    config.set('OPENAI_API_KEY', argv[2])
    print('OpenAI API Key added.')

if __name__ == '__main__':
  main()