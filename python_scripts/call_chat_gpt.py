import pandas as pd
from openai import OpenAI
import markdown
from python_scripts.get_search_links import get_updated_code_with_links
from python_scripts.config import open_ai_key
from datetime import datetime
from tqdm import tqdm

def perform_llm_tasks():
    log = ''
    filename = "./data/processed_1.csv"
    df = pd.read_csv(filename).reset_index(drop=True)
    
    filename_completed = "./data/completed_processed.csv"
    processed_df = pd.read_csv(filename_completed)
    
    tags = {
        "{CLIENT-REQUEST}": "comments",
        "{AGE}": "age",
        "{GENDER}": "gender",
        "{HEIGHT}": "height",
        "{WEIGHT}": "weight",
        "{SESSIONS}": "sessions",
        "{DURATION}": "duration",
    }
    
    advanced_tags = {
        "{GYM-AVAILABILITY}": "gym",
    }
    
    
    with open("./python_scripts/prompt_1.txt", "r") as f:
        prompt1 = f.read()
    
    
    with open("./python_scripts/prompt_2.txt", "r") as f:
        prompt2 = f.read()
        
    
    with open("other/req_html_1.txt", "r") as f:
        pre_text = f.read()
    
    
    with open("other/req_html_2.txt", "r") as f:
        post_text = f.read()
    
    client = OpenAI(api_key=open_ai_key)
    
    completed_ids = processed_df.to_numpy().tolist()
    if completed_ids:
        completed_ids = [tuple(x) for x in completed_ids]
    log+="=====================================================\n"
    log += f"Processing with LLMs started at {datetime.now()}\n"
    
    for i in tqdm(range(len(df))):
        
        if (df['id'][i], df['random_chars'][i]) in completed_ids:
            log+=f"Skipping generation for previously generated {df['random_chars'][i]}"
            log+='\n'
            continue
        else:
            log+=f"Generation for {df['random_chars'][i]} started at {datetime.now()}"
            log+='\n'
            current_prompt = prompt1
            for tag, col in tags.items():
                if df[col][i]:
                    current_prompt = current_prompt.replace(tag, str(df[col][i]))
                else:
                    current_prompt = current_prompt.replace(tag, "")
            for tag, col in advanced_tags.items():
                if str(df[col][i]).strip() == "Full fledged gym":
                    replaced_text = "has a full fledged gym"
                elif str(df[col][i]).strip() == "Body weight workouts":
                    replaced_text = (
                        "does not have access to a gym, and wants to do bodyweight exercises"
                    )
                elif str(df[col][i]).strip() == "Basic gym equipment (dumb-bells)":
                    replaced_text = "has basic gym equipments like dumbbells"
                current_prompt = current_prompt.replace(tag, replaced_text)
        
            response1 = (
                client.chat.completions.create(
                    model="gpt-3.5-turbo",  # Specify the engine you want to use
                    messages=[
                        {
                            "role": "system",
                            "content": "Make sure you give workout for the exact number of days as requested",
                        },
                        {"role": "user", "content": current_prompt},
                    ],
                )
                .choices[0]
                .message.content.strip()
            )
        
            current_prompt = prompt2 + "\n\n" + response1
        
            response2 = (
                client.chat.completions.create(
                    model="gpt-3.5-turbo",  # Specify the engine you want to use
                    messages=[
                        {
                            "role": "system",
                            "content": "Generate the markdown for the entire input, do not skip anything. Always have put the exercise names in the second column for all tables",
                        },
                        {"role": "user", "content": current_prompt},
                    ],
                )
                .choices[0]
                .message.content.strip()
            )
            if df["name"][i]:
                title_sent = f"# Workout for {df['name'][i].title()}" + "\n\n"
                response2 = title_sent + response2
            md_content = markdown.markdown(response2, extensions=["markdown.extensions.tables"])
            md_content = get_updated_code_with_links(md_content)
            with open("./created_workouts/" + df["random_chars"][i] + ".html", "w") as f:
                f.write(pre_text + md_content + post_text)
            completed_ids.append((df['id'][i], df['random_chars'][i]))
            log+=f"Generation for {df['random_chars'][i]} ended at {datetime.now()}"
            log+='--------------------------------------------\n'
            
    log += f"Processing with LLMs ended at {datetime.now()}\n"
    log+="=====================================================\n"
    
    processed_df = pd.DataFrame(completed_ids)
    processed_df.columns = ['id', 'random']
    processed_df.to_csv(filename_completed, index=False)
    
    return log
