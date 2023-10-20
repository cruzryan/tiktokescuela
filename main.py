import os
import pytesseract
from PIL import Image
import markdown
import webbrowser


import openai 


def easy():
    # Ingresa tu key de OpenAI!
    openai.api_key = ''

    # Tus imagenes van en este directorio!
    image_directory = "./images"

    output_directory = "./mid"
    output_filename = "text.txt"
    output_path = os.path.join(output_directory, output_filename)

    os.makedirs(output_directory, exist_ok=True)

    all_text = ""

    for filename in os.listdir(image_directory):
        if filename.endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
            image_path = os.path.join(image_directory, filename)
            try:
                image = Image.open(image_path)

                text = pytesseract.image_to_string(image)

                all_text += text + "\n"

            except Exception as e:
                print(f"Error processing {filename}: {e}")

    with open(output_path, "w", encoding="utf-8") as text_file:
        text_file.write(all_text)

    print(f"OCR text saved to {output_path}")

    messages = [ {"role": "system", "content": "You are a intelligent assistant."} ]

    message = "Genera una guia de estudio en markdown para el siguiente texto: " + all_text 
    if message: 
        messages.append( 
            {"role": "user", "content": message}, 
        ) 
        chat = openai.ChatCompletion.create( 
            model="gpt-3.5-turbo", messages=messages 
        ) 

    reply = chat.choices[0].message.content 
    print(f"ChatGPT: {reply}") 

    print("Mostrando Markdown")


    html_content = markdown.markdown(reply)

    with open("./out/temp.html", "w") as f:
        f.write(html_content)

    webbrowser.open("./out/temp.html")


easy()