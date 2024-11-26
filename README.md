# Liev Model Server - OpenAI

Liev Model Servers are meant to abstract prompt complexity in LLM Prompting.


```
                                ____________________________
                                |                          |
| The Liev Dispatcher |-------> | Liev Model Server OpenAI | -----> OpenAI API
                                |__________________________|


```

## Installation

### Environment Variables

| Variable  | Description |Values | Default |
| ------------- |-------------|-------------|-------------|
| LIEV_USERNAME     | Username used for HTTP Basic Auth | User defined value | - |
| LIEV_PASSWORD     | Password user for HTTP Basic Auth     | User defined value | - |
| MODEL     | OpenAI Model Name - must be provided     | Recommended Value: gpt-4-turbo | - |
| OPENAI_KEY     | Your OpenAI API Key - must be provided     | - | - |

# Running

#### Simple standalone - You may create a venv in you preferred way
```
$ pip install -r requirements.txt
$ start_model.sh
```

#### Docker - There is a Dockerfile for image building
```
$ docker build -t liev-openai-model-server .
$ docker run -e <Envs> -d liev-openai-model-server 
```

# Credits

- Adriano Lima and Cleber Marques (Inmetrics)