from llama_hub.file.unstructured.base import UnstructuredReader
from unstructured.partition.auto import partition
from unstructured.documents.elements import NarrativeText
import llama_index as li
from pathlib import Path
import openai
import os
import re
import ast
import json

openai.api_key = 'your_key'
os.environ['OPENAI_API_KEY'] = 'your_key'

#Path to textbook pdf
pdf = Path(f'data/ex_textbook.pdf')

UnstructuredReader = li.download_loader("UnstructuredReader", refresh_cache=True, use_gpt_index_import=True)
loader = UnstructuredReader()
textbook = loader.load_data(file=pdf, split_documents=True)
elements = partition(filename=pdf)

#What you need to modify

#Start of every chapter
pattern1 = r"(\d+)\s+Chapter\s+(\d+):"
#End of every chapter introduction
pattern2 = r"^\d+[CE](?: [A-Z])+"
#End of last chapter
end = "Need to Know More?"

#Tracking where chapters start/end
chapter_found = {}
chapter_starts = []
intros = []

for iteration, element in enumerate(textbook):
    match1 = re.search(pattern1, element.text)
    match2 = re.search(pattern2, element.text)
    if match1:
        chapter_number = match1.group(2)
        
        if chapter_number not in chapter_found:
            chapter_found[chapter_number] = True
            chapter_starts.append(iteration)
            intros.append(iteration)
    if match2:
        intros.append(iteration)

#Finding where last chapter ends
for x in textbook[chapter_starts[len(chapter_starts) - 1]:]:
    if x.text == end:
        chapter_starts.append(textbook.index(x))

#Collecting chapter summaries for GPT prompts
summaries = []
iteration = 0
for x in intros[::2]:
    temp =''
    for element in elements[x:intros[iteration+1]]:
        temp = temp + textbook[elements.index(element)].text + '\n'
    summaries.append(temp)
    iteration += 2

#Making dictionary with chapter as key and document objects as elements
directory = {}
chapter_num = 1
for x in range(len(chapter_starts) - 1):
    text = []
    for element in elements[chapter_starts[x]:chapter_starts[x+1]]:
        if isinstance(element, NarrativeText):
            text.append(textbook[elements.index(element)])
    directory['Chapter ' + str(chapter_num)] = text
    chapter_num += 1

#Combining all the narrative text of each chapter into one string and adding "This is Chapter 'x': " to the beginning and "This is the end of Chapter 'x'" to the end
final=[]
for chapter in directory:
    txt = ''
    for text in directory[chapter]:
        txt = txt + text.text
    directory[chapter][0].text = txt
    final.append(directory[chapter][0])
    
for iteration, text in enumerate(final):
    final[iteration].text = "This is Chapter " + str(iteration + 1) + ":\n" + text.text  + "\nThis is the end of Chapter " + str(iteration + 1)
node_parser = li.node_parser.SimpleNodeParser()
nodes = node_parser.get_nodes_from_documents(final)
test_index = li.GPTVectorStoreIndex(nodes=nodes, chunk_size_limit=512)
query_engine = test_index.as_query_engine()

def create_questions(num_chapters):
    form ="""[
    {
    "question": ,
    "choices": ,
    "correct_answer_index": ,
    "explanation":
    }
    ]
    """
    final = []
    for chapter in range(num_chapters):
        temp = []
        chap_num = str(chapter + 1)
        summary = query_engine.query(f"""Elaborate on these key topics of chapter {chap_num} in detail:
        {summaries[chapter]}
        """ )
        temp.append(str(summary))
        response = query_engine.query(f"""
        CHAPTER {chap_num}:
        {str(summary)}
        Please generate SIX different multiple choice questions that covers all of the above information. Must be variety in the type of questions (scenario questions, definitions, comparison questions) and some must have multiple correct answers. Do NOT reference the text in the questions and explanations themselves. Do not repeat any questions. In the explanation, provide more insight and also the chapter that it comes from
        Return the result in the following JSON format:


        {form}
        """)
        temp.append(ast.literal_eval(str(response)))
        final.append(temp)
    return final

questions = create_questions(len(chapter_starts) - 1)
test = []
for chap in questions:
    for question in chap[1]:
        test.append(question)
json_string = json.dumps(test, indent=4)

# Write the JSON string to a file
with open("website/ex_questions.json", "w") as json_file:
    json_file.write(json_string)
