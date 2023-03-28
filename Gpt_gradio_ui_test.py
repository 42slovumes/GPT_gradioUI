import gradio as gr

def greet(name):
    return "Hello " + name + "!"

with gr.Blocks(css="#testpls { width : 100% ; height : 75px ;  } #testpls2 { width : 100% ; height : 75px }") as demo:
    with gr.Row():
        with gr.Column(scale=6):
            text1 = gr.Textbox(label="",value="API KEY")
            text2 = gr.Textbox(label="",value="輸入框")
            
        with gr.Column(): 
            
                btn2 = gr.Button(elem_id="testpls",value="API KEY")
                btn1 = gr.Button(elem_id="testpls2",value="輸入框")
    with gr.Row():
        with gr.Tab("Flip Text"):
            with gr.Column(scale=1):
              text_input1 = gr.Markdown(value="將現有程式碼重新改寫。AI 會先解讀程式碼邏輯並重新寫一次程式，如果你覺得程式太過雜亂，或想看看有沒有更好的寫法，可以利用這個工具改寫看看。",label="")
              text_input2 = gr.Markdown(value="PS：改寫後的程式有可能會有 bug，可以利用 Debug 工具找看看問題。",label="")
              text_input3 = gr.Markdown(value="指令功能：改寫既有程式碼，尋求改進或效率提升",label="")
              text_input4= gr.Markdown(value="指令：重新改寫下方 <{程式語言}> 程式碼，並附上詳細說明。<{程式碼}> ",label="")
              gr.Dropdown( ["python", "java", "javascipt"], label="請選擇一個程式語言")
              text_output = gr.Textbox(lines=5)
        with gr.Tab("Flip Image"):
              text_input = gr.Textbox()

demo.launch()   