"""Combinatorics cheat sheet calculator (FastAPI).

Based on the course example app_final.py (lesson 4, "Infrastructure and
administration"): routes / and /health, settings read with os.getenv.
"""

import logging
import math
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

load_dotenv()

APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
MAX_N = int(os.getenv("MAX_N", "1000"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("combinatorics")

app = FastAPI(title="Шпаргалка по комбинаторике", version=APP_VERSION)

logger.info("Application started: version=%s, MAX_N=%s", APP_VERSION, MAX_N)


FORMULAS = {
    (True, False): {
        "name": "Размещения без повторений",
        "formula": "A(n,k) = n! / (n-k)!",
        "example": "Выбрать старосту и заместителя из 5 студентов: A(5,2) = 20",
        "route": "/permutations?n=5&k=2&repeat=false",
    },
    (True, True): {
        "name": "Размещения с повторениями",
        "formula": "n^k",
        "example": "Двузначные коды из цифр 1, 2, 3: 3^2 = 9",
        "route": "/permutations?n=3&k=2&repeat=true",
    },
    (False, False): {
        "name": "Сочетания без повторений",
        "formula": "C(n,k) = n! / (k! · (n-k)!)",
        "example": "Выбрать 2 дежурных из 5 студентов: C(5,2) = 10",
        "route": "/combinations?n=5&k=2&repeat=false",
    },
    (False, True): {
        "name": "Сочетания с повторениями",
        "formula": "C(n+k-1,k)",
        "example": "Купить 2 пирожка, если есть 3 вида: C(3+2-1,2) = 6",
        "route": "/combinations?n=3&k=2&repeat=true",
    },
}


def check_range(name: str, value: int, minimum: int = 0):
    """Stop the request with error 400 if value is outside minimum..MAX_N."""
    if value < minimum or value > MAX_N:
        message = f"{name} должно быть от {minimum} до {MAX_N}, получено {value}"
        logger.warning("Bad input: %s", message)
        raise HTTPException(status_code=400, detail=message)


def check_k_not_greater_than_n(n: int, k: int):
    """Without repetition you cannot pick more items than there are."""
    if k > n:
        message = f"Без повторений k не может быть больше n: n={n}, k={k}"
        logger.warning("Bad input: %s", message)
        raise HTTPException(status_code=400, detail=message)


@app.get("/")
def root():
    return {
        "message": "Шпаргалка-калькулятор по комбинаторике работает",
        "routes": {
            "/factorial/{n}": "факториал n!",
            "/permutations?n=5&k=2&repeat=false": "размещения: порядок важен",
            "/combinations?n=5&k=2&repeat=false": "сочетания: порядок не важен",
            "/choose?order=true&repeat=false": "какую формулу выбрать",
            "/cheatsheet": "все формулы с примерами",
            "/docs": "интерактивная документация",
        },
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
    logger.info("Calculated: %s", explanation)
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
    logger.info("Calculated: %s", explanation)
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
    logger.info("Calculated: %s", explanation)
    return {
        "n": n,
        "k": k,
        "repeat": repeat,
        "result": result,
        "explanation": explanation,
    }


@app.get("/choose")
def choose(order: bool, repeat: bool):
    answer = FORMULAS[(order, repeat)]
    logger.info("Chosen formula: order=%s, repeat=%s -> %s", order, repeat, answer["name"])
    return {"order": order, "repeat": repeat, **answer}


@app.get("/cheatsheet")
def cheatsheet():
    return {
        "how_to_choose": "Ответьте на два вопроса: важен ли порядок и могут ли элементы повторяться",
        "factorial": "n! = 1 · 2 · ... · n, 0! = 1. Пример: 5! = 120",
        "formulas": list(FORMULAS.values()),
    }