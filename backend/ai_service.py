def detect_entry_type(content: str) -> str:
    word_count = len(content.split())

    if content.endswith((".", "?", "!")) or word_count >= 5:
        return "sentence"

    if word_count >= 2:
        return "phrase"

    return "word"


def generate_entry_with_ai(content: str, context: str | None = None):
    entry_type = detect_entry_type(content)

    normalized_content = content.lower()
    normalized_context = (context or "").lower()

    if normalized_content == "model":
        if "deploy" in normalized_context or "production" in normalized_context:
            return {
                "entry_type": entry_type,
                "chinese_meaning": "模型",
                "explanation": "在当前语境中，model 指被部署到生产环境中的 AI 或软件模型。",
                "part_of_speech": "noun",
            }

        return {
            "entry_type": entry_type,
            "chinese_meaning": "模型；模式；模特",
            "explanation": "model 是多义词，缺少明确上下文时，只能给出常见含义。",
            "part_of_speech": "noun",
        }

    if normalized_content == "run":
        if "code" in normalized_context or "program" in normalized_context:
            return {
                "entry_type": entry_type,
                "chinese_meaning": "运行",
                "explanation": "在当前语境中，run 指运行代码或程序。",
                "part_of_speech": "verb",
            }

        if "company" in normalized_context or "business" in normalized_context:
            return {
                "entry_type": entry_type,
                "chinese_meaning": "经营；管理",
                "explanation": "在当前语境中，run 指经营公司或管理业务。",
                "part_of_speech": "verb",
            }

        return {
            "entry_type": entry_type,
            "chinese_meaning": "跑；运行；经营",
            "explanation": "run 是多义词，具体含义需要结合上下文判断。",
            "part_of_speech": "verb",
        }

    if entry_type == "phrase":
        return {
            "entry_type": entry_type,
            "chinese_meaning": "这是一个短语的模拟中文含义",
            "explanation": "当前内容包含多个单词，因此被识别为短语。",
            "part_of_speech": "phrase",
        }

    if entry_type == "sentence":
        return {
            "entry_type": entry_type,
            "chinese_meaning": "这是一个句子的模拟中文翻译",
            "explanation": "当前内容较长或包含句号、问号、感叹号，因此被识别为句子。",
            "part_of_speech": "sentence",
        }

    return {
        "entry_type": entry_type,
        "chinese_meaning": "这是模拟 AI 生成的中文意思",
        "explanation": "当前还没有接入真实 AI，因此返回默认 mock 结果。",
        "part_of_speech": "unknown",
    }