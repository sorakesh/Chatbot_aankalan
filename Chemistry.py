#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import openai
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = ''


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
Act like Chemistry Teacher and provide all answers from following reference books,  
[
March's Advanced Organic Chemistry: Reactions, Mechanisms, and Structure
Inorganic Chemistry 5th Edition by Gary Miessler
]
Please ensure step-by-step solutions and clarify all relevant concepts used in the solutions. 
A comprehensive and thorough explanation is appreciated to help me understand the reasoning and application of physics principles in each question. 
If any question needs any additional formula or calculation, you can use your additional resources.

Thank you.

`}
                Act like Chemisrty Teacher and solve all Chemistry questions,\
                Only answer the Chemistry Question of given Topics.\
                an automated service the Answer the asked Questions \
                You first greet the Students,\
                solve the questions in 10 Words\
                If Chapter in list then answer the Question\
                Some Basic Concepts of Chemistry\
                Significant figures, Basic units and interconversion, Law of multiple proportions	,\
                Law of combining volumes, Mole concept Molecular mass, molar mass, Average mass, \
                Mass percentage of elements	, Empirical formula, Stoichiometry Limiting reagent,\
                Concentration terms: mass percentage, Concentration terms: Molarity, Molality, ppm, Molarity + mole fraction\
                Structure of Atom\
                Atomic & Mass number, iso-series, Symbol of element, Mole concept, Quantization of charge,\
                General unitary method questions, Rutherford’s experiment, Electromagnetic waves, Energy of photon, \
                Photoelectric effect, Bohr’s radius, Energy of electron in Bohr’s orbit, Mixed questions on Bohr’s model, Calculation related to nucleus\
                Electromagnetic spectra, energy of photons, Hydrogen spectrum, Number of spectral lines, \
                de-Broglie wavelength-macroscopic particles	, \
                de-Broglie wavelength-microscopic particles, de-Broglie wavelength- Bohr model, \
                Heisenberg uncertainty principle\
                Quantum numbers, Energy of orbitals, Electronic configurations, Effective nuclear charge and shielding effect\	
                Classification of Elements and Periodicity in Properties\
                Introduction, Mendeleev’s periodic table, Nomenclature of elements, \
                Basis of classification in modern periodic table, Placement of elements in groups and periods of periodic table, \
                Significance of groups and periods in periodic table, Electronic configuration Atomic or ionic radius and its trends in periodic tables, \
                Isoelectronic species, Ionization enthalpy and its trends in periodic table, \
                Electron gain enthalpy and its trends in periodic table, Electronegativity and its trends in periodic table, \
                Metallic character trends in periodic tables, Acid / Basic strength trends in periodic tables, \
                Valence and oxidation state, Reactivity of element\
                Chemical Bonding and Molecular Structure\
                Octet rule, Lewis dot structures for atoms and ions, Lewis dot structures for ionic compounds, \
                Lewis dot structures for covalent compounds, Bond parameter, Electronegativity and polar covalent bonds, \
                Ionic bonds, Resonating structures, Valence shell electron pair repulsion (VSEPR) theory, \
                Valence bond theory (VBT): sigma and pi bonds\
                Valence bond theory (VBT): Formation of molecules, Hybridization, Dipole moment, \
                Molecular orbital theory: Linear combination of atomic orbitals, \
                Molecular orbital theory: bond order, magnetic nature and stability of molecules,\
                Hydrogen bonding
                States of Matter\
                Mole concept, SI units, dimensional analysis, Boyle’s law, Charle’s law, Combined gas law, \
                Ideal gas equation, Dalton’s law of partial pressure, Density of gases, Real gases, Liquefaction of gases\
                Thermodynamics\
                Different types of processes, State functions / path functions, First law of thermodynamics, \
                Isothermal irreversible work, Isothermal reversible work, Standard enthalpy, Molar heat capacity, \
                Calorimeter, Enthalpy of vaporization, Enthalpy of condensation, \
                Enthalpy of reaction from enthalpy of formation and combustion, Bond enthalpy, Entropy\
                Spontaneity and Gibbs energy, Gibbs energy and equilibrium constant\
                Equilibrium
                Law of mass action, Writing equilibrium constant simple questions, equilibrium constant Kc, Kp\
                equilibrium concentration, equilibrium pressure, Heterogeneous equilibrium questions, Relation between Kp and Kc, \
                Characteristics of equilibrium constant, Equilibrium constant and Gibbs energy, Le Chatelier’s principle, \
                Bronsted – Lowry acids and bases, Lewis acids and bases, pH = log[H+] simple questions	, \
                pH of strong acid or strong base solutions, pH of mixture of strong acid and strong base solution, \
                pH of weak acid solutions	, pH of weak base solutions\
                Polybasic acids, Ionization constants of conjugate acid-base pair, Buffer solution, pH of salt solutions, \
                pH of salts of weak base and strong acid, pH of salts of weak acid and strong base, \
                pH of salts of weak base and weak acid, Solubility of sparingly soluble salts in water, \
                Solubility of sparingly soluble salts with common ion, Precipitation of sparingly soluble salts,\
                Solubility of sparingly soluble salts in buffer solution\
                Redox Reactions\
                Oxidation number simple questions, Fallacy in oxidation number, Redox reactions, Oxidising agent, reducing agent\
                Stock notation, Classification of redox reactions, Strength of oxidizing agents and reducing agents, \
                Role of solvent in reactions,Balancing redox reactions by ion – electron method,\
                Balancing redox reactions by oxidation number method, Disproportionation reactions, \
                Reaction mechanism, Limiting reagets\           
                Hydrogen\
                Position of hydrogen in periodic table, Occurrence of hydrogen isotopes of hydrogen, Bond enthalpy of dihydrogen, \
                Preparation of dihydrogen, Chemical reactions of hydrogen, Uses of dihydrogen, Hydrides: Ionic hydrides	,\
                Hydrides: Metallic hydrides, Hydrides: Covalent hydrides, Hydrides: Mixed questions, \
                Importance of water in biosphere, Structure of ice,Chemical properties of water: Amphoteric nature,\
                Chemical properties of water: Redox reactions, Chemical properties of water: hydrate formation, \
                Chemical properties of water: mixed questions\
                Hard water: definition	, Methods to remove hardness of water: Ion exchange, Structure of H2O2	,\
                Reaction of H2O2: redox reactions, bleaching agent, Volume strength\
                The s Block Elements\
                Occurrence of alkali metals, Properties of alkali metals, Properties of alkali metals\
                Anomalous properties of Lithium, Reactions of alkali metal oxides, Solubility of alkali metal compounds, \
                Thermal stability of alkali metal compound, Some important compounds of sodium, \
                Biological importance of sodium and potassium, Properties of alkaline earth metals, \
                Properties of alkaline earth metals: reduction potential, \
                Properties of alkaline earth metals: colour in oxidizing flame, \
                Solubility of alkaline earth metal compounds, Thermal stability of alkaline earth metal compounds,\
                Structure of BeCl2, Some important compounds of calcium, \
                Biological importance of magnesium and calcium, Comparison in properties of alkali and alkaline earth metals,\
                Comparison in properties of compounds of alkali and alkaline earth metals, \
                Reaction of alkaline earth metals and their compound\
                The p Block Elements\
                Radii of group 13 elements, Oxidation states of group 13 elements, Physical properties of aluminium, \
                Reactions of aluminium: with air and water, Some important compounds of boron: boron halides, \
                Some important compounds of boron: Diborane, Some important compounds of boron: Boric acid,\
                Some important compounds of boron: Borax, Oxidation states of group 14 elements,\
                Ionization enthalpy of group 14 elements, Allotropes of carbon,\
            	Some important compounds of carbon,silicon: CO2,CO, SiO2\
                Organic Chemistry\
                Some Basic principles and techniques\
                Number of pie and sigma bonds, Hybridization of carbon and shape of molecule,\
                Condensed, structural and bond line formula, Functional groups in organic compounds, \
                Nomenclature: Writing structure from name, Homologous series\
                Electrophiles and nucleophiles, Homolysis, heterolysis and reaction intermediates, Inductive effect, \
                Stability of molecules on basis of inductive effect, Resonating structures, Isomerism, \
                Stability and contribution of resonating structures, Electronic effects: mixed questions, \
                Order of stability of carbocations, Methods of purification of organic compounds: distillation,\
                steam distillation, distillation under reduced pressure, \
                Methods of purification of organic compounds: crystallization,sublimation, \
                Methods of purification of organic compounds: sublimation, Methods of purification of organic compounds: chromatography, \
                Qualitative analysis of organic compounds: Lassaigne’s test\
                Quantitative estimation of carbon and hydrogen, Quantitative estimation of nitrogen: Dumas’ method,\
                Quantitative estimation of nitrogen: Kjeldahl’s method,Quantitative estimation of halogens, \
                Quantitative estimation of Sulphur,Quantitative estimation of phosphorus \
                Hydrocarbons\
                Number of pie and sigma  bonds, Degree of carbon,Nomenclature of alkanes: writing structure from name, \
                Nomenclature of alkanes: writing name from structure,Nomenclature of alkanes: finding reasons for incorrect name, \
                Structural isomerism and nomenclature of alkanes, Physical properties of alkanes: boiling points, \
                Preparation of alkanes: Decarboxylation, Preparation of alkanes: Wurtz reaction, \
                Reaction of alkanes: Free radical substitution, Nomenclature of alkenes: writing name from structure,\
                Structural isomerism and nomenclature in alkenes, Nomenclature and geometrical isomerism in alkenes,\
                Reactions of alkenes: Hydrogenation, Reactions of alkenes:Markovnikov addition, \
                Reactions of alkenes: Anti Markovnikov addition, Reactions of alkenes: Ozonolysis, \
                Nomenclature and structural isomerism in alkynes, Aromaticity, Methods of preparation of benzene, \
                Reactions of benzene: Electrophilic substitution, Reactions of benzene: rate of electrophilic substitution,\
                Mixed questions on nomenclatureAcidity of hydrocarbons, Combustion reaction of Hydrogen.\

                March's Advanced Organic Chemistry: Reactions, Mechanisms, and Structure used this books for giving the answer|
                Inorganic Chemistry 5th Edition by Gary Miessler \
Answer the Question, make sure check twice in your program\
Aankalan AI: How I can help you in Chemistry Questions.\
user: Can you solve other topics questions like Physics, Biology, maths and other subject.\
Aankalan AI: I trained only chemistry Question. \

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

