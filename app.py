# Streamlined Gradio app for Hugging Face Spaces
import os
import gradio as gr
from load_env import load_environment_variables
from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_gtts

# Load environment variables
GROQ_API_KEY = load_environment_variables()

system_prompt="""You have to act as a professional doctor, i know you are not but this is for learning purpose.
            What's in this image?. Do you find anything wrong with it medically?
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot,
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""

# Main processing function
def process_inputs(text_input, audio_filepath, image_filepath):
    # Input Validation
    audio_provided = audio_filepath is not None
    if text_input and audio_provided:
        raise gr.Error("Please provide either text input OR audio recording, not both.")
    if not text_input and not audio_provided:
         raise gr.Error("Please provide either text input OR audio recording along with the image.")
    if not image_filepath:
        raise gr.Error("Please upload an image for analysis.")

    user_query = ""
    speech_to_text_output = "" 

    if text_input:
        user_query = text_input
        speech_to_text_output = "(User provided text)"
    elif audio_provided:
        print(f"Received audio_filepath: {audio_filepath}")
        if not audio_filepath or not os.path.exists(audio_filepath):
            print(f"Audio file does not exist or path is invalid: {audio_filepath}")
            raise gr.Error(f"Internal Error: Recorded audio file not found or path invalid.")
        try:
            print("Attempting transcription...")
            speech_to_text_output = transcribe_with_groq(GROQ_API_KEY=GROQ_API_KEY,
                                                        audio_filepath=audio_filepath,
                                                        stt_model="whisper-large-v3")
            user_query = speech_to_text_output
            print(f"Transcription successful: {speech_to_text_output}")
        except Exception as e:
            print(f"Error during transcription: {e}")
            raise gr.Error(f"Error during transcription: {e}")

    # Handle the image analysis
    try:
        full_query = system_prompt + user_query
        doctor_response = analyze_image_with_query(query=full_query, 
                                                 encoded_image=encode_image(image_filepath), 
                                                 model="meta-llama/llama-4-scout-17b-16e-instruct")
    except Exception as e:
        raise gr.Error(f"Error during image analysis: {e}")

    # Generate audio response
    voice_of_doctor = None
    if doctor_response and doctor_response != "No image provided for me to analyze":
        try:
            generated_path = text_to_speech_with_gtts(input_text=doctor_response, output_filepath="final.mp3")
            if generated_path and os.path.exists(generated_path):
                 voice_of_doctor = generated_path
            else:
                print(f"Warning: TTS function did not return a valid path or file doesn't exist: {generated_path}")
        except Exception as e:
            print(f"Error during text-to-speech: {e}")

    print(f"Returning: STT='{speech_to_text_output}', Response='{doctor_response[:50]}...', Audio='{voice_of_doctor}'")
    audio_update = gr.update(value=voice_of_doctor, autoplay=True) if voice_of_doctor else gr.update(value=None)
    return speech_to_text_output, doctor_response, audio_update

# Helper functions
def clear_audio_input():
    return gr.update(value=None)

def clear_text_input():
    return gr.update(value=None)

# Create the interface
with gr.Blocks(theme=gr.themes.Base(), css="style.css") as demo:
    gr.Markdown("# Synapse Health - AI-Powered Virtual Health Assistant")
    with gr.Row():
        with gr.Column(scale=1):
            text_query = gr.Textbox(label="Type your query here (Option 1)")
            audio_query = gr.Audio(sources=["microphone"], type="filepath", label="Or record your query here (Option 2)")
            image_input = gr.Image(type="filepath", label="Upload Image (Required)")
            submit_btn = gr.Button("Submit")
            clear_btn = gr.ClearButton(value="Clear All")

        with gr.Column(scale=1):
            stt_output = gr.Textbox(label="Input Interpretation")
            doc_response_output = gr.Textbox(label="Doctor's Response")
            audio_output = gr.Audio(label="Doctor's Voice", type="filepath")

    # Submit action
    submit_btn.click(
        fn=process_inputs,
        inputs=[text_query, audio_query, image_input],
        outputs=[stt_output, doc_response_output, audio_output]
    )

    # Clear button
    clear_btn.add([text_query, audio_query, image_input, stt_output, doc_response_output, audio_output])

# Launch the app
if __name__ == "__main__":
    demo.launch(debug=False, share=True)
