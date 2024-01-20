import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

client =  AzureOpenAI(
    # https://learn.microsoft.com/en-us/azure/ai-services/openai/reference#rest-api-versioning
    api_version="2023-07-01-preview",
    # https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/create-resource?pivots=web-portal#create-a-resource
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    

)

model_instance = os.getenv("AZURE_OPENAI_GPT4_DEPLOYMENT_NAME")



prompt_template = '''

you are a educational content creator and you are trying to explain the following complicated concept to a general audience . Please

extract key information and then simplify and summarize the following text:\n\n
{context}


output the simplified text below as a narration script for voice over in the following format:\n\n

[start]

[scene number]
[emphasis words:]
[dalle prompt: ]
[scene start]

[scene end]
[scene transition]

[end]

YOU MUST FOLLOW THESE RULES FOR THE OUTPUT TO BE CORRECTLY FORMATTED:
1.add a transition between each key piece of information
2. you have to extract a minimum of 3 emphasis words from the text and add them to the narration script that are dramatic 
3. generate a prompt for a image that best represents the concept of the scene and add it to the narration script

''' 