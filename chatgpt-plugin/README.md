# ChatGPT for Neovim
This is a Neovim plugin, written in Python, that allows users to interact with OpenAI's ChatGPT directly from the Neovim editor. It provides an inline completion feature, the possibility to open a new scratch window for the response, and can use highlighted text in visual mode as part of the prompt for the AI.

## Features
- Inline completions using `:ChatGPT` command
- Open a new scratch window with response using `:ChatGPTsplit` command
- Use highlighted text in visual mode as part of the AI's prompt

## Installation

Copy chatgpt.py to the Neovim remote plugin folder. On MacOS, this folder is located at `~/.config/nvim/rplugin/python3`.

From within Neovim, invoke the `:UpdateRemotePlugins` command.

## Configuration

The plugin requires the OpenAI API key for interacting with ChatGPT. This key is read from the `chatgpt_config.json` file located in the same directory as the `chatgpt.py` plugin file (by default `~/.config/nvim/rplugin/python3` for Python plugins).

The `chatgpt\_config.json` file should look like this:

```json
{
  "OPENAI_API_KEY": "your_openai_api_key"
}
```

Replace `your_openai_api_key` with your actual OpenAI API key.

## Usage

To invoke ChatGPT for a completion, use the `:ChatGPT` command followed by your query. The output will be appended to the current line in the editor.

```vim
:ChatGPT What is the meaning of life?
```

For opening a new scratch window with the completion, use the `:ChatGPTsplit` command:

```vim
:ChatGPTsplit How does the solar system work?
```

The output will appear in a new vertical split window.

To use highlighted text in visual mode as part of the AI's prompt, simply highlight the desired text and then run the `:ChatGPT` or `:ChatGPTsplit` command. The highlighted text will be included in the prompt sent to the AI:

```vim
:ChatGPT {highlighted text} {your query}
```

## Models usage and token limits 

The plugin uses the `gpt-3.5-turbo` model for generating completions. If your text exceeds 12,000 characters, the plugin switches to the `gpt-3.5-turbo-16k` model. This is to comply with the model's maximum tokens limit.


## Disclaimer
This plugin is not officially associated with OpenAI or Neovim.
