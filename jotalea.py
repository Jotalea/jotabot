      # pip install aiohttp
      # pip install requests
      # pip install discord

GPT_ENDPOINT = "https://api.openai.com/v1/chat/completions"
GPT_KEY = ""
GPT_HEADERS = {"Content-Type": "application/json", "Authorization": f"Bearer {GPT_KEY}"}
GPT_MODEL = "gpt-4"
GPT_TTS_URL = ""

def gemini(prompt, uRequests:bool=False):
    # curl -H 'Content-Type: application/json' -d '{"contents":[{"parts":[{"text":"Write a story about a magic backpack"}]}]}' -X POST https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=YOUR_API_KEY
    import os
    gemini_api_key = os.environ['GEMINI']
    if uRequests:
        import requests
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        headers = {
            'Content-Type': 'application/json',
        }
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }
        params = {
            'key': gemini_api_key
        }
        response = requests.post(url, headers=headers, json=data, params=params)

        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    else:
        import google.generativeai as genai

        genai.configure(api_key=gemini_api_key)

        model = genai.GenerativeModel('models/gemini-pro')
        chat = model.start_chat()
        try:
            response = chat.send_message(prompt)
        except Exception as e:
            return f"Your message was blocked:\n{e}"

        print(response.text)
    
        return response.text

def chatgpt(prompt:str, history_payload:list):
          import requests, json
          global GPT_ENDPOINT, GPT_HEADERS, GPT_KEY, GPT_MODEL, GPT_TTS_URL, payload, data

          payload = [
              {"role": "system", "content": "You are a helpful AI."},
              {"role": "user", "content": prompt}
          ]

          data = {
              "model": GPT_MODEL,
              "messages": history_payload + [{"role": "user", "content": prompt}]
          }

          try:
              if GPT_ENDPOINT == "https://api.openai.com/v1/chat/completions":
                  response = requests.post(GPT_ENDPOINT, headers=GPT_HEADERS, data=json.dumps(data))
              else:
                  response = requests.post(GPT_ENDPOINT, headers=GPT_HEADERS, json=data)
              return response.json()
          except Exception as e:
              return e

def tts(text, api_key):
    import requests
    api_domain = "api.shuttleai.app"
    url = f"https://{api_domain}/v1/audio/speech"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "eleven-labs",
        "input": text,
        "voice": "james"
    }

    import random

    random_v = random.randint(1000000, 9999999)
    
    response = requests.post(url, headers=headers, json=data)
    print(response)
    print(response.json())
    print(response.content)
    
    response_a = requests.get(response.content)

    with open(f"/files/speech_{random_v}.png", "wb") as file:
        file.write(response_a)

    path = "/files/speech_{random_v}.mp3"
#    with open(f"/files/speech{random_v}.mp3", "rb") as file:
#        file_send = file.read()
#    return file_send
    return path

def webhook(url:str, content:str="Test content", debug:bool=False):
          import requests
          try:
              rs = requests.post(url, json={"content": content})
              if rs.status_code == 200:
                  return True
          except Exception as e:
              if debug:
                  return str(e)
              else:
                  return False

async def async_webhook(url: str, content: str = "Test content", debug: bool = False):
          import aiohttp, asyncio, json
          try:
              async with aiohttp.ClientSession() as session:
                  async with session.post(url, json={"content": content}) as response:
                      if response.status == 200:
                          return True
                      else:
                          if debug:
                              return response.status
                          return False
          except Exception as e:
              if debug:
                  return str(e)
              return False

log = []

def prettyprint(color, text):
      global outcolor
      if color == "red":
          outcolor = "\033[31m"
      elif color == "green":
          outcolor = "\033[32m"
      elif color == "yellow":
          outcolor = "\033[33m"
      elif color == "blue":
          outcolor = "\033[34m"
      elif color == "purple":
          outcolor = "\033[35m"
      elif color == "cyan":
          outcolor = "\033[36m"
      elif color == "white":
          outcolor = "\033[37m"
      else:
          outcolor = "\033[0m"  # Default
      print(outcolor + str(text) + "\033[0m")
      return

async def old_tts(ttsText, download=False, upload=False, uplURL="https://example.com"):
          import aiohttp

          # Request for TTS generation
          async with aiohttp.ClientSession(headers={'Authorization': f'Bearer {GPT_KEY}'}) as session:
              async with session.post(GPT_TTS_URL, json={'text': ttsText}) as resp:
                  response = await resp.json()

          ttsURL = response["url"]

          if upload == False:
              return ttsURL

          if download:
              async with aiohttp.ClientSession() as session:
                  async with session.get(ttsURL) as audio_response:
                      if audio_response.status == 200:
                          audio_data = await audio_response.read()
                          with open('ai_tts.mp3', 'wb') as audio_file:
                              audio_file.write(audio_data)

          if upload:
              import os
              # Send the downloaded TTS audio file as an attachment
              with open('ai_tts.mp3', 'rb') as audio_file:
                  pass # UPLOAD API GOES HERE
              os.remove('ai_tts.mp3')
          return

def getIP(returnIP:bool=True,returnLoc:bool=True,returnCoords:bool=True,returnAll:bool=False):
          import requests, json, os
          # g=lambda r,l,c,a:json.dumps({k:v for k,v in requests.get('https://ipinfo.io/json').json().items() if k in ["ip","loc"]+["country","region","city"]*(l-1)+(a-1)*["country","region","city"]}) if r or l or c or a else ""
          data = requests.get('https://ipinfo.io/json').json()
          r = ""
          if returnIP:
              r = r + str(data["ip"])
              pass
          if returnLoc:
              r = r + str(data["country"]) + ", " + str(data["region"]) + ", " + str(data["city"])
              pass
          if returnCoords:
              r = r + str(data["loc"])
              pass
          if returnAll:
              r = str(f"IP: {data['ip']}\nUser: {os.getlogin()}\nCity: {data['city']}\nState: {data['region']}\nCountry: {data['country']}\nCoords: {data['loc']}\nZIP Code: {data['postal']}\nTimezone: {data['timezone']}")
              pass
          return r

