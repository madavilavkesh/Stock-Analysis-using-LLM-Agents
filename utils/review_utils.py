from agents.reviewer_agents import (
    legal_reviewer,
    textalignment_reviewer,
    consistency_reviewer,
    completion_reviewer,
    meta_reviewer,
    structure_reviewer
)

def reflection_message(recipient, messages, sender, config):
    latest_content = recipient.chat_messages_for_summary(sender)[-1]['content']
    return (
        "You are now reviewing the latest draft of a financial report written by the writer agent.\n\n"
        "Please read the content below and follow your specific reviewer role instructions to provide feedback.\n\n"
        f"{latest_content}"
    )

# Define a unified prompt structure for all reviewers except Meta Reviewer
review_json_prompt = (
    "Return your review as a JSON object with the following format:\n"
    "{\n"
    "  'reviewer': '<your role>',\n"
    "  'review': '<your feedback in up to 3 concise bullet points>'\n"
    "}"
)

review_chats = [
    {
        "recipient": legal_reviewer,
        "message": reflection_message,
        "summary_method": "reflection_with_llm",
        "summary_args": {
            "summary_prompt": review_json_prompt
        },
        "max_turns": 1
    },
    
    {
        "recipient": textalignment_reviewer,
        "message": reflection_message,
        "summary_method": "reflection_with_llm",
        "summary_args": {
            "summary_prompt": review_json_prompt
        },
        "max_turns": 1
    },
    
    {
        "recipient": consistency_reviewer,
        "message": reflection_message,
        "summary_method": "reflection_with_llm",
        "summary_args": {
            "summary_prompt": review_json_prompt
        },
        "max_turns": 1
    },
    
    {
        "recipient": completion_reviewer,
        "message": reflection_message,
        "summary_method": "reflection_with_llm",
        "summary_args": {
            "summary_prompt": review_json_prompt
        },
        "max_turns": 1
    },
    
    {
         "recipient": structure_reviewer,
         "message": reflection_message,
         "summary_method": "reflection_with_llm",
         "summary_args": {
            "summary_prompt": review_json_prompt
         },
         "max_turns": 1
    },

    {
        "recipient": meta_reviewer,
        "message": (
            "You are the Meta Reviewer.\n"
            "Your job is to aggregate and summarize the feedback from all the other reviewers "
            "(legal, consistency, alignment, and completion reviewers).\n\n"
            "Return your final verdict and improvements as a JSON object:\n"
            "{\n"
            "  'reviewer': 'Meta Reviewer',\n"
            "  'review': '<your final, aggregated feedback>'\n"
            "}"
        ),
        "max_turns": 1
    }
]
