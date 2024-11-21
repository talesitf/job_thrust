import gradio as gr
from src.scrapping import scrap
from src.doc_loader import updateCV

from dotenv import load_dotenv

load_dotenv()

with gr.Blocks() as demo:
    with gr.Row():  # Linha que separa os dois lados
        # Coluna para os INPUTS (lado esquerdo)
        with gr.Column(scale=1):  # Scale maior para inputs
            input_webpage = gr.Textbox(
                label="Adicione aqui um link de alguma vaga no gupy IO para atualizar seu currículo. Para outras plataformas, coloque a descrição da vaga manualmente."
            )
            input_descricao_vaga = gr.Textbox(label="Vaga para atualizar o currículo")
            button_check = gr.Button("Carregar vaga", size="sm")
            button_check.click(
                scrap,
                inputs=[input_webpage],
                outputs=[input_descricao_vaga],
                concurrency_limit=30,
            )
            document = gr.File(file_types=[".pdf"])
            button_final = gr.Button("Atualizar currículo", size="lg")
            

        # Coluna para o OUTPUT (lado direito)
        with gr.Column(scale=1):  # Scale menor para output
            output = gr.Textbox(label="Currículo Atualizado", lines = 30)
        
        button_final.click(
                updateCV,
                inputs=[document, input_descricao_vaga],
                outputs=[output],
                concurrency_limit=30,
            )
        
demo.launch(server_name="0.0.0.0")