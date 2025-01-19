import fitz
import os
import asyncio
from ollama import chat
import pandas as pd
import json
import ast
import argparse

ans = []

def read_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def read_pdfs_from_folder(folder_path):
    pdf_texts = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            pdf_text = read_pdf(file_path)
            pdf_texts.append(pdf_text)
    return pdf_texts

async def send_to_ollama_async(content, prompt):
    response = chat(model='llama3.2', messages=[
        {
            'role': 'user',
            'content': f'{prompt}\n\n{content}',
        },
    ])
    return response['message']['content']

async def send_to_ollama_batch_async(contents, prompt, batch_size=10):
    responses = []
    for i in range(0, len(contents), batch_size):
        batch = contents[i:i + batch_size]
        tasks = [send_to_ollama_async(content, prompt) for content in batch]
        batch_responses = await asyncio.gather(*tasks)
        responses.extend(batch_responses)
    return responses

async def main(folder_path, batch_size):
    prompt = """
    Extract information from resume:

    None if no info present

    Give the output in a Dictionary

    Give the output in the following format: {
     "Name": "Name from resume", 
     "Email": "email from resume ending with .com",
     "Phone Number": "phone number from resume",
     "University": "University from resume", 
     "Year of Study": "Year of study from resume", 
     "Course": "Course from resume", 
     "Discipline": "Discipline from resume", 
     "CGPA/Percentage": "CGPA/Percentage from resume", 
     "Key Skills": "Key skills from resume", 
     "Gen AI Experience Score": "1 or 2 or 3", 
     "AI/ML Experience Score": "1 or 2 or 3", 
     "Internships/Work Experience": "Give list of comapanies worked at or None"
     "Certifications": "Give list of cerifications or None"
     "Projects": "Give list of project titles or None"
    }


     Score can have values 1-3,
     0 - No mention of Gen AI in Resume
     1 - Exposed of any Gen AI, 
     2 - Did some projects on Gen AI,
     3 - Worked on advanced areas such as Agentic RAG, Evals etc. 
     
     Similarly for AI/ML experience score as well.
     You can only give one score that is either 1 or 2 or 3.

     Score very Harshly
    """
    
    l1 = read_pdfs_from_folder(folder_path)
    pdf_summaries = await send_to_ollama_batch_async(l1, prompt, batch_size=batch_size)
    
    for summary in pdf_summaries:
        try: 
            start = summary.find('{') 
            end = summary.rfind('}') + 1 
            trimmed_data = summary[start:end] 
            data_dict = ast.literal_eval(trimmed_data) 
            
            for key in data_dict.keys(): 
                if isinstance(data_dict[key], list) and len(data_dict[key]) > 0: 
                    data_dict[key] = '\n'.join(data_dict[key]) 
            ans.append(data_dict) 
                    
        except Exception as e: 
            print(summary)
            print(f"An error occurred: {e}") 
            print("Skipping this summary due to error.")
    
    df = pd.DataFrame(ans)
    print(df)
    df.to_csv('test1.csv', index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process resumes and extract information")
    parser.add_argument('--folder_path', type=str, required=True, help="Folder path containing PDF resumes")
    parser.add_argument('--batch_size', type=int, default=3, help="Batch size for processing resumes")
    
    args = parser.parse_args()
    
    asyncio.run(main(args.folder_path, args.batch_size))
