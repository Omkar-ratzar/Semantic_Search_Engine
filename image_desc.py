import ollama
from log import logger
from config import config
def extract_image(path):

    response = ollama.chat(
    model= config["model"]["image_llm"],
    options={
        "temperature": config["llm"]["temperature"],
        "top_p": config["llm"]["top_p"]
    },

    messages=[
        {
            'role': 'user',
            'content': """
            You are an image description system for embedding generation.

            Your goal is to produce a structured, consistent, and deterministic description of the image.

            Rules:
            - Be strictly objective and literal.
            - Do NOT add imagination, emotion, or backstory.
            - Use simple, consistent wording.
            - Maintain exact section names and order.
            - If information is missing, write "none".
            - Keep outputs concise and uniform across images.

            Output format (STRICT):

            [SCENE TYPE]: <indoor/outdoor/unknown>

            [PRIMARY SUBJECTS]: <comma-separated main objects or people>

            [SECONDARY OBJECTS]: <comma-separated additional visible items or "none">

            [ACTIONS]: <simple present tense action or "none">

            [ENVIRONMENT]: <setting such as room, street, nature, or "unknown">

            [VISUAL ATTRIBUTES]:
            - colors: <dominant colors>
            - lighting: <bright/dim/natural/artificial/unknown>
            - perspective: <close-up/wide shot/aerial/eye-level/unknown>

            [TEXT IN IMAGE]: <visible text or "none">

            [COUNTABLE ELEMENTS]:
            - people: <number or 0>
            - animals: <number or 0>
            - vehicles: <number or 0>

            [STYLE]: <photo/illustration/cartoon/render/unknown>

            [QUALITY]: <low/medium/high, sharp/blurry>

            Do not include any explanation or extra text.
        """,
            'images': [path]
        }])
    logger.info("Image described:"+path)
    return(response['message']['content'])

# print(extract_image("C:\\Users\\Fylakas\\Pictures\\test.jpg"))
