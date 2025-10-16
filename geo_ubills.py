from langchain.prompts import  ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper
from opencc import OpenCC
def generate_script(subject,video_length,creativity,api_key):
    cc = OpenCC('t2s')  # 繁体转简体

    title_template = ChatPromptTemplate.from_messages(
       [
           ("human","请为{subject}这个地理主题的视频写一个吸引人的标题。请使用简体中文。")
       ]
    )
    script_template = ChatPromptTemplate.from_messages(
        [
            "human",
            """你是一位地理方向短视频频道的博主。根据以下的标题和相关信息，为短视频频道写一个视频脚本。
            视频标题: {title},视频时长: {duration}分钟,生成的脚本的长度尽量遵循视频时长的要求。
            要求开头抓住眼球，中间提供干货内容，结尾有惊喜，脚本格式也请按照【开头、中间、结尾】分隔。
            整体内容的表达方式要尽量轻松有趣，吸引年轻人。
            脚本内容可以结合一下维基百科搜索出的信息，但仅作为参考，直结合相关的即可，对不相关的内容进行忽略：
            '''{wikipedia_search}'''全部内容请使用简体中文。"""
        ]
    )

    model = ChatOpenAI(
        openai_api_key=api_key,  # 你的 DeepSeek API Key
        openai_api_base="https://api.deepseek.com/v1",  # DeepSeek API 地址
        model_name="deepseek-chat",
        temperature=creativity)

    title_chain =title_template| model
    script_chain = script_template | model

    title = title_chain.invoke({"subject":subject}).content
    search = WikipediaAPIWrapper(lang = "zh")
    search_result = search.run(subject)

    script =script_chain.invoke({"title":title,"duration":video_length,
                                 "wikipedia_search":search_result}) .content
    title_simplified = cc.convert(title)
    script_simplified = cc.convert(script)
    search_result_simplified = cc.convert(search_result)
    return  title_simplified,script_simplified,search_result_simplified
