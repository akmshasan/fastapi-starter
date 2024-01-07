from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from api.database.database import Base


class DBFruit(Base):
    __tablename__ = "fruits"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    fruit: Mapped[str] = mapped_column(String(30))
    color: Mapped[str] = mapped_column(String(30))
