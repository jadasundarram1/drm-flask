import openai
#openai.api_key = ###################

def cluster_emails(descriptions_list):
    prompts = [f"You are being given four categories: Cancellation request, refund request, product question, and accesibility issues. Predict the category for the following email:\n'{email}'\nCategory:" for email in descriptions_list]
    predicted_categories = []

    for prompt in prompts:
        response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1 )
        predicted_categories.append(response.choices[0].text.strip())
        lst = dict(zip(descriptions_list, predicted_categories))

    return predicted_categories

'''for email, category in zip(descriptions_list, predicted_categories):
            print(f"Email: '{email}'")
            print(f"Category: {category}")
            print("-" * 30)'''




