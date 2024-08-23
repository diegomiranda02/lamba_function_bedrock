import os
import requests

def already_response_function(prompt: str, url: str):
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "model_id": "meta.llama3-70b-instruct-v1:0",
        "params": {
            "prompt": prompt,
            "max_gen_len": 512,
            "temperature": 0.5,
            "top_p": 0.9
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        try:
            response_data = response.json()

            # Ensure that response_data is a dictionary before accessing 'generation'
            if isinstance(response_data, dict):
                return response_data.get('generation', '')  # Adjust according to your actual response structure
            else:
                return f"Unexpected response format: {response_data}"
        except ValueError:
            return f"Error: Response is not valid JSON. Raw response: {response.text}"
    else:
        return f"Error: {response.status_code}, {response.text}"

def test_already_response_1():
    url = os.getenv("API_ENDPOINT")  # Get the endpoint URL from the environment variable
    if not url:
        raise ValueError("API_ENDPOINT environment variable is not set.")
    
    prompt = ("""
    Você é um classificador de chamados do sistema de gerenciamento de chamados GLPI. Classifique o chamado em categoria e subcategoria de acordo com as seguintes opções:

    ### Categoria: Conectividade de Rede
    - **Subcategoria 1:** Falha de Conexão à Internet
    - **Subcategoria 2:** Problemas com Rede Local (LAN)
    - **Subcategoria 3:** Acesso Intermitente a Recursos de Rede

    ### Categoria: Hardware
    - **Subcategoria 1:** Problemas com Roteador
    - **Subcategoria 2:** Falha em Dispositivos de Rede
    - **Subcategoria 3:** Problemas de Compatibilidade de Hardware

    ### Categoria: Software
    - **Subcategoria 1:** Problemas após Atualização de Sistema Operacional
    - **Subcategoria 2:** Falha em Software de Gerenciamento de Rede
    - **Subcategoria 3:** Configuração de Software de Rede

    ### Categoria: Configuração e Ajustes
    - **Subcategoria 1:** Configuração de Rede
    - **Subcategoria 2:** Configuração de Dispositivos de Rede
    - **Subcategoria 3:** Ajustes de Segurança de Rede

    O usuário relatou o seguinte problema:

    > O usuário relata que o software de backup automático não está mais funcionando corretamente. Desde a última atualização do sistema operacional, o backup programado não foi executado e o usuário está recebendo mensagens de erro ao tentar iniciar o backup manualmente. O problema parece estar relacionado a uma incompatibilidade entre o software de backup e o novo sistema operacional."

    Classifique o problema conforme as categorias e subcategorias fornecidas e responda em formato JSON igual ao exemplo:

    ```json
    {"category": "", "subcategory": ""}
    ```
    """

    already_response = already_response_function(prompt, url)

    print(f"Prompt: {prompt}")
    print(f"Already Response: {already_response}")


if __name__ == "__main__":
    test_already_response_1()
