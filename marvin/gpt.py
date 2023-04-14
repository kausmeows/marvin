import os, openai
from . import config
from utils import logs, prompt
from .fine_tune_data import FineTuneData

def generate_bash(user_input):
  logs.debug('openai.generate_bash("' + user_input + '"): ')
  answer = "\nA:"
  question = "\nQ: "

  openai.api_key = config.get('OPENAI_API_KEY')
  openai.organization = os.getenv('ORG')
  history = FineTuneData()

  prompt_content = prompt.PROMPT_FOR_GPT
  prompt_content += history.get_ques_ans()
  prompt_content += question + user_input + answer

  try:
    output = openai.Completion.create(
      engine="text-davinci-003",
      prompt=prompt_content,
      temperature=0.5,
      max_tokens=100,
      top_p=1,
      frequency_penalty=0.2,
      presence_penalty=0,
      stop=["\n"]
    )
    
    logs.debug(prompt_content + output.choices[0].text)
    return output.choices[0].text

  except openai.error.AuthenticationError as e:
    logs.error['arg']('[ OpenAI ] : ' + str(e))
    return False