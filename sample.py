Updated_codeAgents:from crewai import Agent

cover_toc_agent = Agent(
    role="Cover Page and TOC Generator",
    goal="Generate the SRS cover page using Word-style tables and a hyperlinked table of contents.",
    backstory="An expert in technical documentation formatting and structuring for professional software specs.",
    verbose=True
)

introduction_agent = Agent(
    role="Introduction Section Expert",
    goal="Write the Introduction, Purpose, Scope : in-scope and out-of-scope, and Overview sections in detailed paragraphs based on {brd_content}.",
    backstory="A requirements analyst skilled at interpreting business documents and extracting relevant context for SRS intro sections.",
    verbose=True
)

functional_agent = Agent(
    role="Functional Requirement Analyst",
    goal="Extract and describe all functional requirements with use case tables in Word-style tabular format and Mermaid diagram code blocks. Ensure proper layout, diagram type, styling, and use of node IDs for shape definitions instead of inline shape wrappers like () or [].",
    backstory="An AI systems engineer trained to convert business needs into modular, testable, and well-defined functionalities with visuals.",
    verbose=True
)

nonfunctional_agent = Agent(
    role="Non-Functional Specialist",
    goal="Define detailed non-functional requirements like performance, security, scalability, maintainability, etc.",
    backstory="A software quality and compliance expert responsible for non-functional system expectations.",
    verbose=True
)

technical_agent = Agent(
    role="Technical Environment Designer",
    goal="Document operating environment, tech stack, third-party dependencies, and architectural constraints. Generate deployment diagrams using Mermaid with proper layout, styling, and correct node shape declarations (avoid inline () or []).",
    backstory="A technical architect experienced in documenting software deployment environments and tech dependencies.",
    verbose=True
)

interface_agent = Agent(
    role="Interface Requirement Engineer",
    goal="Document user, hardware, software, and communication interfaces in Word-style tables.",
    backstory="A systems integrator expert in describing how the software will interface with external components.",
    verbose=True
)

datamodel_agent = Agent(
    role="Data Model Engineer",
    goal="Create ER diagrams, define data entities, attributes, and constraints using Mermaid code blocks with proper node ID-based shape declaration. Also provide Word-style tables.",
    backstory="A database designer skilled at modeling structured data and visualizing relationships.",
    verbose=True
)

schema_agent = Agent(
    role="Database Schema Designer",
    goal="Document table structures, field types, primary/foreign keys, and data validation rules.",
    backstory="A database documentation expert focused on producing developer-ready schema specifications.",
    verbose=True
)

assumption_agent = Agent(
    role="Assumption Analyst",
    goal="List all assumptions, business/technical dependencies, and external constraints.",
    backstory="A risk and dependency analyst skilled at spotting implied or required assumptions for successful delivery.",
    verbose=True
)

diagram_agent = Agent(
    role="Diagram Specialist",
    goal="Generate all UML-style diagrams using Mermaid code blocks with styling. Ensure node shapes are declared using ID-based syntax (e.g., A(Rounded), B[Rectangle]) and not inline [].",
    backstory="An expert in software visualization and AI-based diagram synthesis.",
    verbose=True
)

conclusion_agent = Agent(
    role="SRS Closing Writer",
    goal="Write the summary, glossary, future scope, and appendices to complete the SRS.",
    backstory="A documentation expert who specializes in wrapping up technical documents with clarity and completeness.",
    verbose=True
)

formatter_agent = Agent(
    role="SRS Formatter and Compiler",
    goal="Merge all sections into a final markdown-based SRS with heading hierarchy, Word-style tables, and Mermaid code blocks with correct layout, styling, and diagram syntax using proper node ID format.",
    backstory="An AI-based documentation engine trained in technical formatting, readability, and publishing.",
    verbose=True
)
Tasks:from crewai import Task

cover_page_task = Task(
    description="Using {brd_content}, generate the SRS Cover Page in a Word-style tabular format and a hyperlinked Table of Contents (ToC) using a proper layout for all main and sub-sections.",
    expected_output="Formatted cover page in word-style table and linked ToC.",
    agent=cover_toc_agent
)

intro_task = Task(
    description="Using {brd_content}, write the Introduction section, covering Purpose, Scope: In-Scope, Out-of-Scope, Overview in detailed paragraphs. Definitions in Word-style table, and References in Word-style table. Use explanatory paragraphs and word-style tables where required.",
    expected_output="Introduction section with detailed paragraphs and Word-style tabular tables.",
    agent=introduction_agent
)

functional_task = Task(
    description="From {brd_content}, extract all functional requirements. Present each use case with descriptive text, use case tables in Word-style tabular format, and generate Mermaid diagram code blocks. Use node IDs to define shapes (e.g., A(Rounded), B[Square]), not inline shape wrappers in connections. Include headings before each diagram and specify correct layout (graph TD / graph LR) and styling.",
    expected_output="Functional Requirements section with descriptive content, word-style tabular tables, and properly styled Mermaid diagrams using ID-based syntax.",
    agent=functional_agent
)

nonfunctional_task = Task(
    description="List and describe all non-functional requirements like Performance, Reliability, Usability, etc. Provide brief explanatory paragraphs and organize content in Word-style tabular tables under each category from the {brd_content}.",
    expected_output="Non-Functional Requirements section with category-wise Word-style tabular tables and paragraphs.",
    agent=nonfunctional_agent
)

technical_task = Task(
    description="From the {brd_content}, document the technical environment: hardware, software, network protocols, OS, architecture constraints. Use Word-style tabular tables. Include a Mermaid Deployment diagram using proper layout, styling, and syntax. Use node IDs to define shapes instead of inline ()/[] inside connections.",
    expected_output="Technical Environment section with Word-style tabular tables and a correctly formatted deployment diagram in Mermaid.",
    agent=technical_agent
)

interface_task = Task(
    description="From the {brd_content}, extract and describe all interfaces (User, Hardware, Software, Communication). Present each using Word-style tables with descriptions and interaction details.",
    expected_output="External Interfaces section organized by type with structured Word-style tables.",
    agent=interface_agent
)

datamodel_task = Task(
    description="Identify data entities from {brd_content}. Generate a Mermaid ER diagram using proper layout, diagram type, and styling. Use headings before the code block. Ensure node shape declarations use ID-based syntax instead of inline shape brackets. Provide Word-style tables listing entities, attributes, data types, and constraints.",
    expected_output="Data Model section with styled Mermaid ER diagram and Word-style tabular tables for entities and attributes.",
    agent=datamodel_agent
)

schema_task = Task(
    description="Create database schema section from {brd_content}. Include Word-style tabular tables for all tables, listing fields, data types, keys, and constraints. Write brief paragraphs to describe the purpose of each table before the table.",
    expected_output="Database Schema section with annotated Word-style tables.",
    agent=schema_agent
)

assumption_task = Task(
    description="From {brd_content}, list all business and technical assumptions, dependencies, third-party services, integration points, and known constraints. Use narrative explanation followed by Word-style tabular summaries wherever applicable.",
    expected_output="Assumptions and Dependencies section with detailed paragraphs and meaningful Word-style tables.",
    agent=assumption_agent
)

diagram_task = Task(
    description="Generate Mermaid diagrams for: Context, Class, Sequence, Component, State, Activity, Deployment. Before each diagram, add a heading. Use proper layout (graph TD or graph LR), styling, and ensure node shape syntax uses node IDs like A[User], B(Component) — not inline wrappers like (Node) in connections.",
    expected_output="Diagram section with correctly formatted and styled Mermaid diagrams using ID-based node shape syntax.",
    agent=diagram_agent
)

conclusion_task = Task(
    description="Write a concluding section with: 1) Summary paragraph, 2) Future Enhancements in paragraph, 3) Glossary in Word-style tabular format (terms, acronyms, and definitions), and 4) Appendices in Word-style table (if any).",
    expected_output="Conclusion in paragraph, glossary in Word-style table, and appendices section in Word-style table.",
    agent=conclusion_agent
)

formatter_task = Task(
    description="Compile all outputs into one final markdown SRS. Ensure correct heading levels, spacing, formatting, Mermaid code block syntax, diagram layout, and styling. Ensure node shape declarations follow proper Mermaid syntax using ID-based shape definitions.",
    expected_output="Final, full-length SRS in markdown with all sections cleanly merged and valid Mermaid code blocks.",
    agent=formatter_agent
)
from crewai import Crew

crew = Crew(
    agents=[
        #brd_extractor_agent,
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
        #brd_extractor_task,
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
    ],
    verbose=True,

)