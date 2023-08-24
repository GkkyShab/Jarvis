import openai
import speech_recognition as sr
import pyttsx3

openai.api_key = "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"


engine = pyttsx3.init()


while True:
    
    r = sr.Recognizer()

   
    with sr.Microphone() as source:
        print("Speak now:")
        audio = r.listen(source)

    
    try:
        prompt = r.recognize_google(audio, language="en-EN", show_all=False)
        print("You asked:", prompt)

       
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=300
        )

       
        response_text = str(response['choices'][0]['text']).strip('\n\n')
        print(response_text)

        
        engine.say(response_text)
        engine.runAndWait()
        print()

    
    except:
        response_text = "Sorry, I didn't get that!"
        print(response_text)
        engine.say(response_text)
        engine.runAndWait()
        print()