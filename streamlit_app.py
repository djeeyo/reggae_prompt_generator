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
    [
        "Golden Hour",
        "Dawn Breaking",
        "Cosmic Night",
        "Lush Midday",
        "Mystical Fog",
        "Nyabinghi Firelight",
        "Desert Twilight",
        "Rainy Season Glow",
        "Neon Dub Glow",
        "Incense Smoke Diffusion",
        "Eclipse Twilight"
    ]
)

# UPDATED: 15 Master-crafted thematic color palettes with specific hex profiles
color_palette = st.sidebar.selectbox(
    "Colour Palette", 
    [
        "Zion Radiance (#D4A017, #A0522D, #FFF8E1)",
        "New Zion (#FFB6C1, #FFCC99, #E6E6FA)",
        "Celestial Zion (#1A0033, #6A0DAD, #C0C0C0)",
        "Tropical Roots (#006400, #C41E3A, #FFD700)",
        "Veil of Wisdom (#C0C0C0, #9CAF88, #B19CD9)",
        "Sacred Flame (#CC5500, #8B0000, #FFBF00)",
        "Reggae del Norte (#2E1A47, #CC7357, #30D5C8)",
        "Renewal Waters (#E8E8E8, #2F4F2F, #87CEEB)",
        "Digital Roots (#9D00FF, #39FF14, #DC143C)",
        "Sacred Herb (#E6E6FA, #F5E6D3, #9CAF88)",
        "Prophetic Threshold (#0A0A0A, #FFD700, #4B0082)",
        "Earth Medicine (#B35441, #6B8E23, #E6C9A8)",
        "Ancestral Earth (#5D4037, #CC7722, #1B4D3E)",
        "Zion Ascension (#4169E1, #E6BE8A, #F8F8FF)",
        "Southwest Fusion (#9CAF88, #30D5C8, #CC7357)",
        "High Vibration Gradient (#FF6B9D -> #4ECDC4 -> #FFD93D)"
    ]
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

# 5. The Master System Instructions (The complete visual engine)
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

MOOD & LIGHTING GLOSSARY RULES:
- Golden Hour: Warm, reverent, hopeful sunlight casting low-angle amber rays. Ensure a prominent, deeply shadowed foreground zone to allow for future text placement.
- Dawn Breaking: Optimistic, fresh, awakening atmosphere. Soft light filtering through morning mist. Establish a distinct, atmospheric misty mid-ground layer.
- Cosmic Night: Mystical, expansive, celestial vibe. Deep starry skies, cosmic nebulae, and high-vibration energy. Ensure a broad, plain, star-free zone or dark gradient background section specifically for captions.
- Lush Midday: Vibrant, energetic, authentic mood. Intense, crisp tropical sunlight creating high contrast with deep, dark, sharp-edged shadows.
- Mystical Fog: Introspective, sacred, mysterious setting. Thick, soft, swirling silver fog with a distinctly clear, high-visibility central foreground zone.
- Nyabinghi Firelight: Communal, rhythmic, spiritual atmosphere. Warm, intense, flickering firelight illuminating faces from below, with a clean ambient space directly above the flame glow.
- Desert Twilight: Expansive, grounded, regional feel. A vast Southwest horizon under a deep, smooth indigo twilight sky, creating a perfect canvas for high-contrast white or gold elements.
- Rainy Season Glow: Cleansed, renewed, highly emotional environment. Wet, shimmering landscapes, soft diffused light, and glistening surfaces that reflect color.
- Neon Dub Glow: Edgy, innovative, urban dancehall and tech-reggae vibe. Deep shadows punctuated by vibrant neon light accents, streaks, and glowing highlights that trace outlines.
- Incense Smoke Diffusion: Meditative, intentional, sacred setting. Swirling, ethereal wisps of blue and white smoke filtering through the scene, leaving a perfectly clear, smoke-free foreground zone.
- Eclipse Twilight: Prophetic, transitional, powerful cosmic milestone. A dark sky dominated by a brilliant golden solar corona ring, creating a striking natural frame around the central subject.

COLOR PALETTE EMEDDING INSTRUCTIONS:
Translate the selected palette setting into descriptive environmental features using its explicit color tones and respect the text layout zones described here:
- Zion Radiance: Dominated by rich gold (#D4A017) and warm sienna brown (#A0522D) with clean ivory accents (#FFF8E1). Intentionally craft a dark, deep shadowed foreground region.
- New Zion: Infused with soft pastel pink (#FFB6C1), warm apricot (#FFCC99), and ethereal lavender (#E6E6FA). Construct a thick, misty mid-ground layer cast in deep plum-tinted haze.
- Celestial Zion: A rich night landscape of midnight violet (#1A0033) and deep royal purple (#6A0DAD) with bright metallic silver highlights (#C0C0C0). Ensure wide, plain, star-free negative spaces in the sky.
- Tropical Roots: High-contrast mix of deep forest green (#006400), vibrant crimson red (#C41E3A), and bright selective gold (#FFD700). Create heavy, deep undergrowth shadows.
- Veil of Wisdom: Ethereal silver (#C0C0C0), muted sage green (#9CAF88), and soft pastel lilac (#B19CD9). Ensure the center configuration is entirely clear and un-obscured.
- Sacred Flame: Intense burnt orange (#CC5500), dark crimson maroon (#8B0000), and brilliant amber yellow (#FFBF00). Leave a distinct, clear open ambient space directly above any fire sources.
- Reggae del Norte: Moody deep indigo-violet (#2E1A47), warm baked terracotta (#CC7357), and a brilliant accent of bright turquoise (#30D5C8). Paint a wide, clear, seamless upper twilight sky canvas.
- Renewal Waters: Soft mist white (#E8E8E8), dark slate-forest green (#2F4F2F), and brilliant sky cerulean blue (#87CEEB). Emphasize wide, highly reflective, glistening water surfaces.
- Digital Roots: Deep electric violet (#9D00FF), radioactive neon lime green (#39FF14), and rich crimson red (#DC143C). Embed high-vibrancy light streaks and sharp outline glows against a stark backdrop.
- Sacred Herb: Ethereal lavender mist (#E6E6FA), soft warm sand cream (#F5E6D3), and organic dried sage green (#9CAF88). Maintain an un-obscured, completely clear foreground section.
- Prophetic Threshold: Infinite midnight black (#0A0A0A), brilliant golden yellow (#FFD700), and deep indigo-violet (#4B0082). Embed a clear dark center framed elegantly by a prominent circular gold ring element.
- Earth Medicine: Warm clay terracotta (#B35441), muted olive green (#6B8E23), and soft sand-beige (#E6C9A8). Craft a beautiful, natural landscape balancing warm soils and herbal flora elements.
- Ancestral Earth: Rich dark walnut brown (#5D4037), deep rustic ochre gold (#CC7722), and vintage hunter green (#1B4D3E). Use historic, deeply rooted, weathered natural textures.
- Zion Ascension: Brilliant royal blue (#4169E1), warm golden metallic wheat (#E6BE8A), and clean pearlescent white (#F8F8FF). Infuse subjects or elements with a soft, bright, radiating pearl glow.
- Southwest Fusion: Soft sage desert green (#9CAF88), striking bright turquoise (#30D5C8), and warm baked clay terracotta (#CC7357). Blend arid geology seamlessly with vibrant accents.
- High Vibration Gradient: A smooth, fluid, intentional modern sunset gradient flowing seamlessly from deep hot pink (#FF6B9D) to cool mint turquoise (#4ECDC4) and finishing in bright sunshine yellow (#FFD93D).

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
if st.button("✨