# retriever.py
from db import fetch_recent

def prepare_context(limit: int = 200) -> str:
    """
    Convert recent sensor data into a readable context for RAG or AI models.
    
    Parameters:
        limit (int): Number of recent records to fetch from the database.
    
    Returns:
        str: A summarized context string containing average, min, and max readings.
    """
    df = fetch_recent(limit)
    
    if df.empty:
        return "No sensor data available currently."

    # Calculate averages
    avg_temp = round(df['temperature'].mean(), 2)
    avg_ph = round(df['ph'].mean(), 2)
    avg_do = round(df['dissolved_oxygen'].mean(), 2)

    # Calculate min and max
    min_temp, max_temp = df['temperature'].min(), df['temperature'].max()
    min_ph, max_ph = df['ph'].min(), df['ph'].max()
    min_do, max_do = df['dissolved_oxygen'].min(), df['dissolved_oxygen'].max()

    # Prepare context string
    context = f"""
Latest Water Quality Summary:
- Average Temperature: {avg_temp}°C
- Temperature Range: {min_temp}–{max_temp}°C
- Average pH: {avg_ph}
- pH Range: {min_ph}–{max_ph}
- Average Dissolved Oxygen: {avg_do} mg/L
- Dissolved Oxygen Range: {min_do}–{max_do} mg/L
"""
    return context

# Example usage
if __name__ == "__main__":
    context = prepare_context()
    print(context)