import serial
import folium
import pynmea2
import sqlite3
from db import models
import geopandas as gpd
from pathlib import Path
from db.schemas import GPS
import folium.raster_layers
from db.models import GpsModel
from sqlalchemy.orm import Session
from db.db import SessionLocal, engine
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, Depends, BackgroundTasks
from config import comPort, colorsList, dbName, Center, zoom_start, max_bounds, min_zoom, min_lat, min_lon, max_lat, max_lon, savePath, layerPath


app = FastAPI()
models.Base.metadata.create_all(bind=engine)
BASE_DIR = Path(__file__).resolve().parent
static_files_path = BASE_DIR / 'application' / 'static'
templates = Jinja2Templates(directory=BASE_DIR / 'application' / 'templates')
app.mount("/static", StaticFiles(directory=str(static_files_path)), name="static")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def read_gps_data(serial_port=comPort, baudrate=9600):
    ser = serial.Serial(serial_port, baudrate=baudrate, timeout=1)
    while True:
        data = ser.readline()
        if data.startswith(b'$GPGGA'):
            msg = pynmea2.parse(data.decode('utf-8'))
            return msg.latitude, msg.longitude
    

def updateMap():
    colors = colorsList

    connection = sqlite3.connect(dbName)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM locations")
    data = cursor.fetchall()

    gdf = gpd.read_file(f"{layerPath}\REGIONS_shp.shx")
    m = folium.Map(location=Center,
                    zoom_start=zoom_start,
                    max_bounds=max_bounds,
                    min_zoom=min_zoom,
                    min_lat=min_lat,
                    min_lon=min_lon,
                    max_lat=max_lat,
                    max_lon=max_lon)
    
    folium.GeoJson(gdf, name = 'Layer 2',
                    style_function = lambda feature: {
                        "fillColor": "none",
                        "color": "black",
                        "weight": 2 },
                    zoom_on_click=True).add_to(m)

    for i in data:
        if i[1] is not None:
            folium.Marker([i[1], i[2]], icon=folium.Icon(color=colors[i[4]])).add_to(m)
            
    folium.LayerControl().add_to(m)
    m.save(savePath)


def fetchLoc(id: int):
    db = SessionLocal()
    gpsModel = db.query(GpsModel).filter(GpsModel.id == id).first()
    lat, lon = read_gps_data(comPort)
    gpsModel.longitude = lon
    gpsModel.latitude = lat
    db.add(gpsModel)
    db.commit()


@app.get("/")
def test(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.post("/add_mark")
async def add_mark(request: GPS, bt: BackgroundTasks, db: Session = Depends(get_db)):

    gpsModel = GpsModel()
    gpsModel.message = request.message
    gpsModel.group = request.group
    
    db.add(gpsModel)
    db.commit()
    bt.add_task(fetchLoc, gpsModel.id)
    bt.add_task(updateMap)
