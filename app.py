from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from fastapi.responses import StreamingResponse, HTMLResponse
from gtts import gTTS
import io

app = FastAPI(title="Text to Speech API")

class TTSRequest(BaseModel):
    text: str
    language: str = "en"  
    slow: bool = False    

@app.get("/", response_class=HTMLResponse)
async def home():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Text to Speech API</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                text-align: center;
            }
            h1 {
                color: #333;
            }
        </style>
    </head>
    <body>
        <h1>Welcome to my Text to Speech API</h1>
        <p>Use the /speak endpoint to convert text to speech.</p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

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
