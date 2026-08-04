from sqlalchemy import text

from database import engine


def check_database_connection() -> None:
    try:
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT 1")
            )

            value = result.scalar_one()

        print(f"Database connection successful: {value}")

    except Exception as exc:
        print("Database connection failed:")
        print(exc)
        raise


if __name__ == "__main__":
    check_database_connection()