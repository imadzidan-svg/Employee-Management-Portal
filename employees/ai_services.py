from openai import OpenAI

import os


client = OpenAI(
    api_key=os.getenv(
        'OPENAI_API_KEY'
    )
)


def generate_workforce_insights(
    employees
):

    if not employees:

        return (
            "No employee data available."
        )

    summary = []

    for employee in employees:

        summary.append(

            f"""
            Employee:
            {employee.first_name}
            {employee.last_name}

            Department:
            {employee.department}

            Salary:
            {employee.salary}
            """
        )

    prompt = f"""

    Analyze this workforce dataset.

    Provide:
    - workforce observations
    - salary insights
    - department insights
    - HR recommendations

    Data:

    {''.join(summary)}

    """

    response = client.chat.completions.create(

        model="gpt-4.1-mini",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content

def analyze_resume_text(
    resume_text
):

    prompt = f"""

    Analyze this resume.

    Provide:
    - professional summary
    - key technical skills
    - strengths
    - possible weaknesses
    - suitable job roles
    - seniority level estimate

    Resume:

    {resume_text}

    """

    response = client.chat.completions.create(

        model="gpt-4.1-mini",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content