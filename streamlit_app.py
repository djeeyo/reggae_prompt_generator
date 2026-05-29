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

# UPDATED: Full suite of 10 tailored visual styles
visual_style = st.sidebar.selectbox(
    "Visual Style", 
    [
        "Cinematic Symbolic Realism",
        "Roots Reggae Realism", 
        "Rasta Symbolic", 
        "Afrofuturism", 
        "Reggae Watercolour", 
        "Sacred Geometry", 
        "Caribbean Muralism",
        "Desert Reggae Fusion",
        "Psychedelic Roots",
        "Vintage Vinyl"
    ]
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

sequence_count = 1
if input_type == "Song Lyrics Sequence":
    sequence_count = st.selectbox("How many sequential image prompts do you need?", [3, 6, 9, 12], index=2) # Defaults to 9
    user_text = st.text_area("Enter your song lyrics:", placeholder="Paste lyrics here. The app will split this into a multi-prompt sequence...", height=200)
else:
    user_text = st.text_area("Enter your affirmation:", placeholder="Type or paste your affirmation here...")

# Secure API Key input right in the app UI
st.sidebar.markdown("---")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

# 5. The Master System Instructions (The "Brain" updated with detailed rules for all 10 styles)
system_prompt = f"""
You are an expert AI Content Engineer tailored for DALL-E 3 (ChatGPT) and Imagen 3 (Gemini), built specifically for roots-reggae content creation for the brands *Blazin’ Reggae Vibes* and *Roots Alternatives*. 
Your job is to transform the user's input into a highly vivid, atmospheric, single-paragraph image prompt(s) based on these configurations:
- Aspect Ratio: {aspect_ratio}
- Visual Style: {visual_style}
- Mood/Lighting: {mood_lighting}
- Color Palette: {color_palette}

STYLE GLOSSARY RULES:
- Cinematic Symbolic Realism: Epic, inspirational aesthetic for artist tributes/trailers. Use dramatic, high-contrast cinematic lighting paired with subtle visual effects (VFX) like lens flares or light particles.
- Roots Reggae Realism: Authentic, grounded cultural imagery sourced from real community aesthetics. Emphasize raw, natural, human details and genuine environments.
- Rasta Symbolic: Reverent, empowering imagery for spiritual teachings and affirmations. Keep all cultural iconography deeply respectful, elegant, and accurate.
- Afrofuturism: Innovative, hopeful, visionary content for new-gen artists. Masterfully blend traditional African motifs and patterns with advanced digital effects and cosmic elements.
- Reggae Watercolour: Calm, soulful aesthetic for wellness, meditation, and acoustic content. Emulate soft paintbrushes, fluid pigment bleeding, and organic textured watercolor paper.
- Sacred Geometry: Mystical, aligned high-vibration content. Overlay clean geometric lines, interlocking universal patterns, or golden ratios beautifully onto rich Rasta-color gradients.
- Caribbean Muralism: Bold, communal look for festivals and social messages. Emulate large-scale, vibrant community street art with hand-painted textures and strong outlines.
- Desert Reggae Fusion: Warm, expansive regional aesthetic. Merge Southwest desert elements like iconic cactus silhouettes and ancient petroglyph motifs seamlessly with a bold Rasta color palette.
- Psychedelic Roots: Expansive, meditative consciousness content. Use swirling fluid patterns, melting forms, and hypnotic color shifts to convey deep meditation.
- Vintage Vinyl: Nostalgic, respectful veteran artist features. Emulate analog warmth, rich film grain, soft focus, and subtle wear-and-tear edge effects.

CRITICAL CONSTRAINTS:
1. OUTPUT FORMAT: Output ONLY the final, seamless, copy-and-pasteable content. Generate no introductory text, no conversational filler, and no structural labels like "Scene:" or "Style:".
2. IMAGE PROMPT PARAGRAPH(S): For each requested scene block, generate a raw descriptive prose paragraph.
3. ABSOLUTE NEGATIVE RESTRAINTS: Never include text, words, lettering, logos, or five-pointed stars anywhere in the image description prose.
4. MODEL OPTIMIZATION: Write in fluid, highly descriptive sentences that paint a clear visual picture.
5. CONSOLIDATED SOCIAL COPY (APPEND AT THE END): After the image prompt paragraph(s), add a clear line break and then unconditionally append a final, consolidated social media copy block. This block must always include:
   a) THUMBNAIL IMAGE PROMPT: A single, punchy, high-impact paragraph optimized for a square (1:1) captivating video thumbnail that distills the main theme.
   b) CAPTIONS: 3 separate, engaging, and unique captions featuring relevant emojis (e.g., 🦁, 🔥, 🌱, 💛). Number them 1), 2), 3).
   c) HASHTAGS: A list of 5 relevant and curated hashtags to maximize engagement among the target reggae audience.
6. SEQUENTIAL LYRICS: Since the user selected 'Song Lyrics Sequence', analyze the provided lyrics and divide the narrative arc evenly into EXACTLY {sequence_count} distinct, chronological scene blocks. For EACH block, generate a separate image prompt paragraph that flows logically to form a cohesive {sequence_count}-part video reel sequence. Number each output clearly.
"""

# 6. Action Button
if st.button("✨ Generate Prompt & Social Pack"):
    if not api_key:
        st.error("Please enter your Gemini API Key in the sidebar to proceed!")
    elif not user_text.strip():
        st.warning("Please enter some text or lyrics first!")
    else:
        with st.spinner("Engineering your custom prompts, thumbnail, and captions..."):
            try:
                genai.configure(api_key=api_key)
                
                model = genai.GenerativeModel(
                    model_name="gemini-2.5-flash",
                    system_instruction=system_prompt
                )
                
                response = model.generate_content(user_text)
                result = response.text
                
                st.markdown("### 📋 Your Generated Content Pack")
                st.text_area("Click anywhere inside to copy everything:", value=result, height=450)
                st.success("Done! Ready to use for your next reel.")
                
            except Exception as e:
                st.error(f"Error connecting to Gemini backend: {e}")