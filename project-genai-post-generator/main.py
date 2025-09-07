import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post

length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish"]
tone_options = [
    "Professional & Informative",
    "Conversational & Relatable",
    "Inspirational & Motivational",
    "Thought-Provoking & Opinionated",
    "Storytelling & Narrative-Driven",
    "Educational / Value-Driven",
    "Humble & Authentic",
    "Celebratory & Appreciative"
]
format_options = ["Paragraph", "Bullet Points", "Essay"]

def main():
    st.subheader("LinkedIn Post Generator 🚀")
    fs = FewShotPosts()
    tags = fs.get_tags()

    # Session state to store post
    if 'post' not in st.session_state:
        st.session_state['post'] = ""

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        selected_tag = st.selectbox("Topic", options=tags)
    with col2:
        selected_length = st.selectbox("Length", options=length_options)
    with col3:
        selected_language = st.selectbox("Language", options=language_options)
    with col4:
        selected_tone = st.selectbox("Tone/Style", options=tone_options)

    selected_format = st.selectbox("Output Format", options=format_options)
    external_links = st.text_input("External links (comma-separated)")
    custom_prompt = st.text_area("Custom Prompt / Instructions (Optional)")

    # Generate initial post
    if st.button("Generate Post"):
        st.session_state['post'] = generate_post(
            length=selected_length,
            language=selected_language,
            tag=selected_tag,
            tone=selected_tone,
            output_format=selected_format,
            external_links=external_links,
            custom_prompt=custom_prompt
        )
    if st.session_state['post']:
        st.markdown("### Generated Post:")
        st.write(st.session_state['post'])

    # Rewrite section
    rewrite_prompt = st.text_area("Rewrite Instructions (Optional)", placeholder="Make it more persuasive, add examples, etc.")
    if st.button("Rewrite Post") and st.session_state['post']:
        if rewrite_prompt.strip():
            st.session_state['post'] = generate_post(
                length=selected_length,
                language=selected_language,
                tag=selected_tag,
                tone=selected_tone,
                output_format=selected_format,
                external_links=external_links,
                custom_prompt=rewrite_prompt
            )
            st.markdown("### Rewritten Post:")
            st.write(st.session_state['post'])

if __name__ == "__main__":
    main()
