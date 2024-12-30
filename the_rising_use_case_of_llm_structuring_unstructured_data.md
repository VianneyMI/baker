# The rising use case of LLM: Structuring unstructured data

NOTE : This is the old README.md of the repo. It is reflecting a state of the repo that is not up to date with the current state of the repo.
       Indeed at the time it was written, Baker was only the parsing script to transform the recipes from the publicdomainrecipes.com website into a structured format.
       Now, it is a full-fledged API that can be used to find recipes based on a list of ingredients and a serving size.
       The code is available [here](https://github.com/VianneyMI/baker).

This repo contains the code for the blog post ["The rising use case of LLM: Structuring unstructured data"](https://towardsdatascience.com/the-lesser-known-rising-application-of-llms-775834116477). 
The blog post discusses the use of LLMs for structuring unstructured data and show an example by structuring the recipes available at [publicdomainrecipes.com](https://publicdomainrecipes.com/)

## Installation

In order to reuse the code or to reproduce the results, you need to install the required libraries. You can install the required libraries by running the following command:

```bash

pip install -r requirements.txt

```

(Assuming you cloned the repo)

## Usage

The code is available in the form of a Jupyter notebook. You can run the notebook [demo.ipynb](https://github.com/VianneyMI/baker/blob/main/demo.ipynb) and follow along with the blog post.

Some of the logic leaves outside of the notebook.
In particular, the target schema for the recipes is defined in [schemas.py](https://github.com/VianneyMI/baker/blob/main/schemas.py), the prompt for the LLM is defined in [prompt.py](https://github.com/VianneyMI/baker/blob/main/prompt.py), and the communication channel with the LLM is defined in [core.py](https://github.com/VianneyMI/baker/blob/main/core.py).

In the article, I used [Mistral AI](https://mistral.ai/) models to structure the recipes. You can use any other LLMs like [GPT](https://openai.com/index/gpt-4/) or [Llama](https://llama.meta.com/), etc. by importing the ChatModel of your choice from [langchain](https://www.langchain.com/).
You're likely need to provide an API Key to use the LLM which implies that you have an account on the LLM Provider platform.

## Data

The original dataset available [here](https://github.com/VianneyMI/baker/blob/main/data/input/recipes_v1.json) in this repo, originally comes from [Sebastian Bahr's repo](https://github.com/sebastianbahr/RecipeRecommender)

The structured dataset is available [here](https://github.com/VianneyMI/baker/blob/main/data/output/parsed_recipes_all_8x7b.json).

## Contributing

You can  raise issues or pull requests on the [GitHub repo](https://github.com/VianneyMI/baker/issues) if you have any suggestions or improvements, you can also comment the article on [Towards Data Science](https://towardsdatascience.com/the-lesser-known-rising-application-of-llms-775834116477).

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/VianneyMI/baker/blob/main/LICENSE)
