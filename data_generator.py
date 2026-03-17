import random
import numpy as np
from datetime import datetime
import json

class LanguageDataGenerator:
    def __init__(self):
        self.languages = [
            "English", "Chinese", "Hindi", "Spanish", "French",
            "Arabic", "Bengali", "Portuguese", "Russian", "Urdu"
        ]
        self.continents = ["Asia", "Africa", "Europe", "Americas", "Oceania"]
        
    def get_live_stats(self):
        """Generate real-time statistics"""
        return {
            "total_languages": 7151 + random.randint(-5, 5),
            "total_speakers": round(8.1 + random.uniform(-0.1, 0.1), 2),
            "dominant_language": "English",
            "fastest_growing": random.choice(["Hindi", "Spanish", "Arabic"]),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_top_languages(self):
        """Generate top languages with variations"""
        base_data = [1500, 1100, 600, 560, 310, 300, 270, 260, 255, 230]
        # Add some random variation (±2%)
        varied_data = [int(x * (1 + random.uniform(-0.02, 0.02))) for x in base_data]
        
        return {
            "labels": [f"🇬🇧 {self.languages[0]}", f"🇨🇳 {self.languages[1]}", 
                      f"🇮🇳 {self.languages[2]}", f"🇪🇸 {self.languages[3]}", 
                      f"🇫🇷 {self.languages[4]}", f"🇸🇦 {self.languages[5]}",
                      f"🇧🇩 {self.languages[6]}", f"🇵🇹 {self.languages[7]}", 
                      f"🇷🇺 {self.languages[8]}", f"🇵🇰 {self.languages[9]}"],
            "data": varied_data
        }
    
    def get_continent_distribution(self):
        """Generate continent distribution with variations"""
        base_data = [45, 30, 15, 8, 2]
        # Ensure sum is 100
        varied = [x + random.randint(-2, 2) for x in base_data]
        total = sum(varied)
        normalized = [int(100 * x / total) for x in varied]
        
        return {
            "labels": self.continents,
            "data": normalized
        }
    
    def get_growth_trends(self):
        """Generate growth trends data"""
        years = [2020, 2021, 2022, 2023, 2024]
        return {
            "labels": [str(y) for y in years],
            "datasets": [
                {
                    "label": "English",
                    "data": [1400, 1420, 1450, 1480, 1500 + random.randint(-10, 10)]
                },
                {
                    "label": "Hindi",
                    "data": [580, 585, 590, 595, 600 + random.randint(-5, 5)]
                },
                {
                    "label": "Spanish",
                    "data": [540, 545, 550, 555, 560 + random.randint(-5, 5)]
                }
            ]
        }
    
    def get_projections(self):
        """Generate 2030 projections"""
        return {
            "labels": ["English", "Chinese", "Hindi", "Spanish", "Arabic", "French"],
            "datasets": [
                {
                    "label": "Speakers 2024",
                    "data": [1500, 1100, 600, 560, 300, 310]
                },
                {
                    "label": "Projection 2030",
                    "data": [1700, 1250, 750, 650, 400, 350]
                }
            ]
        }
    
    def get_world_map(self):
        """Generate world map data"""
        regions = [
            {"label": "North America", "x": 150, "y": 100, "r": 25},
            {"label": "South America", "x": 200, "y": 250, "r": 18},
            {"label": "Europe", "x": 300, "y": 120, "r": 22},
            {"label": "Africa", "x": 350, "y": 220, "r": 30},
            {"label": "Asia", "x": 500, "y": 150, "r": 45},
            {"label": "Oceania", "x": 650, "y": 280, "r": 8}
        ]
        return regions

    def get_historical_data(self, language, years=10):
        """Generate historical data for ML predictions"""
        np.random.seed(hash(language) % 2**32)
        base = [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
        noise = np.random.normal(0, 50, years)
        return [int(b + n) for b, n in zip(base[:years], noise)]
