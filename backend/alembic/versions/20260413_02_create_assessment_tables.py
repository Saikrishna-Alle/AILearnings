"""create assessment tables

Revision ID: 20260413_02
Revises: 20260413_01
Create Date: 2026-04-13
"""

from alembic import op
import sqlalchemy as sa


revision = "20260413_02"
down_revision = "20260413_01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "assessments",
        sa.Column("id", sa.String(length=32), primary_key=True),
        sa.Column("course_id", sa.String(length=32), sa.ForeignKey("courses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("ix_assessments_course_id", "assessments", ["course_id"])

    op.create_table(
        "assessment_attempts",
        sa.Column("id", sa.String(length=32), primary_key=True),
        sa.Column("assessment_id", sa.String(length=32), sa.ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="in_progress"),
        sa.Column("score", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("max_score", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("feedback", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("ix_assessment_attempts_assessment_id", "assessment_attempts", ["assessment_id"])
    op.create_index("ix_assessment_attempts_user_id", "assessment_attempts", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_assessment_attempts_user_id", table_name="assessment_attempts")
    op.drop_index("ix_assessment_attempts_assessment_id", table_name="assessment_attempts")
    op.drop_table("assessment_attempts")

    op.drop_index("ix_assessments_course_id", table_name="assessments")
    op.drop_table("assessments")
