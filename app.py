from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from gtts import gTTS
import io

app = FastAPI(title="Text to Speech API")

class TTSRequest(BaseModel):
    text: str
    language: str = "en"  
    slow: bool = False    

@app.post("/speak")
async def text_to_speech(request: TTSRequest):

    try:
        audio_buffer = io.BytesIO()
        
        tts = gTTS(text=request.text, lang=request.language, slow=request.slow)
        tts.write_to_fp(audio_buffer)
        
        audio_buffer.seek(0)
        
        return StreamingResponse(
            audio_buffer, 
            media_type="audio/mpeg",
            headers={"Content-Disposition": "attachment; filename=speech.mp3"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
