# AI Vocabulary Assistant

Repository: ai-vocab

AI Vocabulary Assistant 是一个基于 Python/FastAPI + AI 大模型的轻量级 AI 单词本项目。

用户在阅读英文内容时，可以选中不认识的单词、短语或句子。系统根据当前上下文生成准确中文意思，并加入个人单词本。

## 核心规则

- content 是用户选中的内容，需要保存。
- context 只作为 AI 判断当前语境下中文意思的临时输入，不保存到数据库。
- 不保存网页 URL、网页标题、原始上下文。
- 核心对象叫 Entry，不叫 Word。
- Entry 支持 word、phrase、sentence 三种类型。

## 项目结构

```text
backend/    FastAPI 后端
frontend/   Web 单词本页面
extension/  浏览器插件
docs/       项目文档