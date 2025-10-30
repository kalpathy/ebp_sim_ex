import os, streamlit as st
from openai import OpenAI
try:
    from google import genai
    HAS_GEMINI = True
except Exception:
    HAS_GEMINI = False

st.set_page_config(page_title="SimPatient", layout="wide")
st.title("SimPatient — Tele-visit Role-play")

with st.sidebar:
    st.markdown("### Model & Options")
    model = st.selectbox("Model", ["openai:gpt-4o-mini","gemini:gemini-2.5-flash"] if HAS_GEMINI else ["openai:gpt-4o-mini"])
    tight = st.checkbox("Use tighter constraints", True)
    guard = st.checkbox("Include safety guardrails", True)
    auto_turn = st.number_input("Auto-reveal turn (safety)", min_value=3, max_value=10, value=6, step=1)
    st.markdown("API keys via env: `OPENAI_API_KEY`, `GEMINI_API_KEY`.")

system_base = open("prompts/system_prompt.txt").read()
tight_txt = open("prompts/constraints_tight.txt").read()
guard_txt = open("prompts/safety_guardrails.txt").read()

# Persona selection
tabs = st.tabs(["Persona","Chat","Observer"])
with tabs[0]:
    preset = st.selectbox("Persona", ["HF exacerbation","Post-op pain & constipation","Custom"])
    if preset == "HF exacerbation":
        persona = open("personas/persona_hf.md").read()
    elif preset == "Post-op pain & constipation":
        persona = open("personas/persona_postop.md").read()
    else:
        persona = open("personas/persona_template.md").read()
    persona = st.text_area("PATIENT CARD (edit if needed)", persona, height=300)
    if st.button("Start Simulation / Reset", key="reset"):
        st.session_state.chat = []
        st.session_state.turn = 0
        st.success("Simulation reset. Go to the Chat tab.")

def build_instructions():
    s = system_base.replace("{AUTO_REVEAL_TURN}", str(auto_turn))
    if tight: s += "\n\n" + tight_txt.replace("{AUTO_REVEAL_TURN}", str(auto_turn))
    if guard: s += "\n\n" + guard_txt
    return s

def call_openai(instructions, transcript, nurse_input, persona):
    c = OpenAI()
    prompt = f\"\"\"PATIENT CARD:
{persona}

CONVERSATION SO FAR:
{transcript}

Nurse: {nurse_input}
Patient:\"\"\"
    r = c.responses.create(model="gpt-4o-mini",
                           instructions=instructions, input=prompt)
    return r.output_text.strip()

def call_gemini(instructions, transcript, nurse_input, persona):
    client = genai.Client()
    prompt = f\"\"\"{instructions}

PATIENT CARD:
{persona}

CONVERSATION SO FAR:
{transcript}

Nurse: {nurse_input}
Patient:\"\"\"
    r = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return r.text.strip()

with tabs[1]:
    st.markdown("**Chat**")
    if "chat" not in st.session_state: st.session_state.chat = []
    if "turn" not in st.session_state: st.session_state.turn = 0
    nurse_input = st.text_input("Nurse:", "")
    send = st.button("Send")
    transcript = ""
    for role, text in st.session_state.chat:
        st.markdown(f"**{role}:** {text}")
        transcript += f\"{role}: {text}\n\"
    if send and nurse_input.strip():
        st.session_state.turn += 1
        st.session_state.chat.append(("Nurse", nurse_input))
        instructions = build_instructions()
        persona_cur = persona  # from Persona tab
        try:
            if model.startswith("openai"):
                reply = call_openai(instructions, transcript, nurse_input, persona_cur)
            else:
                reply = call_gemini(instructions, transcript, nurse_input, persona_cur)
        except Exception as e:
            reply = f"[Model error: {e}]"
        st.session_state.chat.append(("Patient", reply))
        st.experimental_rerun()

with tabs[2]:
    st.markdown("**Observer rubric (quick score 1–3)**")
    st.markdown(open("facilitator/observer_rubric.md").read())
    if st.session_state.get("chat"):
        if st.button("Export transcript (.txt)"):
            txt = "\n".join([f"{r}: {t}" for r,t in st.session_state.chat])
            st.download_button("Download", txt, file_name="transcript.txt")
