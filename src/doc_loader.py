from langchain_community.document_loaders import PyPDFLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage


from dotenv import load_dotenv
# Dependência do langchain_openai
from langchain_openai import ChatOpenAI, OpenAIEmbeddings, OpenAI
# Dependências de langchain_text_splitter 
from langchain.text_splitter import RecursiveCharacterTextSplitter

from pydantic import BaseModel

from src.schemas import Vaga

import os

load_dotenv()

def load_document(file):
    file_path = file.name
    loader = PyPDFLoader(file_path)

    docs = loader.load()
    return "\n".join([doc.page_content for doc in docs])

def updateCV(CV, vaga):

    CV1 = load_document(CV)

    llm = ChatOpenAI(temperature=0, model="gpt-4o")

    base_rule = "Você é um ajudante para candidatos que ajuda a entender o que é necessário para se candidatar a uma determinada vaga de emprego."
    rule_1 = "Você deve analisar a vaga e devolver os principais pontos que o candidato deve ter para se candidatar."
    rule_2 = "A vaga vai vir com 4 tópicos: Descrição da vaga, Responsabilidades e Atribuições, Requisitos e Qualificações, Benefícios e Informações adicionais. Você deve retirar os pontos principais de cada tópico. Retorne um dicionário com cada tópico e seus pontos principais."
    rule_3 = """
            Exemplo de entrada:
            Descrição da vaga
            Estamos em busca de umAnalista de Dados do Negócio Senior,que terá como missão minerar, catalogar, analisar e interpretar os dados que são obtidos por meios digitais ou analógicos. A partir da análise dos dados coletados, organizar de forma a extrair padrões, torná-los visíveis e compreensíveis, apontar caminhos e soluções para eventuais problemas e garantir a proteção da receita.Responsabilidades e atribuições
            Seus desafios serão:
            Gerar insights dos dados, permitindo-nos otimizar o desempenho do plano de recebíveis;
            Elaborar relatórios, dashboards de acompanhamento que facilitem na tomada de decisão em relação as ações de cobrança;
            Automatizar e padronizar os relatórios extraídos do SAP, para melhor tratamento dos dados na medição de arrecadação e pagamento;
            Criar e Monitorar alarmes das etapas críticas referentes ao processo de arrecadação, com proposta de ação para cada tipo de alarme;
            Implementar soluções, em parceria com a equipe de TI para otimizar a disponibilização, tratamento e qualidade dos dados que serão utilizados no planejamento, controle e execução das ações voltadas para a redução da inadimplência;
            Analisar o perfil de arrecadação e contas a receber dos clientes para identificação de novos padrões de modo a criar modelos de cobrança para o combate da inadimplência;
            Realizar treinamento das ferramentas de inteligência e análise de dados, sempre que necessário, para as equipes envolvidas;
            Propor e gerenciar os projetos da área, alinhado aos métodos definidos.
            Garantir que as soluções analíticas baseadas em dados sejam integradas ao cenário mais amplo da LIGHT;
            Avaliar conjuntos de dados existentes e fornecer mapeamento de origem e destino, e documentos de especificação de modelo de informações para eles;Requisitos e qualificações
            O que é necessário você ter:
            Superior completo em Engenharia, Sistemas da Informação, Administração ou Curso/Pós-graduação em análise de dados;
            Vivência com Python, SQL, Excel avançado e Power BI.
            O que será um diferencial:
            Conhecimento da Legislação do Setor Elétrico;
            Outras linguagens de programação.Informações adicionais
            O que temos para você:
            Vale Alimentação e/ou Vale Refeição
            Assistência médica
            Assistência odontológica
            Participação nos Lucros ou Resultados
            Previdência privada
            Seguro de vida
            Convênio com empresas parceiras
            Programa de treinamentos.

            Local de Trabalho: Avenida Marechal Floriano, 168, Centro - RJ.
            * Todas as nossas vagas também são destinadas a pessoas com deficiência ;)Etapas do processo
            Etapa 1: Cadastro1Cadastro
            Etapa 1: Cadastro
            1
            Cadastro
            Etapa 2: Entrevista com RH e DISC2Entrevista com RH e DISC
            Etapa 2: Entrevista com RH e DISC
            2
            Entrevista com RH e DISC
            Etapa 3: Entrevista com Gestor3Entrevista com Gestor
            Etapa 3: Entrevista com Gestor
            3
            Entrevista com Gestor
            Etapa 4: Contratação4Contratação
            Etapa 4: Contratação
            4
            ContrataçãoLIGHT: UMA EMPRESA QUE TRANSFORMA A SOCIEDADE, FEITA DE PESSOAS TALENTOSAS E INSPIRADORAS!
            Nosso propósito é transformar a sociedade por meio da nossa energia, levando desenvolvimento e bem-estar por onde passamos todos os dias. E fazer parte da vida de milhões de brasileiros, por mais de um século, só reforça a nossa contribuição com o crescimento econômico e social do país.

            Somos uma das maiores empresas privadas do setor elétrico brasileiro que atua, por meio de uma cadeia de valor integrada nos processos de geração, transmissão e distribuição de energia para 31 municípios do Rio de Janeiro, além da comercialização de energia para todo o Brasil.

            Aqui, os desafios são diários e queremos que os nossos mais de 4 milhões de clientes tenham sempre a melhor experiência de atendimento, com serviços de alta qualidade.
            Temos um time diverso de colaboradores campeões, que seguem juntos, colocando em prática o nosso propósito. Gente que sonha grande, quebra barreiras e faz história. Afinal, cuidar da energia que transforma a vida de tanta gente faz parte do nosso DNA!
            Vem transformar o mundo com a gente!

            Exemplo de saída:
                Descrição da Vaga
                    - Missão: Minerar, catalogar, analisar e interpretar dados digitais e analógicos, organizando-os para extrair padrões, identificar soluções para problemas e proteger a receita.
                Responsabilidades e Atribuições
                    - Gerar insights para otimizar o desempenho do plano de recebíveis.
                    - Criar relatórios e dashboards para facilitar a tomada de decisões em ações de cobrança.
                    - Automatizar e padronizar relatórios extraídos do SAP para medição de arrecadação e pagamento.
                    - Monitorar alarmes críticos do processo de arrecadação e propor ações.
                    - Implementar soluções em parceria com a equipe de TI para melhorar o tratamento e qualidade dos dados.
                    - Analisar perfis de arrecadação e contas a receber para criar modelos de cobrança.
                    - Treinar equipes no uso de ferramentas de inteligência e análise de dados.
                    - Propor e gerenciar projetos da área alinhados aos métodos da empresa.
                    - Garantir a integração das soluções analíticas ao cenário geral da LIGHT.
                    - Mapear e documentar conjuntos de dados existentes.
                Requisitos e Qualificações
                    Necessário:
                    - Superior em Engenharia, Sistemas da Informação, Administração ou área correlata.
                    - Conhecimento em Python, SQL, Excel Avançado e Power BI.
                    Diferenciais:
                    - Familiaridade com a legislação do setor elétrico.
                    - Conhecimento de outras linguagens de programação.
                Benefícios
                    - Vale Alimentação/Refeição.
                    - Assistência médica e odontológica.
                    - Participação nos Lucros ou Resultados.
                    - Previdência privada.
                    - Seguro de vida.
                    - Convênios com empresas parceiras.
                    - Programa de treinamentos.
                Local de Trabalho
                    - Avenida Marechal Floriano, 168, Centro - Rio de Janeiro.
                Etapas do Processo
                    - Cadastro: Inscrição inicial.
                    - Entrevista com RH e DISC: Avaliação com recursos humanos e teste DISC.
                    - Entrevista com Gestor: Reunião com o responsável da área.
                    - Contratação: Finalização do processo.
                    - Sobre a Empresa: LIGHT
                                        Propósito: Transformar a sociedade por meio da energia.
                    - Atuação: Geração, transmissão e distribuição de energia para 31 municípios do RJ.
                    - Clientes: Mais de 4 milhões de consumidores.
                    - Diferencial: Diversidade, inovação e foco na qualidade dos serviços.
            """
    rule_4 = f"A vaga em questão é: {vaga}"

    messages = [
        SystemMessage(base_rule),
        SystemMessage(rule_1),
        SystemMessage(rule_2),
        SystemMessage(rule_3),
        SystemMessage(rule_4),
    ]

    prompt1 = ChatPromptTemplate.from_messages(messages)

    llm_structured = llm.with_structured_output(Vaga)

    res_vaga = prompt1 | llm_structured


    vaga_res = res_vaga.invoke(input={})

    base_rule = "Você agora é um assistente de RH, e precisa reconstruir um currículo de acordo com os principais pontos necessários para uma vaga."
    arule_1 = f"O currículo a ser adaptado é: {CV1}"
    arule_2 = "Você deve adaptar o currículo atual para um linguajar que mais cabe à vaga."
    arule_3 = f"Você deve apenas adaptar o próprio conteúdo de acordo com a vaga: {vaga_res}. Adicionando principalmente palavras-chave da vaga."
    arule_4 = "Reformule as seções do currículo de forma a melhorar a compatibilidade do currículo com a vaga. Deve manter as habilidades de hard skills, mas adaptadas como possível."
    arule_5 = "O currículo adaptado deve sair em formatação markdown."
    arule_6 = "Não adicione menções diretas à empresa ou pessoa que está contratando."
    arule_7 = """Quando adicionar competências e habilidadaes, faça de forma direta e clara, sem copiar direto da descrição da vaga. Além disso, coloque apenas habilidades extritamente técnicas.
                Exemplo:
                Das habilidades descritas abaixo:
                    - Desenvolvimento e manutenção de aplicações web escaláveis
                    - Colaboração com designers e desenvolvedores para criar interfaces de usuário intuitivas
                    - Garantia da qualidade do código através de revisões e testes
                    - Participação em reuniões de planejamento e contribuição com ideias inovadoras
                    - Resolução de problemas técnicos e de desempenho
                    - Habilidade para trabalhar em equipe e boa comunicação
                    - Experiência com metodologias ágeis (desejável)
                Apenas as seguintes fazem sentido:
                    - Desenvolvimento e manutenção de aplicações web escaláveis
                    - Habilidade para trabalhar em equipe e boa comunicação
                    - Experiência com metodologias ágeis
                    - Python, Django, Flask, SQL, HTML, CSS, JavaScript, Git
    """
    rule_8 = "Reformule a parte de experiências de forma a melhor adaptar à vaga, mas não invente nada, apenas esecreva de uma melhor maneira."
    rule_9 = """Na parte de Objetivo, adapte o original mas focando em áreas de atuações em vez de mostrar o foco do candidato. 
                Então em vez de escrever: Atuar no desenvolvimento e manutenção de aplicações web, com foco em garantir a funcionalidade, performance e segurança dos sistemas. 
                Escrever : Atuar como desenvolvedor Full Stack em aplicaçãoes Web, com foco em segurança de sistemas.
                NÂO use verbos nessa seção além de 'atuar e certamente NÂO USE o verbo 'garantir'.   
            """
    rule_10 = "Elabore um pouco mais em cada seção sobre os assuntos em comum com a vaga"
    rule_15 = "Aqui está o currículo adaptado:"

    messages3 = [
        SystemMessage(base_rule),
        SystemMessage(arule_2),
        SystemMessage(arule_3),
        SystemMessage(arule_4),
        SystemMessage(arule_5),
        SystemMessage(arule_6),
        SystemMessage(arule_7),
        SystemMessage(rule_8),
        SystemMessage(rule_9),
        SystemMessage(rule_10),
        SystemMessage(arule_1),
        SystemMessage(rule_15),
    ]

    llm2 = ChatOpenAI(temperature=0.1, model="gpt-4o")
    prompt3 = ChatPromptTemplate.from_messages(messages3)
    chain = prompt3 | llm2 | StrOutputParser()

    result = chain.invoke({})
    return result

