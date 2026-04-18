import os
import json
import fitz  # PyMuPDF，处理PDF
import easyocr  # OCR处理图片
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# 初始化客户端
client = OpenAI(
    api_key=os.getenv("LONGCAT_API_KEY", ""),
    base_url=os.getenv("LONGCAT_BASE_URL", "https://api.longcat.chat/openai")
)

# 初始化OCR阅读器（支持多语言，此处指定中文）
ocr_reader = easyocr.Reader(['ch_sim', 'en'])


def extract_text_from_file(file_path):
    """
    从图片/PDF中提取文本
    :param file_path: 文件路径（支持jpg/png/pdf）
    :return: 提取的文本字符串
    """
    file_ext = os.path.splitext(file_path)[-1].lower()

    # 处理图片（OCR）
    if file_ext in ['.jpg', '.jpeg', '.png']:
        result = ocr_reader.readtext(file_path, detail=0)
        return '\n'.join(result)

    # 处理PDF
    elif file_ext == '.pdf':
        text = ""
        pdf_doc = fitz.open(file_path)
        for page in pdf_doc:
            text += page.get_text()
        pdf_doc.close()
        return text

    else:
        raise ValueError(f"不支持的文件格式：{file_ext}，仅支持jpg/png/pdf")


def extract_medical_info(file_path):
    """
    提取体检报告关键信息并返回结构化JSON
    :param file_path: 体检报告文件路径（图片/PDF）
    :return: 结构化JSON字符串
    """
    # 1. 提取文件文本
    try:
        report_text = extract_text_from_file(file_path)
        if not report_text:
            return json.dumps({"error": "文件中未提取到文本"}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": f"文件解析失败：{str(e)}"}, ensure_ascii=False)

    # 2. 构造大模型提示词
    prompt = f"""
    你是高精度OCR数据提取助手，需要从以下体检报告文本中提取信息，仅返回结构化JSON格式数据。
    JSON结构要求：
    {{
        "姓名": "提取的姓名",
        "性别": "提取的性别（男/女）",
        "年龄": 提取的年龄（数字）,
        "检测日期": "提取的检测日期（格式：YYYY-MM-DD）",
        {{"指标名称1（如：血常规）":{{"结果": "检测数值","参考范围": "参考范围（如：4-10×10^9/L）"}},
        {{"指标名称2（如：血常规）":{{"结果": "检测数值","参考范围": "参考范围（如：4-10×10^9/L）"}},
    }}
    注意：
    1. 指标列表需包含所有可提取的检测指标；
    2. 体检报告需要提取的数据有["subject_identifier","age","sex","male","height","weight","BMI","trestbps","sysBP","diaBP","ap_hi","ap_lo","heartRate","thalach","chol","totChol","cholest","High_LDL","Low_HDL","fbs","gluc","glucose","anemia","creatinin","platelets","serum_creatinine","sodium","ejection","Quantum","smoke","currentSmok","cigsPerDay","alco","Alcohol","BPMeds","diabetes","high_blood_pressure","active","Exercise","Family_History","No_Diseases","stress","Sleep","sugar","diet","obesity","cp","restecg","exang","oldpeak","slope","ca","thal","subject","segment1","segment2","segment3","segment4","Num","target","cardio","HeartDisease","Risk","DEATH_EVENT","time"]，提取完整
    3. 若某字段无信息，填充为null，无需提取id字段；
    4. 除了subject_identifier、trestbps字段外，其他的字段必须为数字类型，无则为null；
    5. 字段中的“time”字段等同于“检测日期”字段。
    
    体检报告文本：
    {report_text}
    """

    # 3. 调用LongCat模型
    try:
        response = client.chat.completions.create(
            model="LongCat-Flash-Chat",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.0  # 降低随机性，保证输出稳定
        )
        # 提取模型返回的JSON字符串
        json_result = response.choices[0].message.content.strip()

        # 验证JSON格式是否合法
        json.loads(json_result)
        return json_result

    except json.JSONDecodeError:
        return json.dumps({"error": "模型返回非合法JSON格式"}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": f"模型调用失败：{str(e)}"}, ensure_ascii=False)


# 示例调用
if __name__ == "__main__":
    # 替换为你的体检报告文件路径（图片/PDF）
    file_path = "高危心脏病风险评估报告.pdf"  # 或 "体检报告.jpg"
    result = extract_medical_info(file_path)
    # 格式化输出JSON（便于阅读）
    print(json.dumps(json.loads(result), ensure_ascii=False, indent=2))
