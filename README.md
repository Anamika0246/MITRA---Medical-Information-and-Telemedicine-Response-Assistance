# MITRA---Medical-Information-and-Telemedicine-Response-Assistance


# How to run?
### STEPS:
Clone the repository

```bash
Project repo: https://github.com/Anamika0246/MITRA---Medical-Information-and-Telemedicine-Response-Assistance
```

### STEP 01- Create a conda environment after opening the repository
```bash
conda create -n mitra python=3.10 -y
```
```bash
conda activate medibot
```

### STEP 02- install the requirements
```bash
pip install -r requirements.txt
```
### Create a .env file in the root directory and add your Pinecone & openai credentials as follows:
PINECONE_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"<br>
OPENAI_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
# Run the following command to store embeddings to pinecone
```bash
python store_index.py
```
# Finally run the following command
```bash
python app.py
```
Now,

# Open the localhost
# Techstack Used:
Python
LangChain
Flask
GROQ_API
Pinecone