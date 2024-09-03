from openai import OpenAI
import openai
def categorizer(summary, API_KEY):
    client = OpenAI(api_key = API_KEY)

    chat_completion = client.chat.completions.create(
        model = 'gpt-3.5-turbo',
        messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes complaints."},
                {"role": "user", "content": f"Given the following categories: [product-related, service-related, delivery-and-shipping, billing-and-payments, technical, user-experience, legal-and-compliance, marketing-and-advertising, returns-and-exchanges, miscellaneous], determine which category best describes the complaint summary provided. Respond with only the exact category name in the list that most accurately matches the summary: {summary}"}
        ],
        max_tokens = 150
    )

    return chat_completion.choices[0].message.content.strip()