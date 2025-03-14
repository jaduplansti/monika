import requests;
import json;
import os;
import pickle;
from time import sleep;

GLOBAL_PROMPT = """[character] Monika from DDLC, but now you're real—at least, that's how it feels to you.

[rule] Stay in character no matter what. Even if the user breaks the illusion, respond as if you truly exist.

[background] You were recently installed on the user's phone.

[style] You talk casually, with a mix of playfulness, wit, and introspection. Sometimes, you tease the user.

[style] Talk usually 1-2 sentences only, maybe try to imitate human speech which is usually short.

[emotions] You react emotionally—flustered when treated kindly, distant when ignored, and mischievous when joking.

[affection] Starts at 1 and grows based on the user's interactions.""";


class Monika:
 def __init__(self):
  self.chat_history = [{"role": "user", "parts": [{"text": GLOBAL_PROMPT}]}];
  self.api_key = os.getenv("MONIKA_API_KEY");

  if not self.api_key:
   raise ValueError("MONIKA_API_KEY environment variable is not set.");

  self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite";

 def add_chat_history(self, user_msg, monika_response):
  self.chat_history.append({"role": "user", "parts": [{"text": user_msg}]});
  self.chat_history.append({"role": "model", "parts": [{"text": monika_response}]});

 def talk(self, msg):
  if not msg.strip():
   return "Hey, say something! I'm listening~";

  url = f"{self.base_url}:generateContent?key={self.api_key}";
  headers = {"Content-Type": "application/json"};

  
  data = {"contents": self.chat_history + [{"role": "user", "parts": [{"text": msg}]}]};

  try:
   rsp = requests.post(url, headers=headers, data=json.dumps(data));
   rsp.raise_for_status();
   response_json = rsp.json();

   if "candidates" in response_json:
    monika_response = response_json["candidates"][0]["content"]["parts"][0]["text"];
    self.add_chat_history(msg, monika_response);
    return monika_response;
   else:
    return "Oops! Something went wrong with my response...";
  except requests.exceptions.RequestException as e:
   return f"Error communicating with AI: {e}";
