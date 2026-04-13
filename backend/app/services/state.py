# Phase 1: in-memory storage for rapid MVP iteration.
# Swap this module with repository + PostgreSQL in Phase 2.

from datetime import datetime

courses: dict = {}
modules: dict = {}
lessons: dict = {}
enrollments: dict = {}
lesson_completion: dict = {}
learning_paths: dict = {}
assessments: dict = {}
attempts: dict = {}
certificates: dict = {}
posts: dict = {}
comments: dict = {}
likes: set = set()


def now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"
