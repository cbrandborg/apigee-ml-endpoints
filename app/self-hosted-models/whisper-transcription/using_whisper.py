import whisper
import csv
import os

def transcribe(model_size, output_path, header, known_language=None):

    with open(output_path, 'a', newline='') as f:

        # create the csv writer
        writer = csv.writer(f, delimiter=',')

        # write a row to the csv file
        writer.writerow(header)

    # assign directory
    directory = '../inputs'

    model = whisper.load_model(model_size)

    # iterate over files in that directory

    for root, dirs, files in os.walk(directory, topdown=True):
        for filename in files:
            path_to_file = os.path.join(root, filename)
            folder = path_to_file.split('/')[2]
            subfolder = path_to_file.split('/')[3]

            row = [folder, subfolder, path_to_file]

            # load audio and pad/trim it to fit 30 seconds
            audio = whisper.load_audio(path_to_file)
            audio = whisper.pad_or_trim(audio)

            # make log-Mel spectrogram and move to the same device as the model
            mel = whisper.log_mel_spectrogram(audio).to(model.device)

            if known_language is None:

                # detect the spoken language
                _, probs = model.detect_language(mel)
                print(f"Detected language: {max(probs, key=probs.get)}")

                # decode the audio
                options = whisper.DecodingOptions(fp16 = False)
                result = whisper.decode(model, mel, options)

            else:

                # decode the audio
                options = whisper.DecodingOptions(fp16 = False, language=known_language)
                result = whisper.decode(model, mel, options)

            # print the recognized text
            print(result.text)

            transcription = result.text

            row = [folder, subfolder, path_to_file, transcription]

            with open(output_path, 'a', newline='') as f:

                # create the csv writer
                writer = csv.writer(f, delimiter=',')

                # write a row to the csv file
                writer.writerow(row)


researched_values = {
                "small-danish-whisper": {
                    "output_path":"../outputs/small-da-whisper-output.csv",
                    "header": ['folder', 'subfolder', 'file_name', 'transcription'],
                    "model_size":"small",
                    "known_language":"da"
                },
                "small-unknownLang-whisper": {
                    "output_path":"../outputs/small-ul-whisper-output.csv",
                    "header": ['folder', 'subfolder', 'file_name', 'transcription', 'pred_lang'],
                    "model_size":"small",
                    "known_language":None
                }
            }


for values in researched_values.values():

    output_path = values["output_path"]
    header = values["header"]
    model_size = values['model_size']
    known_language = values['known_language']

    transcribe(model_size, output_path, header, known_language)