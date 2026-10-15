"""Combinatorics cheat sheet calculator (FastAPI).

Based on the course example app_final.py (lesson 4, "Infrastructure and
administration"): routes / and /health, settings read with os.getenv.
"""

import os

from fastapi import FastAPI

APP_VERSION = os.getenv("APP_VERSION", "0.1.0")

app = FastAPI(title="Шпаргалка по комбинаторике", version=APP_VERSION)


@app.get("/")
def root():
    return {
        "message": "Шпаргалка-калькулятор по комбинаторике работает",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/version")
def version():
    return {"version": APP_VERSION}