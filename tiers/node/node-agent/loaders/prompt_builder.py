def build_prompt(message, context=None, system_prompt="", user_prompt_prefix=""):
    prompt_parts = []
    if system_prompt: prompt_parts.append(f"System: {system_prompt}")
    if not context:
        prompt_parts.append(user_prompt_prefix + message)
        return "\n".join(prompt_parts)
    prompt_parts.append("Previous conversation:")
    for exchange in context[-5:]:
        if exchange.get("role") == "user":
            prompt_parts.append(f"Human: {user_prompt_prefix}{exchange.get('content', '')}")
        elif exchange.get("role") == "assistant":
            prompt_parts.append(f"Assistant: {exchange.get('content', '')}")
    prompt_parts.append(f"\nCurrent message: {user_prompt_prefix}{message}")
    prompt_parts.append("\nPlease respond naturally to the current message, taking the conversation history into account.")
    return "\n".join(prompt_parts)
