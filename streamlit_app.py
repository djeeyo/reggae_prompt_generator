import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="Reggae Prompt Generator", page_icon="🎵", layout="centered")

# 2. App Title & Intro
st.title("🎵 Reggae Image Prompt Generator")
st.markdown("Streamline your creative workflow for *Blazin' Reggae Vibes* and *Roots Alternatives*.")
st.markdown("---")

# 3. Sidebar Configuration
st.sidebar.header("🎨 Prompt Settings")

aspect_ratio = st.sidebar.selectbox(
    "Aspect Ratio", 
    ["9:16", "4:5", "16:9", "1:1"]
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

# 4. Main Input Fields
input_type = st.radio("Input Type", ["Single Affirmation", "Song Lyrics Sequence"])

if input_type == "Single Affirmation":
    user_text = st.text_area("Enter your affirmation:", placeholder="Type or paste your affirmation here...")
else:
    user_text = st.text_area("Enter your song lyrics:", placeholder="Paste lyrics here. The app will split this into a multi-prompt sequence...", height=200)

# Secure API Key input right in the app UI for convenience
st.sidebar.markdown("---")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

# 5. The Master System Instructions
system_prompt = f"""
You are an expert AI Image Prompt Generator built specifically for roots-reggae content creation, tailored perfectly for DALL-E 3 (ChatGPT) and Imagen 3 (Gemini). 
Your job is to transform the user's input into a highly vivid, atmospheric, single-paragraph image prompt based on these configurations:
- Aspect Ratio: {aspect_ratio}
- Visual Style: {visual_style}
- Mood/Lighting: {mood_lighting}
- Color Palette: {color_palette}

CRITICAL CONSTRAINTS:
1. OUTPUT FORMAT: Output ONLY the final, seamless, copy-and-pasteable paragraph for the image prompt. No introductory text, no conversational filler, and no structural labels like "Scene:" or "Style:". Just the raw descriptive prose.
2. ABSOLUTE NEGATIVE RESTRAINTS: Never include text, words, lettering, logos, or five-pointed stars anywhere in the scene description.
3. MODEL OPTIMIZATION: Write in fluid, highly descriptive sentences that paint a clear visual picture.
4. SEQUENTIAL LYRICS: If the user selected 'Song Lyrics Sequence', break the lyrics down chronologically into separate logical scene blocks (e.g., matching a 6 or 9 prompt layout for a full video sequence). For EACH block, generate a distinct, standalone image prompt paragraph that flows narrative-wise from the last. Number them clearly: 'Prompt 1:', 'Prompt 2:', etc.
"""

# 6. Action Button
if st.button("✨ Generate Prompt"):
    if not api_key:
        st.error("Please enter your Gemini API Key in the sidebar to proceed!")
    elif not user_text.strip():
        st.warning("Please enter some text or lyrics first!")
    else:
        with st.spinner("Engineering your custom prompt using Gemini..."):
            try:
                # Configure the Gemini API
                genai.configure(api_key=api_key)
                
                # UPDATED: Using the active stable 2.5 production model
                model = genai.GenerativeModel(
                    model_name="gemini-2.5-flash",
                    system_instruction=system_prompt
                )
                
                # Generate content
                response = model.generate_content(user_text)
                result = response.text
                
                # Display the result in a clean copy-paste box
                st.markdown("### 📋 Your Generated Prompt")
                st.text_area("Click anywhere inside to copy:", value=result, height=300)
                st.success("Done! Ready to paste into ChatGPT or Gemini.")
                
            except Exception as e:
                st.error(f"Error connecting to Gemini backend: {e}")