from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser


def classifier(text: str, context: str):
    class Output(BaseModel):
        output: str = Field(
            description=f"whether the text is related to {context} 'yes'/'no'")

    llm = ChatOllama(model="qwen2.5:32b", temperature=0, format='json')
    parser = JsonOutputParser(pydantic_object=Output)

    template = """
        Identify whether text is related to AI applications and
        technologies for {context}.\n
        If related return 'yes' else 'no'.\n
        {text}

        Strictly follow the format instructions to return
        the response as a JSON.
        {format_instructions}
        """

    format_instructions = parser.get_format_instructions()
    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "text"],
        partial_variables={"format_instructions": format_instructions},
    )

    chain = prompt | llm | parser
    response = chain.invoke({"context": context, "text": text})
    return response
