import gradio as gr
import openai
def check_tab(name):
    return "Hello " + name + "!"
def chat_with_gpt(input,apikey,input_messages):
    openai.api_key = apikey
    messages = []
    messages.append({"role":"user","content":input_messages+input})   # 添加 user 回應
    print(messages)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=500,
        temperature=0.5,
        messages=messages
    )
    ai_msg = response.choices[0].message.content.replace('\n','\n')
     # 將輸入的代碼轉換為Markdown格式的代碼塊
    markdown_code = f'{ai_msg}'
    # 將轉換後的Markdown格式代碼塊返回給Gradio Text框元件進行顯示
    messages.append({"role":"assistant","content":ai_msg})   # 添加 ChatGPT 回應
    print(markdown_code)
    return markdown_code 
def output_ans(input,apikey,programming_language,key):
    input_messages =""
    print(key)
    if(key == "改寫程式碼"):
        input_messages="重新改寫下方 "+programming_language+" 程式碼，並附上詳細說明，並且請將程式碼區塊用三個反引號框起來"
    elif(key =="模擬程式碼執行"):
        input_messages="執行以下程式碼，並將結果顯示在畫面上，並且請將程式碼區塊用三個反引號框起來"
    else:
        input_messages =""
    return chat_with_gpt(input,apikey,input_messages)
with gr.Blocks(css="#testpls { width : 100% ; height : 67px ;  } #testpls2 {margin-top : 10px ; width : 100% ; height : 67px } #margin_tab {margin-top : 10px ;} #margin_markdown {margin-top : -22px ;}") as demo:
 with gr.Tab("改寫程式碼"):
    with gr.Row():
        with gr.Column(scale=6):
            text1 = gr.Textbox(label="",value="",placeholder="api key")
            text2 = gr.Textbox(label="",value="",placeholder="程式碼")
            
        with gr.Column(): 
            with gr.Box():
                btn2 = gr.Button(elem_id="testpls",value="CLEAR APIKEY")
                btn1 = gr.Button(elem_id="testpls2",value="START")
                
    with gr.Row():
            with gr.Column(scale=1):   
              with gr.Box():
                with gr.Column():
                    key =gr.Text(value="改寫程式碼",label="",interactive=False)
                    gr.Markdown(value="將現有程式碼重新改寫。AI 會先解讀程式碼邏輯並重新寫一次程式，如果你覺得程式太過雜亂，或想看看有沒有更好的寫法，可以利用這個工具改寫看看。",label="")
                    gr.Markdown(value="PS：改寫後的程式有可能會有 bug，可以利用 Debug 工具找看看問題。",label="")
                    gr.Markdown(value="指令功能：改寫既有程式碼，尋求改進或效率提升",label="")
                    gr.Markdown(value="指令：重新改寫下方 <{程式語言}> 程式碼，並附上詳細說明。<{程式碼}> ",label="")
                    dropdown1=gr.Dropdown( ["python", "java", "javascipt","html","rust", "Go", "Perl", "PHP", "Ruby", "Swift"], label="請選擇一個程式語言" ,elem_id="margin_tab")
              with gr.Box():
                with gr.Column():
                    text_output = gr.Markdown(lines=5,label="output")
 btn1.click(output_ans, inputs=[text2,text1,dropdown1,key], outputs=[text_output])
 with gr.Tab("模擬程式碼執行"):
    with gr.Row():
        with gr.Column(scale=6):
            text1 = gr.Textbox(label="",value="",placeholder="api key")
            text2 = gr.Textbox(label="",value="",placeholder="程式碼")
            
        with gr.Column(): 
            with gr.Box():
                btn2 = gr.Button(elem_id="testpls",value="CLEAR APIKEY")
                btn1 = gr.Button(elem_id="testpls2",value="START")
                
    with gr.Row():
            with gr.Column(scale=1):   
              with gr.Box():
                with gr.Column():
                    key =gr.Text(value="模擬程式碼執行",label="",interactive=False)
                    text_input1 = gr.Markdown(value="這個指令可以讓 ChatGPT 模擬您提供的程式碼，並將結果回傳。 根據 OpenAI 官方文件，ChatGPT 可以處理的程式語言有： JavaScript, Go, Perl, PHP, Ruby, Swift。",label="")
                    text_input2 = gr.Markdown(value="指令功能：模擬程式碼執行",label="")
                    text_input3 = gr.Markdown(value="指令：執行以下程式碼，並將結果顯示在畫面上<{程式碼}>",label="")
                    text_input4= gr.Markdown(value="範例：",label="")
                    text_input4= gr.Markdown(value="執行以下程式碼，並將結果顯示在畫面上",label="")
                    gr.Markdown(value="```def fibonacci(num):```",label="")
                    gr.Markdown(value="```　if num <= 1:```",label="",elem_id="margin_markdown")
                    gr.Markdown(value="```　　return num```",label="",elem_id="margin_markdown")
                    gr.Markdown(value="```　else:```",label="",elem_id="margin_markdown")
                    gr.Markdown(value="```　　return fib(num-1) + fib(num-2)```",label="",elem_id="margin_markdown")
                    gr.Markdown(value="```print(fibonacci(10))```",label="",elem_id="margin_markdown")
              with gr.Box():
                with gr.Column():
                    text_output = gr.Markdown(lines=5,label="output")
 btn1.click(output_ans, inputs=[text2,text1,dropdown1,key], outputs=[text_output])

        
demo.launch()   