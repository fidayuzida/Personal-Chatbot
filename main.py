from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
from dotenv import load_dotenv
import os
import re

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
app = FastAPI()

# =========================
# LOAD KNOWLEDGE
# =========================
def load_knowledge():
    with open("data.txt", "r") as f:
        return f.read()

KNOWLEDGE = load_knowledge()

# =========================
# SECTION-BASED CHUNKING
# =========================
def build_sections(knowledge):
    parts = re.split(r"={4,}\n(.+?)\n={4,}", knowledge)
    sections = {}
    for i in range(1, len(parts) - 1, 2):
        title = parts[i].strip()
        content = parts[i + 1].strip()
        sections[title] = content
    return sections

SECTIONS = build_sections(KNOWLEDGE)

TOPIC_MAP = {
    "identitas":   ["IDENTITAS & POSISI TERKINI"],
    "pendidikan":  ["PENDIDIKAN"],
    "pengalaman":  ["PENGALAMAN MAGANG", "PENGALAMAN PART-TIME"],
    "magang":      ["PENGALAMAN MAGANG"],
    "parttime":    ["PENGALAMAN PART-TIME"],
    "organisasi":  ["PENGALAMAN ORGANISASI"],
    "skill":       ["SKILLS & SERTIFIKASI"],
    "sertifikasi": ["SKILLS & SERTIFIKASI"],
    "portfolio":   ["PORTFOLIO & LINK PROYEK"],
    "publikasi":   ["PUBLIKASI"],
    "motivasi":    ["MOTIVASI & MINAT", "KEPRIBADIAN & CARA KERJA", "GOALS & PREFERENSI KARIR"],
    "kepribadian": ["KEPRIBADIAN & CARA KERJA"],
    "goals":       ["GOALS & PREFERENSI KARIR"],
    "kontak":      ["IDENTITAS & POSISI TERKINI"],
    "aktivitas":   ["AKTIVITAS SELAMA KULIAH"],
    "faq":         ["FAQ (PERTANYAAN UMUM)"],
}
KEYWORD_TOPIC = {
    "siapa":        "identitas",
    "profil":       "identitas",
    "perkenalan":   "identitas",
    "tentang":      "identitas",
    "diri":         "identitas",
    "who":          "identitas",
    "kuliah":       "pendidikan",
    "pendidikan":   "pendidikan",
    "universitas":  "pendidikan",
    "telkom":       "pendidikan",
    "ipk":          "pendidikan",
    "jurusan":      "pendidikan",
    "lulus":        "pendidikan",
    "s1":           "pendidikan",
    "s2":           "pendidikan",
    "d3":           "pendidikan",
    "lulusan":      "pendidikan",
    "magang":       "magang",
    "internship":   "magang",
    "intern":       "magang",
    "part-time":    "parttime",
    "parttime":     "parttime",
    "part time":    "parttime",
    "asisten":      "parttime",
    "assistant":    "parttime",
    "laboratorium": "parttime",
    "pengalaman":   "pengalaman",
    "kerja":        "pengalaman",
    "magang":       "pengalaman",
    "internship":   "pengalaman",
    "perusahaan":   "pengalaman",
    "posisi":       "pengalaman",
    "karir":        "pengalaman",
    "pernah":       "pengalaman",
    "organisasi":   "organisasi",
    "himpunan":     "organisasi",
    "bendahara":    "organisasi",
    "treasurer":    "organisasi",
    "skill":        "skill",
    "kemampuan":    "skill",
    "bisa":         "skill",
    "keahlian":     "skill",
    "teknologi":    "skill",
    "tools":        "skill",
    "aplikasi":     "skill",
    "software":     "skill",
    "platform":     "skill",
    "programming":  "skill",
    "bahasa":       "skill",
    "cisco":        "skill",
    "packet tracer":"skill",
    "grafana":      "skill",
    "flask":        "skill",
    "esp32":        "skill",
    "mikrotik":     "skill",
    "fluent":       "skill",
    "opensearch":   "skill",
    "whmcs":        "skill",
    "cpanel":       "skill",
    "cyberpanel":   "skill",
    "firebase":     "skill",
    "easyeda":      "skill",
    "autocad":      "skill",
    "python":       "skill",
    "linux":        "skill",
    "ubuntu":       "skill",
    "sql":          "skill",
    "dns":          "skill",
    "ssl":          "skill",
    "mqtt":         "skill",
    "http":         "skill",
    "pcb":          "skill",
    "sensor":       "skill",
    "random forest":"skill",
    "aws":          "skill",
    "machine learning": "skill",
    "deep learning":"skill",
    "networking":   "skill",
    "jaringan":     "skill",
    "sertifikat":   "sertifikasi",
    "certification":"sertifikasi",
    "ccna":         "sertifikasi",
    "aws":          "sertifikasi",
    "cpanel":       "sertifikasi",
    "portfolio":    "portfolio",
    "portofolio":   "portfolio",
    "proyek":       "portfolio",
    "project":      "portfolio",
    "github":       "portfolio",
    "youtube":      "portfolio",
    "karya":        "portfolio",
    "publikasi":    "publikasi",
    "jurnal":       "publikasi",
    "paper":        "publikasi",
    "penelitian":   "publikasi",
    "publish":      "publikasi",
    "motivasi":     "motivasi",
    "tertarik":     "motivasi",
    "kenapa":       "motivasi",
    "alasan":       "motivasi",
    "passion":      "motivasi",
    "kepribadian":  "kepribadian",
    "kelebihan":    "kepribadian",
    "kelemahan":    "kepribadian",
    "strength":     "kepribadian",
    "weakness":     "kepribadian",
    "cara kerja":   "kepribadian",
    "goals":        "goals",
    "tujuan":       "goals",
    "rencana":      "goals",
    "masa depan":   "goals",
    "target":       "goals",
    "kontak":       "kontak",
    "hubungi":      "kontak",
    "email":        "kontak",
    "linkedin":     "kontak",
    "nomor":        "kontak",
    "hp":           "kontak",
    "aktivitas":    "aktivitas",
    "kegiatan":     "aktivitas",
    "selama kuliah":"aktivitas",
    "semasa kuliah":"aktivitas",
    "waktu kuliah": "aktivitas",
    "gaji":         "faq",
    "salary":       "faq",
    "ekspektasi":   "faq",
    "bayaran":      "faq",
    "gabung":       "faq",
    "join":         "faq",
    "available":    "faq",
    "mulai":        "faq",
    "kapan":        "faq",
    "cocok":        "faq",
    "berbeda":      "faq",
    "tantangan":    "faq",
}
# =========================
# 🔥 PARSE PORTFOLIO ITEMS
# =========================
def parse_portfolio_items(text):
    items = []
    current = {}

    lines = text.split("\n")

    for line in lines:
        line = line.strip()

        if re.match(r"\[\d+\]", line):
            if current:
                items.append(current)
            current = {"title": line, "content": ""}

        elif current:
            current["content"] += line + "\n"

    if current:
        items.append(current)

    return items


# =========================
# 🔥 SIMPLE SCORING
# =========================
def score_item(query, item):
    q = query.lower()
    text = (item["title"] + " " + item["content"]).lower()

    score = 0
    for word in q.split():
        if word in text:
            score += 1

    return score


# =========================
# 🔥 EXACT RETRIEVAL
# =========================
def retrieve_portfolio_exact(query):
    portfolio_text = SECTIONS.get("PORTFOLIO & LINK PROYEK", "")
    items = parse_portfolio_items(portfolio_text)

    scored = [(score_item(query, item), item) for item in items]
    scored.sort(reverse=True, key=lambda x: x[0])

    top_items = [item for score, item in scored if score > 0]

    if not top_items:
        return portfolio_text

    result = []
    for item in top_items:
        result.append(item["title"] + "\n" + item["content"])

    return "\n\n".join(result)

def detect_special_intent(query):
    q = query.lower()
    if "pernah" in q and ("google" in q or "amazon" in q or "meta" in q):
        return "external_experience"
    if "kapan" in q and ("mulai" in q or "gabung" in q):
        return "availability"
    return None

def is_choice_question(query):
    return " atau " in query.lower()

def detect_topics(query):
    query_lower = query.lower()
    matched = set()
    for keyword, topic in KEYWORD_TOPIC.items():
        if keyword in query_lower:
            matched.add(topic)
    return list(matched)

def retrieve_context(query):
    q = query.lower()

    # 🔥 FORCE pendidikan (TARUH PALING ATAS)
    if any(x in q for x in ["s1", "s2", "d3", "lulusan", "kuliah"]):
        return SECTIONS.get("PENDIDIKAN", "")

    special = detect_special_intent(query)

    # =========================
    # 🔥 SPECIAL INTENT HANDLING
    # =========================

    if special == "external_experience":
        return (
            SECTIONS.get("PENGALAMAN MAGANG", "")
            + "\n\n" +
            SECTIONS.get("PENGALAMAN PART-TIME", "")
        )

    if special == "availability":
        return SECTIONS.get("FAQ (PERTANYAAN UMUM)", "")

    # =========================
    # 🔥 NORMAL TOPIC FLOW
    # =========================
    topics = detect_topics(query)

    if "portfolio" in topics:
        return retrieve_portfolio_exact(query)

    if not topics or "identitas" in topics:
        return KNOWLEDGE

    relevant = []
    seen = set()

    for t in topics:
        for sec in TOPIC_MAP.get(t, []):
            if sec not in seen and sec in SECTIONS:
                relevant.append(f"=== {sec} ===\n{SECTIONS[sec]}")
                seen.add(sec)

    return "\n\n".join(relevant) if relevant else KNOWLEDGE


def load_prompt():
    with open("prompt.txt", "r") as f:
        return f.read()

BASE_SYSTEM_PROMPT = load_prompt()

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("index.html", "r") as f:
        return f.read()

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    user_input = body.get("message", "").strip()
    history = body.get("history", [])

    greetings = ["halo", "hai", "hi", "hello", "hey", "p", "hei"]
    if user_input.lower() in greetings:
        return JSONResponse({"reply": "halo! ada yang bisa aku bantu? 😄"})

    context = retrieve_context(user_input)
    BASE_SYSTEM_PROMPT = load_prompt()
    dynamic_system = (
        BASE_SYSTEM_PROMPT
        + "\n\n==============================\n"
        + "DATA TENTANG FIDA (gunakan HANYA ini untuk menjawab):\n"
        + "==============================\n"
        + context
    )

    MAX_HISTORY = 8
    messages_to_send = (
        [{"role": "system", "content": dynamic_system}]
        + history[-MAX_HISTORY:]
        + [{"role": "user", "content": user_input}]
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages_to_send,
        temperature=0.3,
        max_tokens=700
    )
    reply = response.choices[0].message.content
    return JSONResponse({"reply": reply})
