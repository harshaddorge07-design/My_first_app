# AI Travel Assistant

A Streamlit app that uses Google Gemini to create personalized travel suggestions from a destination, trip length, budget, traveler type, interests, and preferred transportation.

## Features

- Collects trip preferences through a simple Streamlit form.
- Generates bullet-point travel recommendations with Gemini.
- Supports budget, moderate, and luxury travel styles.
- Supports solo, couple, family, and group trips.
- Lets travelers select interests and transportation options.
- Displays a travel-themed loading animation while the recommendation is generated.

## Requirements

- Python 3.10 or newer
- A Google Gemini API key

## Setup

1. Clone or download this repository and open its directory.
2. Create and activate a virtual environment:

	```powershell
	python -m venv .venv
	.\.venv\Scripts\Activate.ps1
	```

3. Install the required packages:

	```powershell
	pip install streamlit google-genai python-dotenv
	```

4. Create a `.env` file in the project root:

	```text
	GEMINI_API_KEY=your_api_key_here
	```

	Keep this file private. It is excluded from Git by `.gitignore`.

## Run the app

```powershell
streamlit run main.py
```

Streamlit will display a local URL, usually `http://localhost:8501`. Open it in a browser and complete the trip form.

## How to use it

1. Enter the destination.
2. Choose the number of days, budget, and traveler type.
3. Select interests and preferred transportation.
4. Click **Plan trip**.
5. Review the generated travel suggestions.

## Project structure

```text
travel_assistant/
|-- main.py       # Streamlit interface and Gemini request
|-- README.md     # Project documentation
|-- .gitignore    # Keeps local environment secrets out of Git
```

## Troubleshooting

- **Missing API key:** Confirm that `.env` exists in the same directory as `main.py` and contains `GEMINI_API_KEY`.
- **Command not found:** Activate the virtual environment before running `streamlit`.
- **API errors:** Check that the Gemini API key is valid and that the selected Gemini model is available for your account.

## Security

Never commit API keys or other secrets to the repository. Rotate the key immediately if it is exposed.

