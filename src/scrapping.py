import requests
from bs4 import BeautifulSoup

def scrap(url):
    # Faz a requisição para obter o HTML
    response = requests.get(url)
    final = "\n"
    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        
        sections={}

        # Parseia o conteúdo HTML da página
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Exemplo: Extrair todos os links
        vaga = soup.find_all('section')

        for sec in vaga[0].find_all('div'):
            
            section_name = sec.find('h2')
            if section_name is None:
                continue
            content = sec.find_all(['p', 'span', 'li'])

            sections[section_name.get_text(strip=True)] = '\n'.join([c.get_text(strip=True) for c in content])

        for s,v in sections.items():
            final+=s
            final+= "\n" + v

        return final
    else:
        return "Adicione manualmente asua vaga desejada aqui"