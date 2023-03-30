import gradio as gr
import openai
import pdfplumber
#判斷檔案是否為圖片
message_pdf =""
def is_imag(filename):
    return filename[-4:] in ['.pdf']

def upload_file(files,apikey):
    print(files.name)
    user_text=''
    is_pdf = is_imag(files.name)
    if(is_pdf):
        print(files.name)
        pdf = pdfplumber.open(str(files.name))   # 開啟 pdf
        page = pdf.pages[0]  # 获取第一页
        text = page.extract_text()  # 提取文本   # 取出文字
        print(text)
        return chat_with_gpt_filepdf(text,apikey,user_text)        # [<Page:1>, <Page:2>, <Page:3>]，共有三頁
    else:
        return "請傳送PDF檔"
def chat_with_gpt_filepdf(input,apikey,input_messages):
    print(input)
    print(apikey)
    print(input_messages)
    openai.api_key = apikey
    messages = []
    messages.append({"role":"user","content":input+input_messages})   # 添加 user 回應
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
    return 123

    
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
def clear_code():
    return ""
def output_ans(input,apikey,programming_language,key):
    input_messages =""
    print(key)
    if(key == "改寫程式碼"):
        input_messages="重新改寫下方 "+programming_language+" 程式碼，並附上詳細說明，並且請將程式碼區塊用三個反引號框起來"
    elif(key =="模擬程式碼執行"):
        input_messages="執行以下程式碼，並將結果顯示在畫面上，並且請將程式碼區塊用三個反引號框起來"
    elif(key =="自動產生程式碼"):
        input_messages="以 "+programming_language+" 語法，撰寫一段程式，並以中文舉例說明為什麼這樣寫，並且請將程式碼區塊用三個反引號框起來。  ： "
    elif(key =="分析，解讀程式碼"):
         input_messages="指令：解讀下方 "+programming_language+" 程式碼，以中文註解告訴我這個程式碼要達成什麼目的。並且請將程式碼區塊用三個反引號框起來。\n"
    elif(key =="自動產生程式碼"):
         input_messages="以 "+programming_language+" 語法，撰寫一段程式，並以中文舉例說明為什麼這樣寫，並且請將程式碼區塊用三個反引號框起來。  ： "
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
                btn2 = gr.Button(elem_id="testpls",value="Clear Code")
                btn1 = gr.Button(elem_id="testpls2",value="START")
                
    with gr.Row():
            with gr.Column(scale=1):   
              with gr.Box():
                with gr.Column():
                    key =gr.HighlightedText(value="改寫程式碼",label="",interactive=False,)
                with gr.Box():
                    gr.Markdown(value="將現有程式碼重新改寫。AI 會先解讀程式碼邏輯並重新寫一次程式，如果你覺得程式太過雜亂，或想看看有沒有更好的寫法，可以利用這個工具改寫看看。",label="")
                    gr.Markdown(value="PS：改寫後的程式有可能會有 bug，可以利用 Debug 工具找看看問題。",label="")
                    gr.Markdown(value="指令功能：改寫既有程式碼，尋求改進或效率提升",label="")
                    gr.Markdown(value="指令：重新改寫下方 <{程式語言}> 程式碼，並附上詳細說明。<{程式碼}> ",label="")
                    dropdown1=gr.Dropdown( ["python", "java", "javascipt","html","rust", "Go", "Perl", "PHP", "Ruby", "Swift"], label="請選擇一個程式語言" ,elem_id="margin_tab")
              with gr.Box():
                with gr.Column():
                    text_output = gr.Markdown(lines=5,label="output")
 btn2.click(clear_code,outputs=[text2])
 btn1.click(output_ans, inputs=[text2,text1,dropdown1,key], outputs=[text_output])
 
 #模擬程式碼執行
 
 with gr.Tab("模擬程式碼執行"):
    with gr.Row():
        with gr.Column(scale=6):
            text1 = gr.Textbox(label="",value="",placeholder="api key")
            text2 = gr.Textbox(label="",value="",placeholder="程式碼")
            
        with gr.Column(): 
            with gr.Box():
                btn2 = gr.Button(elem_id="testpls",value="Clear Code")
                btn1 = gr.Button(elem_id="testpls2",value="START")
                
    with gr.Row():
            with gr.Column(scale=1):   
              with gr.Box():
                with gr.Column():
                    key =gr.HighlightedText(value="模擬程式碼執行",label="",interactive=False)
                with gr.Box(): 
                    text_input1 = gr.Markdown(value="這個指令可以讓 ChatGPT 模擬您提供的程式碼，並將結果回傳。 根據 OpenAI 官方文件，ChatGPT 可以處理的程式語言有： JavaScript, Go, Perl, PHP, Ruby, Swift。",label="")
                    text_input2 = gr.Markdown(value="指令功能：模擬程式碼執行",label="")
                    text_input3 = gr.Markdown(value="指令：執行以下程式碼，並將結果顯示在畫面上<{程式碼}>",label="")
                    text_input4= gr.Markdown(value="範例：",label="")
                    text_input4= gr.Markdown(value="執行以下程式碼，並將結果顯示在畫面上",label="")
        
                with gr.Column():    
                    gr.Markdown(value="```def fibonacci(num):```",label="")
                    gr.Markdown(value="```　if num <= 1:```",label="",elem_id="margin_markdown")
                    gr.Markdown(value="```　　return num```",label="",elem_id="margin_markdown")
                    gr.Markdown(value="```　else:```",label="",elem_id="margin_markdown")
                    gr.Markdown(value="```　　return fib(num-1) + fib(num-2)```",label="",elem_id="margin_markdown")
                    gr.Markdown(value="```print(fibonacci(10))```",label="",elem_id="margin_markdown")
              with gr.Box():
                with gr.Column():
                    text_output = gr.Markdown(lines=5,label="output")
 btn2.click(clear_code,outputs=[text2])
 btn1.click(output_ans, inputs=[text2,text1,dropdown1,key], outputs=[text_output])

#自動產生程式碼

 with gr.Tab("自動產生程式碼"): 
     with gr.Row():
        with gr.Column(scale=6):
            text1 = gr.Textbox(label="",value="",placeholder="api key")
            text2 = gr.Textbox(label="",value="",placeholder="需求")
            
        with gr.Column(): 
            with gr.Box():
                btn2 = gr.Button(elem_id="testpls",value="Clear Code")
                btn1 = gr.Button(elem_id="testpls2",value="START")
     with gr.Row():
        with gr.Column(scale=1):   
              with gr.Box():
                with gr.Column():
                    key =gr.HighlightedText(value="自動產生程式碼",label="",interactive=False)
                with gr.Box(): 
                    text_input1 = gr.Markdown(value="由 AI 根據你指定的需求產生程式碼，可以有效提升開發工作效率。不過有時 AI 產生的程式碼會有 bug，如果運作上發生問題，可以再透過這個 Debug 工具請 AI 協助找出問題點。",label="")
                    text_input2 = gr.Markdown(value="PS：如果原本的 input 就有問題，AI 可能也無法識別出資料錯誤導致的程式處理問題。",label="")
                    text_input3 = gr.Markdown(value="指令功能：撰寫可實際操作且可運行的程式碼，作為開發參考。",label="")
                    text_input4= gr.Markdown(value="以 <{程式語言}> 語法，撰寫一段程式，並以中文舉例說明為什麼這樣寫。我的需求是： <{需求}>。",label="")
                    dropdown1=gr.Dropdown( ["python", "java", "javascipt","html","rust", "Go", "Perl", "PHP", "Ruby", "Swift"], label="請選擇一個程式語言" ,elem_id="margin_tab")
              with gr.Box():
                with gr.Column():
                    text_output = gr.Markdown(lines=5,label="output")
 btn2.click(clear_code,outputs=[text2])
 btn1.click(output_ans, inputs=[text2,text1,dropdown1,key], outputs=[text_output])
#分析，解讀程式碼

 with gr.Tab("分析，解讀程式碼"):               
    with gr.Row():
        with gr.Column(scale=6):
            text1 = gr.Textbox(label="",value="",placeholder="api key")
            text2 = gr.Textbox(label="",value="",placeholder="程式碼")

        with gr.Column(): 
            with gr.Box():
                btn2 = gr.Button(elem_id="testpls",value="Clear Code")
                btn1 = gr.Button(elem_id="testpls2",value="START")
    with gr.Row():
        with gr.Column(scale=1):   
              with gr.Box():
                with gr.Column():
                    key =gr.HighlightedText(value="分析，解讀程式碼",label="",interactive=False)
                with gr.Box(): 
                    text_input1 = gr.Markdown(value="請 AI 幫助逐行解釋程式碼邏輯及用途，可做為學習或確認需求使用。若程式碼比較長，AI 也可能會透過註解的方式將描述加在程式碼內，方便你更清楚理解。",label="")
                    text_input2 = gr.Markdown(value="指令功能：分析、解讀程式碼 (幫程式碼加上註解)",label="")
                    text_input3 = gr.Markdown(value="指令：解讀下方 <{程式語言}> 程式碼，以中文註解告訴我這個程式碼要達成什麼目的。",label="")
                    text_input4= gr.Markdown(value="<{程式碼}>",label="")
                    dropdown1=gr.Dropdown( ["python", "java", "javascipt","html","rust", "Go", "Perl", "PHP", "Ruby", "Swift"], label="請選擇一個程式語言" ,elem_id="margin_tab")
              with gr.Box():
                with gr.Column():
                    text_output = gr.Markdown(lines=5,label="output")
 btn2.click(clear_code,outputs=[text2])
 btn1.click(output_ans, inputs=[text2,text1,dropdown1,key], outputs=[text_output])
 # 程式碼 Debug
 with gr.Tab("程式碼 Debug"):               
    with gr.Row():
        with gr.Column(scale=6):
            text1 = gr.Textbox(label="",value="",placeholder="api key")
            text2 = gr.Textbox(label="",value="",placeholder="程式碼")
            
        with gr.Column(): 
            with gr.Box():
                btn2 = gr.Button(elem_id="testpls",value="Clear Code")
                btn1 = gr.Button(elem_id="testpls2",value="START")
    with gr.Row():
        with gr.Column(scale=1):   
              with gr.Box():
                with gr.Column():
                    key =gr.HighlightedText(value="程式碼 Debug",label="",interactive=False)
                with gr.Box(): 
                    text_input1 = gr.Markdown(value="這個指令可以幫你檢查現有程式碼是否有執行上的 bug 或一些潛在問題。",label="")
                    text_input2 = gr.Markdown(value="指令功能：檢查現有程式碼，排除問題程式碼。",label="")
                    text_input3 = gr.Markdown(value="分析下方 <{程式語言}> 程式碼，針對邏輯和文法上偵錯，並提出正確改寫方式。",label="")
                    text_input4= gr.Markdown(value="<{程式碼}>",label="")
              with gr.Box():
                with gr.Column():
                    text_output = gr.Markdown(lines=5,label="output")
 btn2.click(clear_code,outputs=[text2])
 btn1.click(output_ans, inputs=[text2,text1,dropdown1,key], outputs=[text_output])
 
# 撰寫程式碼測試案例

 with gr.Tab("撰寫程式碼測試案例"):               
   with gr.Row():
        with gr.Column(scale=6):
            text1 = gr.Textbox(label="",value="",placeholder="api key")
            text2 = gr.Textbox(label="",value="",placeholder="程式碼")
            
        with gr.Column(): 
            with gr.Box():
                btn2 = gr.Button(elem_id="testpls",value="Clear Code")
                btn1 = gr.Button(elem_id="testpls2",value="START")
   with gr.Row():
        with gr.Column(scale=1):   
              with gr.Box():
                with gr.Column():
                    key =gr.HighlightedText(value="程式碼 Debug",label="",interactive=False)
                with gr.Box(): 
                    text_input1 = gr.Markdown(value="這段指令可以幫你提供的程式碼撰寫測試案例，可以在指令中指定要產生的案例數。",label="")
                    text_input2 = gr.Markdown(value="指令功能：撰寫程式測試案例",label="")
                    text_input3 = gr.Markdown(value="指令：請幫下方 <{程式語言}> 程式碼，設計 <{數量}> 個測試案例，並確定這些測試案例皆可正確使用。",label="")
                    text_input4= gr.Markdown(value="<{程式碼}>",label="")
        with gr.Box():
                with gr.Column():
                    text_output = gr.Markdown(lines=5,label="output")
 btn2.click(clear_code,outputs=[text2])
 btn1.click(output_ans, inputs=[text2,text1,dropdown1,key], outputs=[text_output])
 with gr.Tab("chatpdf"):               
    with gr.Row():
        with gr.Column(scale=6):
            text1 = gr.Textbox(label="",value="",placeholder="api key")
    with gr.Row():
        with gr.Column(scale=1):   
              with gr.Box():
                with gr.Column():
                    key =gr.HighlightedText(value="程式碼 Debug",label="",interactive=False)
                with gr.Box(): 
                    text_input1 = gr.Markdown(value="這個指令可以幫你檢查現有程式碼是否有執行上的 bug 或一些潛在問題。",label="")
                    text_input2 = gr.Markdown(value="指令功能：檢查現有程式碼，排除問題程式碼。",label="")
                    text_input3 = gr.Markdown(value="分析下方 <{程式語言}> 程式碼，針對邏輯和文法上偵錯，並提出正確改寫方式。",label="")
                    text_input4= gr.Markdown(value="<{程式碼}>",label="")
              with gr.Box():
                with gr.Column():
                        file_output = gr.File()
                        file_button = gr.Button(elem_id="testpls2",value="update")
                        text_output = gr.Markdown(lines=5,label="output")
 file_button.click(upload_file,inputs=[file_output,text1], outputs=[text_output])
demo.launch()   