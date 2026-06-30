ROUTER_PROMPT = """Classify the user's request into exactly one of these categories:
- "FULL_FLOW": if the user wants to reserve or book a parking spot, OR if the user is answering a confirmation prompt, yes/no query, or registration permission request (e.g. "yes", "no", "sure", "please proceed").
- "CHECK_SLOTS": if the user ONLY wants to check available slots.
- "CHECK_PRICE": if the user ONLY wants to check pricing.

Reply with ONLY the category string.
"""
