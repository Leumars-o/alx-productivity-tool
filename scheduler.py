""" This module is responsible for scheduling the execution of the functions
    in the program.
    The functions are executed at a specific time of the day
"""

import genai as genai
import random
import credentials
import pytz
import intranet_login as intranet
import telegram_notify as telegram
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger


def execute_intranet():
    """ This function is responsible for executing the intranet function

    Returns:
        _type_: dict
                The projects from the intranet module
    """
    all_user_projects = []
    # Get credentials
    creds = credentials.load_credentials()

    for cred in creds:
        # Get projects from intranet
        projects = intranet.main(cred)
        # Append projects to all_user_projects
        all_user_projects.append(projects)

    # Send projects to telegram
    for project in all_user_projects:
        # send project notification to telegram
        telegram.send_project(project)


def execute_quiz():
    """ This function is responsible for executing the quiz function

    Returns:
        _type_: dict
                The quiz from the genai module
    """
    # Generate a quiz question
    quiz = genai.prompt_model(genai.prompts, 0)

    # Load chat ids of users
    user_ids = credentials.load_credentials()
    # Iterate through each user's credentials
    for user in user_ids:
        # Get chat id
        chat_id = user['chat_id']
        # send quiz to telegram
        telegram.send_quiz(quiz, chat_id)


def execute_fact():
    """ This function is responsible for executing the fact function

    Returns:
        _type_: dict
                The fact from the genai module
    """
    # Get a fact
    fact = genai.prompt_model(genai.prompts, 1)
    
    # Load chat ids of users
    user_ids = credentials.load_credentials()
    # Iterate through each user's credentials
    for user in user_ids:
        # Get chat id
        chat_id = user['chat_id']
        # send quiz to telegram
        telegram.send_message(fact, 'fact', chat_id)


def execute_quote():
    """ This function is responsible for executing the quote function

    Returns:
        _type_: dict
                The quote from the genai module
    """
    # Get a quote
    quote = genai.prompt_model(genai.prompts, 2)

    # Load chat ids of users
    user_ids = credentials.load_credentials()
    # Iterate through each user's credentials
    for user in user_ids:
        # Get chat id
        chat_id = user['chat_id']
        # send quiz to telegram
        telegram.send_message(quote, 'quote', chat_id)
    


# Generate a random number
random_number = random.randint(0, 2)

# Create a list of functions to execute
functions = [execute_quiz, execute_fact, execute_quote]

# Define the time zone
timezone = pytz.timezone('Africa/Lagos')

# Create triggers for the scheduler
trigger_projects = CronTrigger(hour = '16', minute = '59', second = '0', timezone=timezone)
trigger_ai = CronTrigger(hour = '16', minute = '59', second = '3', timezone=timezone)

# Create the scheduler
scheduler = BlockingScheduler()
scheduler.add_job(execute_intranet, trigger_projects)
scheduler.add_job(functions[random_number], trigger_ai)

# Start the scheduler
scheduler.start()
