# AI Skill Platform - Phase-Wise Blueprint

## Phase 1 (MVP)
- Architecture: Next.js + FastAPI modular monolith + in-memory persistence fallback.
- Database: PostgreSQL schema planned, in-memory runtime for rapid iteration.
- Scope: Course management, enroll/progress/resume, learning path basics, assessments, certificate JSON, dashboard, minimal social, admin basics.

## Phase 2 (Productize)
- Add PostgreSQL persistence with repositories and Alembic migrations.
- Add Redis caching and background workers for async jobs.
- Add OpenAI integration (descriptive evaluations, feedback, skill-gap hints) behind a feature flag.
- Add certificate PDF generation.

## Phase 3 (Scale)
- Add authentication/authorization, rate limiting, robust observability.
- Extract heavy modules into services (assessment + AI evaluation first).
- Add event-driven workflows and analytics store.

## Backend Services
- Course service
- Enrollment & progress service
- Learning path service
- Assessment service
- Certificate service
- Dashboard aggregation
- Social service
- Admin orchestration

## API Base
- Version prefix: `/api/v1`
- Health: `/health`

## Core Endpoint Map
- Courses: `POST/GET/PUT/DELETE /courses`
- Structure: `POST /courses/{id}/modules`, `POST /modules/{id}/lessons`
- Learning: `POST /courses/{id}/enroll`, `POST /lessons/{id}/complete`, `GET /users/{u}/courses/{c}/progress`, `GET /users/{u}/courses/{c}/resume`
- Learning Path: `POST /learning-paths`, `POST /learning-paths/{id}/courses`, `GET /users/{u}/learning-paths/{id}/progress`, `GET /users/{u}/learning-paths/{id}/next-course`
- Assessment: `POST /assessments/{id}/start`, `POST /assessments/{attempt_id}/submit`
- Certificate: `POST /certificates/generate`, `GET /certificates/{id}/preview`
- Dashboard: `GET /users/{u}/dashboard`
- Social: `POST /posts`, `GET /feed`, `POST /posts/{id}/like`, `POST /posts/{id}/comments`
- Admin: `GET /admin/users/{u}/progress`, `POST /admin/courses/{id}/assessments`

## PostgreSQL Tables (Phase 2 migration target)
- users
- courses, modules, lessons, lesson_resources
- enrollments, lesson_progress, course_progress
- learning_paths, learning_path_courses, user_path_progress
- assessments, questions, assessment_attempts, attempt_answers
- certificates
- posts, post_likes, post_comments
- activity_logs

## Mock vs Production
- Mock in Phase 1: auth, AI evaluator, coding evaluator, advanced recommendations.
- Production-ready in Phase 1: course CRUD, enroll/progress, rule-based assessment scoring, dashboard aggregation contract, social basics.
