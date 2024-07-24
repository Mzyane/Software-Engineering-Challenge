# Software-Engineering-Challenge

# SaveSmart(Wallet)

## Description
SaveSmart is a web application designed to help users manage and optimize their savings goals. 

## Setup

### Prerequisites
- Python 3.11
- Django

## Installation

1. Clone the repository:
      ```bash
      git clone <repository_url>
      cd <project_directory>
      
2. Set up the virtual environment:
     python -m venv venv
     source venv/bin/activate

3. Install the dependencies
   pip install -r requirements.txt
   
## Configuration

1. Set up environment variables
   Create a .env file and add the required environment variables.

2. Apply migrations
   python manage.py migrate

## Running the Application
1. Start the development server
      python manage.py runserver
   
2. Open your browser and visit
     http://127.0.0.1:8000/


## Savings Insights Algorithm

## Assumptions

1. Data Availability:
   - The Contribution model is populated with data that includes contributions from users towards various savings goals.
   - Each Contribution entry includes fields such as user, goal, amount, and date.
  
2. Goal Information:
   - The SavingsGoal model contains information about each savings goal, including target_amount and target_date.

3. Application Environment:
   - The algorithm is intended to run as a custom Django management command.
   - The django package and its dependencies are correctly installed and configured in the environment.

## Algorithm Overview
   The algorithm aims to provide users with detailed insights and recommendations on their savings behavior. It is implemented in a Django management command located in          savings/management/commands/generate_insights.py. Here's a breakdown of the logic:

   1. Fetch All Savings Goals:
   - Retrieve all savings goals from the SavingsGoal model.

   2. Calculate Total Contributions:
   - For each savings goal, aggregate the total contributions made by users using the Contribution model.

   3. Calculate Average Contributions:
   - Compute the average contribution amount for each goal.

   4. Determine Progress:
   - Calculate the percentage of progress towards the target amount for each goal.

   5. Generate Recommendations:
   - Compare user progress with benchmarks and generate recommendations. For example:
      - If progress is less than 50%, recommend increasing monthly contributions.
      - If progress is between 50% and 80%, encourage maintaining the current savings rate.
      - If progress exceeds 80%, suggest setting a new goal or increasing the target amount.

   6. Output Insights:
   - Format the results into a readable format and print them to the console.

   7. Running the Command
   - Execute the insights generation command, use the following command in the terminal:
     python manage.py generate_insights
