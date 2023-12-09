# Generating posts for a real estate account on Instagram using OpenAI ChatGPT and DELLE3

## Solution description
Load the key from the environment and connect to the client:

```Python
_ = load_dotenv(find_dotenv())

client = openai.OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)
```

The code includes two functions for generating text and images based on a prompts

```Python
def get_text_completion(prompt, model="gpt-3.5-turbo"):
    ...
    return

def get_image_completion(prompt, model="dall-e-3"):
    ... 
    return
```

The function of generating prompts for the presented house parameters:

```Python
def get_prompt(house_params):
    ...
    # Generate text and prompt
    return
```

And the function of sampling and generating the corresponding description and image:
```Python
def get_data(input_file, output_file, n_samples=20):
    ...
    # Download data
    # Sample 20 examples
    # Generate and write description and image in loop
```

## Answers to the questions:

- How to mimic the style of *successful* Instagram posts?

More detailed prompts should be used to indicate what the model text should be, namely: evocative, emotional, but in a consistent style in a storytelling format. Also it should include popular, real hashtags which i found in the Instagram


- What prompt engineering techniques can improve quality?

I provide clear and specific instructions. Use delimiters to clearly indicate distinct parts of the input.  It is important to iterate through different prompts and parameters to find the best combination. I also use 0.3 temperature parameter to allow the model to be more creative without being too random, and I set a 200 word limit to keep the model from producing too long texts.

- How to ensure the model doesn't invent extra features?

Clear instructions in the prompt, a word limit, and a temperature setting help avoid this. The optimal option is found over the course of several iterations.
