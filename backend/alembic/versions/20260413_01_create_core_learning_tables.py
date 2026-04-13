"""create core learning tables

Revision ID: 20260413_01
Revises:
Create Date: 2026-04-13
"""

from alembic import op
import sqlalchemy as sa


revision = "20260413_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "courses",
        sa.Column("id", sa.String(length=32), primary_key=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("level", sa.String(length=32), nullable=False, server_default="beginner"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="draft"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    op.create_table(
        "modules",
        sa.Column("id", sa.String(length=32), primary_key=True),
        sa.Column("course_id", sa.String(length=32), sa.ForeignKey("courses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False, server_default="0"),
    )
    op.create_index("ix_modules_course_id", "modules", ["course_id"])

    op.create_table(
        "lessons",
        sa.Column("id", sa.String(length=32), primary_key=True),
        sa.Column("module_id", sa.String(length=32), sa.ForeignKey("modules.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("lesson_type", sa.String(length=32), nullable=False),
        sa.Column("content_url", sa.Text(), nullable=True),
        sa.Column("content_text", sa.Text(), nullable=True),
        sa.Column("duration_sec", sa.Integer(), nullable=True),
        sa.Column("position", sa.Integer(), nullable=False, server_default="0"),
    )
    op.create_index("ix_lessons_module_id", "lessons", ["module_id"])

    op.create_table(
        "enrollments",
        sa.Column("id", sa.String(length=32), primary_key=True),
        sa.Column("user_id", sa.String(length=64), nullable=False),
        sa.Column("course_id", sa.String(length=32), sa.ForeignKey("courses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("enrolled_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("ix_enrollments_user_id", "enrollments", ["user_id"])
    op.create_index("ix_enrollments_course_id", "enrollments", ["course_id"])

    op.create_table(
        "lesson_completion",
        sa.Column("id", sa.String(length=32), primary_key=True),
        sa.Column("user_id", sa.String(length=64), nullable=False),
        sa.Column("lesson_id", sa.String(length=32), sa.ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("ix_lesson_completion_user_id", "lesson_completion", ["user_id"])
    op.create_index("ix_lesson_completion_lesson_id", "lesson_completion", ["lesson_id"])


def downgrade() -> None:
    op.drop_index("ix_lesson_completion_lesson_id", table_name="lesson_completion")
    op.drop_index("ix_lesson_completion_user_id", table_name="lesson_completion")
    op.drop_table("lesson_completion")

    op.drop_index("ix_enrollments_course_id", table_name="enrollments")
    op.drop_index("ix_enrollments_user_id", table_name="enrollments")
    op.drop_table("enrollments")

    op.drop_index("ix_lessons_module_id", table_name="lessons")
    op.drop_table("lessons")

    op.drop_index("ix_modules_course_id", table_name="modules")
    op.drop_table("modules")

    op.drop_table("courses")
