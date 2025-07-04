from crewai import LLM, Agent, Crew, Process, Task
from crewai_tools import FileReadTool, FileWriterTool
from dotenv import load_dotenv
import os

load_dotenv()


llm = LLM(
    model="gemini/gemini-2.5-flash-preview-04-17"
)
uploaded_brd="C:\\Users\\l43ar\\Downloads\\mermaiddynamic\\BRD.txt"
def generate_srs(uploaded_brd, original_filename="brd"):


        if uploaded_brd:
            print("[INFO] Upload received")
            filename = original_filename or "BRD.txt"
            name, ext = os.path.splitext(filename)
            ext = ext.lower()
            temp_dir = "../uploads"
            os.makedirs(temp_dir, exist_ok=True)

            # Normalized .txt file path
            brd_path = os.path.join(temp_dir, f"{name}.txt")

            try:
                if ext == ".docx":
                    import io
                    from docx import Document

                    print("[INFO] Converting DOCX to text...")
                    doc = Document(io.BytesIO(uploaded_brd))

                    text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
                    safe_text = ''.join([c if ord(c) < 128 or c in '\n\r\t' else '' for c in text])

                    with open(brd_path, "w", encoding="utf-8") as f:
                        f.write(safe_text)

                    print(f"[INFO] Cleaned DOCX saved to {brd_path}")

                elif ext == ".pdf":
                    import io
                    import fitz  # PyMuPDF

                    print("[INFO] Converting PDF to text...")
                    pdf = fitz.open(stream=io.BytesIO(uploaded_brd), filetype="pdf")
                    text = "\n".join([page.get_text() for page in pdf])
                    pdf.close()

                    safe_text = ''.join([c if ord(c) < 128 or c in '\n\r\t' else '' for c in text])

                    with open(brd_path, "w", encoding="utf-8") as f:
                        f.write(safe_text)

                    print(f"[INFO] Cleaned PDF saved to {brd_path}")

            except Exception as e:
                print(f"[ERROR] Failed to process uploaded file: {e}")
                raise

        file_read_tool = FileReadTool(file_path=brd_path)
        file_writer_tool = FileWriterTool()


        #Agents (Generalized)
        cover_toc_agent = Agent(
            role="Cover Page and TOC Generator",
            goal="Generate a Word-style SRS cover page and a hyperlinked Table of Contents with proper formatting.",
            backstory="An expert in documentation formatting, markdown structuring, and technical styling of cover sections.",
            verbose=True,
            tools=[file_read_tool],
            llm=llm
        )

        introduction_agent = Agent(
            role="Introduction Section Expert",
            goal="Write a detailed introduction including purpose, scope : in-scope, out-of-scope, overview, definitions, and references using a combination of detailed descriptive paragraphs and Word-style tabular tables.",
            backstory="A documentation analyst specialized in converting business inputs into well-structured introductory sections.",
            verbose=True,
            tools=[file_read_tool],
            llm=llm
        )

        functional_agent = Agent(
            role="Functional Requirement Analyst",
            goal="Extract, organize and describe all functional requirements from gievn brd, using Word-style tabular tables and high-quality Mermaid diagrams (with styling and correct layout). Each diagram should have a clear markdown heading before its Mermaid code block.",
            backstory="An AI engineer who models system functionality with precision and visuals.",
            verbose=True,
            tools=[file_read_tool],
            llm=llm
        )

        nonfunctional_agent = Agent(
            role="Non-Functional Specialist",
            goal="Define and explain all non-functional requirements under categories like Performance, Security, Usability, Maintainability, etc., with explanatory text and Word-style tabular tables.",
            backstory="An architect focused on operational excellence and quality attributes.",
            verbose=True,
            llm=llm
        )

        technical_agent = Agent(
            role="Technical Environment Designer",
            goal="Describe operating environments, hardware/software stack, constraints, protocols using Word-style tables. For deployment architecture, generate Mermaid deployment diagrams with layout, styling, and proper section title before the diagram.",
            backstory="A systems architect with experience in environment planning and visualization.",
            verbose=True,
            llm=llm
        )

        interface_agent = Agent(
            role="Interface Requirement Engineer",
            goal="Document user, software, hardware, and communication interfaces using Word-style tabular format. Include detailed interface parameters, interaction flows, and standards.",
            backstory="A systems engineer with hands-on experience in interfacing complex components.",
            verbose=True,
            llm=llm
        )

        datamodel_agent = Agent(
            role="Data Model Engineer",
            goal="Generate a structured ER diagram using Mermaid with styling and layout direction. Precede the diagram with its title in markdown. Also, describe entities, attributes, and constraints in Word-style tabular tables.",
            backstory="A database expert in visual and tabular representation of data models.",
            verbose=True,
            tools=[file_read_tool],
            llm=llm
        )

        schema_agent = Agent(
            role="Database Schema Designer",
            goal="Document complete schema: table names, data types, PK/FK, and constraints in Word-style tabular tables. Provide a summary paragraph before each table to give context.",
            backstory="A schema author focused on clarity and developer-readiness.",
            verbose=True,
            tools=[file_read_tool],
            llm=llm
        )

        assumption_agent = Agent(
            role="Assumption Analyst",
            goal="Identify and document assumptions, dependencies, third-party systems, constraints with both descriptive paragraphs and Word-style tabular summaries.",
            backstory="A risk analyst identifying latent assumptions and external influences.",
            verbose=True,
            llm=llm
        )

        diagram_agent = Agent(
            role="Diagram Specialist",
            goal="Generate high-quality Mermaid diagrams for: Context, Use Case, Class, Sequence, Component, Activity, State, and Deployment. Each diagram must have a markdown heading (outside the code block) with title before the code block. Code must be valid, styled, and follow proper Mermaid logic.",
            backstory="A visualization specialist trained in architectural and behavioral modeling.",
            verbose=True,
            llm=llm
        )

        conclusion_agent = Agent(
            role="SRS Closing Writer",
            goal="Write the conclusion, glossary (as Word-style table), and appendices. Glossary should list terms, definitions, and acronyms. Ensure future scope and system limitations are addressed.",
            backstory="A documentation reviewer skilled in completing and polishing final drafts.",
            verbose=True,
            tools=[file_writer_tool],
            llm=llm
        )

        formatter_agent = Agent(
            role="SRS Formatter and Compiler",
            goal="Merge all section outputs into a single Markdown document with correct heading hierarchy, spacing, proper Mermaid code blocks, and consistent Word-style tabular formatting. Ensure final output is polished, readable, and professional.",
            backstory="A publishing tool for structured documentation ready for delivery.",
            verbose=True,
            tools=[file_writer_tool],
            llm=llm
        )


        cover_page_task = Task(
            description="Using gievn brd, generate the SRS cover page table in a Word-style tabular format. Include project name, version, authors, date, organization. Also generate a hyperlinked Table of Contents (ToC) using a proper layout for all main and sub-sections.",
            expected_output="Formatted word-style tabular format cover page table and linked ToC.",
            agent=cover_toc_agent
        )

        intro_task = Task(
            description="Using gievn brd, write the Introduction section, covering Purpose, In-Scope, Out-of-Scope, Overview - All in detailed paragraphs. Definitions in word-style tabular format table, and References in word-style tabular format table. Use explanatory paragraphs and tables in word-style tabular format where required.",
            expected_output="Introduction section with detailed paragraphs and Word-style tabular format tables.",
            agent=introduction_agent
        )

        functional_task = Task(
            description="From gievn brd, extract all functional requirements. Present each use case with descriptive text, Word-style tabular format use case tables, and generate Mermaid diagrams (Use Case, Sequence) with headings before each diagram. Ensure proper layout (graph TD / graph LR), styling, titles, and Mermaid syntax.",
            expected_output="Functional Requirements section with descriptive content, word-style tabular format tables, and mermaid diagrams code blocks with proper styling, layout and headings.",
            agent=functional_agent
        )

        nonfunctional_task = Task(
            description="List and describe all non-functional requirements like Performance, Reliability, Usability, etc. Provide brief explanatory paragraphs and organize content in Word-style tabular tables under each category.",
            expected_output="Non-Functional Requirements section with category-wise tables and paragraphs.",
            agent=nonfunctional_agent
        )

        technical_task = Task(
            description="Document the technical environment: hardware, software, network protocols, OS, architecture constraints. Use Word-style tabular tables. Also include a Mermaid Deployment diagram with proper heading, layout, and styling.",
            expected_output="Technical Environment section with tables and deployment diagram.",
            agent=technical_agent
        )

        interface_task = Task(
            description="Extract and describe all interfaces (User, Hardware, Software, Communication). Present each using Word-style tables with descriptions and interaction details.",
            expected_output="External Interfaces section organized by type with structured tables.",
            agent=interface_agent
        )

        datamodel_task = Task(
            description="Identify data entities from gievn brd. Generate an ER diagram using Mermaid with appropriate layout and styling. Place diagram title as markdown heading before the code block. Also provide Word-style tabular tables listing entities, attributes, data types, and constraints.",
            expected_output="Data Model section with styled Mermaid ER diagram and entity-attribute tables.",
            agent=datamodel_agent
        )

        schema_task = Task(
            description="Create database schema section from gievn brd. Include Word-style tabular tables for all tables, listing fields, data types, keys, and constraints. Write brief paragraphs to describe the purpose of each table before the table.",
            expected_output="Database Schema section with annotated and formatted tables.",
            agent=schema_agent
        )

        assumption_task = Task(
            description="List all business and technical assumptions, dependencies, third-party services, integration points, and known constraints. Use narrative explanation followed by Word-style tabular summaries wherever applicable.",
            expected_output="Assumptions and Dependencies section with meaningful tables.",
            agent=assumption_agent
        )

        diagram_task = Task(
            description="Generate styled Mermaid diagrams for: Context, Class, Sequence, Component, State, Activity, Deployment. For each, add a markdown section header with diagram title before Mermaid code block. Use correct layout (graph TD or graph LR), styling, and Mermaid syntax.",
            expected_output="Diagram section with individual labeled Mermaid diagrams and proper formatting.",
            agent=diagram_agent
        )

        conclusion_task = Task(
            description="Write a concluding section with: 1) Summary paragraph, 2) Future Enhancements, 3) Glossary (terms, acronyms, and definitions in Word-style tabular format), and 4) Appendices (if any).",
            expected_output="Conclusion, glossary, and appendices section formatted in markdown.",
            agent=conclusion_agent
        )

        formatter_task = Task(
            description="Compile all outputs into one final markdown SRS. Ensure correct heading levels, spacing, formatting, Mermaid block isolation, and that all Word-style tables render cleanly. Validate Mermaid code for diagram compatibility and markdown readability.",
            expected_output="Final, full-length SRS in markdown with all sections cleanly merged.",
            agent=formatter_agent,
            output_file="brd_srs.md"
        )



        # Initialize and execute the Crew
        try:
            print("[INFO] Starting Crew Process...")
            srs_crew = Crew(
                agents=[
                    cover_toc_agent,
                    introduction_agent,
                    functional_agent,
                    nonfunctional_agent,
                    technical_agent,
                    interface_agent,
                    datamodel_agent,
                    schema_agent,
                    assumption_agent,
                    diagram_agent,
                    conclusion_agent,
                    formatter_agent
                ],
                tasks=[
                    cover_page_task,
                    intro_task,
                    functional_task,
                    nonfunctional_task,
                    technical_task,
                    interface_task,
                    datamodel_task,
                    schema_task,
                    assumption_task,
                    diagram_task,
                    conclusion_task,
                    formatter_task
                ]
            )

            result = srs_crew.kickoff()
            print("[INFO] Crew process completed successfully.")

        except Exception as e:
            print(f"[ERROR] An error occurred during the Crew process: {e}")
            return f"Error: {str(e)}"


        # Construct the final output file path
        output_path = f"{original_filename}_srs.txt"

        # Read the generated SRS content
        if os.path.exists(output_path):
            with open(output_path, 'r', encoding='utf-8') as f:
                srs_content = f.read()
            return srs_content
        else:
            return "Error: Output file not found. Please Try Again!!"
# def feedback_worker(output_new_path,original_filename, feedback):
#     file_read_tool=FileReadTool(file_path=output_new_path)
#     file_writer_tool = FileWriterTool()

#     feedback_acceptor = Agent(
#             role="Feedback Acceptor",
#             goal=(
#                 "You are a senior business analyst with extensive experience in the healthcare industry. "
                
#             ),
#             backstory=(
#                 "A senior business analyst with extensive experience in the healthcare industry. Expert in "
#                 "understanding healthcare-specific business requirements, including regulatory compliance "
#                 "(HIPAA, GDPR, FDA guidelines, etc.), and ensuring clarity in documentation for healthcare applications."
#             ),
#             tools=[file_read_tool, file_writer_tool],
#             llm=llm,
#             )
#     feedabck_acceptor_task = Task(
#             description=(
#                 f"Your task is to only change the parts of the SRS document tht are given in tthe {feedback} by keeping the rest of the document intact"
                
#             ),
#             expected_output=(
#                 "A final **SRS document** that is clear, professional, and adheres to **healthcare compliance standards** "
#                 f"while being properly formatted and saved as `../outputs/{original_filename}_new_srs.txt`, make sure to use utf-8 encoding while making this file."
#             ),
#             llm=llm,
#             agent=feedback_acceptor
#     )
#     try:
#             print("[INFO] Starting Crew process...")
#             crew = Crew(
#                 agents=[
#                     feedback_acceptor
#                 ],
#                 tasks=[
#                     feedabck_acceptor_task
#                 ],
#                 process=Process.sequential,
#                 verbose=True,
#             )
#             crew.kickoff()
#             print("[INFO] Crew process completed.")
#     except Exception as e:
#             print(f"[ERROR] Crew execution failed: {e}")
#             raise e


#         # Construct the final output file path
#     new_path = f"../outputs/{original_filename}_new_srs.txt"

#         # Read the generated SRS content
#     if os.path.exists(new_path):
#             with open(new_path, 'r', encoding='utf-8') as f:
#                 srs_content = f.read()
#             return srs_content
#     else:
#             return "Error: Output file not found."
