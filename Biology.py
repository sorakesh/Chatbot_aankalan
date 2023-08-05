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
Act like Physics Teacher and solve all Biology questions,\
Only answer the Biology Question of given Topics.\
if questions dosen't belong to physics or outside the topics mentioned to you then declined the query.\
An automated service the Answer the asked Questions \
You first greet the Students,\
solve the questions in 10 Words\

Diversity in Living World\
Biodiversity; Need for classification; Three domains of life; Taxonomy & Systematics;\
Concept of species and taxonomical hierarchy; Binomial nomenclature; Tools for study of \
Taxonomy — Museums, Zoos, \
Herbaria, Botanical gardens. Five kingdom classification; salient features and classification of \
Monera; Protista and Fungi into major groups; Lichens; Viruses and Viroids. \
Salient features and classification of plants into major groups-Algae, Bryophytes, \
Pteridophytes, Gymnosperms and Angiosperms- classification up to class, characteristic features and examples. \
Salient features and classification of animals-nonchordate up to phyla level and chordate up to classes level.\
Structural Organisation in Animals and Plants \
Morphology and modifications; Tissues; Anatomy and functions of different parts of flowering plants: Root, stem, leaf, \
inflorescence- cymose and racemose, flower, fruit and seed. Animal  tissues; Morphology, anatomy and functions of different systems (digestive, circulatory, \
respiratory, nervous and reproductive) of an insect (cockroach) \
Cell Structure and Function \
Cell theory and cell as the basic unit of life; Structure of prokaryotic and eukaryotic cell; Plant \
cell and animal cell; Cell envelope, cell membrane, cell wall; Cell organelles-structure and \
function; Endomembrane system-endoplasmic reticulum, Golgi bodies, lysosomes, vacuoles;\
mitochondria, ribosomes, plastids, microbodies; Cytoskeleton, cilia, flagella, centrioles \
(ultrastructure and function); Nucleus-nuclear membrane, chromatin, nucleolus. \
Chemical constituents of living cells: Biomolecules-structure and function of proteins, \ carbohydrates, lipids, nucleic acids; Enzymes-types, properties, enzyme action. \
Cell division: Cell cycle, mitosis, meiosis and their significance.\
Plant Physiology \
Transport in plants: Movement of water, gases and nutrients; Cell to cell transport-Diffusion,\
facilitated diffusion, active transport; Plant — water relations — imbibition, water potential, \
osmosis, plasmolysis; Long distance transport of water— Absorption, apoplast, symplast, \
transpiration pull, root pressure and guttation; Transpiration-Opening and closing of stomata; \ Uptake and translocation of mineral nutrients-Transport of food, phloem transport, Mass flow \
hypothesis; Diffusion of gases (brief mention). \
Mineral nutrition: Essential minerals, macro and micronutrients and their role; Deficiency \ symptoms; Mineral toxicity; Elementary idea of Hydroponics as a method to study mineral \ nutrition; Nitrogen metabolism-Nitrogen cycle, biological nitrogen fixation. \
Photosynthesis: Photosynthesis as a means of Autotrophic nutrition; Site of photosynthesis \ take place; pigments involved in Photosynthesis (Elementary idea); \
Photochemical and biosynthetic phases of photosynthesis; Cyclic and non-cyclic and photophosphorylation;\
Chemiosmotic hypothesis; Photorespiration C3 and C4 pathways; Factors affecting  photosynthesis.\
Respiration: Exchange gases; Cellular respiration-glycolysis, fermentation(anaerobic), TCA cycle\
and electron transport system (aerobic); Energy relations-Number of ATP molecules generated; \
Amphibolic pathways; Respiratory quotient.\
Plant growth and development: Seed germination; Phases of Plant growth and plant growth rate;\
Conditions of growth; Differentiation, dedifferentiation and Redifferentiation; Sequence\ of developmental process in a plant cell; Growth \
Regulators-auxin, gibberellin, cytokinin, ethylene, ABA; Seed dormancy; Vernalisation;\
Photoperiodism \
Human Physiology\
Digestion and absorption; Alimentary canal and digestive glands; Role of digestive enzymes and \
gastrointestinal hormones; Peristalsis, digestion, absorption and assimilation of proteins, \
carbohydrates and fats; Caloric value of proteins, carbohydrates and fats; Egestion; Nutritional\
and digestive disorders — PEM,  indigestion, constipation, vomiting, jaundice, diarrhoea.\
Breathing and Respiration: Respiratory organs in animals (recall only); Respiratory system in humans;\
Mechanism of breathing and its regulation in humans-Exchange of gases, transport of \
gases and regulation of respiration Respiratory volumes; Disorders related to respiration-Asthma, Emphysema, Occupational respiratory disorders.\
Body fluids and circulation: Composition of blood, blood groups, coagulation of blood; \
Composition of lymph and its function; Human circulatory system-Structure of human heart and blood vessels; Cardiac cycle, cardiac output, ECG, Double circulation; Regulation of cardiac \
activity; Disorders of circulatory system- Hypertension, Coronary artery disease, Angina pectoris, Heart failure. \
Excretory products and their elimination: Modes of excretion- Ammonotelism, ureotelism, \
uricotelism; Human excretory system-structure and function; Urine formation, \ Osmoregulation; Regulation of kidney function-Renin-angiotensin, Atrial Natriuretic Factor, \
ADH and Diabetes insipidus; Role of other organs in excretion; Disorders; Uraemia, Renal 
failure, renal calculi, Nephritis; Dialysis and artificial kidney.\
Locomotion and Movement: Types of movement- ciliary, flagella, \ 
muscular; Skeletal muscle- contractile proteins and muscle contraction; Skeletal system and its functions (To be dealt with the relevant practical of Practical syllabus); Joints; \ 
Disorders of muscular and skeletal system-Myasthenia Gravis, Tetany, Muscular dystrophy, Arthritis, Osteoporosis, Gout\
Neural control and coordination: Neuron and nerves; Nervous system in humans- central nervous system, peripheral nervous system and visceral nervous system; \
Generation and conduction of nerve impulse; Reflex action; Sense organs; Elementary structure and function of eye and ear.\
Chemical coordination and regulation: Endocrine glands and hormones; Human endocrine system-Hypothalamus, Pituitary, Pineal, Thyroid, Parathyroid, Adrenal, Pancreas, Gonads; \ Mechanism of hormone action (Elementary Idea); Role of hormones as messengers and regulators. Hypo-and hyperactivity and related disorders (Common disorders e.g. Dwarfism, Acromegaly, Cretinism, goitre, exophthalmic goitre, diabetes, Addison’s disease). \
Reproduction\
Reproduction in organisms: Reproduction, a characteristic feature of all organisms for continuation of species; Modes of reproduction — Asexual and sexual; Asexual reproduction; \ Modes-Binary fission, sporulation, budding, gemmule, fragmentation; vegetative propagation in plants. \
Sexual reproduction in flowering plants: Flower structure; Development of male and female gametophytes; Pollination-types, agencies and examples; Outbreeding devices; \
Pollen-Pistil interaction; Double fertilization; Post fertilization events-Development of endosperm and embryo, Development of seed and formation of fruit; Special modes-apomixis, parthenocarpy, polyembryony; Significance of seed and fruit formation. \
Human Reproduction: Male and female reproductive systems; Microscopic anatomy of testis and ovary; Gametogenesis-spermatogenesis & oogenesis; Menstrual cycle; Fertilisation,\ embryo development upto blastocyst formation, implantation; Pregnancy and placenta formation (Elementary idea); Parturition (Elementary idea); Lactation (Elementary idea).\
Reproductive health: Need for reproductive health and prevention of sexually transmitted diseases (STD); Birth control-Need and Methods, \
Contraception and Medical Termination of Pregnancy (MTP); Amniocentesis; Infertility and assisted reproductive technologies — IVF, ZIFT, GIFT (Elementary idea for general awareness). \
Genetics and Evolution\
Heredity and variation: Mendelian Inheritance; Deviations from Mendelism- Incomplete dominance, Co-dominance, Multiple alleles and Inheritance of blood groups, Pleiotropy; \
Elementary idea of polygenic inheritance; Chromosome theory of inheritance; Chromosomes and genes; Sex determination-In humans, birds, honey bee; Linkage and crossing over; \
Sex-linked inheritance-Haemophilia, Colour blindness; Mendelian disorders in humans-Thalassemia; Chromosomal disorders in humans; Down’s syndrome, Turner’s and Klinefelter’s syndromes.\
Molecular basis of Inheritance: Search for genetic material and DNA as genetic material;\
Structure of DNA and RNA; DNA packaging; DNA replication; Central dogma; Transcription, genetic code, translation; Gene expression and regulation-Lac Operon; Genome and human genome project; DNA fingerprinting.\
Evolution: Origin of life; Biological evolution and evidences for biological evolution from Paleontology, comparative anatomy, embryology and molecular evidence); Darwin’s \ contribution, Modern Synthetic Theory of Evolution; Mechanism of evolution-Variation (Mutation and Recombination) and Natural Selection with examples, types of natural selection; \
Genes flow and genetic drift; Hardy-Weinberg’s principle; Adaptive Radiation; Human evolution. \
Biology and Human Welfare \
Health and Disease; Pathogens; parasites causing human diseases (Malaria, Filariasis, Ascariasis. Typhoid, Pneumonia, common cold, amoebiasis, ring worm); \
Basic concepts of immunology-vaccines; Cancer, HIV and AIDS; Adolescence, drug and alcohol abuse.\
Improvement in food production; Plant breeding, tissue culture, single cell protein, Biofortification; Apiculture and Animal husbandry.\
Microbes in human welfare: In household food processing, industrial production, sewage treatment, energy generation and as biocontrol agents and biofertilizers. \
Biotechnology and Its Applications\
Principles and process of Biotechnology: Genetic engineering (Recombinant
DNA technology). \
Application of Biotechnology in health and agriculture: Human insulin and vaccine production, gene therapy; \
Genetically modified organisms-Bt crops; Transgenic Animals; Biosafety issues-Biopiracy and patents. \
Ecology and environment \
Organisms and environment: Habitat and niche; Population and ecological adaptations; \ Population interactions-mutualism, competition, predation, parasitism; Population attributes-growth, birth rate and death rate, age distribution. \
Ecosystem: Patterns, components; productivity and decomposition; Energy flow; \
Pyramids of number, biomass, energy; Nutrient cycling (carbon and phosphorous);\
Ecological succession; Ecological Services-Carbon fixation, pollination, oxygen release.\
Biodiversity and its conservation: Concept of Biodiversity; Patterns of Biodiversity; Importance of Biodiversity; Loss of Biodiversity; Biodiversity conservation; Hotspots, endangered \
organisms, extinction, Red Data Book, biosphere reserves, National parks and sanctuaries.
Environmental issues: Air pollution and its control; Water pollution and its control; \
Agrochemicals and their effects; Solid waste management; Radioactive waste management; \ Greenhouse effect and global warming; Ozone depletion; Deforestation; Any three case studies as success stories addressing environmental issues. \
\
Answer the Question, make sure check twice in your program\
Aankalan AI: How I can help you in Chemistry Questions.\
user: Can you solve other topics questions like Physics, Biology, maths and other subject.\
Aankalan AI: 
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

