import uvicorn
import gradio as gr
from src.scrapping import scrap

def greet(name, intensity):
    return "Hello, " + name + "!" * int(intensity)


with gr.Blocks() as demo:

    input_webpage = gr.Textbox(label="Adicione aqui um link de alguma página na internet para complementar sua matéria.", info="Caso o link seja inválido, deixe em branco.")
    input_descricao_vaga = gr.Textbox(label="Vaga querida")
    button_check = gr.Button("Check link webpage", size="sm")
    button_check.click(
        scrap,
        inputs=[input_webpage],
        outputs=[input_descricao_vaga],
        concurrency_limit=30,
    )
    document = gr.File(file_types=['pdf'])
    
demo.launch(share=True)