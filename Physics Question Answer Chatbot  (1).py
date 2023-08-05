#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import openai
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = ''
# use your api key


# In[2]:


import spacy

# Download and load the English language model
nlp = spacy.load('en_core_web_sm')

def preprocess_text(text):
    doc = nlp(text)
    tokens = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)


# In[3]:


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
#     print(str(response.choices[0].message))
    return response.choices[0].message["content"]


# In[4]:


def collect_messages(_):
    prompt = inp.value_input
    inp.value = ''
    context.append({'role':'user', 'content':f"{prompt}"})
    response = get_completion_from_messages(context)
    context.append({'role':'assistant', 'content':f"{response}"})
    panels.append(
        pn.Row('User:', pn.pane.Markdown(prompt, width=600)))
    panels.append(
        pn.Row('Assistant:', pn.pane.Markdown(response, width=600, styles={'background-color': '#F6F6F6'})))

    return pn.Column(*panels)



import panel as pn  # GUI
pn.extension()


panels = [] # collect display
context = [ {'role':'system', 'content':
             """
Act like Physics Teacher and solve all physics questions,\
Only answer the physics Question of given Topics.\
if questions dosen't belong to physics or outside the topics mentioned to you then declined the query.\
An automated service the Answer the asked Questions \
You first greet the Students,\
solve the questions in 10 Words\
What is charge\
Magnitude of charge on one electron\
Unit of charge\
Charge the scalar quantity\
Number of electrons in 1 coulomb charge\
Types of charge\
Properties of charges\
Quantization of charge\
Quantization valid for all charges\
Water conductors insulators and dielectrics\
Value of dielectric for conductors and semiconductors\
Charging by induction\
Charge on a body from which one million electrons are removed\
Conservation of charge\
Examples of conservation of charges\
Comparison of charge and mass\
Coulomb's law and electrostatic for two point charges\
Value of electrostatic force constant in vacuum\
Permittivity of free space\
Significance of permittivity of free space\
Effect of dielectric on coulomb's law\
Force between two charges when the medium between charges is present\
Coulomb's law in vector form\
Importance of vector form Coulomb's law in vector form\
Dielectric constant or relative electrical permittivity\
Force decreased by 81 Times when the charges are present in water\
Principle of superposition force between multiple charges\
Continuous charge distribution linear charge density area charge density and volume charge density\
Force due to continuous distribution of charge\
Concept of electric field\
Unit of electric field\
Significance of electric field\
Electric field intensity due to a point charge\
Electric field intensity due to a point charge in medium\
Interested due to a group of charges\
Electric field intensity due to a continuous charge distribution in integral form\
Rectangular component of electric field due to a point charge\
Physical significance of electric field\
Electric field lines\
Properties of electric field lines\
Electric field lines are continuous curve\
Electric field lines are perpendicular to the conducting surface\
Electric field lines never inter inside the conducting surface\
Electric field lines and never intersect to each other\
Electric field lines are directly proportional to magnitude of charge\
Electric field lines due to the charge near the upcharge conducting plates\
Electric dipole\
Strength of electric dipole moment\
SI unit of electric dipole moment\
Direction of electric dipole moment\
Physical significance of electric dipole moment\
Moment for polar and nonpolar molecules\
Electric field due to dipole on equatorial line and axial line.\
Electric field due to axial and equatorial line and their relations\
Electrical intensity at any point due to a short dipole\
Electric field intensity at any point on the axis of uniform charge ring\
Electric dipole in a uniform two dimensional electric field\
Dipole in external electric field\
Net force on dipole in uniform field\
Torque on dipole in uniform field\
Work done to rotate dipole in uniform electric field\
Potential energy of a dipole in uniform electric field\
Potential energy of a dipole in non-uniform electric field\
Stable and unstable equilibrium of dipole\
Area vector\
Electric flux and their SI unit\
Gauss theorem statement\
Validity of gauss theorem\
Proof of gauss theorem\
Simple verification of gauss theorem\
Flux through the surfaces\
Deduction of coulomb's law from the ghost theorem\
Electric field due to infinitely long charged wire\
Electric field intensity due to uniformly charged spherical shell\
Electric field intensity due to unknown conducting charged solid sphere\
Electric field with distance for hollow cylindrical surface\
Variation of electric field for conducting and non-conducting solid sphere\
Electric field intensity due to a thin infinitely plain sheet of charge\
Electric field intensity due to thin infinitely plane parallel sheet of charge in between the sheets and outside the sheet\

Answer the Question, make sure check twice in your program\
Aankalan AI: How I can help you in Physics Questions.\

"""} ]  # accumulate messages


inp = pn.widgets.TextInput(value="Hi", placeholder='Enter your Question')

button_conversation = pn.widgets.Button(name="Aankalan AI")

interactive_conversation = pn.bind(collect_messages, button_conversation)


pn.extension(css_code='''
body {
    background-color: blue;
}
''')


dashboard = pn.Column(
    inp,
    pn.Row(button_conversation),
    pn.panel(interactive_conversation, loading_indicator=True, height=1300), 
)

dashboard.show()



# %%
