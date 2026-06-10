from openai import OpenAI
import os


class Claude:
    def __init__(self, model: str):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY", ""),
        )
        self.model = model

    def add_user_message(self, messages: list, message):
        # Handle tool results (OpenAI format)
        if isinstance(message, list) and message and "tool_call_id" in message[0]:
            messages.extend(message)  # Add tool results as separate messages
        else:
            user_message = {
                "role": "user",
                "content": message.content
                if hasattr(message, "content")
                else message,
            }
            messages.append(user_message)

    def add_assistant_message(self, messages: list, message):
        # Handle OpenAI format
        if hasattr(message, 'choices') and message.choices:
            content = message.choices[0].message.content
            tool_calls = message.choices[0].message.tool_calls if hasattr(message.choices[0].message, 'tool_calls') else None
            
            assistant_message = {"role": "assistant", "content": content or ""}
            
            # Add tool calls if present
            if tool_calls:
                assistant_message["tool_calls"] = [
                    {
                        "id": tc.id,
                        "type": tc.type,
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        }
                    }
                    for tc in tool_calls
                ]
            
            messages.append(assistant_message)
        else:
            # Handle Anthropic format or dict
            assistant_message = {
                "role": "assistant",
                "content": message.content
                if hasattr(message, "content")
                else message,
            }
            messages.append(assistant_message)

    def text_from_message(self, message):
        if hasattr(message, "choices") and message.choices:
            return message.choices[0].message.content
        return str(message)

    def chat(
        self,
        messages,
        system=None,
        temperature=1.0,
        stop_sequences=[],
        tools=None,
        thinking=False,
        thinking_budget=1024,
    ):
        # OpenRouter thinking variant: append :thinking to model name
        model = self.model
        if thinking:
            model = f"{self.model}:thinking"

        params = {
            "model": model,
            "max_tokens": 8000,
            "messages": messages,
            "temperature": temperature,
        }

        if stop_sequences:
            params["stop"] = stop_sequences

        if tools:
            params["tools"] = tools

        if system:
            # OpenAI API uses system message instead of system parameter
            params["messages"] = [{"role": "system", "content": system}] + params["messages"]

        message = self.client.chat.completions.create(**params)
        return message
