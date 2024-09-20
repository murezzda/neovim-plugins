import json
import pynvim
from pathlib import Path
from openai import AzureOpenAI


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
        self.model = data["MODEL_VERSION"]
        self.openai_client = AzureOpenAI(
            api_key=data["AZURE_OPENAI_KEY"],
            api_version=data["AZURE_OPENAI_VERSION"],
            azure_endpoint=data["AZURE_OPENAI_ENDPOINT"],
        )

    @pynvim.command("ChatGPT", nargs="*", range="", sync=True)  # pyright: ignore
    def chatgpt_split_command(self, args, range):
        self.query_chatgpt_new_window("", args, range)

    @pynvim.command("GPTcomment", nargs="*", range="", sync=True)  # pyright: ignore
    def chatgpt_comment_command(self, args, range):
        prompt = "Create a google style docstring for this function."
        self.query_chatgpt_new_window(prompt, args, range)

    @pynvim.command("GPTtest", nargs="*", range="", sync=True)  # pyright: ignore
    def chatgpt_unittest_command(self, args, range):
        prompt = "Create a pytest unit test for this function."
        self.query_chatgpt_new_window(prompt, args, range)

    @pynvim.command("GPTexplain", nargs="*", range="", sync=True)  # pyright: ignore
    def chatgpt_explain_command(self, args, range):
        prompt = "Explain this code to me."
        self.query_chatgpt_new_window(prompt, args, range)

    def query_chatgpt_new_window(self, prompt, args, range):
        completion = self.get_completion(args, prompt, range)

        self.create_vertical_split()

        # split the completion into lines and append each line
        for i, line in enumerate(completion.split("\n")):
            self.nvim.current.buffer.append(line, i)

        # move the cursor back to the original window
        self.nvim.command("wincmd h")

    def create_vertical_split(self):
        # create a new vertical split
        self.nvim.command("vnew")
        self.nvim.command("wincmd x")
        self.nvim.command("wincmd l")
        self.nvim.current.buffer.options["buftype"] = "nofile"

    def get_completion(self, args, prompt, range) -> str:
        # If a range is specified, get the selected text
        selected_text = ""
        if range:
            selected_text = "\n".join(self.nvim.current.buffer[range[0] - 1 : range[1]])

        if len(args) > 0:
            prompt += f"\n{selected_text}\n{' '.join(args)}"
        else:
            prompt += f"\n{selected_text}"

        # create a chat completion
        chat_completion = self.openai_client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4096,
        )

        # get the chat completion
        result = chat_completion.choices[0].message.content

        if result is None:
            result = "Warning: Unable to access chatgpt result."

        return f"Question:\n{prompt}\n\nResult:\n{result}"
