# app/main.py
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from fastapi.responses import StreamingResponse

# Load Titanic dataset
titanic_df = pd.read_csv('app/titanic.csv')

# Initialize FastAPI
app = FastAPI()

# Define a model for user queries
class Query(BaseModel):
    question: str

# Process the query
def process_query(question: str):
    # Handle questions regarding male passengers percentage
    if "percentage of passengers were male" in question.lower():
        male_percentage = (titanic_df[titanic_df['Sex'] == 'male'].shape[0] / titanic_df.shape[0]) * 100
        return f"The percentage of male passengers was {male_percentage:.2f}%."
    
    # Handle questions regarding the average fare
    elif "average ticket fare" in question.lower():
        average_fare = titanic_df['Fare'].mean()
        return f"The average ticket fare was ${average_fare:.2f}."
    
    # Handle histogram requests for ages
    elif "histogram of passenger ages" in question.lower():
        return plot_age_histogram()
    
    # Handle embarked ports
    elif "how many passengers embarked from each port" in question.lower():
        embarked_counts = titanic_df['Embarked'].value_counts()
        return f"Passengers embarked from the following ports: {embarked_counts.to_dict()}"
    
    return "I'm sorry, I cannot answer that question."

# Function to generate a histogram of passenger ages
def plot_age_histogram():
    fig, ax = plt.subplots()
    sns.histplot(titanic_df['Age'].dropna(), kde=False, bins=20, ax=ax)
    ax.set_title("Histogram of Passenger Ages")
    
    # Save the plot to a BytesIO object to return as a streaming response
    img_stream = BytesIO()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    
    return StreamingResponse(img_stream, media_type="image/png")

# API endpoint to handle user queries
@app.post("/ask")
def ask_question(query: Query):
    return {"answer": process_query(query.question)}
