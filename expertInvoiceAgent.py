from litellm.agents.expert_agent import prompt_expert
from litellm.agents import register_tool, ActionContext
# Creating the invoic categorization expert agent. This expert tales one sentence descriptions of invoices
# of the invoice and returns the best-fitting category from our predefined list.

@register_tool(tags=["invoice processing", "categorization"]) 
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

# Creating the purchasing rules expert agent.
@register_tool(tags=["invoice processing", "validation"])
def check_purchasing_rules(action_context: ActionContext, invoice_data: dict) -> dict:
    """
    validate an invoice against company purchasing policies.
    Args:
        invoice_data: Extracted invoice details, including vendor, amount, and line items.
    Returns:
        A structured json format indicating whether the invoice is compliant, with explanations.
    """
    # Load the latest purchasing rules from the disk
    rules_path = "config/purchasing_rules.txt"

    try:
        with open(rules_path, 'r') as file:
            purchasing_rules = file.read()
    except FileNotFoundError:
        purchasing_rules = "No rules available. Assume all invoices are compliant."

    validation_schema = {
        "type": "object",
        "properties": {
            "compliant": {"type": "boolean"},
            "issues": {"type": "string"}
        }
    }
    
    return prompt_llm_for_json(
        action_context = action_context,
        schema = validation_schema,
        prompt = f"""Given this invoice data: {invoice_data}, check whether it complies with company purchasing rules.
        The latest purchasing rules are as follows:
        
        {purchasing_rules}
        
        Respond with json object containing:
        - `compliant`: true if the invoice follows all policies, false otherwise.
        - `issues`: A brief explanation of any violations or missing requirements.
        """
    )

