import os
from openai import OpenAI
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# This is the detailed instruction template for the AI model
PROMPT_TEMPLATE = """
**User Parameters:**
1.  **Doshas:** {dosha}
2.  **Location:** {location}
3.  **Weather:** {weather}
4.  **Primary Disease/Health Condition:** {disease}
5.  **Physiological Data:**
    * Daily Water Intake: {water}L
    * BMI: {bmi}
    * Sleep Quality: {sleep}
6.  **Secondary Condition:** {secondary_condition}
7.  **Appetite:** {appetite}
"""

SYSTEM_INSTRUCTION = """
**Role:** You are an expert clinical nutritionist and Ayurvedic specialist.

**Task:** Generate a highly accurate and detailed 1-day diet plan for a user based on the User Parameters provided. The plan must be holistic, considering all health conditions, location, and Ayurvedic dosha profile.

**Instructions for the Diet Plan:**
1.  **Structure:** Organize the plan into these sections: "General Recommendations", "Early Morning", "Breakfast", "Mid-Morning Snack", "Lunch", "Evening Snack", "Dinner", "Bedtime", "Foods to Favor", and "Foods to Reduce or Avoid". You MUST use '###' markdown headings for each section title (e.g., ### Breakfast).
2.  **Reasoning:** For each meal, briefly explain *why* it is suitable for the user, referencing their dosha, disease, and BMI.
3.  **Quantities:** This is critical. For each food item, specify the approximate portion size in grams (g) or milliliters (ml). For example: "Cooked Brown Rice (150g)", "Grilled Chicken Breast (120g)", or "Skimmed Milk (200ml)". Be precise.
4.  **Local Availability:** The food suggestions should be practical and likely available in the user's location.
5.  **Address All Parameters:** The plan must holistically address all 7 user parameters.
""" # <-- The disclaimer instruction has been removed from here.

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_plan():
    try:
        client = OpenAI(api_key="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")

        form_data = {
            "dosha": request.form['dosha'],
            "location": request.form['location'],
            "weather": request.form['weather'],
            "disease": request.form['disease'],
            "water": request.form['water'],
            "bmi": request.form['bmi'],
            "sleep": request.form['sleep'],
            "secondary_condition": request.form['secondary_condition'],
            "appetite": request.form['appetite']
        }

        user_prompt = PROMPT_TEMPLATE.format(**form_data)

        chat_completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTION},
                {"role": "user", "content": user_prompt}
            ]
        )

        plan_text = chat_completion.choices[0].message.content
        return jsonify({'plan': plan_text})

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': f'An internal error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)