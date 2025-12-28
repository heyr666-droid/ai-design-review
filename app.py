import streamlit as st
from PIL import Image
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="AI设计图评审助手", page_icon="🎨")
st.title("🎨 基于大模型的设计稿评审与优化建议生成")
st.markdown("上传你的设计图，并填写简单描述，AI将从专业角度分析设计的优缺点并提出优化建议。")

uploaded_file = st.file_uploader("📤 上传设计图（JPG/PNG）", type=["jpg", "jpeg", "png"])

if uploaded_file:
    
    image = Image.open(uploaded_file)
    st.image(image, caption="上传的设计图", use_column_width=True)

    image_desc = st.text_area("📝 请描述设计图的内容（如风格、配色、排版、情绪等）", height=120)

    if st.button("🧠 开始AI文本分析"):
        if not image_desc.strip():
            st.warning("⚠️ 请输入设计图的描述内容！")
        else:
            with st.spinner("AI 正在分析中，请稍候..."):
                try:
                    prompt = f"""
你是一位拥有10年经验的设计评审专家。以下是用户上传的设计图的描述：
{image_desc}

请你作为专业评审，从以下几个维度进行评价：
- 设计风格（是否统一、是否表达清晰）
- 配色搭配（是否协调，是否有冲突）
- 排版结构（信息层次是否清晰）
- 情绪表达（视觉传达是否到位）

请你：
1. 列出该设计图的**优点**（若有）
2. 明确指出存在的**不足或问题**（若存在）
3. 提出**3条具体改进建议**

务必保持客观、中肯、专业。
"""

                    response = openai.ChatCompletion.create(
                        model="gpt-4",  
                        messages=[
                            {"role": "system", "content": "你是专业的AI设计分析助手"},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7
                    )

                    result = response['choices'][0]['message']['content']
                    st.success("🎉 分析完成！")
                    st.markdown("### ✨ 设计分析结果")
                    st.write(result)

                except Exception as e:
                    st.error(f"❌ 出错了: {e}")
