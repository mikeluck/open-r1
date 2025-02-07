import gradio as gr
import pandas as pd

# 全局变量存储 CSV 数据和索引
csv_data = None
current_index = 0
annotations = []

def upload_csv(file):
    global csv_data, current_index, annotations
    csv_data = pd.read_csv(file.name)
    current_index = 0
    annotations = []
    return display_current()

def display_current():
    if csv_data is None or current_index >= len(csv_data):
        return "No Data", "", ""
    
    row = csv_data.iloc[current_index]
    return f"## Prompt\n{row['prompt']}", f"## Model A\n{row['model_a']}", f"## Model B\n{row['model_b']}"

def annotate(label):
    global current_index
    if csv_data is None or current_index >= len(csv_data):
        return "No Data", "", ""

    # 记录标注
    row = csv_data.iloc[current_index].copy()
    row['label'] = label
    annotations.append(row)

    # 移动到下一条数据
    current_index += 1
    return display_current()

def save_csv():
    if not annotations:
        return "No annotations to save."

    df = pd.DataFrame(annotations)
    df.to_csv("annotated_data.csv", index=False)
    return "Annotations saved to annotated_data.csv"


def main():

    with gr.Blocks() as demo:
        gr.Markdown("# CSV Data Annotation Tool")
        upload_button = gr.File(label="Upload CSV", file_types=[".csv"], interactive=True)
        
        with gr.Row():
            prompt_md = gr.Markdown()
            model_a_md = gr.Markdown()
            model_b_md = gr.Markdown()
        
        with gr.Row():
            btn_a = gr.Button("Model A is better")
            btn_b = gr.Button("Model B is better")
            btn_tie = gr.Button("Tie")
            btn_bad = gr.Button("Both are bad")
        
        save_button = gr.Button("Save Annotations")
        save_status = gr.Textbox(label="Status", interactive=False)

        # 事件绑定
        upload_button.upload(upload_csv, upload_button, [prompt_md, model_a_md, model_b_md])

        btn_a.click(lambda: annotate("Model A is better"), None, [prompt_md, model_a_md, model_b_md])
        btn_b.click(lambda: annotate("Model B is better"), None, [prompt_md, model_a_md, model_b_md])
        btn_tie.click(lambda: annotate("Tie"), None, [prompt_md, model_a_md, model_b_md])
        btn_bad.click(lambda: annotate("Both are bad"), None, [prompt_md, model_a_md, model_b_md])

        save_button.click(save_csv, None, save_status)

    demo.launch(
            share=False,
            server_port=2333,
            server_name='127.0.0.1'
        )

if __name__ == "__main__":
    main()