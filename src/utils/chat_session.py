"""
contains only the implementation of ChatHandler
"""

# external imports
import openai
from typing import Dict, List, Tuple
import json

instruct_models = [
    'Phind/Phind-CodeLlama-34B-v2',
    'WizardLM/WizardCoder-Python-7B-V1.0',
    'WizardLM/WizardCoder-Python-13B-V1.0',
    'WizardLM/WizardCoder-Python-34B-V1.0',
    'codellama/CodeLlama-7b-Instruct-hf',
    'codellama/CodeLlama-13b-Instruct-hf',
    'codellama/CodeLlama-34b-Instruct-hf',
    'Salesforce/codegen25-7b-instruct',
    'Salesforce/instructcodet5p-16b',
    'mistralai/Mistral-7B-Instruct-v0.1',
    'lmsys/vicuna-7b-v1.5',
    'lmsys/vicuna-7b-v1.5-16k',
    'lmsys/vicuna-13b-v1.5',
    'lmsys/vicuna-13b-v1.5-16k',
]

completion_models = [
    'bigcode/santacoder', # other versions exist
    'bigcode/starcoder',
    'bigcode/starcoderplus',
    'codellama/CodeLlama-7b-hf',
    'codellama/CodeLlama-13b-hf',
    'codellama/CodeLlama-34b-hf',
    'Salesforce/codegen-2B-multi',
    'Salesforce/codegen-2B-nl',
    'Salesforce/codegen-6B-multi',
    'Salesforce/codegen-6B-nl',
    'Salesforce/codegen-16B-multi',
    'Salesforce/codegen-16B-nl',
    'Salesforce/codegen2-1B',
    'Salesforce/codegen2-3_7B',
    'Salesforce/codegen2-7B',
    'Salesforce/codegen2-16B',
    'Salesforce/codet5p-2b', # not sure
    'Salesforce/codet5p-6b', # not sure
    'Salesforce/codet5p-16b', # not sure
    'mistralai/Mistral-7B-v0.1'
    'facebook/incoder-1B',
    'facebook/incoder-6B',
    'EleutherAI/gpt-j-6b',
    'EleutherAI/gpt-neo-2.7B',
    'NinedayWang/PolyCoder-2.7B',
    'stabilityai/stablelm-base-alpha-7b-v2', # not sure
]

class ChatSession:
    """
    This class is used to automatically keep track of ChatGPT sessions.
    Handles single-shot and multi-shot prompts
    """
    
    def __init__(
        self,
        key: str,
        org: str=None,
        model: str='gpt-3.5-turbo',
        system_msg: str=None
    ):
        
        # initialize OpenAI API
        openai.api_key = key
        openai.organization = org
        
        # assign session variables
        self.model_name = model
        self.system_msg = system_msg
        self.msg_history = \
            [] if system_msg is None \
            else [{
                'role' : 'system',
                'content' : system_msg
            }]

        sys_msg_len = 0 if system_msg is None else len(system_msg.split())
        self.usage = {
            'completion_tokens' : 0,
            'prompt_tokens' : sys_msg_len,
            'total_tokens' : sys_msg_len,
        }

    def __call__(self, message: str):
        """
        wraps the get_response() function
        """
        return self.get_response(message)

    def __str__(self):
        """
        returns the message history as a JSON formatted string
        """
        return json.dumps(self.msg_history, indent=4)

    def get_response(self, message):
        """
        sends a message to openai and retrieves the response(s).
        response is saved to chat history. get history by calling <obj>.history()
        if message is passed as a List[str] then multi-shot prompting is performed.
        Otherwise single-shot prompting is used. The corresponding responses are returned.

        :param message: the message to be sent. 
        :type message: List[str] or str

        :param multi_shot: determines if the multi-shot procedure. (Default: False)
        :type multi_shot: bool

        :return: the response from chatgpt
        :type return: str or List[str]
        """

        # convert to single element list if is a single-shot message
        if isinstance(message, str):
            message = [message]

        responses = []
        for msg in message:
            # append message to history
            self.msg_history.append({
                'role' : 'user',
                'content' : msg
            })

            # make api call
            resp = openai.ChatCompletion.create(
                model=self.model_name,
                messages=self.msg_history
            )

            # append response to history
            responses.append(resp['choices'][0]['message']['content'])
            self.msg_history.append({
                'role' : 'assistant',
                'content' : resp['choices'][0]['message']['content']
            })
            
            # update usage statistics
            self.usage = json.loads(str(resp['usage']))
        
        
        if len(responses) == 1:
            return responses[0]
        else:
            return responses

    def get_history(self) -> List[Dict[str, str]]:
        """
        returns the message history

        :return: List[Dict[str, str]]
        """
        return self.messages

    def get_usage(self) -> Dict[str, int]:
        """
        returns the usage statistics of the current session

        :return: Dict[str, str]
        """
        return self.usage
