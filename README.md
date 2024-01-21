# Brainrot Plus: Inverse Digital Fentanyl

## Inspiration
Social media platforms like Instagram and TikTok have given rise to a phenomenon where the younger generation is developing shorter attention spans due to the addictive nature of entertaining but often low-quality content. This content not only consumes precious time that could be used for more productive activities but also lacks educational value. Our idea is to leverage the addictive and easy-to-consume nature of such content to make it both educational and helpful.


## What it Does
Brainrot Plus takes a piece of text, whether it's lecture notes, book chapters, or complex concepts, and utilizes AI to transform it into easy-to-understand reels. The process involves:

1. Summarizing and simplifying the information.
2. Extracting key points and generating keywords for relevant images.
3. Generating a narration script for a text-to-speech AI, broken down into scenes with voiceovers and images.
4. Using a text-to-speech model to create an AI voiceover of the script.
5. Employing a web scraper to fetch relevant images from Google using generated keywords.
6. Compiling all elements into a reel with text transitions and background gameplay footage, like Subway Surfers.

## How We Built It
### Frontend
- React + Vite
- Tailwind CSS and Shacdn UI

### Backend
- FastAPI
- OpenAI
- MoviePy

## Challenges We Ran Into
- Achieving a TikTok-like scroll UI with autoplay and pause functionality during swipe/scroll.
- Resolving Python dependencies and environment issues collaboratively as a team.
- Programmatically generating videos with non-trivial custom transitions and inconsistent image formats.
- Obtaining relevant images related to the text with consistency and accuracy.

## Accomplishments We're Proud Of
Successfully generating reels dynamically and programmatically from an input passage of text.

## What We Learned
- Working with text-to-speech models.
- Programmatically generating videos using Python.
- Prompting language models for desired outputs and information.

## What's Next for Brainrot Plus
- More variations on the format, e.g. different effects, variety of gameplay footage, etc.
- Adding support for PDF and Word documents.
- Enhancing the quality of reels to make them more entertaining and engaging to watch.
