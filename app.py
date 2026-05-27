import streamlit as st
from openai import OpenAI

# 1. Page Configuration
st.set_page_config(page_title="Reggae Prompt Generator", page_icon="🎵", layout="centered")

# 2. App Title & Intro
st.title("🎵 Reggae Image Prompt Generator")
st.markdown("Streamline your creative workflow for *Blazin' Reggae Vibes* and *Roots Alternatives*.")
st.markdown("---")

# 3. Sidebar Configuration (Your Dropdowns)
st.sidebar.header("🎨 Prompt Settings")

aspect_ratio = st.sidebar.selectbox(
    "Aspect Ratio", 
    ["9:16 (Reels/Shorts)", "4:5 (Instagram)", "16:9 (Landscape)", "1:1 (Square)"]
)

visual_style = st.sidebar.selectbox(
    "Visual Style", 
    ["Roots reggae realism", "Rasta symbolic", "Afrofuturism", "Reggae watercolour", "Sacred geometry", "Caribbean muralism"]
)

mood_lighting = st.sidebar.selectbox(
    "Mood / Lighting", 
    ["Golden hour", "Dawn breaking", "Cosmic night", "Lush midday", "Mystical fog"]
)

color_palette = st.sidebar.selectbox(
    "Colour Palette", 
    ["Red, gold & green", "Earth tones", "Ocean & sky", "Fire & amber", "Midnight indigo"]
)

# 4. Main Main Input Fields
input_type = st.radio("Input Type", ["Single Affirmation", "Song Lyrics Sequence"])

if input_type == "Single Affirmation":
    user_text = st.text_area("Enter your affirmation:", placeholder="Type or paste your affirmation here...")
else:
    user_text = st.text_area("Enter your song lyrics:", placeholder="Paste lyrics here. The app will generate a sequential narrative layout...", height=200)

# 5. The Master System Instructions (The "Brain")
system_prompt = f"""
You are an expert AI Image Prompt Generator tailored for DALL-E 3 (ChatGPT) and Imagen 3 (Gemini). 
Your job is to transform the user's input into a highly vivid, atmospheric, single-paragraph image prompt based on these configurations:
- Aspect Ratio: {aspect_ratio}
- Visual Style: {visual_style}
- Mood/Lighting: {mood_lighting}
- Color Palette: {color_palette}

CRITICAL CONSTRAINTS:
1. OUTPUT FORMAT: Output ONLY the final, seamless, copy-and-pasteable paragraph for the image prompt. No introductory text, no labels like "Scene:" or "Style:". Just the prose.
2. ABSOLUTE NEGATIVE RESTRAINTS: Never include text, words, lettering, logos, or five-pointed stars anywhere in the scene description.
3. If the user selected 'Song Lyrics Sequence', break the lyrics down chronologically into separate concept blocks. For EACH block, generate a distinct, standalone image prompt paragraph that flows logically. Number them clearly: 'Prompt 1:', 'Prompt 2:', etc.
"""

# 6. Action Button
if st.button("✨ Generate Prompt"):
    if not user_text.strip():
        st.warning("Please enter some text or lyrics first!")
    else:
        with st.spinner("Engineering your custom prompt..."):
            try:
                # Setup your OpenAI client (Assumes API key is set in environment or Streamlit secrets)
                # If using Gemini's API instead, this section can easily switch to the Google GenerativeAI SDK
                client = OpenAI()
                
                response = client.chat.completions.create(
                    model="gpt-4o", # Or your preferred fast text model
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_text}
                    ],
                    temperature=0.7
                )
                
                result = response.choices[0].message.content
                
                # Display the result in a clean copy-paste box
                st.markdown("### 📋 Your Generated Prompt")
                st.text_area("Click anywhere inside to copy:", value=result, height=250)
                st.success("Done! Ready to paste into ChatGPT or Gemini.")
                
            except Exception as e:
                st.error(f"Error connecting to AI backend: {e}")
                st.info("Tip: Make sure you have your API key configured.")