import openai
import os
import random
import time
from dotenv import load_dotenv, find_dotenv
import csv
from urllib.request import urlopen
random.seed(1)

_ = load_dotenv(find_dotenv())

client = openai.OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

def get_text_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.3
    )
    return response.choices[0].message.content

def get_image_completion(prompt, model="dall-e-3"):
    response = client.images.generate(
            model=model,
            prompt=prompt,
            size="1024x1024",
            quality='standard',
            n=1
        )
    url = response.data[0].url
    return url


def get_prompt(house_params):
    house_info = f"""HOUSE SPECIFICATIONS:
- Price : {house_params['price']}
- Area : {house_params['area']}
- Number of bedrooms : {house_params['bedrooms']}
- Number of bathrooms : {house_params['bathrooms']}
- Number of storeys: {house_params['stories']}
- {'Located on the main road' if house_params['mainroad'] == 'yes' else 'It is not located on the main road'}
- {'There is a guest room' if house_params['guestroom'] == 'yes' else 'There is no a guest room'}
- {'There is a basement' if house_params['basement'] == 'yes' else 'There is no a basement'}
- {'Hot water heating is connected' if house_params['hotwaterheating'] == 'yes' else 'Hot water heating is not connected'}
- {'Air conditioning is connected' if house_params['airconditioning'] == 'yes' else 'Air conditioning is not connected'}
- Number of parking places : {house_params['parking']}
- {'Preferred area' if house_params['prefarea'] == 'yes' else 'Not a preffered area'}
- {house_params['furnishingstatus']}
"""
    prompt_description = f"""
Your task is to help the real estate sales team create
an advertising product description for an instagram account based on a technical fact sheet.

Write an advertising product description based on the information
provided in the technical specifications, delimited by triple backticks.

The description is intended for potential buyers in Instagram, therefore it should be attractive and instagram-style that is:
- Craft captions that are concise, compelling, and evoke emotion.
- Incorporate 3-5 popular hashtags, such as: #realestate, #dreamhome, #forsale, #property, #realestateforsale, #homeforsale, #luxuryrealestate, #housegoals, #househunting, #housesofinstagram.
- Maintain a consistent writing style to establish a recognizable brand.
- Pose questions and tell stories to an audience.


Use no more than 200 words

Technical specifications: ```{house_info}```
"""
    prompt_image = f"""Сreate a realistic advertising image {house_params['furnishingstatus']} {house_params['stories']}-storey house with {house_params['bedrooms']} bedrooms, {'basement' if house_params['basement'] == 'yes' else ''} and {house_params['parking'] if house_params['parking']!= '0' else 'without'} parking places 
"""
    return prompt_description, prompt_image, house_info

def get_data(input_file, output_file, n_samples=20):
    with open(input_file, "r") as in_file:
        csv_reader = csv.DictReader(in_file)
        rows = list(csv_reader)
        sample_rows = random.sample(rows, n_samples)
        with open(output_file, "w") as out_file:
            for i, house_params in enumerate(sample_rows):
                prompt_text, prompt_image, house_params = get_prompt(house_params)
                descpt = get_text_completion(prompt_text)

                time.sleep(70) # rate-generation limit, no more than 1 img
                url = get_image_completion(prompt_image)
                path = os.path.join('./img', 'image' + str(i + 1) + '.png')
                resource = urlopen(url)
                with open(path, 'wb') as image_out:
                    image_out.write(resource.read())
                
                image = f"![]({path})"

                out_file.write(house_params + '\n')
                out_file.write(descpt + '\n')
                out_file.write(image)
                out_file.write("\n------------------------\n")
                


if __name__ == '__main__':
    data_path = './data/Housing.csv'
    get_data(data_path, 'EXAMPLE.md', 20)
