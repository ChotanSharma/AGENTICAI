from litellm.agents.expert_agent import prompt_expert
from litellm.agents import register_tool, ActionContext
# Creating the invoic categorization expert agent. This expert tales one sentence descriptions of invoices
# of the invoice and returns the best-fitting category from our predefined list.

@register_tool(tags=["invoce processing", "categorization"]) 
def categorize_expenditure(action_context: ActionContext, description: str) -> str:
    """
    Categorize an invoice expenditure based on a short description. 

    Args:
        description: A one-sentence summary of expenditure.

    Returns:
        A category name from the predefined set of 20 categories.
    """
    categories = [
        "Office Supplies", "IT Equipment", "Software Licenses", "Consulting Services", 
        "Travel Expenses", "Marketing", "Training & Development", "Facilities Maintenance",
        "Utilities", "Legal Services", "Insurance", "Medical Services", "Payroll",
        "Research & Development", "Manufacturing Supplies", "Construction", "Logistics",
        "Customer Support", "Security Services", "Miscellaneous"
    ]

    return prompt_expert(
        action_context = action_context,
        description_of_expert = "A senior financial analyst with deep expertise in corporate spending categorization.",
        prompt = f"Given the following description: '{description}' classify the expense into one of these categories: \n{categories}" 

    )