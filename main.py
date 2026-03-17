from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import asyncio
import random
from datetime import datetime
from typing import List
import json

from data_generator import LanguageDataGenerator

app = FastAPI(title="Linguasphere API", 
              description="Real-time Language Statistics API",
              version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize data generator
data_gen = LanguageDataGenerator()

# Store active WebSocket connections
active_connections: List[WebSocket] = []

# Serve HTML file
@app.get("/", response_class=HTMLResponse)
async def get_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

# REST API Endpoints
@app.get("/api/v1/stats/live")
async def get_live_stats():
    """Get real-time statistics"""
    return data_gen.get_live_stats()

@app.get("/api/v1/languages/top")
async def get_top_languages():
    """Get top 10 languages data"""
    return data_gen.get_top_languages()

@app.get("/api/v1/continents/distribution")
async def get_continent_distribution():
    """Get continent distribution"""
    return data_gen.get_continent_distribution()

@app.get("/api/v1/trends/growth")
async def get_growth_trends():
    """Get growth trends"""
    return data_gen.get_growth_trends()

@app.get("/api/v1/projections/2030")
async def get_projections():
    """Get 2030 projections"""
    return data_gen.get_projections()

@app.get("/api/v1/map/world")
async def get_world_map():
    """Get world map data"""
    return data_gen.get_world_map()

@app.get("/api/v1/language/{lang_name}/historical")
async def get_language_history(lang_name: str):
    """Get historical data for a specific language"""
    valid_languages = ["English", "Chinese", "Hindi", "Spanish", "French", 
                      "Arabic", "Bengali", "Portuguese", "Russian", "Urdu"]
    
    if lang_name not in valid_languages:
        raise HTTPException(status_code=404, detail="Language not found")
    
    return {
        "language": lang_name,
        "historical_data": data_gen.get_historical_data(lang_name),
        "years": list(range(2015, 2025))
    }

# WebSocket for real-time updates
@app.websocket("/ws/live")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            # Send real-time updates every 5 seconds
            data = {
                "timestamp": datetime.now().isoformat(),
                "stats": data_gen.get_live_stats(),
                "top_languages": data_gen.get_top_languages(),
                "message": "Live data update"
            }
            await websocket.send_json(data)
            await asyncio.sleep(5)
    except:
        active_connections.remove(websocket)

# Broadcast to all connected clients
@app.post("/api/v1/broadcast")
async def broadcast_message(message: str):
    """Broadcast a message to all connected WebSocket clients"""
    for connection in active_connections:
        try:
            await connection.send_json({
                "type": "broadcast",
                "message": message,
                "timestamp": datetime.now().isoformat()
            })
        except:
            pass
    return {"message": f"Broadcast sent to {len(active_connections)} clients"}

# Machine Learning prediction endpoint (simulated)
@app.get("/api/v1/predict/{language}/{year}")
async def predict_language_growth(language: str, year: int):
    """Predict language speakers for a future year"""
    if year < 2024 or year > 2050:
        raise HTTPException(status_code=400, detail="Year must be between 2024 and 2050")
    
    # Simple linear regression simulation
    base_data = {
        "English": 1500, "Chinese": 1100, "Hindi": 600, "Spanish": 560,
        "French": 310, "Arabic": 300, "Bengali": 270, "Portuguese": 260,
        "Russian": 255, "Urdu": 230
    }
    
    if language not in base_data:
        raise HTTPException(status_code=404, detail="Language not found")
    
    growth_rates = {
        "English": 2.5, "Chinese": 2.0, "Hindi": 7.2, "Spanish": 3.1,
        "French": 2.8, "Arabic": 4.5, "Bengali": 3.5, "Portuguese": 2.9,
        "Russian": 1.5, "Urdu": 4.2
    }
    
    years_from_now = year - 2024
    growth_rate = growth_rates[language] / 100
    predicted = base_data[language] * (1 + growth_rate) ** years_from_now
    
    return {
        "language": language,
        "year": year,
        "predicted_speakers": round(predicted, 2),
        "confidence": random.uniform(85, 98),
        "growth_rate": growth_rates[language]
    }

# Health check
@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "websocket_clients": len(active_connections)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
