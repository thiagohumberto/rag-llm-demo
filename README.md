# LLM + RAG Simple Chat

This is a simple chatbot demo. The context is to interact with an Assistant or an Athlete from the Paris 2024 Olympic Games. The RAG process loads a PDF file to update the base model with this context. Note that the model does not have any references to Paris '24, as it was trained before the games.

Bot rules (check the prompt_template.py to customize yours):

- Will never answer anything out of the '24 games context
- Will never talk about politics
- Will answer only about asked sport
- Won't explain anything that is not sport related

I compiled a review of the games (source: official Olympic Games site) into a PDF file located in `/pdf_demo/raf_test_paris.pdf`.

When you run the app, load this PDF and try to ask something about the games.


Do you like it? Please consider ⭐ and follow me to trade experiences about. 

## How to Load the LLM Model

I used Ollama ([ollama.com](https://ollama.com/)), a model hub. Once installed, you can list and run models locally.

## Install dependencies

Please pip requirements.txt, I really recommend to use venv.

## How to run

`streamlit run app.py`


</br>
</br>

![image](/pdf_demo/image.png) 