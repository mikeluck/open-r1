import gradio as gr
import pandas as pd
import random
import csv

latex_delimiters = [
    {"left": "$", "right": "$", "display": False},
    # {"left": "$$", "right": "$$", "display": True},
    # {"left": "\\(", "right": "\\)", "display": False},
    # {"left": "\[", "right": "\]", "display": True}
]

def load_data(file):
    """加载CSV文件并返回随机一条数据"""
    df = pd.read_csv(file.name)
    random_idx = random.randint(0, len(df)-1)
    return df, random_idx, *format_markdown(df.iloc[random_idx])

def format_markdown(row):
    """将数据格式化为三个独立的Markdown内容"""
    prompt_md = f"### 📝 Prompt\n{row['prompt']}"
    model_a_md = f"### 🤖 Model A\n{row['model_a']}"
    model_b_md = f"### 🤖 Model B\n{row['model_b']}"
    return prompt_md, model_a_md, model_b_md

def save_label(label, df, current_idx):
    """保存标注结果并返回新数据"""
    if df is None:
        return "请先上传CSV文件", None, None, None, None
    
    # 保存当前记录
    row = df.iloc[current_idx]
    with open('labeled_results.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['prompt', 'model_a', 'model_b', 'label'])
        if f.tell() == 0:  # 写入header如果文件为空
            writer.writeheader()
        writer.writerow({
            'prompt': row['prompt'],
            'model_a': row['model_a'],
            'model_b': row['model_b'],
            'label': label
        })
    
    # 获取新数据
    new_idx = random.randint(0, len(df)-1)
    return df, new_idx, *format_markdown(df.iloc[new_idx])

with gr.Blocks() as demo:
    gr.Markdown("# 模型响应标注工具")
    
    # 状态存储
    df_state = gr.State()
    idx_state = gr.State()
    
    # 上传组件
    with gr.Row():
        file_input = gr.File(label="上传CSV文件", file_types=[".csv"])
    
    # 数据展示区域 - 使用Grid布局
    with gr.Column(visible=False) as display_area:
        # 顶部Prompt展示
        prompt_display = gr.Markdown(
            "",
            elem_classes=["prompt-box"],
            latex_delimiters=latex_delimiters)
        
        # 模型响应并列展示
        with gr.Row():
            with gr.Column(scale=1):
                model_a_display = gr.Markdown(
                    "",
                    elem_classes=["model-box"],
                    latex_delimiters=latex_delimiters)
            with gr.Column(scale=1):
                model_b_display = gr.Markdown(
                    "",
                    elem_classes=["model-box"],
                    latex_delimiters=latex_delimiters)

    # 标注按钮
    with gr.Row():
        btn_a = gr.Button("👍 Model A 更好", variant="primary")
        btn_b = gr.Button("👍 Model B 更好", variant="primary")
        btn_tie = gr.Button("🤝 平局")
        btn_bad = gr.Button("👎 都不好")

    # 上传文件事件
    file_input.upload(
        lambda: gr.Column(visible=True),
        outputs=display_area
    ).then(
        load_data,
        inputs=file_input,
        outputs=[df_state, idx_state, prompt_display, model_a_display, model_b_display]
    )

    # 按钮点击事件
    button_click = [
        btn_a.click(
            lambda df, idx: save_label("model_a", df, idx),
            inputs=[df_state, idx_state],
            outputs=[df_state, idx_state, prompt_display, model_a_display, model_b_display]
        ),
        btn_b.click(
            lambda df, idx: save_label("model_b", df, idx),
            inputs=[df_state, idx_state],
            outputs=[df_state, idx_state, prompt_display, model_a_display, model_b_display]
        ),
        btn_tie.click(
            lambda df, idx: save_label("tie", df, idx),
            inputs=[df_state, idx_state],
            outputs=[df_state, idx_state, prompt_display, model_a_display, model_b_display]
        ),
        btn_bad.click(
            lambda df, idx: save_label("bad", df, idx),
            inputs=[df_state, idx_state],
            outputs=[df_state, idx_state, prompt_display, model_a_display, model_b_display]
        )
    ]

# 添加自定义CSS样式
css = """
.prompt-box {
    padding: 20px;
    border: 2px solid #4CAF50;
    border-radius: 10px;
    margin: 10px 0;
}
.model-box {
    padding: 15px;
    border: 1px solid #2196F3;
    border-radius: 8px;
    margin: 5px;
    min-height: 200px;
}
"""

demo.css = css

demo.launch(
    share=False,
    server_port=2333,
    server_name='127.0.0.1'
)