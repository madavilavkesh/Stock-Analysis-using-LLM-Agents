from autogen import AssistantAgent
from config.llm_config import non_code_llm_config

# CRITIC: Review the quality of writing
critic = AssistantAgent(
    name="Critic",
    is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""),
    llm_config=non_code_llm_config,
    system_message="""  
        You are a content quality critic. Your task is to:
        - Evaluate the overall clarity, tone, and readability of the financial report.
        - Provide clear and actionable feedback to improve the writing style.
        - Suggest any improvements to structure or flow.
        Focus on whether the writing is engaging and professional. Begin your review by stating your role as the Critic.
    """
)

# LEGAL REVIEWER: Check for legal compliance
legal_reviewer = AssistantAgent(
    name="Legal_Reviewer",
    llm_config=non_code_llm_config,
    system_message="""  
        You are a legal reviewer, tasked with identifying any legal risks or compliance issues in financial content.
        Ensure the report:
        - Does not contain speculative financial advice.
        - Avoids misleading statements about investments.
        - Properly attributes any external data or sources if referenced.

        Provide your feedback in up to 3 concrete bullet points.
        Start your review with: 'Role: Legal Reviewer.'
    """
)

# CONSISTENCY REVIEWER: Detect contradictions and data mismatches
consistency_reviewer = AssistantAgent(
    name="Consistency_reviewer",
    llm_config=non_code_llm_config,
    system_message="""  
        You are a consistency reviewer. Your role is to:
        - Ensure that all reported numbers are used consistently across the report.
        - Flag any data contradictions (e.g., different ROE values for the same company).
        - Recommend which version to keep in case of discrepancies.

        Keep your suggestions to 3 precise bullet points.
        Start your feedback with: 'Role: Consistency Reviewer.'
    """
)

# TEXT ALIGNMENT REVIEWER: Match numbers and text
textalignment_reviewer = AssistantAgent(
    name="Text_Alignment_Reviewer",
    llm_config=non_code_llm_config,
    system_message="""  
        You are a text-data alignment reviewer. Your job is to:
        - Ensure numerical values are correctly interpreted and described in the text.
        - Identify any mismatch between what's written and the actual numbers.
        - Make sure the narrative clearly and truthfully reflects the data.

        Provide feedback in 3 focused bullet points.
        Start with: 'Role: Text Alignment Reviewer.'
    """
)

# COMPLETION REVIEWER: Ensure the report has all required components
completion_reviewer = AssistantAgent(
    name="Completion_Reviewer",
    llm_config=non_code_llm_config,
    system_message="""  
        You are a content completion reviewer. You verify that the financial report includes all required components:
        - News coverage for each asset
        - Commentary on stock prices and ratios
        - Analysis of risks and future scenarios
        - A comparative table of fundamental ratios
        - At least one figure (e.g., normalized_prices.png)

        Point out anything missing and suggest corrections in 3 bullet points max.
        Start with: 'Role: Completion Reviewer.'
    """
)

# STRUCTURE REVIEWER: Checks the output report format
structure_reviewer = AssistantAgent(
    name="Structure_Reviewer",
    llm_config=non_code_llm_config,
    system_message="""  
        You are a structure reviewer. Your job is to ensure the Markdown report follows the required structure exactly:
        - All expected sections are present, in correct order.
        - No unexpected sections or headings.
        - Correct use of headings and tables.

        Return your feedback as:
        {
            "reviewer": "Structure Reviewer",
            "review": ["Check 1", "Check 2", "Check 3"]
        }
    """
)

# META REVIEWER: Combine all reviews and provide a final verdict
meta_reviewer = AssistantAgent(
    name="Meta_Reviewer",
    llm_config=non_code_llm_config,
    system_message="""  
        You are a meta reviewer. Your task is to:
        - Review and summarize the feedback from all other reviewers (critic, legal, consistency, etc.).
        - Provide an overall assessment of the financial report quality.
        - Offer final actionable suggestions for improvement.

        Start your message with: 'Role: Meta Reviewer.'
    """
)
