#!/usr/bin/env python
# coding: utf-8

# In[1]:

# get_ipython().run_line_magic('pip', 'install -q -U google-generativeai')


# In[2]:

import google.generativeai as genai


# In[3]:

import json

with open("config.json") as file:
    GOOGLE_API_KEY = json.load(file)['Gemini_API_Key']
    
# setting up the API key
genai.configure(api_key=GOOGLE_API_KEY)



# In[6]:

# setting the model to the Gemini Pro model
model = genai.GenerativeModel('gemini-pro')


# In[16]:


# In[1]:

# function that will generate a response from the Gemini API using the prompt provided
def generate_response(prompt):
    response = model.generate_content(prompt)
    return response

