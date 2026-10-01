import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

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
    
    # Left border only (SAP Navy #0070D2)
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

def build_blueprint():
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
    run_sub = title_p.add_run("ENTERPRISE SAP MODERNIZATION BLUEPRINT | WEEK 1 DELIVERABLE\n")
    run_sub.font.name = "Calibri"
    run_sub.font.size = Pt(10)
    run_sub.font.bold = True
    run_sub.font.color.rgb = RGBColor(0, 112, 210) # SAP Blue
    
    run_title = title_p.add_run("Virtual SAP ABAP Coding Assistant")
    run_title.font.name = "Calibri Light"
    run_title.font.size = Pt(26)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(20, 35, 60)
    
    subtitle_p = doc.add_paragraph()
    subtitle_p.paragraph_format.space_before = Pt(0)
    subtitle_p.paragraph_format.space_after = Pt(18)
    run_desc = subtitle_p.add_run("Comprehensive Technical Strategy, System Architecture, Timeline, Risk Mitigation & Resource Allocation Blueprint for Prototype Execution")
    run_desc.font.name = "Calibri"
    run_desc.font.size = Pt(12)
    run_desc.font.italic = True
    run_desc.font.color.rgb = RGBColor(100, 100, 100)

    # Metadata Table Box
    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_widths = [2.0, 4.5]
    meta_data = [
        ("Project Identifier:", "SAP-AI-ABAP-2026-V1"),
        ("Target Platform:", "SAP S/4HANA (On-Premise / Cloud) & SAP BTP AI Core"),
        ("Document Scope:", "Architecture, Objectives, WBS Timeline, Risk & Resource Blueprint"),
        ("Version & Status:", "v1.0 (Final Prototype Blueprint - Approved for Execution)")
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
    
    # Helper for Headings
    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(16)
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
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = RGBColor(40, 90, 140)
        return p

    def add_body(text, space_after=6):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.name = "Calibri"
        run.font.size = Pt(11)
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
        r_pre.font.size = Pt(11)
        r_pre.font.color.rgb = RGBColor(30, 30, 30)
        
        r_txt = p.add_run(text)
        r_txt.font.name = "Calibri"
        r_txt.font.size = Pt(11)
        r_txt.font.color.rgb = RGBColor(60, 60, 60)
        return p

    # --- CHAPTER 1 ---
    add_h1("1. Executive Summary & Strategic Vision")
    add_body(
        "Enterprise software development within the SAP ecosystem is undergoing a generational shift. As global enterprises "
        "accelerate their migration from legacy SAP ECC 6.0 environments to SAP S/4HANA and SAP Business Technology Platform (BTP), "
        "the demand for highly specialized ABAP (Advanced Business Application Programming) developers has vastly outstripped market supply. "
        "Furthermore, decades of legacy ABAP custom code—often characterized by procedural constructs, direct table selects, obsolete syntax, "
        "and missing unit tests—presents a major hurdle to clean core maintenance and cloud readiness."
    )
    add_body(
        "The Virtual SAP ABAP Coding Assistant Project aims to construct an intelligent, context-aware, enterprise-grade virtual assistant "
        "designed specifically for ABAP engineers and SAP solution architects. Leveraging state-of-the-art Large Language Models (LLMs) integrated "
        "with Retrieval-Augmented Generation (RAG) over SAP ABAP Keyword Documentation, Clean ABAP standards, and enterprise repository metadata, "
        "the assistant acts as a pair-programmer within developer IDEs (Eclipse ADT and VS Code)."
    )
    
    add_callout_box(
        doc,
        "The strategic objective of the Virtual SAP ABAP Assistant is to increase developer throughput by 35-45%, eliminate critical syntax and "
        "security defects prior to SAP Transport submission, enforce Clean ABAP standards automatically, and drastically reduce the technical debt "
        "associated with legacy SAP S/4HANA migrations.",
        "EXECUTIVE MANDATE"
    )

    # --- CHAPTER 2 ---
    add_h1("2. Project Scope & S.M.A.R.T. Objectives")
    add_body(
        "To ensure high execution fidelity and disciplined prototype delivery, the project scope is rigorously bound into in-scope functional "
        "modules and out-of-scope boundaries, underpinned by quantitative S.M.A.R.T. objectives."
    )
    
    add_h2("2.1 Detailed Scope Definition")
    add_bullet("In-Scope Features: ", "Real-time context-aware ABAP code completion and inline code generation for modern syntax (ABAP 7.4+ and 7.5+ constructs).")
    add_bullet("In-Scope Features: ", "Automated ABAP RESTful Application Programming Model (RAP) and Core Data Services (CDS) view generator.")
    add_bullet("In-Scope Features: ", "Automated ABAP Test Cockpit (ATC) static analysis evaluation and one-click code refactoring suggestions.")
    add_bullet("In-Scope Features: ", "ABAP Unit test suite auto-generation adhering to isolated mock framework paradigms (CL_ABAP_UNIT_ASSERT).")
    add_bullet("In-Scope Features: ", "ABAP Doc / docstring generation for classes, methods, function modules, and BAPI interfaces.")
    add_bullet("In-Scope Features: ", "RAG-driven SAP Keyword Documentation & Clean ABAP style guide lookup engine.")
    
    add_bullet("Out-of-Scope (Phase 1 Prototype): ", "Direct automated release of SAP Transports (SE09/SE10) without human developer authorization.")
    add_bullet("Out-of-Scope (Phase 1 Prototype): ", "Modifications to standard SAP SAPL* core kernel modules or locked SAP standard namespace (/0S/) objects.")
    add_bullet("Out-of-Scope (Phase 1 Prototype): ", "Non-ABAP SAP UI technologies (such as SAPUI5/Fiori XML view auto-coding) in the initial milestone phase.")

    add_h2("2.2 S.M.A.R.T. Project Objectives")
    add_body("The success of the Virtual SAP ABAP Coding Assistant prototype will be evaluated against six specific S.M.A.R.T. criteria:")
    
    # Objectives Table
    obj_table = doc.add_table(rows=7, cols=3)
    obj_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    obj_widths = [1.8, 3.2, 1.5]
    
    headers = ["Objective Area", "Target Description", "Measurement Metric"]
    for idx, h in enumerate(headers):
        obj_table.rows[0].cells[idx].paragraphs[0].text = h
    style_table_header(obj_table.rows[0], obj_widths)
    
    obj_rows = [
        ("Code Generation Speed", "Reduce average developer time spent writing boilerplate ABAP CDS views and RAP BOs.", "> 40% reduction in time-to-first-commit"),
        ("ATC Quality Compliance", "Ensure generated ABAP code passes ABAP Test Cockpit static code checks with zero priority 1 & 2 errors.", "100% compliance on ATC Priority 1 & 2"),
        ("Clean ABAP Alignment", "Automate compliance with Clean ABAP guidelines (e.g., modern SELECT syntax, inline declarations).", "> 95% adherence rating in peer review"),
        ("ABAP Unit Coverage", "Generate automated unit test scaffolds for custom ABAP methods.", "> 80% statement coverage on custom methods"),
        ("Inference Latency", "Deliver inline code completions rapidly to avoid breaking developer context flow in Eclipse ADT.", "< 1.5 seconds median response latency"),
        ("Developer Adoption", "Achieve high satisfaction rating among pilot enterprise ABAP developers during pilot phase.", "> 85% positive NPS score in Pilot (W12)")
    ]
    
    for r_idx, row_data in enumerate(obj_rows, start=1):
        row = obj_table.rows[r_idx]
        bg = "F9FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = Inches(obj_widths[c_idx])
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.size = Pt(9.5)
            if c_idx == 0:
                run.font.bold = True
                run.font.color.rgb = RGBColor(0, 70, 140)
            else:
                run.font.color.rgb = RGBColor(50, 50, 50)
                
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # --- CHAPTER 3 ---
    add_h1("3. SAP ABAP Research & Methodological Foundations")
    add_body(
        "Developing an AI assistant for SAP ABAP requires a domain-specific understanding of SAP software engineering architecture. "
        "Unlike generic programming languages (such as Python or JavaScript), ABAP code operates strictly inside the SAP NetWeaver / ABAP Platform "
        "application server, closely coupled with the SAP database dictionary (DDIC), transaction control, and SAP transport organizers."
    )
    
    add_h2("3.1 Key SAP ABAP Design Methodology Frameworks")
    add_bullet("Clean ABAP Paradigm: ", "Adherence to the official SAP Clean ABAP style guide. The assistant must systematically promote expressions such as inline declarations (DATA(lv_var) = ...), string templates (|Hello { lv_name }|), method chaining, and avoid obsolete statements like TABLES, MOVE, COMPUTE, or HEADER LINE constructs.")
    add_bullet("ABAP RESTful Programming Model (RAP): ", "Modern SAP S/4HANA development relies on CDS (Core Data Services) views, Business Object Behavior Definitions (BDEF), and Service Definitions. The assistant must understand RAP lifecycle annotations, transactional processing via EML (Entity Manipulation Language), and draft handling.")
    add_bullet("Code-to-Data Architecture: ", "Pushing intensive data computations down to the SAP HANA database layer via CDS views, ABAP Managed Database Procedures (AMDP), and open SQL aggregate expressions rather than pulling massive internal tables into ABAP memory.")
    add_bullet("ABAP Test Cockpit (ATC) & Code Inspector: ", "Integration of ATC rule checks directly into the LLM prompt-response evaluation loop. Code suggestions must be pre-evaluated against security rules (SQL injection prevention, authorization check validations via AUTHORITY-CHECK OBJECT).")

    add_h2("3.2 Retrieval-Augmented Generation (RAG) Architecture for ABAP")
    add_body(
        "Due to the specialized syntax of ABAP 7.5+ and custom SAP enterprise structures, generic public LLMs often hallucinate invalid keywords. "
        "To mitigate this, our blueprint embeds a specialized RAG engine storing vectorized representations of:"
    )
    add_bullet("SAP Keyword Documentation: ", "Official SAP ABAP language references for versions 7.40 through 7.58.")
    add_bullet("Custom Enterprise Dictionary (DDIC) Schemas: ", "Standard BAPIs (e.g., BAPI_PO_CREATE1), BAdI definitions, standard CDS views (I_PurchaseOrderTP), and customer Z-tables.")
    add_bullet("Corporate Clean ABAP Rulesets: ", "Specific enterprise coding guidelines and naming conventions (e.g., zcl_*, zif_*).")

    # --- CHAPTER 4 ---
    add_h1("4. Overall System Architecture & Technical Design")
    add_body(
        "The Virtual SAP ABAP Coding Assistant architecture is designed as a secure, decoupled, hybrid cloud/on-premise system. "
        "It connects the developer's IDE with an enterprise AI Orchestration Engine and the target SAP S/4HANA environment."
    )
    
    # Architecture Visual Diagram Representation
    add_h2("4.1 High-Level Architectural Diagram")
    
    arch_box = doc.add_table(rows=1, cols=1)
    arch_box.alignment = WD_TABLE_ALIGNMENT.CENTER
    arch_cell = arch_box.cell(0, 0)
    arch_cell.width = Inches(6.5)
    set_cell_background(arch_cell, "F4F6FB")
    set_cell_margins(arch_cell, top=140, bottom=140, left=150, right=150)
    
    arch_p = arch_cell.paragraphs[0]
    arch_p.paragraph_format.space_before = Pt(2)
    arch_p.paragraph_format.space_after = Pt(2)
    arch_text = (
        "+---------------------------------------------------------------------------------------+\n"
        "|                             1. CLIENT & DEVELOPER IDE LAYER                           |\n"
        "|  +-------------------------------------+   +---------------------------------------+  |\n"
        "|  |  Eclipse ADT Plugin (ABAP Dev)      |   |  VS Code ABAP Assistant Extension    |  |\n"
        "|  |  - Inline Completion & Chat Panel   |   |  - Syntax Highlight & ATC Alerts      |  |\n"
        "|  +------------------+------------------+   +-------------------+-------------------+  |\n"
        "+---------------------|------------------------------------------|----------------------+\n"
        "                      | HTTPS / gRPC (TLS 1.3 + mTLS)            |\n"
        "                      v                                          v\n"
        "+---------------------------------------------------------------------------------------+\n"
        "|                        2. AI ORCHESTRATION & GATEWAY LAYER                            |\n"
        "|  +---------------------------------------------------------------------------------+  |\n"
        "|  |  FastAPI / Node.js AI Middleware Gateway (Deployed on SAP BTP / Kubernetes)       |  |\n"
        "|  |  - JWT Auth / SAP IAS Validation  - Prompt Sanitizer & PII Masking Engine       |  |\n"
        "|  |  - Rate Limiter & Token Metering  - Context Assembler & Prompt Orchestrator     |  |\n"
        "|  +------------------+------------------------------------------+-------------------+  |\n"
        "+---------------------|------------------------------------------|----------------------+\n"
        "                      | Vector Search                            | LLM Prompt Dispatch\n"
        "                      v                                          v\n"
        "+------------------------------------+   +----------------------------------------------+\n"
        "|     3. RAG VECTOR DATABASE         |   |         4. LLM INFERENCE ENGINE              |\n"
        "|  - Qdrant / FAISS Vector DB        |   |  - Enterprise Azure OpenAI / SAP BTP AI Core |\n"
        "|  - SAP ABAP 7.5+ Syntax Index      |   |  - Fine-Tuned ABAP Coding Model              |\n"
        "|  - Clean ABAP Style Vector Index   |   |  - Code Generation & Refactoring Pipeline    |\n"
        "+------------------------------------+   +----------------------------------------------+\n"
        "                                                                |\n"
        "                      +-----------------------------------------+\n"
        "                      | RFC / OData v4 Syntax Validation\n"
        "                      v\n"
        "+---------------------------------------------------------------------------------------+\n"
        "|                         5. TARGET SAP S/4HANA BACKEND ENVIRONMENT                     |\n"
        "|  +-----------------------------------+   +-----------------------------------------+  |\n"
        "|  | SAP Syntax Verification RFC Service|   | SAP ATC (ABAP Test Cockpit) RFC Service |  |\n"
        "|  | - Performs real-time syntax check  |   | - Executes static security check        |  |\n"
        "|  +-----------------------------------+   +-----------------------------------------+  |\n"
        "+---------------------------------------------------------------------------------------+"
    )
    arch_run = arch_p.add_run(arch_text)
    arch_run.font.name = "Consolas"
    arch_run.font.size = Pt(8.5)
    arch_run.font.color.rgb = RGBColor(0, 50, 100)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_h2("4.2 System Component Descriptions")
    add_bullet("1. Client IDE Layer: ", "Integrates directly into Eclipse ABAP Development Tools (ADT) via Java/Eclipse plugin hooks and VS Code via a custom extension. Captures cursor position, active method body, and surrounding class context.")
    add_bullet("2. AI Orchestration Middleware: ", "Hosted on SAP Business Technology Platform (BTP) Kyma/Cloud Foundry or enterprise Kubernetes. Handles security authorization via SAP Identity Authentication Service (IAS), strips confidential business PII data, and constructs contextual prompts.")
    add_bullet("3. RAG Vector Knowledge Base: ", "Vector database storing high-density embeddings of SAP standard function modules, BAPIs, modern ABAP syntax trees, and company-specific coding guidelines.")
    add_bullet("4. LLM Inference Engine: ", "Utilizes specialized code models (e.g., Azure OpenAI GPT-4o / Claude 3.5 Sonnet / fine-tuned DeepSeek Coder) optimized for code synthesis and low-latency inference via SAP BTP AI Core.")
    add_bullet("5. SAP S/4HANA RFC Gateway: ", "Communicates with target SAP systems via Secure Network Communications (SNC) RFC calls to execute background syntax checks (`SYNTAX-CHECK STATEMENT`) and ATC inspections prior to returning suggested code to the developer.")

    # --- CHAPTER 5 ---
    add_h1("5. Detailed Project Timeline, WBS & Strategic Milestones")
    add_body(
        "The project will be executed over a structured 12-week timeframe organized into five distinct phases using a hybrid Agile-StageGate methodology. "
        "Below is the comprehensive Work Breakdown Structure (WBS) and Gantt Chart schedule."
    )
    
    add_h2("5.1 Work Breakdown Structure (WBS)")
    add_bullet("Phase 1: Inception, Architecture & Environment Setup (Weeks 1 - 2)", "Finalize blueprint, establish SAP BTP sandbox, setup vector DB, deploy baseline IDE plugins.")
    add_bullet("Phase 2: RAG Pipeline & ABAP Domain Embeddings (Weeks 3 - 5)", "Parse SAP ABAP 7.5+ syntax docs, build chunking pipeline, index Clean ABAP rules, integrate DDIC metadata connector.")
    add_bullet("Phase 3: Core Assistant Engine & IDE Integration (Weeks 6 - 9)", "Develop prompt orchestration gateway, implement inline completion, build ATC refactoring module and ABAP Unit auto-generator.")
    add_bullet("Phase 4: Evaluation, Fine-Tuning & ATC Validation (Weeks 10 - 11)", "Conduct benchmark suite evaluation across 200 real-world ABAP tasks, fine-tune context windowing, optimize RFC validation calls.")
    add_bullet("Phase 5: Prototype Deployment & Enterprise Pilot Execution (Week 12)", "Deploy v1.0 prototype to pilot developer cohort, execute user evaluation, present executive readout.")

    add_h2("5.2 12-Week Gantt Chart Schedule")
    
    # Gantt Chart Table
    gantt_table = doc.add_table(rows=6, cols=7)
    gantt_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    gantt_widths = [2.2, 0.7, 0.7, 0.7, 0.7, 0.7, 0.8]
    
    g_headers = ["Phase / Activity", "W1-2", "W3-5", "W6-8", "W9-10", "W11", "W12"]
    for idx, h in enumerate(g_headers):
        gantt_table.rows[0].cells[idx].paragraphs[0].text = h
    style_table_header(gantt_table.rows[0], gantt_widths)
    
    gantt_rows = [
        ("P1: Inception & Architecture Setup", "█████", "░░░░░", "░░░░░", "░░░░░", "░░░░░", "░░░░░"),
        ("P2: RAG Pipeline & Data Indexing", "░░░░░", "█████", "░░░░░", "░░░░░", "░░░░░", "░░░░░"),
        ("P3: Core Engine & IDE Integration", "░░░░░", "░░░░░", "█████", "█████", "░░░░░", "░░░░░"),
        ("P4: Testing, ATC & Fine-Tuning", "░░░░░", "░░░░░", "░░░░░", "█████", "█████", "░░░░░"),
        ("P5: Pilot Execution & Final Readout", "░░░░░", "░░░░░", "░░░░░", "░░░░░", "░░░░░", "█████")
    ]
    
    for r_idx, row_data in enumerate(gantt_rows, start=1):
        row = gantt_table.rows[r_idx]
        bg = "F9FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = Inches(gantt_widths[c_idx])
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=80, bottom=80, left=60, right=60)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.size = Pt(9.5)
            if c_idx == 0:
                run.font.bold = True
                run.font.color.rgb = RGBColor(0, 70, 140)
            elif "█" in val:
                run.font.bold = True
                run.font.color.rgb = RGBColor(0, 112, 210)
            else:
                run.font.color.rgb = RGBColor(180, 180, 180)
                
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_h2("5.3 Key Strategic Milestones")
    add_bullet("Milestone M1 (End of Week 2): ", "Architecture Sign-off & SAP BTP Environment Provisioned.")
    add_bullet("Milestone M2 (End of Week 5): ", "ABAP 7.5+ RAG Vector Store Built & Indexed (>10,000 keyword & pattern vectors).")
    add_bullet("Milestone M3 (End of Week 8): ", "Eclipse ADT & VS Code Plugins Functioning with Low-Latency Completion (<1.5s).")
    add_bullet("Milestone M4 (End of Week 10): ", "ATC Syntax Validation & ABAP Unit Generator Fully Integrated via RFC.")
    add_bullet("Milestone M5 (End of Week 12): ", "Pilot Phase Completed with >85% Positive Developer Satisfaction & Final Executive Readout.")

    # --- CHAPTER 6 ---
    add_h1("6. Comprehensive Risk Assessment & Mitigation Framework")
    add_body(
        "Operating an AI assistant within an enterprise SAP landscape entails specific technical, operational, security, and compliance risks. "
        "The risk management matrix below defines likelihood, impact, and actionable mitigation strategies."
    )
    
    # Risk Table
    risk_table = doc.add_table(rows=6, cols=5)
    risk_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    risk_widths = [1.5, 1.2, 0.8, 0.8, 2.2]
    
    r_headers = ["Risk Category", "Specific Risk Description", "Likelihood", "Impact", "Mitigation Strategy"]
    for idx, h in enumerate(r_headers):
        risk_table.rows[0].cells[idx].paragraphs[0].text = h
    style_table_header(risk_table.rows[0], risk_widths, bg_hex="005A9C")
    
    risk_rows = [
        ("IP & Security", "Exposure of proprietary SAP ABAP code or business data to external public cloud LLMs.", "Medium", "High", "Deploy isolated Azure OpenAI / SAP BTP AI Core tenant with strict zero-data-retention policy and local PII masking gateway."),
        ("Hallucination", "LLM generates obsolete ABAP syntax (e.g., TABLES statement) or non-existent BAPIs.", "High", "High", "Implement RAG with ABAP 7.5+ ruleset and enforce background SAP RFC syntax check (`SYNTAX-CHECK`) prior to displaying code."),
        ("Version Mismatch", "Code suggestions optimized for SAP S/4HANA fail on legacy SAP ECC 6.0 system.", "High", "Medium", "Inject target SAP release version (e.g., ABAP 7.40 vs 7.55) into LLM system prompt context dynamically."),
        ("Latency Bottleneck", "RAG vector lookup and LLM inference cause developer IDE lag exceeding 3 seconds.", "Medium", "Medium", "Utilize speculative decoding, local vector caching, and async gRPC streaming for inline code completion."),
        ("Developer Trust", "Developers reject AI suggestions due to inaccurate formatting or lack of Clean ABAP style.", "Medium", "High", "Incorporate automated Clean ABAP linters into prompt output validation; involve senior SAP architects early in pilot.")
    ]
    
    for r_idx, row_data in enumerate(risk_rows, start=1):
        row = risk_table.rows[r_idx]
        bg = "F9FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = Inches(risk_widths[c_idx])
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.size = Pt(9.0)
            if c_idx == 0:
                run.font.bold = True
                run.font.color.rgb = RGBColor(0, 70, 140)
            elif c_idx in [2, 3]:
                run.font.bold = True
                if val == "High":
                    run.font.color.rgb = RGBColor(180, 0, 0)
                else:
                    run.font.color.rgb = RGBColor(180, 100, 0)
            else:
                run.font.color.rgb = RGBColor(50, 50, 50)
                
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # --- CHAPTER 7 ---
    add_h1("7. Resource Allocation, Infrastructure & Operational Blueprint")
    add_body(
        "A successful prototype delivery requires balanced human resource allocation, cloud infrastructure provisioning, "
        "and proactive strategy execution to overcome operational bottlenecks."
    )
    
    add_h2("7.1 Human Resource Allocation Matrix")
    
    res_table = doc.add_table(rows=6, cols=4)
    res_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    res_widths = [1.8, 1.2, 2.5, 1.0]
    
    res_headers = ["Project Role", "FTE Commitment", "Key Responsibilities & Deliverables", "Allocation Phase"]
    for idx, h in enumerate(res_headers):
        res_table.rows[0].cells[idx].paragraphs[0].text = h
    style_table_header(res_table.rows[0], res_widths)
    
    res_rows = [
        ("Lead SAP ABAP Architect", "1.0 FTE", "Define Clean ABAP standards, lead ATC integration, validate RAP/CDS models, conduct code reviews.", "Weeks 1 - 12"),
        ("AI / ML Lead Engineer", "1.0 FTE", "Design RAG pipeline, manage vector DB, build prompt orchestration gateway, optimize LLM inference.", "Weeks 1 - 12"),
        ("SAP BTP / Cloud Developer", "1.0 FTE", "Implement SAP BTP middleware, configure SAP IAS authentication, build RFC/OData connectors.", "Weeks 2 - 10"),
        ("Frontend IDE Developer", "0.5 FTE", "Develop Eclipse ADT Java plugin and VS Code extension UI components.", "Weeks 4 - 9"),
        ("SAP QA & Security Specialist", "0.5 FTE", "Execute security audit, validate data masking gateway, manage pilot developer benchmark testing.", "Weeks 8 - 12")
    ]
    
    for r_idx, row_data in enumerate(res_rows, start=1):
        row = res_table.rows[r_idx]
        bg = "F9FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = Inches(res_widths[c_idx])
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.size = Pt(9.0)
            if c_idx == 0:
                run.font.bold = True
                run.font.color.rgb = RGBColor(0, 70, 140)
            else:
                run.font.color.rgb = RGBColor(50, 50, 50)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_h2("7.2 Infrastructure & Tooling Requirements")
    add_bullet("SAP Sandbox Instance: ", "Dedicated SAP S/4HANA 2023 On-Premise / Private Cloud sandbox system with developer access (Developer keys & ATC enabled).")
    add_bullet("SAP BTP Enterprise Tenant: ", "SAP Business Technology Platform runtime environment (Kyma/Cloud Foundry) with SAP AI Core subscription.")
    add_bullet("AI Vector Infrastructure: ", "Qdrant Enterprise / FAISS cluster hosted with minimum 32GB RAM for low-latency similarity vector searches.")
    add_bullet("LLM Cloud API Access: ", "Enterprise Azure OpenAI Service endpoint (GPT-4o deployment with zero-data-logging agreement).")

    add_h2("7.3 Operational Challenges & Countermeasure Strategies")
    add_bullet("Challenge 1: SAP System Access & RFC Auth Delays", "Strategy: Pre-provision SAP developer licenses and RFC service users during Week 1 inception phase.")
    add_bullet("Challenge 2: Enterprise Security Approval for Cloud LLMs", "Strategy: Present pre-sanitized PII architecture and data protection impact assessment (DPIA) to InfoSec in Week 2.")
    add_bullet("Challenge 3: ABAP Developer Inertia & Change Management", "Strategy: Run hands-on workshops during pilot (Week 12) showing clear velocity gain on repetitive CDS & unit test creation tasks.")

    # Save document
    output_filename = "Virtual_SAP_ABAP_Assistant_Project_Blueprint.docx"
    doc.save(output_filename)
    print(f"Document successfully created: {output_filename}")
    return output_filename

if __name__ == "__main__":
    build_blueprint()
