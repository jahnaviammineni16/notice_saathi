# Notice Saathi

Upload a photo of any public notice, form or poster. Notice Saathi reads it, checks it for scam red flags, checks whether you are eligible, and gives you a clear action plan.

Built for Hacktoberfest Hack Day Bengaluru '26, Track 1: Best Use of Gemma 4, PS 01: Multimodal Community Intelligence.

## The problem
Scholarship, scheme, job, civic and health notices are long, confusing and often in Kannada or Hindi. People miss deadlines, misread eligibility rules, or fall for fake notices.

## What it does
1. Reads the notice from a photo and detects its type (scholarship, government scheme, job, civic notice, health, form).
2. Scam Shield looks for red flags such as fee demands, OTP or bank detail requests, personal contact details and urgency pressure.
3. Asks eligibility questions that fit that notice, then gives a verdict (likely eligible, likely not eligible, unsure) with the reason.
4. Document readiness meter shows which documents you have and which are missing.
5. Action checklist with the next steps.
6. Calendar reminder downloads the deadline as a .ics file with alerts 3 days and 1 day before.
7. Read aloud and WhatsApp share in English, Kannada or Hindi.

## How Gemma 4 is used
Gemma 4 is the core of the app. It reads the notice image, extracts the rules, deadline and documents, judges scam red flags, asks eligibility questions, and writes the verdict, checklist and share message in the chosen language. We use the model gemma-4-31b-it through the Gemini API. Gemma 4 is an open-weight model.

## Run it yourself
1. Install Python 3.10 or newer.
2. Download this repo and open the folder.
3. Install the dependencies: `pip install -r requirements.txt`
4. Get a free API key from Google AI Studio and create a file named `.env` in the project folder with this line: `GEMINI_API_KEY=your_key_here`
5. Start the app: `python -m streamlit run app.py`

## Tech used
Python, Streamlit, Google GenAI SDK (google-genai), python-dotenv, and Gemma 4.

## Limitations
- Results depend on photo quality. Blurry or incomplete notices are flagged as unclear.
- The AI can be wrong. Scam Shield is an estimate, not proof.
- It does not check live scholarship or government databases.
- The app does not store uploaded photos. They are sent to the Gemini API to be read.
- Always confirm details with the official office before paying, applying or sharing personal information.
- This is a prototype built during one Hack Day.

## Team
[jahnavi ammineni] and [hacknova]

## License
MIT
