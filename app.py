import gradio as gr
from src.scrapping import scrap
from src.doc_loader import load_document, updateCV

def greet(name, intensity):
    return "Hello, " + name + "!" * int(intensity)


with gr.Blocks() as demo:

    input_webpage = gr.Textbox(label="Adicione aqui um link de alguma vaga no gupy IO para atualizar seu currículo. Para outras plataformas, coloque a descrição da vaga manualmente.")
    input_descricao_vaga = gr.Textbox(label="Vaga paraatualizar o currículo")
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
        inputs=[input_descricao_vaga],
        concurrency_limit=30,
    )
    
demo.launch(share=True)