"""create learning path tables

Revision ID: 20260413_03
Revises: 20260413_02
Create Date: 2026-04-13
"""

from alembic import op
import sqlalchemy as sa


revision = "20260413_03"
down_revision = "20260413_02"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "learning_paths",
        sa.Column("id", sa.String(length=32), primary_key=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("role", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
    )

    op.create_table(
        "learning_path_courses",
        sa.Column("id", sa.String(length=32), primary_key=True),
        sa.Column("path_id", sa.String(length=32), sa.ForeignKey("learning_paths.id", ondelete="CASCADE"), nullable=False),
        sa.Column("course_id", sa.String(length=32), sa.ForeignKey("courses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False, server_default="0"),
        sa.UniqueConstraint("path_id", "course_id", name="uq_path_course"),
    )
    op.create_index("ix_learning_path_courses_path_id", "learning_path_courses", ["path_id"])
    op.create_index("ix_learning_path_courses_course_id", "learning_path_courses", ["course_id"])


def downgrade() -> None:
    op.drop_index("ix_learning_path_courses_course_id", table_name="learning_path_courses")
    op.drop_index("ix_learning_path_courses_path_id", table_name="learning_path_courses")
    op.drop_table("learning_path_courses")
    op.drop_table("learning_paths")
