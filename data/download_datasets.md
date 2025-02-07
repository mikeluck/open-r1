# Download Datasets



- `bespokelabs/Bespoke-Stratos-17k`：这是一个复制伯克利 Sky-T1 数据处理管道的项目，使用 DeepSeek-R1 创建一个包含问题、推理轨迹和答案的数据集。随后，这些数据被用于通过类似 R1 论文的蒸馏方法来微调 7B 和 32B Qwen 模型。

- `open-thoughts/OpenThoughts-114k`：这是一个“开放的合成推理数据集，包含 114,000 个高质量的示例，涵盖数学、科学、代码和谜题”。这是 Open Thoughts 计划的一部分。

- `cognitivecomputations/dolphin-r1`：这是一个包含 80万个样本的数据集，样本来源于 DeepSeek-R1、Gemini flash 和 20万个来自 Dolphin 聊天的样本，旨在帮助训练 R1 风格的模型。

- `ServiceNow-AI/R1-Distill-SFT`：目前有 17,000 个样本，这是 ServiceNow 语言模型实验室的努力，旨在创建数据以支持 Open-R1 计划。

- `NovaSky-AI/Sky-T1_data_17k`：这是一个用于训练 Sky-T1-32B-Preview 的数据集。该数据集是为了复制 o1 风格推理的较早努力之一。基于这个数据集训练的模型花费不到 450 美元。有关更多细节，可以查看这篇博客文章。

- `Magpie-Align/Magpie-Reasoning-V2-250K-CoT-Deepseek-R1-Llama-70B`：这个数据集扩展了 Magpie，并采用没有初始提示的生成指令数据的方法，以便在回答中包含推理。指令由 Llama 3.1 70B Instruct 和 Llama 3.3 70B Instruct 生成，响应由 DeepSeek-R1-Distill-Llama-70B 生成。