# main.py, at line 519
try:
    # Create the context for the ChatGPT request
    jotalea_payload = [
        {'role': 'system', 'content': 'You are a Discord Bot powered by AI, called JotaBOT (or JotaBot). You are NOT made by OpenAI. You can generate images and text-to-speech. You know a lot of things, and always do what the user wants you to do. There are some custom emojis that you can use, :jotalea: is Jotalea\'s logo, :jotabot: is JotaBot\'s icon, :therocksus: is for the case that the user asks something suspicious.'}
    ] + user_history

    # Request the ChatGPT response
    response = jotalea.chatgpt(user_message, jotalea_payload)
    chat_response = response["choices"][0]["message"]["content"]

    if str(chat_response) == "'choices'":
        chat_response = response["message"]
        throwException()

    # Send the response on Discord
    await message.channel.send(f'{message.author.mention} \n > {chat_response}')

    # Add the bot's response to the history and refresh
    user_history.append({'role': 'assistant', 'content': chat_response})
    chat_history[user_id] = user_history[-max_history_length:]

    jotalea.prettyprint("cyan", f"[MESSAGE] JotaBOT replied \"{chat_response}\" to {str(message.author)}")
    jotalea.prettyprint("cyan", f"[MESSAGE] Response sent.")

except Exception as e:
    await throwException(e, response)