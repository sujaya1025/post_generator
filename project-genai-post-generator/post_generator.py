from llm_helper import llm
from few_shot import FewShotPosts

few_shot = FewShotPosts()

TONE_STYLES = {
    "Professional & Informative": "Formal but approachable. Share industry insights, data, research, or explain concepts.",
    "Conversational & Relatable": "Friendly, casual, and engaging. Share personal experiences, lessons learned, or storytelling.",
    "Inspirational & Motivational": "Uplifting, encouraging, optimistic. Career advice, celebrating achievements, or motivating others.",
    "Thought-Provoking & Opinionated": "Bold, confident, sometimes contrarian. Start discussions, challenge conventional wisdom, spark debate.",
    "Storytelling & Narrative-Driven": "Engaging, emotional, sometimes dramatic. Share career journeys, case studies, or anecdotes.",
    "Educational / Value-Driven": "Clear, structured, practical. Share tips, how-tos, frameworks, checklists.",
    "Humble & Authentic": "Honest, vulnerable, human. Share struggles, failures, or behind-the-scenes experiences.",
    "Celebratory & Appreciative": "Grateful, positive, and warm. Acknowledge milestones, thank teams, or celebrate success."
}

def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    if length == "Long":
        return "11 to 15 lines"

def generate_post(length, language, tag, tone=None, output_format="Paragraph", external_links=None, custom_prompt=None):
    prompt = get_prompt(length, language, tag, tone, output_format, external_links, custom_prompt)
    response = llm.invoke(prompt)
    return response.content

def get_prompt(length, language, tag, tone=None, output_format="Paragraph", external_links=None, custom_prompt=None):
    length_str = get_length_str(length)

    prompt = f"Generate a LinkedIn post with the following details:\n"
    prompt += f"1) Topic: {tag}\n"
    prompt += f"2) Length: {length_str}\n"
    prompt += f"3) Language: {language}\n"
    prompt += f"4) Format: {output_format}\n"

    if language.lower() == "hinglish":
        prompt += "The script should always be in English, but include Hindi words as appropriate.\n"

    if tone and tone in TONE_STYLES:
        prompt += f"5) Tone/Style: {tone}. {TONE_STYLES[tone]}\n"

    if external_links:
        links_list = [link.strip() for link in external_links.split(",") if link.strip()]
        if links_list:
            prompt += f"6) Include or reference the following external links: {', '.join(links_list)}\n"

    # Few-shot examples
    examples = few_shot.get_filtered_posts(length, language, tag)
    if examples:
        prompt += "7) Use the writing style from the following examples:\n"
        for i, post in enumerate(examples[:2]):
            prompt += f"\nExample {i+1}:\n{post['text']}\n"

    # Custom prompt overrides/additions
    if custom_prompt and custom_prompt.strip():
        prompt += f"\n8) Additional instructions: {custom_prompt}\n"

    return prompt
