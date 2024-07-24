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


## Algorithm for Improving Savings Behavior

### Assumptions

- Users input their income, expenses, and savings accurately.
- Users update their financial data regularly.

### Overall Structure

1. **Data Collection**: The application collects data on the user's income, expenses, and savings.
2. **Analysis**: The collected data is analyzed to identify spending patterns and deviations from the user's saving goals.
3. **Feedback Generation**: Based on the analysis, the application provides detailed insights and tips to help the user improve their savings behavior.

### Logic

1. **Calculate Averages**: Compute the average monthly income and expenses based on user data.
2. **Identify High-Expense Categories**: Determine which expense categories have the highest spending.
3. **Compare Savings**: Compare the user's actual savings to their target savings.
4. **Generate Insights**: Provide insights into spending behavior. For example, "You spend 20% more on dining out than planned."
5. **Provide Tips**: Offer actionable tips to improve savings. For example, "Consider reducing dining out expenses by 10% to increase savings."

### For Example

If the user spends significantly more on entertainment than budgeted, the algorithm might suggest:

- "Reduce entertainment expenses by 15%."
- "Consider free or low-cost entertainment options."

## How to Use

1. **Setup**: Follow the installation instructions to set up the web application.
2. **Input Data**: Enter your income, expenses, and savings in the respective fields.
3. **View Insights**: Navigate to the insights page by clicking view financial insights on progress page to see personalized recommendations and tips.
4. **Update Regularly**: Keep your data up-to-date to receive accurate feedback and improve your savings behavior.
