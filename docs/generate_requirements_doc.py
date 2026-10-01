import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

# Paths to generated images
ARTIFACT_DIR = r"C:\Users\pc\.gemini\antigravity\brain\ad342231-cf63-4e23-af07-f6fc505610d9"
IMG_ECLIPSE = os.path.join(ARTIFACT_DIR, "eclipse_adt_ui_sketch_1788791006972.jpg")
IMG_VSCODE = os.path.join(ARTIFACT_DIR, "vscode_abap_ui_sketch_1788791187022.jpg")
IMG_ARCH = os.path.join(ARTIFACT_DIR, "sap_architecture_diagram_1788791210220.jpg")

def set_cell_background(cell, fill_hex):
    """Set background color of a table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set padding/margins for a table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_callout_box(doc, text_content, title="STRATEGIC DIRECTIVE"):
    """Adds a stylish callout box with a colored left accent border."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "F0F4F8")
    
    tcPr = cell._element.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="none"/>
            <w:left w:val="single" w:sz="36" w:space="0" w:color="0070D2"/>
            <w:bottom w:val="none"/>
            <w:right w:val="none"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=150)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    run_t = p.add_run(f"📌 {title}\n")
    run_t.bold = True
    run_t.font.name = "Calibri"
    run_t.font.size = Pt(11)
    run_t.font.color.rgb = RGBColor(0, 112, 210)
    
    run_b = p.add_run(text_content)
    run_b.font.name = "Calibri"
    run_b.font.size = Pt(10.5)
    run_b.font.color.rgb = RGBColor(40, 40, 40)
    
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(6)

def style_table_header(row, col_widths, bg_hex="0070D2"):
    for idx, cell in enumerate(row.cells):
        cell.width = Inches(col_widths[idx])
        set_cell_background(cell, bg_hex)
        set_cell_margins(cell, top=120, bottom=120, left=120, right=120)
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.bold = True
                r.font.size = Pt(10)
                r.font.color.rgb = RGBColor(255, 255, 255)

def build_docx():
    doc = Document()
    
    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    # Styles configuration
    styles = doc.styles
    normal_style = styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(50, 50, 50)
    
    # Title Header Block
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(2)
    run_sub = title_p.add_run("ENTERPRISE SAP MODERNIZATION SPECIFICATION | WEEK 2 DELIVERABLE\n")
    run_sub.font.name = "Calibri"
    run_sub.font.size = Pt(10)
    run_sub.font.bold = True
    run_sub.font.color.rgb = RGBColor(0, 112, 210) # SAP Blue
    
    run_title = title_p.add_run("Virtual SAP ABAP Coding Assistant:\nRequirements Analysis & Functional Design")
    run_title.font.name = "Calibri Light"
    run_title.font.size = Pt(24)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(20, 35, 60)
    
    subtitle_p = doc.add_paragraph()
    subtitle_p.paragraph_format.space_before = Pt(4)
    subtitle_p.paragraph_format.space_after = Pt(18)
    run_desc = subtitle_p.add_run("Detailed Functional Specification, System Flowcharts, API Schemas, UI Sketches, Module Specifications, and Resiliency Strategies for SAP S/4HANA Modernization")
    run_desc.font.name = "Calibri"
    run_desc.font.size = Pt(11.5)
    run_desc.font.italic = True
    run_desc.font.color.rgb = RGBColor(100, 100, 100)

    # Metadata Table Box
    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_widths = [2.0, 4.5]
    meta_data = [
        ("Document Identifier:", "SAP-AI-ABAP-REQ-FUNC-2026-V2"),
        ("Target System Environment:", "SAP S/4HANA (2023+), SAP BTP AI Core & ABAP 7.5+ RAP"),
        ("Specification Scope:", "Functional Specs, System Diagrams, UI Sketches, Data Flows & Resiliency"),
        ("Document Status:", "v2.0 (Final Approved Requirements & Functional Design)")
    ]
    for r_idx, (k, v) in enumerate(meta_data):
        row = meta_table.rows[r_idx]
        for c_idx, val in enumerate([k, v]):
            cell = row.cells[c_idx]
            cell.width = Inches(meta_widths[c_idx])
            set_cell_background(cell, "F7F9FC" if r_idx % 2 == 0 else "FFFFFF")
            set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.size = Pt(9.5)
            if c_idx == 0:
                run.font.bold = True
                run.font.color.rgb = RGBColor(0, 112, 210)
            else:
                run.font.color.rgb = RGBColor(60, 60, 60)
                
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    
    # Helper functions
    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(15)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 80, 160)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(12.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(40, 90, 140)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 112, 210)
        return p

    def add_body(text, space_after=6):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(10.5)
        run.font.color.rgb = RGBColor(50, 50, 50)
        return p

    def add_bullet(bold_prefix, text):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.bold = True
        r_pre.font.size = Pt(10.5)
        r_pre.font.color.rgb = RGBColor(30, 30, 30)
        
        r_txt = p.add_run(text)
        r_txt.font.name = "Calibri"
        r_txt.font.size = Pt(10.5)
        r_txt.font.color.rgb = RGBColor(60, 60, 60)
        return p

    def add_code_block(code_text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.5)
        set_cell_background(cell, "272822") # Dark code background
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(code_text)
        run.font.name = "Consolas"
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(248, 248, 242)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # --- CHAPTER 1 ---
    add_h1("1. Executive Summary & Industry Benchmark Analysis")
    add_body(
        "Enterprise application development within the SAP ecosystem is undergoing a generational shift. As global enterprises "
        "migrate from legacy SAP ECC 6.0 environments to SAP S/4HANA and SAP Business Technology Platform (BTP), software engineering teams "
        "face significant friction. Decades of legacy ABAP custom code (procedural Z-programs, direct SQL table accesses, missing unit tests, and "
        "obsolete syntax) present a major operational bottleneck to achieving SAP's 'Clean Core' paradigm."
    )
    add_body(
        "Industry research into existing commercial SAP coding assistants (such as SAP Build Code / Joule for ABAP and general-purpose tools "
        "like GitHub Copilot) reveals critical capability gaps. General LLM assistants lack deep context regarding enterprise-specific SAP data dictionaries, "
        "custom BAPIs, modern ABAP RESTful Application Programming Model (RAP) constructs, and real-time ABAP Test Cockpit (ATC) static analysis feedback. "
        "Conversely, standard SAP tools lack inline context-aware code generation inside modern developer environments like VS Code or custom Eclipse ADT instances."
    )
    
    add_callout_box(
        doc,
        "The Virtual SAP ABAP Coding Assistant bridges this gap by marrying Retrieval-Augmented Generation (RAG) over official SAP Keyword Documentation "
        "and Clean ABAP style rules with live SAP RFC syntax validation. This architecture delivers real-time contextual inline code completions, automated "
        "ATC refactoring, ABAP Unit test scaffolding, and CDS/RAP model generation within <1.5s sub-second latency targets.",
        "SYSTEM DESIGN PHILOSOPHY"
    )

    # Benchmark Table
    add_h2("1.1 Comparative Benchmark Matrix")
    bench_table = doc.add_table(rows=5, cols=4)
    bench_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    bench_widths = [1.6, 1.6, 1.6, 1.7]
    style_table_header(bench_table.rows[0], bench_widths, bg_hex="0070D2")
    
    headers = ["Feature Capability", "General AI (Copilot)", "SAP Joule / Build Code", "Virtual SAP Assistant (Proposed)"]
    for idx, h in enumerate(headers):
        bench_table.rows[0].cells[idx].paragraphs[0].text = h
        
    data_bench = [
        ("ABAP 7.5+ / RAP Context", "Limited / Generic syntax", "Moderate (SAP BTP focused)", "High (RAG + AST Context Assembly)"),
        ("Live SAP Syntax Checking", "None (Static string predictions)", "Delayed server syntax check", "Real-Time RFC Validation (<300ms)"),
        ("ATC Refactoring & Fixes", "Generic suggestions", "Manual prompt triggers", "1-Click ATC Remediation Pipeline"),
        ("IDE Multi-Platform", "VS Code / JetBrains", "SAP Business Application Studio", "Eclipse ADT & VS Code Plugins")
    ]
    for r_idx, row_data in enumerate(data_bench):
        row = bench_table.rows[r_idx + 1]
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = Inches(bench_widths[c_idx])
            set_cell_background(cell, "F7F9FC" if r_idx % 2 == 0 else "FFFFFF")
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.size = Pt(9)
            if c_idx == 3:
                run.font.bold = True
                run.font.color.rgb = RGBColor(0, 112, 210)
            else:
                run.font.color.rgb = RGBColor(60, 60, 60)
                
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # --- CHAPTER 2 ---
    add_h1("2. Requirements Analysis & User Persona Modeling")
    add_body(
        "To ensure precise functional alignment with enterprise engineering workflows, user requirements were gathered across three primary "
        "enterprise SAP personas: Senior ABAP Developer, SAP Solution Architect, and Lead QA / Transport Manager."
    )
    
    add_h2("2.1 Target User Personas")
    add_bullet("Persona 1: Senior ABAP Developer (Dev-User): ", "Requires instant inline completions for modern ABAP 7.5+ expressions (table expressions, string templates, VALUE #() constructs) and automated unit test generation to meet sprint coverage goals.")
    add_bullet("Persona 2: SAP Solution Architect (Arch-User): ", "Requires automated RAP/CDS view scaffolding, Clean ABAP adherence, and automated migration path suggestions for legacy procedural Z-code to modern S/4HANA constructs.")
    add_bullet("Persona 3: Lead QA / Transport Manager (QA-User): ", "Requires strict ABAP Test Cockpit (ATC) static analysis enforcement, P1/P2 security vulnerability checks, and automated ABAP Doc generation prior to transport release.")

    add_h2("2.2 Functional Requirements (FR)")
    fr_table = doc.add_table(rows=7, cols=4)
    fr_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    fr_widths = [1.0, 1.8, 2.5, 1.2]
    style_table_header(fr_table.rows[0], fr_widths, bg_hex="285A8C")
    
    fr_headers = ["Req ID", "Module Name", "Detailed Functional Requirement", "Priority"]
    for idx, h in enumerate(fr_headers):
        fr_table.rows[0].cells[idx].paragraphs[0].text = h
        
    fr_data = [
        ("FR-1", "Inline Code Completion", "System shall provide context-aware ghost-text code completions for ABAP 7.4+ and 7.5+ syntax within IDE editors with median latency <1.5s.", "High (P1)"),
        ("FR-2", "RAP & CDS Generator", "System shall auto-generate Core Data Services (CDS) view definitions and Business Object Behavior Definitions (BDEF) based on natural language or DB tables.", "High (P1)"),
        ("FR-3", "ATC Refactoring Engine", "System shall evaluate active ABAP code against SAP ATC static checks and provide 1-click remediation diffs for security, syntax, and performance findings.", "High (P1)"),
        ("FR-4", "ABAP Unit Generator", "System shall automatically scaffold ABAP Unit test classes utilizing CL_ABAP_UNIT_ASSERT and test double frameworks for custom classes/methods.", "Medium (P2)"),
        ("FR-5", "ABAP Doc Generator", "System shall parse method signatures and parameters to auto-generate ABAP Doc format inline docstrings.", "Medium (P2)"),
        ("FR-6", "Clean ABAP RAG Engine", "System shall index official Clean ABAP style guides and SAP Keyword Documentation into a vector database to answer developer query prompts.", "High (P1)")
    ]
    for r_idx, row_data in enumerate(fr_data):
        row = fr_table.rows[r_idx + 1]
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = Inches(fr_widths[c_idx])
            set_cell_background(cell, "F7F9FC" if r_idx % 2 == 0 else "FFFFFF")
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.size = Pt(9)
            if c_idx == 0:
                run.font.bold = True

    add_h2("2.3 Non-Functional Requirements (NFR)")
    add_bullet("NFR-1 (Performance & Latency): ", "Inline code completion response generation shall complete within a median time of <1.5 seconds. SAP RFC syntax checking shall complete within <300ms.")
    add_bullet("NFR-2 (Security & Data Privacy): ", "No proprietary customer source code or database values shall be stored in external LLM logs. Prompt sanitization and client-side PII scrubbing engine shall mask Z-table schemas.")
    add_bullet("NFR-3 (Availability & Reliability): ", "The AI Gateway and Middleware service shall achieve 99.9% operational uptime. Fallback offline RAG lookup mode shall operate when SAP RFC gateway is unreachable.")
    add_bullet("NFR-4 (Compatibility): ", "System shall seamlessly integrate with Eclipse ADT 3.32+ and VS Code ABAP Extension 1.85+. Target backend support includes SAP S/4HANA 1909 through 2023+.")

    add_h2("2.4 Use Case Scenarios")
    add_h3("Use Case UC-1: Refactoring Legacy SELECT Statements to ABAP 7.5+ Modern Constructs")
    add_bullet("Actor: ", "Senior ABAP Developer")
    add_bullet("Pre-condition: ", "Developer highlights legacy SELECT...ENDSELECT loop with repeated table reads in Eclipse ADT editor.")
    add_bullet("Main Flow: ", "1. Developer triggers 'Refactor with Clean ABAP' code action.\n2. IDE plugin sends code snippet and AST context to Gateway.\n3. Gateway queries RAG vector store for ABAP 7.5+ Table Expressions and Array Fetch rules.\n4. Gateway prompts LLM to generate modern inline `SELECT ... INTO TABLE @DATA(lt_data)` and `VALUE #()` constructs.\n5. Gateway dispatches generated code to SAP RFC Syntax Checker.\n6. Modern code returned to IDE diff viewer for developer confirmation.")
    add_bullet("Post-condition: ", "Code replaced with clean ABAP 7.5+ syntax passing all ATC performance checks.")

    # --- CHAPTER 3 ---
    add_h1("3. System Architecture & Interaction Diagrams")
    add_body(
        "The Virtual SAP ABAP Coding Assistant is built upon a 5-layer decoupled microservice architecture connecting developer IDEs "
        "to SAP BTP AI Core middleware and target SAP S/4HANA backend environments via gRPC/HTTPS and SAP RFC."
    )
    
    # Architecture Diagram Image
    if os.path.exists(IMG_ARCH):
        doc.add_paragraph().paragraph_format.space_before = Pt(4)
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_img = p_img.add_run()
        run_img.add_picture(IMG_ARCH, width=Inches(6.2))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Figure 3.1: 5-Layer Decoupled Architecture Diagram for Virtual SAP ABAP Assistant")
        r_cap.font.size = Pt(9)
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(100, 100, 100)
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_h2("3.1 Request Processing Pipeline Flowchart")
    add_code_block(
"""+-----------------------------------------------------------------------------------+
|                            IDE DEVELOPER EDITOR (Client)                           |
|  [User Types Code / Requests Action] -> [Extract AST Window & Surrounding Buffer]  |
+------------------------------------------+----------------------------------------+
                                           | HTTPS / gRPC Request (JSON Payload)
                                           v
+-----------------------------------------------------------------------------------+
|                        LAYER 2: AI GATEWAY & MIDDLEWARE                            |
|  1. Validate JWT Token & SAP IAS Session                                          |
|  2. Execute PII Scrubbing (Mask Customer Z-Tables / Proprietary Schemas)          |
|  3. Assemble System Prompt (Inject Target ABAP Version & Clean ABAP Guidelines)   |
+------------------------------------------+----------------------------------------+
                                           | Vector Embeddings Query
                                           v
+-----------------------------------------------------------------------------------+
|                        LAYER 3: RAG VECTOR KNOWLEDGE DB                           |
|  [Query Qdrant Vector Store] -> [Retrieve Top-K Relevant Clean ABAP Rules / Docs] |
+------------------------------------------+----------------------------------------+
                                           | Combined Context & Code Prompt
                                           v
+-----------------------------------------------------------------------------------+
|                        LAYER 4: LLM INFERENCE ENGINE                              |
|  [Azure OpenAI / SAP BTP AI Core] -> [Generate ABAP 7.5+ Code / RAP Scaffold]     |
+------------------------------------------+----------------------------------------+
                                           | Raw Generated Code Snippet
                                           v
+-----------------------------------------------------------------------------------+
|                        LAYER 5: TARGET SAP S/4HANA BACKEND                        |
|  [Execute RFC SYNTAX-CHECK Statement] -> [Validate ATC Static Analysis Rules]     |
+------------------------------------------+----------------------------------------+
                                           | Validated Code + ATC Diagnostics
                                           v
+-----------------------------------------------------------------------------------+
|                            IDE DEVELOPER EDITOR (Client)                           |
|  [Display Inline Ghost Text / Render Diff Refactoring View / Apply 1-Click Fix]   |
+-----------------------------------------------------------------------------------+"""
    )

    add_h2("3.2 Sequence Diagram: Real-Time Inline Completion & RFC Check")
    add_body(
        "The following sequence diagram outlines the sub-second execution path during an inline completion trigger event:"
    )
    add_code_block(
"""Developer IDE             Gateway / Middleware         Vector DB (Qdrant)       LLM Core            SAP S/4HANA (RFC)
     |                               |                         |                    |                      |
     |-- 1. Trigger Completion ----->|                         |                    |                      |
     |   (Code, Cursor Pos, AST)     |-- 2. Query Embeddings ->|                    |                      |
     |                               |<-- 3. Top-K Rules ------|                    |                      |
     |                               |                                              |                      |
     |                               |-- 4. Dispatch Prompt (Context + Code) ------>|                      |
     |                               |<-- 5. Raw Generated Code --------------------|                      |
     |                               |                                                                     |
     |                               |-- 6. Execute RFC Syntax Check ------------------------------------->|
     |                               |<-- 7. RFC Syntax Verification Result OK / Errors ------------------|
     |                               |
     |<-- 8. Return Ghost Text ------|
     |    (Code + Syntax Status)     |"""
    )

    # --- CHAPTER 4 ---
    add_h1("4. Detailed Functional Module Specification")
    add_body(
        "The Virtual SAP ABAP Coding Assistant application is divided into five core functional modules, each possessing modular, "
        "decoupled responsibilities and standardized API contracts."
    )

    add_h2("4.1 Module 1: Client IDE Plugin Engine (Eclipse ADT & VS Code)")
    add_bullet("Purpose: ", "Manages editor event listeners, inline ghost-text rendering, side-panel chat UI, CodeLens actions, and ATC error highlighting.")
    add_bullet("Inputs: ", "Keyboard cursor movements, trigger key combinations (e.g., Ctrl+Space), document change events.")
    add_bullet("Outputs: ", "gRPC request payloads to Gateway; UI ghost text overlays; side-panel HTML webview streams.")
    add_bullet("Key Subcomponents: ", "1. AST Context Extractor: Captures current class method signature, local variable definitions, and preceding 50 lines buffer.\n2. Ghost Text Renderer: Displays inline speculative code completions.\n3. ATC Alert Controller: Annotates inline code lines with red/yellow squiggly error indicators.")

    add_h2("4.2 Module 2: AI Gateway & Context Orchestrator")
    add_bullet("Purpose: ", "Central middleware orchestrator handling authentication, rate limiting, PII scrubbing, context assembly, and LLM prompt dispatch.")
    add_bullet("Inputs: ", "gRPC / REST JSON payloads from Client IDE Plugin.")
    add_bullet("Outputs: ", "Sanitized LLM prompts; filtered code completion payloads delivered back to IDE.")
    add_bullet("Key Subcomponents: ", "1. PII Scrubbing Engine: Regex and AST scanner masking proprietary company names, confidential data fields, and specific SAP Z-table schemas.\n2. Prompt Sanitizer: Enforces Clean ABAP guidelines into system instructions.\n3. Token Budget Allocator: Trims surrounding code buffers to maintain prompt window limits.")

    add_h2("4.3 Module 3: Clean ABAP & SAP Keyword RAG Engine")
    add_bullet("Purpose: ", "Provides semantic retrieval of official SAP ABAP 7.5+ syntax rules, Clean ABAP repository guidelines, and enterprise BAPI documentation.")
    add_bullet("Inputs: ", "Text embedding vector derived from developer prompt or AST snippet.")
    add_bullet("Outputs: ", "Top-K relevance matched documentation chunks and style rules.")
    add_bullet("Key Subcomponents: ", "1. Qdrant Vector Store: High-performance vector database storing 15,000+ indexed ABAP documentation chunks.\n2. Text-Embedding-3-Large Model: Generates 1536-dimensional embeddings for incoming queries.")

    add_h2("4.4 Module 4: SAP RFC Syntax & ATC Verification Gateway")
    add_bullet("Purpose: ", "Validates LLM-generated code snippets against actual target SAP S/4HANA backend syntax rules and static analysis checkers via RFC connection pooling.")
    add_bullet("Inputs: ", "Generated ABAP code string; target ABAP program/class context.")
    add_bullet("Outputs: ", "Syntax check result (Success / Line Error Diagnostics); ATC static analysis priority findings (P1/P2/P3).")
    add_bullet("Key Subcomponents: ", "1. SAP PyRFC Connection Pool: Maintains high-throughput RFC connections to SAP application server.\n2. RFC Function Module /ZAI/SYNTAX_CHECK: Executes native ABAP SYNTAX-CHECK STATEMENT.\n3. RFC Function Module /ZAI/EXECUTE_ATC: Invokes SAP ABAP Test Cockpit framework headlessly.")

    add_h2("4.5 Module 5: ABAP Unit Test & RAP CDS Code Generator Module")
    add_bullet("Purpose: ", "Specialized code generation pipeline for constructing ABAP Unit test classes and CDS/RAP framework artifacts.")
    add_bullet("Inputs: ", "Target custom class method signature; database table name or entity schema.")
    add_bullet("Outputs: ", "Complete ABAP Unit test class scaffold (CL_ABAP_UNIT_ASSERT); CDS View DDL (DEFINE VIEW ENTITY) and Behavior Definition (BDEF).")

    # --- CHAPTER 5 ---
    add_h1("5. Data Flows, Input/Output Schemas & Data Dictionary")
    add_body(
        "Communication between components uses strictly typed JSON payloads over gRPC/HTTPS. Below are the definitive API data schemas."
    )

    add_h2("5.1 Inline Completion Request Schema (JSON)")
    add_code_block(
"""{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "InlineCompletionRequest",
  "type": "object",
  "properties": {
    "requestId": { "type": "string", "format": "uuid" },
    "sapSystemId": { "type": "string", "example": "S4H_CLNT_100" },
    "abapTargetRelease": { "type": "string", "example": "7.54" },
    "fileName": { "type": "string", "example": "zcl_sales_calculator.clas.abap" },
    "cursorPosition": {
      "type": "object",
      "properties": {
        "line": { "type": "integer", "example": 45 },
        "column": { "type": "integer", "example": 18 }
      },
      "required": ["line", "column"]
    },
    "codeContext": {
      "type": "object",
      "properties": {
        "precedingBuffer": { "type": "string" },
        "followingBuffer": { "type": "string" },
        "currentMethodScope": { "type": "string", "example": "CALCULATE_DISCOUNT" }
      },
      "required": ["precedingBuffer"]
    }
  },
  "required": ["requestId", "sapSystemId", "fileName", "cursorPosition", "codeContext"]
}"""
    )

    add_h2("5.2 Inline Completion Response Schema (JSON)")
    add_code_block(
"""{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "InlineCompletionResponse",
  "type": "object",
  "properties": {
    "requestId": { "type": "string", "format": "uuid" },
    "completionText": { "type": "string", "example": "DATA(lt_items) = VALUE tt_items( ( matnr = 'M-10' kwmeng = 5 ) )." },
    "rfcSyntaxCheck": {
      "type": "object",
      "properties": {
        "isValid": { "type": "boolean", "example": true },
        "lineError": { "type": "integer", "example": 0 },
        "errorMessage": { "type": "string", "example": "" }
      },
      "required": ["isValid"]
    },
    "ragReferences": {
      "type": "array",
      "items": { "type": "string", "example": "Clean ABAP Rule: Use VALUE #() constructor expression" }
    },
    "latencyMs": { "type": "integer", "example": 420 }
  },
  "required": ["requestId", "completionText", "rfcSyntaxCheck", "latencyMs"]
}"""
    )

    add_h2("5.3 Data Flow Diagram (DFD Level 1 Decomposition)")
    add_code_block(
"""+----------------+      1. Capture Cursor & Code AST      +-----------------------+
|  Developer IDE | -------------------------------------> | 1.0 Context Assembly  |
+----------------+                                        +-----------+-----------+
        ^                                                             |
        |                                   2. Sanitized Code Context |
        | 6. Render Ghost Text                                        v
+-------+--------+                                        +-----------------------+
|  Developer IDE | <------------------------------------- | 2.0 AI Orchestration  |
+----------------+      5. Validated Code Payload         +-----------+-----------+
                                                                      |
                                       +------------------------------+------------------------------+
                                       | 3. Query Vector Context                                     | 4. Validate Syntax
                                       v                                                             v
                            +-----------------------+                                     +-----------------------+
                            | 3.0 RAG Vector Search |                                     | 4.0 SAP RFC Gateway   |
                            +-----------------------+                                     +-----------------------+"""
    )

    # --- CHAPTER 6 ---
    add_h1("6. Error Handling, Edge Cases & System Resiliency")
    add_body(
        "To ensure robust operations in high-availability enterprise SAP environments, the architecture implements proactive failure modes and graceful degradation."
    )

    add_h2("6.1 Network Partition & SAP RFC Connection Failure Strategy")
    add_body(
        "When the target SAP S/4HANA application server becomes unreachable (e.g., VPN disconnection or SAP gateway maintenance), "
        "the Gateway automatically switches to 'Degraded Offline RAG Mode'. Code completions continue using local AST syntax parsing and "
        "RAG rules, while live RFC syntax validation is temporarily bypassed with a yellow warning indicator in the IDE status bar."
    )

    add_h2("6.2 LLM Hallucination Prevention & Safety Guardrails")
    add_bullet("AST Syntax Filter: ", "Every LLM-generated snippet is evaluated against an ABAP AST Grammar Parser before RFC dispatch. If invalid syntax structures are detected, the response is discarded.")
    add_bullet("Prohibited ABAP Statements Guardrail: ", "The Gateway enforces a strict blacklist of destructive syntax commands. Snippets containing DELETE FROM <table> WITHOUT WHERE, CALL 'SYSTEM', SE16, or BREAK-POINT are automatically blocked.")
    add_bullet("Loop Execution Guardrail: ", "Prevents infinite loop generation by injecting SAP timeout markers into generated procedural constructs.")

    add_h2("6.3 PII & Confidential Code Scrubbing Engine")
    add_body(
        "To satisfy corporate data privacy mandates, all code context payloads pass through an automated PII Masking Engine prior to LLM submission. "
        "The scrubbing pipeline applies regex replacement and symbol substitution to mask sensitive parameters:"
    )
    add_code_block(
"""[Original ABAP Source Snippet]
SELECT SINGLE * FROM zcustom_payroll INTO @DATA(ls_pay) WHERE emp_ssn = '999-12-3456'.

[Masked Payload Sent to LLM Inference Engine]
SELECT SINGLE * FROM [Z_CUSTOM_TABLE_1] INTO @DATA(ls_pay) WHERE [MASKED_FIELD_1] = '[MASKED_LITERAL_1]'."""
    )

    # --- CHAPTER 7 ---
    add_h1("7. User Interface Sketches & IDE Integration Mockups")
    add_body(
        "The system provides native integration across both primary SAP development environments: Eclipse ADT and VS Code."
    )

    add_h2("7.1 Eclipse ADT Visual Layout Sketch")
    if os.path.exists(IMG_ECLIPSE):
        doc.add_paragraph().paragraph_format.space_before = Pt(4)
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_img = p_img.add_run()
        run_img.add_picture(IMG_ECLIPSE, width=Inches(6.2))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Figure 7.1: Visual UI Mockup Sketch of Eclipse ADT Integration")
        r_cap.font.size = Pt(9)
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(100, 100, 100)
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_bullet("Eclipse UI Feature A (Inline Editor): ", "Displays inline green ghost-text completion overlay. Developer accepts via [Tab] or cancels via [Esc].")
    add_bullet("Eclipse UI Feature B (Side Chat Panel): ", "Embedded JavaFX/Chromium webview containing AI Assistant chat, Clean ABAP rule lookup, and Quick Action buttons.")
    add_bullet("Eclipse UI Feature C (ATC Problem View): ", "Integrates directly into standard Eclipse 'Problems View' with a custom 1-Click 'Quick Fix (AI Refactor)' menu.")

    add_h2("7.2 VS Code Extension Visual Layout Sketch")
    if os.path.exists(IMG_VSCODE):
        doc.add_paragraph().paragraph_format.space_before = Pt(4)
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_img = p_img.add_run()
        run_img.add_picture(IMG_VSCODE, width=Inches(6.2))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Figure 7.2: Visual UI Mockup Sketch of VS Code Extension with Split Refactoring View")
        r_cap.font.size = Pt(9)
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(100, 100, 100)
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_bullet("VS Code Feature A (CodeLens Actions): ", "Floating action links above class methods: 'Refactor with Clean ABAP | Generate ABAP Unit Test | Run ATC Check'.")
    add_bullet("VS Code Feature B (Diff Refactoring Window): ", "Side-by-side split view comparing legacy procedural code against modern AI-refactored Clean ABAP code.")
    add_bullet("VS Code Feature C (Status Bar Indicator): ", "Live status pill indicating RFC connection health and gRPC response latency (e.g. 'SAP AI: Connected 42ms').")

    # --- CHAPTER 8 ---
    add_h1("8. Requirements Traceability Matrix (RTM)")
    add_body(
        "The Requirements Traceability Matrix establishes direct mapping between functional requirements, design modules, API endpoints, and verification procedures."
    )
    
    rtm_table = doc.add_table(rows=7, cols=5)
    rtm_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    rtm_widths = [0.8, 1.3, 1.4, 1.5, 1.5]
    style_table_header(rtm_table.rows[0], rtm_widths, bg_hex="0070D2")
    
    rtm_headers = ["Req ID", "Functional Requirement", "Design Module", "API Endpoint", "Verification Method"]
    for idx, h in enumerate(rtm_headers):
        rtm_table.rows[0].cells[idx].paragraphs[0].text = h
        
    rtm_data = [
        ("FR-1", "Inline ABAP Completion", "Module 1 & Module 2", "/api/v1/completion/inline", "Automated Latency & Syntax Test"),
        ("FR-2", "RAP & CDS Generator", "Module 5 (Generator)", "/api/v1/generator/rap-cds", "CDS Activation Unit Test"),
        ("FR-3", "ATC Refactoring Engine", "Module 4 (RFC Gateway)", "/api/v1/atc/remediate", "ATC Static Analysis Runner"),
        ("FR-4", "ABAP Unit Generator", "Module 5 (Generator)", "/api/v1/generator/abap-unit", "AUNIT Test Execution"),
        ("FR-5", "ABAP Doc Generator", "Module 2 (Orchestrator)", "/api/v1/doc/abapdoc", "Docstring AST Inspection"),
        ("FR-6", "Clean ABAP RAG Lookup", "Module 3 (RAG Engine)", "/api/v1/rag/query", "RAG Precision & Recall Metric")
    ]
    for r_idx, row_data in enumerate(rtm_data):
        row = rtm_table.rows[r_idx + 1]
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = Inches(rtm_widths[c_idx])
            set_cell_background(cell, "F7F9FC" if r_idx % 2 == 0 else "FFFFFF")
            set_cell_margins(cell, top=60, bottom=60, left=60, right=60)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.size = Pt(8.5)
            if c_idx == 0:
                run.font.bold = True

    # --- CHAPTER 9 ---
    add_h1("9. Verification Plan & Acceptance Sign-off")
    add_body(
        "System verification will follow a rigorous automated and manual validation strategy prior to prototype sign-off."
    )
    
    add_h2("9.1 Automated Test Execution Suite")
    add_bullet("1. API Integration Test Suite: ", "Pytest script verifying all FastAPI endpoints (/api/v1/completion/inline, /api/v1/atc/remediate) under load.")
    add_bullet("2. RFC Backend Verification Test: ", "Executes /ZAI/SYNTAX_CHECK against 100 standard SAP test programs to verify syntax error detection accuracy.")
    add_bullet("3. RAG Benchmark Test: ", "Evaluates RAG retrieval context relevance against 50 canonical Clean ABAP style questions.")

    add_h2("9.2 Acceptance Criteria & Prototype Sign-off")
    add_bullet("Criterion 1: ", "100% of generated ABAP code snippets pass target SAP RFC syntax checks without compilation errors.")
    add_bullet("Criterion 2: ", "Zero Priority 1 (Security) or Priority 2 (Performance) warnings reported by ABAP Test Cockpit on generated CDS views.")
    add_bullet("Criterion 3: ", "Median response latency for inline completion remains under 1.5 seconds across 1,000 test requests.")

    # Save document
    output_docx_path = r"c:\Users\pc\OneDrive\Documents\registration form\sap\Virtual_SAP_ABAP_Assistant_Requirements_and_Functional_Design.docx"
    doc.save(output_docx_path)
    print(f"Successfully generated DOCX file at: {output_docx_path}")

def build_markdown():
    md_content = f"""# 📘 Virtual SAP ABAP Coding Assistant
## Requirements Analysis & Functional Design Document (Week 2 Deliverable)

| Document Metadata | Value |
| :--- | :--- |
| **Document Identifier** | `SAP-AI-ABAP-REQ-FUNC-2026-V2` |
| **Target System Environment** | SAP S/4HANA (2023+), SAP BTP AI Core & ABAP 7.5+ RAP |
| **Specification Scope** | Functional Specs, System Diagrams, UI Sketches, Data Flows & Resiliency |
| **Status** | v2.0 (Final Approved Requirements & Functional Design) |

---

## 1. Executive Summary & Industry Benchmark Analysis

Enterprise application development within the SAP ecosystem is undergoing a generational shift. As global enterprises migrate from legacy SAP ECC 6.0 environments to SAP S/4HANA and SAP Business Technology Platform (BTP), software engineering teams face significant friction. Decades of legacy ABAP custom code (procedural Z-programs, direct SQL table accesses, missing unit tests, and obsolete syntax) present a major operational bottleneck to achieving SAP's "Clean Core" paradigm.

Industry research into existing commercial SAP coding assistants (such as SAP Build Code / Joule for ABAP and general-purpose tools like GitHub Copilot) reveals critical capability gaps. General LLM assistants lack deep context regarding enterprise-specific SAP data dictionaries, custom BAPIs, modern ABAP RESTful Application Programming Model (RAP) constructs, and real-time ABAP Test Cockpit (ATC) static analysis feedback.

> 📌 **SYSTEM DESIGN PHILOSOPHY**
> The Virtual SAP ABAP Coding Assistant bridges this gap by marrying Retrieval-Augmented Generation (RAG) over official SAP Keyword Documentation and Clean ABAP style rules with live SAP RFC syntax validation. This architecture delivers real-time contextual inline code completions, automated ATC refactoring, ABAP Unit test scaffolding, and CDS/RAP model generation within <1.5s sub-second latency targets.

### 1.1 Comparative Benchmark Matrix

| Feature Capability | General AI (Copilot) | SAP Joule / Build Code | Virtual SAP Assistant (Proposed) |
| :--- | :--- | :--- | :--- |
| **ABAP 7.5+ / RAP Context** | Limited / Generic syntax | Moderate (SAP BTP focused) | **High (RAG + AST Context Assembly)** |
| **Live SAP Syntax Checking** | None (Static predictions) | Delayed server syntax check | **Real-Time RFC Validation (<300ms)** |
| **ATC Refactoring & Fixes** | Generic suggestions | Manual prompt triggers | **1-Click ATC Remediation Pipeline** |
| **IDE Multi-Platform** | VS Code / JetBrains | SAP Business Application Studio | **Eclipse ADT & VS Code Plugins** |

---

## 2. Requirements Analysis & User Persona Modeling

### 2.1 Target User Personas
- **Senior ABAP Developer**: Requires instant inline completions for modern ABAP 7.5+ expressions (table expressions, string templates, `VALUE #()` constructs) and automated unit test generation to meet sprint coverage goals.
- **SAP Solution Architect**: Requires automated RAP/CDS view scaffolding, Clean ABAP adherence, and automated migration path suggestions for legacy procedural Z-code.
- **Lead QA / Transport Manager**: Requires strict ABAP Test Cockpit (ATC) static analysis enforcement, P1/P2 security vulnerability checks, and automated ABAP Doc generation prior to transport release.

### 2.2 Functional Requirements (FR)

| Req ID | Module Name | Detailed Functional Requirement | Priority |
| :--- | :--- | :--- | :--- |
| **FR-1** | Inline Code Completion | System shall provide context-aware ghost-text code completions for ABAP 7.4+ and 7.5+ syntax within IDE editors with median latency <1.5s. | High (P1) |
| **FR-2** | RAP & CDS Generator | System shall auto-generate Core Data Services (CDS) view definitions and Business Object Behavior Definitions (BDEF) based on natural language or DB tables. | High (P1) |
| **FR-3** | ATC Refactoring Engine | System shall evaluate active ABAP code against SAP ATC static checks and provide 1-click remediation diffs for security, syntax, and performance findings. | High (P1) |
| **FR-4** | ABAP Unit Generator | System shall automatically scaffold ABAP Unit test classes utilizing `CL_ABAP_UNIT_ASSERT` and test double frameworks for custom classes/methods. | Medium (P2) |
| **FR-5** | ABAP Doc Generator | System shall parse method signatures and parameters to auto-generate ABAP Doc format inline docstrings. | Medium (P2) |
| **FR-6** | Clean ABAP RAG Engine | System shall index official Clean ABAP style guides and SAP Keyword Documentation into a vector database to answer developer query prompts. | High (P1) |

### 2.3 Non-Functional Requirements (NFR)
- **NFR-1 (Performance & Latency)**: Inline code completion response generation shall complete within a median time of <1.5 seconds. SAP RFC syntax checking shall complete within <300ms.
- **NFR-2 (Security & Data Privacy)**: No proprietary customer source code or database values shall be stored in external LLM logs. Prompt sanitization and client-side PII scrubbing engine shall mask Z-table schemas.
- **NFR-3 (Availability & Reliability)**: The AI Gateway and Middleware service shall achieve 99.9% operational uptime. Fallback offline RAG lookup mode shall operate when SAP RFC gateway is unreachable.
- **NFR-4 (Compatibility)**: System shall seamlessly integrate with Eclipse ADT 3.32+ and VS Code ABAP Extension 1.85+. Target backend support includes SAP S/4HANA 1909 through 2023+.

---

## 3. System Architecture & Interaction Diagrams

![System Architecture Diagram](file:///{IMG_ARCH.replace('\\', '/')})

### 3.1 Request Processing Pipeline Flowchart

```text
+-----------------------------------------------------------------------------------+
|                            IDE DEVELOPER EDITOR (Client)                           |
|  [User Types Code / Requests Action] -> [Extract AST Window & Surrounding Buffer]  |
+------------------------------------------+----------------------------------------+
                                           | HTTPS / gRPC Request (JSON Payload)
                                           v
+-----------------------------------------------------------------------------------+
|                        LAYER 2: AI GATEWAY & MIDDLEWARE                            |
|  1. Validate JWT Token & SAP IAS Session                                          |
|  2. Execute PII Scrubbing (Mask Customer Z-Tables / Proprietary Schemas)          |
|  3. Assemble System Prompt (Inject Target ABAP Version & Clean ABAP Guidelines)   |
+------------------------------------------+----------------------------------------+
                                           | Vector Embeddings Query
                                           v
+-----------------------------------------------------------------------------------+
|                        LAYER 3: RAG VECTOR KNOWLEDGE DB                           |
|  [Query Qdrant Vector Store] -> [Retrieve Top-K Relevant Clean ABAP Rules / Docs] |
+------------------------------------------+----------------------------------------+
                                           | Combined Context & Code Prompt
                                           v
+-----------------------------------------------------------------------------------+
|                        LAYER 4: LLM INFERENCE ENGINE                              |
|  [Azure OpenAI / SAP BTP AI Core] -> [Generate ABAP 7.5+ Code / RAP Scaffold]     |
+------------------------------------------+----------------------------------------+
                                           | Raw Generated Code Snippet
                                           v
+-----------------------------------------------------------------------------------+
|                        LAYER 5: TARGET SAP S/4HANA BACKEND                        |
|  [Execute RFC SYNTAX-CHECK Statement] -> [Validate ATC Static Analysis Rules]     |
+------------------------------------------+----------------------------------------+
                                           | Validated Code + ATC Diagnostics
                                           v
+-----------------------------------------------------------------------------------+
|                            IDE DEVELOPER EDITOR (Client)                           |
|  [Display Inline Ghost Text / Render Diff Refactoring View / Apply 1-Click Fix]   |
+-----------------------------------------------------------------------------------+
```

### 3.2 Sequence Diagram: Real-Time Inline Completion & RFC Check

```text
Developer IDE             Gateway / Middleware         Vector DB (Qdrant)       LLM Core            SAP S/4HANA (RFC)
     |                               |                         |                    |                      |
     |-- 1. Trigger Completion ----->|                         |                    |                      |
     |   (Code, Cursor Pos, AST)     |-- 2. Query Embeddings ->|                    |                      |
     |                               |<-- 3. Top-K Rules ------|                    |                      |
     |                               |                                              |                      |
     |                               |-- 4. Dispatch Prompt (Context + Code) ------>|                      |
     |                               |<-- 5. Raw Generated Code --------------------|                      |
     |                               |                                                                     |
     |                               |-- 6. Execute RFC Syntax Check ------------------------------------->|
     |                               |<-- 7. RFC Syntax Verification Result OK / Errors ------------------|
     |                               |
     |<-- 8. Return Ghost Text ------|
     |    (Code + Syntax Status)     |
```

---

## 4. Detailed Functional Module Specification

### 4.1 Module 1: Client IDE Plugin Engine (Eclipse ADT & VS Code)
- **Purpose**: Manages editor event listeners, inline ghost-text rendering, side-panel chat UI, CodeLens actions, and ATC error highlighting.
- **Inputs**: Keyboard cursor movements, trigger key combinations (`Ctrl+Space`), document change events.
- **Outputs**: gRPC request payloads to Gateway; UI ghost text overlays; side-panel HTML webview streams.

### 4.2 Module 2: AI Gateway & Context Orchestrator
- **Purpose**: Central middleware orchestrator handling authentication, rate limiting, PII scrubbing, context assembly, and LLM prompt dispatch.
- **Subcomponents**:
  1. **PII Scrubbing Engine**: Regex and AST scanner masking proprietary company names and custom SAP Z-table schemas.
  2. **Prompt Sanitizer**: Enforces Clean ABAP guidelines into system instructions.
  3. **Token Budget Allocator**: Trims surrounding code buffers to maintain prompt window limits.

### 4.3 Module 3: Clean ABAP & SAP Keyword RAG Engine
- **Purpose**: Provides semantic retrieval of official SAP ABAP 7.5+ syntax rules, Clean ABAP repository guidelines, and enterprise BAPI documentation.
- **Subcomponents**: Qdrant Vector Store indexing 15,000+ vector chunks; `text-embedding-3-large` embedding pipeline.

### 4.4 Module 4: SAP RFC Syntax & ATC Verification Gateway
- **Purpose**: Validates LLM-generated code snippets against actual target SAP S/4HANA backend syntax rules and static analysis checkers via RFC connection pooling (`PyRFC`).

### 4.5 Module 5: ABAP Unit Test & RAP CDS Code Generator Module
- **Purpose**: Specialized code generation pipeline for constructing ABAP Unit test classes (`CL_ABAP_UNIT_ASSERT`) and CDS/RAP framework artifacts (`BDEF`, `DDLS`).

---

## 5. Data Flows & API JSON Schemas

### 5.1 Inline Completion Request Payload Schema
```json
{{
  "requestId": "c4b8e1a0-9d2e-4b3f-8a1c-7f5e3b9a2d1e",
  "sapSystemId": "S4H_CLNT_100",
  "abapTargetRelease": "7.54",
  "fileName": "zcl_sales_calculator.clas.abap",
  "cursorPosition": {{ "line": 45, "column": 18 }},
  "codeContext": {{
    "precedingBuffer": "METHOD calculate_discount.\n  DATA(lv_amount) = iv_amount.\n",
    "followingBuffer": "ENDMETHOD.",
    "currentMethodScope": "CALCULATE_DISCOUNT"
  }}
}}
```

### 5.2 Inline Completion Response Payload Schema
```json
{{
  "requestId": "c4b8e1a0-9d2e-4b3f-8a1c-7f5e3b9a2d1e",
  "completionText": "rv_discount = COND #( WHEN lv_amount > 1000 THEN lv_amount * '0.10' ELSE 0 ).",
  "rfcSyntaxCheck": {{
    "isValid": true,
    "lineError": 0,
    "errorMessage": ""
  }},
  "ragReferences": [
    "Clean ABAP Rule: Use COND #( ) conditional expression instead of IF/ELSE blocks"
  ],
  "latencyMs": 380
}}
```

---

## 6. Error Handling & System Resiliency

1. **Network Partition & SAP RFC Failure Strategy**: If SAP application server connection fails, Gateway automatically switches to "Degraded Offline RAG Mode" using local AST syntax validation.
2. **LLM Hallucination Guardrail**: Prohibits destructive commands (`DELETE FROM <table> WITHOUT WHERE`, `CALL 'SYSTEM'`, `BREAK-POINT`).
3. **PII Masking Pipeline**: Sensitive fields and customer Z-tables are masked before sending payloads to cloud LLMs.

---

## 7. User Interface Sketches & Integration Mockups

### 7.1 Eclipse ADT UI Mockup Sketch
![Eclipse ADT UI Mockup](file:///{IMG_ECLIPSE.replace('\\', '/')})

### 7.2 VS Code Extension UI Mockup Sketch
![VS Code UI Mockup](file:///{IMG_VSCODE.replace('\\', '/')})

---

## 8. Requirements Traceability Matrix (RTM)

| Req ID | Functional Requirement | Design Module | API Endpoint | Verification Method |
| :--- | :--- | :--- | :--- | :--- |
| **FR-1** | Inline ABAP Completion | Module 1 & Module 2 | `/api/v1/completion/inline` | Automated Latency & Syntax Test |
| **FR-2** | RAP & CDS Generator | Module 5 (Generator) | `/api/v1/generator/rap-cds` | CDS Activation Unit Test |
| **FR-3** | ATC Refactoring Engine | Module 4 (RFC Gateway) | `/api/v1/atc/remediate` | ATC Static Analysis Runner |
| **FR-4** | ABAP Unit Generator | Module 5 (Generator) | `/api/v1/generator/abap-unit` | AUNIT Test Execution |
| **FR-5** | ABAP Doc Generator | Module 2 (Orchestrator) | `/api/v1/doc/abapdoc` | Docstring AST Inspection |
| **FR-6** | Clean ABAP RAG Lookup | Module 3 (RAG Engine) | `/api/v1/rag/query` | RAG Precision & Recall Metric |

---

## 9. Verification Plan & Acceptance Sign-off

- **Criterion 1**: 100% of generated ABAP code snippets pass target SAP RFC syntax checks without compilation errors.
- **Criterion 2**: Zero Priority 1 (Security) or Priority 2 (Performance) warnings reported by ABAP Test Cockpit on generated CDS views.
- **Criterion 3**: Median response latency for inline completion remains under 1.5 seconds across 1,000 test requests.
"""

    os.makedirs(r"c:\Users\pc\OneDrive\Documents\registration form\sap\docs", exist_ok=True)
    md_file_path = r"c:\Users\pc\OneDrive\Documents\registration form\sap\docs\Week2_Requirements_and_Design.md"
    with open(md_file_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Successfully generated Markdown file at: {md_file_path}")

if __name__ == "__main__":
    build_docx()
    build_markdown()
