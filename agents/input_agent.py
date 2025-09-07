from langchain_core.prompts import PromptTemplate 
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_core.pydantic_v1 import BaseModel, Field 
 
class InputAnalysis(BaseModel): 
    product_line: str = Field(description="The validated and refined product line") 
 
def input_agent_node(state): 
    """ 
    A LangGraph node representing the InputAgent. 
    This agent takes the raw user input and processes it. 
    """ 
    print(f"[InputAgent] -> Analyzing product:{state['product_line']}...") 
     
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash") 
     
    prompt = PromptTemplate( 
        template="""You are a business analysis AI. Your task is to 
validate and refine a given product line. 
        If the input is vague, make it more specific. 
        Return ONLY a short, concise product line name (maximum 10 words).

        Product line: {product_line} 
         
        Refined product line:""", 
        input_variables=["product_line"] 
    ) 
     
    refined_product_line = llm.invoke(prompt.format(product_line=state['product_line'])).content.strip() 
     
    print(f"[InputAgent] -> Refined product line: {refined_product_line}") 
     
    return {"product_line": refined_product_line} 