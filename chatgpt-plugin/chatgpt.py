import json
import openai
import pynvim
from pathlib import Path


@pynvim.plugin
class ChatGPTPlugin(object):
    """
    A plugin that allows chatting with OpenAI's GPT-3 chatbot in Neovim's terminal using the 'ChatGPT' command or in a vertical split using the 'ChatGPTsplit' command. The plugin requires an API key which is obtained from a 'chatgpt_config.json' file in the same directory.

    Args:
        nvim (pynvim): A Neovim instance.

    Returns:
        None.
    """

    def __init__(self, nvim):
        self.nvim = nvim
        config_file = Path(__file__).resolve().parent / "chatgpt_config.json"
        data = json.loads(config_file.read_text())
        self.api_key = data["OPENAI_API_KEY"]

    @pynvim.command("ChatGPT", nargs="*", range="", sync=True)
    def chatgpt_command(self, args, range):
        completion = self.get_completion(args, range)

        # add a newline before and after the completion
        completion = f"\n{completion.strip()}\n\n"

        # get the current cursor position
        row, col = self.nvim.current.window.cursor

        # split the completion into lines and append each line
        for i, line in enumerate(completion.split("\n")):
            insert_row = row if range is None else range[1]
            self.nvim.current.buffer.append(line, insert_row + i)

        # move the cursor to the end of the inserted text
        self.nvim.current.window.cursor = (row + len(completion.split("\n")), col)

    @pynvim.command("ChatGPTsplit", nargs="*", range="", sync=True)
    def chatgpt_split_command(self, args, range):
        completion = self.get_completion(args, range)

        # create a new vertical split
        self.nvim.command("vnew")
        self.nvim.command("wincmd x")
        self.nvim.command("wincmd l")
        self.nvim.current.buffer.options["buftype"] = "nofile"

        # split the completion into lines and append each line
        for i, line in enumerate(completion.split("\n")):
            self.nvim.current.buffer.append(line, i)

        # move the cursor back to the original window
        self.nvim.command("wincmd h")

    def get_completion(self, args, range):
        # set the API key
        openai.api_key = self.api_key

        # If a range is specified, get the selected text
        selected_text = ""
        if range:
            selected_text = "\n".join(self.nvim.current.buffer[range[0] - 1 : range[1]])

        if len(args) > 0:
            prompt = f"{selected_text}\n{' '.join(args)} "
        else:
            prompt = selected_text

        # create a chat completion
        if len(prompt) < 12000:  # 12'000 chars are about 3000 tokens.
            chat_completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
            )
        else:
            chat_completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                messages=[{"role": "user", "content": prompt}],
            )

        # get the chat completion
        result = chat_completion["choices"][0]["message"]["content"]

        return result
