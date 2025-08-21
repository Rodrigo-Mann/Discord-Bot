import requests
import json
import os
FOLDER_NAME = "Audio_Files"
ENDPOINT="https://ttsmp3.com/makemp3_new.php"

class text_to_audio:
    def __init__(self,audio_lang:str,file_name:str=None, file_id:int=None):
        self.audio_lang = audio_lang
        if not os.path.exists(FOLDER_NAME):
            os.makedirs(FOLDER_NAME)
        if(file_name is None or file_name == ""):
            if file_id is not None:
                self.output_file = f"{FOLDER_NAME}\\{file_id}"
            else:
                print("File name is empty and no ID provided, using random name.")
                self.output_file  
        else:
            self.output_file = f"{FOLDER_NAME}\\{file_name}"
        print(f"Output file set to: {self.output_file}")
        self.file_ready=os.path.exists(self.output_file)

    def text_to_speech_request(self,text):
        
        if(not self.file_ready):
            request = requests.post(url=ENDPOINT, data={"msg":text,"lang":self.audio_lang,"source":"testing"})
            if request.status_code==200:
                link=json.loads(request.text)["URL"]
                download_response = requests.get(link, stream=True)
                if download_response.status_code == 200:
                    self.path = self.audio_file_from_stream(download_response)
                else:
                    print("Failed to download the audio file.")
                    self.path = None
        else:
            print(f"file {self.output_file} already exists, skipping download.")
            self.path = os.path.abspath(self.output_file)
        
    def audio_file_from_stream(self,stream):
        if stream.status_code == 200:
            with open(self.output_file, 'wb') as f:
                for chunk in stream.iter_content(chunk_size=8192):
                    f.write(chunk)
            print("Download complete!")
        return os.path.abspath(self.output_file)


