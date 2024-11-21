import gradio as gr
from src.scrapping import scrap
from src.doc_loader import load_document, updateCV

with gr.Blocks() as demo:
    with gr.Row():  # Linha que separa os dois lados
        # Coluna para os INPUTS (lado esquerdo)
        with gr.Column(scale=2):  # Scale maior para inputs
            input_webpage = gr.Textbox(
                label="Adicione aqui um link de alguma vaga no gupy IO para atualizar seu currículo. Para outras plataformas, coloque a descrição da vaga manualmente."
            )
            input_descricao_vaga = gr.Textbox(label="Vaga para atualizar o currículo")
            button_check = gr.Button("Check link webpage", size="sm")
            button_check.click(
                scrap,
                inputs=[input_webpage],
                outputs=[input_descricao_vaga],
                concurrency_limit=30,
            )
            document = gr.File(file_types=[".pdf"])
            button_upload = gr.Button("Upload PDF", size="sm")
            button_upload.click(
                load_document,
                inputs=[document],
                concurrency_limit=30,
            )
            button_final = gr.Button("Finalizar", size="lg")
            button_final.click(
                updateCV,
                inputs=[document, input_descricao_vaga],
                outputs=[],
                concurrency_limit=30,
            )

        # Coluna para o OUTPUT (lado direito)
        with gr.Column(scale=1):  # Scale menor para output
            output = gr.Markdown(label="Currículo Atualizado")
        
demo.launch()