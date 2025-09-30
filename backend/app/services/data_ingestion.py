import clickhouse_connect
from ..core.config import settings

def get_clickhouse_client():
    """
    Establishes a connection to the ClickHouse database.
    """
    try:
        client = clickhouse_connect.get_client(
            host=settings.CLICKHOUSE_HOST,
            port=settings.CLICKHOUSE_PORT,
            user=settings.CLICKHOUSE_USER,
            password=settings.CLICKHOUSE_PASSWORD,
            database=settings.CLICKHOUSE_DB
        )
        print("Connected to ClickHouse successfully.")
        return client
    except Exception as e:
        print(f"Error connecting to ClickHouse: {e}")
        return None

def ingest_session_data(user_id: str, emotion_label: str, audio_features: list, timestamp: str):
    """
    Ingests a single therapy session's metadata and audio features into ClickHouse.

    Args:
        user_id: The ID of the user.
        emotion_label: The emotion detected during the session.
        audio_features: A list of extracted audio features.
        timestamp: The timestamp of the session.
    """
    client = get_clickhouse_client()
    if not client:
        return

    try:
        # Define the table schema if it doesn't exist
        client.command("""
            CREATE TABLE IF NOT EXISTS session_logs (
                user_id String,
                emotion_label String,
                audio_features Array(Float32),
                timestamp DateTime64(3)
            ) ENGINE = MergeTree()
            ORDER BY (user_id, timestamp)
        """)

        # Insert data into the table
        data = [[user_id, emotion_label, audio_features, timestamp]]
        client.insert('session_logs', data)
        print("Session data ingested into ClickHouse.")
    except Exception as e:
        print(f"Failed to ingest data: {e}")
    finally:
        client.close()

def get_mood_trends(user_id: str):
    """
    Retrieves a user's mood trends from the database.

    Args:
        user_id: The user ID to query.

    Returns:
        A list of mood entries.
    """
    client = get_clickhouse_client()
    if not client:
        return []

    try:
        query_result = client.query(f"SELECT emotion_label, timestamp FROM session_logs WHERE user_id = '{user_id}' ORDER BY timestamp")
        
        # The result is a list of tuples, so we convert it to a more readable format
        mood_entries = []
        for row in query_result.result_set:
            mood_entries.append({
                "emotion_label": row[0],
                "timestamp": row[1].isoformat()
            })
        return mood_entries
    except Exception as e:
        print(f"Failed to retrieve mood data: {e}")
        return []
    finally:
        client.close()

# The clickhouse-connect library provides high-performance data ingestion
# and querying capabilities via the ClickHouse HTTP interface.