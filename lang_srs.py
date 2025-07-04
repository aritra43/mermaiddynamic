from dotenv import load_dotenv
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import os
from flowdig import chart_generator
from docx import Document
import json
# from brdtosrsnew import generate_srs
from crewbrdtosrs import generate_srs
load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
# application = "1. Working Process of a Solar Power Generation SystemA Solar Power Generation System is an innovative and sustainable technology designed to convert sunlight into usable electrical energy. The entire process begins with the installation of solar panels, which are strategically positioned on rooftops, open fields, or large-scale solar farms to maximize exposure to sunlight. These panels are composed of numerous photovoltaic (PV) cells made from semiconductor materials such as silicon. When sunlight strikes the surface of these PV cells, the energy from the photons excites the electrons within the semiconductor, causing them to move and generate an electric current. This initial form of electricity produced is known as direct current (DC), which is not directly suitable for powering most household appliances or for integration with the conventional electrical grid. To make the electricity compatible and usable, it is passed through a crucial device called an inverter. The inverter converts the direct current (DC) into alternating current (AC), the standard form of electricity used in homes, industries, and businesses. Once converted, this electrical energy can be utilized immediately to run appliances and machinery, stored in batteries for later use, or fed back into the public power grid, depending on the system's configuration and the user's requirements. In grid-tied solar systems, any surplus energy that is not consumed on-site can be exported to the main electricity grid, allowing users to earn credits or payments through net metering arrangements offered by utility companies. Modern solar power systems also incorporate advanced monitoring units that track real-time energy production, system efficiency, and overall performance, providing users and technicians with valuable insights into system health and functionality. Regular maintenance, including the cleaning of solar panels to remove dust and debris and the routine inspection of inverters and electrical connections, is essential to ensure the system operates at peak efficiency. Through this seamless and efficient process, solar power generation systems provide a reliable, renewable, and environmentally friendly source of electricity, significantly reducing dependence on fossil fuels and contributing to global efforts in combating climate change.2. Working Process of an E-commerce Order Fulfillment SystemThe E-commerce Order Fulfillment System is a complex yet highly efficient logistical operation designed to ensure that products ordered through online platforms are processed, packaged, and delivered accurately to customers in a timely manner. The process initiates when a customer browses an e-commerce website or mobile application, selects the desired products, provides shipping and contact information, and completes the purchase using one of several available payment options, which may include digital wallets, credit or debit cards, net banking, or cash on delivery. Once the order is successfully placed, the order management system of the e-commerce platform automatically processes the details and communicates with the warehouse management system to check product availability and initiate the next phase of the operation. If the product is available in stock, a pick list is generated containing the exact location and quantity of the items to be retrieved from the inventory. Warehouse personnel or automated robotic systems follow this list to accurately locate and collect the ordered items. After the products are picked, they undergo careful packaging using suitable materials that ensure product safety and integrity during transit. During this phase, essential documents such as invoices, warranty cards, and shipping labels are also included in the package. The packed order is then handed over to a designated logistics partner or courier service responsible for transportation and final delivery. A unique tracking number is generated and shared with the customer, enabling them to monitor the status and progress of their order in real time through various digital communication channels such as emails, SMS, or mobile app notifications. The logistics provider transports the package through a network of distribution centers, regional hubs, and delivery routes to ensure efficient and timely delivery. Upon arrival at the customer’s address, the package is delivered by the courier personnel, and in the case of cash-on-delivery orders, payment is collected at the time of receipt. The fulfillment process concludes with the customer receiving their order and, often, the opportunity to provide feedback on their shopping and delivery experience. This entire system, from order placement to final delivery, is designed to be highly streamlined, ensuring accuracy, speed, and customer satisfaction, which are critical for the success and reputation of any e-commerce business."
def extract_text_from_docx(docx_path: str) -> str:
    doc = Document(docx_path)
    full_text = ""
    for para in doc.paragraphs:
        full_text += para.text + "\n"
    return full_text.strip()

# Replace this with your actual Word file path
docx_path = "C:\\Users\\l43ar\\Downloads\\mermaiddynamic\\brd_srs (1).docx"
md_path="C:\\Users\\l43ar\\Downloads\\mermaiddynamic\\srs_sdd.md"
def extract_text_from_md(md_path: str) -> str:
    with open(md_path, "r", encoding="utf-8") as f:
        return f.read().strip()

# Replace this with your actual Markdown file path
md_path = "C:\\Users\\l43ar\\Downloads\\mermaiddynamic\\brd_srs.md"



application = extract_text_from_docx(docx_path)
class State(TypedDict):
    appl: str
    flow_one: str
    flow_two: str
    uploaded_brd:str

# def crew_runner(state:State)->State:
#     state["uploaded_brd"]="C:\\Users\\l43ar\\Downloads\\mermaiddynamic\\BRD.txt"
#     uploaded_brd=state["uploaded_brd"]
#     generate_srs(uploaded_brd=uploaded_brd)
#     return state
md_path="C:\\Users\\l43ar\\Downloads\\mermaiddynamic\\SRS_Healthcare_Appointment_Scheduling.md"
def extract_text_from_md(md_path: str) -> str:
    with open(md_path, "r", encoding="utf-8") as f:
        return f.read().strip()
application_new = extract_text_from_md(md_path)   
print(application_new)

def crew(state: State) -> State:
    state["appl"] = application
    content = state["appl"]
    
    prompt = ("""
        From the given {content} only extract the mermiad codes and then store each memaid code in a json file and for each code assign different keys in json file as 1,2,3,4.....No extra text should be extracted other than the mermaid code. Make the json file and te file should be named as diagramnew.json.Every key should be present only once.Do not generate any diagram schema only the mermaid codes should be given.Extract all type of mermaid code p[resent in teh file do not neglect any ofthem whether they are starting with graph LR or TD or not.
    """)

    chain = ChatPromptTemplate.from_template(prompt) | llm
    response = chain.invoke({"content": content}).content

    # Cleaning
    cleaned = response.replace("```mermaid", "").replace("```", "").strip()
    cleaned_response = response.replace("json", "").replace("```", "").strip()
    json_data = json.loads(cleaned_response)
    with open("diagramnew.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

    state["flow_one"] = cleaned
    print(f"\n[crew node] Generated Mermaid Code:\n{cleaned}\n")
    return state


import json

def crawler(state: State) -> State:
    print("\n[crawler node] Generating charts from diagramnew.json...\n")

    # Load the JSON file
    with open("diagramnew.json", "r") as file:
        diagram_data = json.load(file)

    # Iterate through keys 1 to n in order
    sorted_keys = sorted(diagram_data.keys(), key=lambda x: int(x))

    for key in sorted_keys:
        diagram = diagram_data[key]
        print(f"\n[crawler node] Generating chart for key: {key}\n")
        chart_generator(diagram)

    return state



workflow = StateGraph(State)
workflow.add_node("crew", crew)
workflow.add_node("crawler", crawler)
# workflow.add_node("crew_runner",crew_runner)
workflow.add_edge(START, "crew")
# workflow.add_edge("crew_runner","crew")
workflow.add_edge("crew", "crawler")
workflow.add_edge("crawler", END)

graph = workflow.compile()

# Invoke the workflow, nodes will print outputs themselves
final_state = graph.invoke({"appl": ""})
