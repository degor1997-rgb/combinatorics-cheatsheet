"""Combinatorics cheat sheet calculator (FastAPI).

Based on the course example app_final.py (lesson 4, "Infrastructure and
administration"): routes / and /health, settings read with os.getenv.
"""

import math
import os

from fastapi import FastAPI, HTTPException

APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
MAX_N = 1000

app = FastAPI(title="Шпаргалка по комбинаторике", version=APP_VERSION)


def check_range(name: str, value: int, minimum: int = 0):
    """Stop the request with error 400 if value is outside minimum..MAX_N."""
    if value < minimum or value > MAX_N:
        message = f"{name} должно быть от {minimum} до {MAX_N}, получено {value}"
        raise HTTPException(status_code=400, detail=message)


def check_k_not_greater_than_n(n: int, k: int):
    """Without repetition you cannot pick more items than there are."""
    if k > n:
        message = f"Без повторений k не может быть больше n: n={n}, k={k}"
        raise HTTPException(status_code=400, detail=message)


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


@app.get("/factorial/{n}")
def factorial(n: int):
    check_range("n", n)
    result = math.factorial(n)
    if n == 0:
        explanation = "0! = 1 по определению"
    else:
        explanation = f"{n}! = 1 · 2 · ... · {n} = {result}"
    return {"n": n, "result": result, "explanation": explanation}


@app.get("/permutations")
def permutations(n: int, k: int, repeat: bool = False):
    check_range("k", k)
    if repeat:
        check_range("n", n, minimum=1)
        result = n**k
        explanation = f"{n}^{k} = {result}"
    else:
        check_range("n", n)
        check_k_not_greater_than_n(n, k)
        result = math.perm(n, k)
        explanation = f"A({n},{k}) = {n}! / {n - k}! = {result}"
    return {
        "n": n,
        "k": k,
        "repeat": repeat,
        "result": result,
        "explanation": explanation,
    }


@app.get("/combinations")
def combinations(n: int, k: int, repeat: bool = False):
    check_range("k", k)
    if repeat:
        check_range("n", n, minimum=1)
        result = math.comb(n + k - 1, k)
        explanation = f"C({n}+{k}-1,{k}) = C({n + k - 1},{k}) = {result}"
    else:
        check_range("n", n)
        check_k_not_greater_than_n(n, k)
        result = math.comb(n, k)
        explanation = f"C({n},{k}) = {n}! / ({k}! · {n - k}!) = {result}"
    return {
        "n": n,
        "k": k,
        "repeat": repeat,
        "result": result,
        "explanation": explanation,
    }