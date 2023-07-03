## this handles saving and loading of chats
import apiUtils
import unicodedata
import re

def saveChat(chat):

    ## convert chat to string
    import json
    chat_string = json.dumps(chat)
    length = len(chat_string)
    ## 4 chars = 1 token
    tokenapprox = length / 4
    if tokenapprox > 4097:
        ## take last 4097 tokens
        chat_string = chat_string[-3800:]

    # get name for chat

    prompt = "This is a portion of a chat with an AI assistant. Give it a name that is informative to what the conversation as a whole is about, without refering to the fact it is a AI Conversation with an assistant in any way. The conversation may have been truncated at any point, however use the context of the conversation to give it a name that is informative. The name will become a filename so ensure it contains no spaces or illegal characters. Make sure the name is very brief and at maximum 30 characters."
    prompt = "I want you to act as a filename generator that takes a chatGPT conversation and summarises it into a concise yet informative file name. The filename should not only include the subject title, but also provide a brief overview of what was discussed in the conversation. Consider the keywords and main points of the conversation to create an accurate and effective summary. Follow any or all file nameing conventions you think are appropriate. In addition, dont include any filename extensions such as .txt or .docx, and the name must be at maximum 30 characters."
    nameChat = [{"role": "system", "content": prompt}]
    ## remove all special characters other than {, }, :

    ptChat = ""
    for line in chat:
        role = line["role"]
        content = line["content"]
        ptChat += role + ": " + content + "\n"

    nameChat.append({"role": "user", "content": ptChat})

    name = apiUtils.getCompletion("gpt-3.5-turbo-16k", nameChat)
    name = slugify(name)

    # check to see if name already exists
    from os import path
    if path.isfile("chats/" + name + ".txt"):
        print("Chat with this name already exists")
        return False
    print(name)
    file = open("chats/" + name + ".txt", "w", encoding="utf-8")
    for line in chat:
        file.write(line["role"] + ": " + line["content"] + "\n")
    file.close()
    ## check if file exists
    ## if not, an error occured


    if not path.isfile("chats/" + name + ".txt"):
        print("Error saving chat")
        return False
    else:
        return True



def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')










