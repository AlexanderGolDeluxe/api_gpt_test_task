from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)


class UserQuery(Base):
    __tablename__ = "user_query"

    text: Mapped[str]

    def __repr__(self) -> str:
        return f"UserQuery(id={self.id!r}, text={self.text[:30]!r})"


class GPTAnswer(Base):
    __tablename__ = "gpt_answer"

    user_query_id: Mapped[int] = mapped_column(
        ForeignKey("user_query.id")
    )
    response_one: Mapped[str] = mapped_column(nullable=True)
    response_two: Mapped[str] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return (
            f"GPTAnswer(id={self.id!r}, "
            f"response_two={self.response_two[:30]!r})")
