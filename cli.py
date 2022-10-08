from PyInquirer import prompt
import copy

def get_password():
    """
        Prompts the user to enter password
        PARAMETERS
            None
        RETURNS
            The password typed by the user
    """
    answer = prompt(questions[0])
    return answer['password']

def get_entry_choice():
    """
        Provides a choice to the user
        PARAMETERS
            None
        RETURNS
            The choice selected by the user
    """
    print()
    answer = prompt(questions[1])
    return answer['entrychoice']

def get_website_info():
    """
        Lets the user to enter various informations related to that particular website
        PARAMETERS
            None
        RETURNS
            The inputs entered by the user as a dict
    """

    question = copy.deepcopy(questions[2:6])

    print('\nWebsite name, either username or email, and password is mandatory\n')

    question[0]['message'] = question[0]['message'].format('')
    question[1]['message'] = question[1]['message'].format('', '', 'does not exist')
    question[2]['message'] = question[2]['message'].format('', '', 'does not exist')
    question[3]['message'] = question[3]['message'].format('', 'for the site')

    answer = prompt(question)
    return answer

def get_website_name(action):
    """
        Lets the user to enter the website name to search for
        PARAMETERS
            None
        RETURNS
            The website name entered by the user
    """
    print()

    question = copy.deepcopy(questions[2])

    question['message'] = question['message'].format(action)

    answer = prompt(question)
    return answer['site_name']

def get_website_info_to_delete():
    """
        Lets the user to enter various informations related to that particular website to be removed
        PARAMETERS
            None
        RETURNS
            The inputs entered by the user as a dict
    """

    question = copy.deepcopy(questions[2:5])

    print('\nWebsite name is mandatory\n')

    question[0]['message'] = question[0]['message'].format(' to delete')
    question[1]['message'] = question[1]['message'].format('', ' related to the site', 'does not exist')
    question[2]['message'] = question[2]['message'].format('', ' related to the site', 'does not exist')

    answer = prompt(question)
    return answer

def get_row_id(action):
    """
        Lets the user to enter the row id to be deleted
        PARAMETERS
            None
        RETURNS
            The row id entered by the user
    """
    print()

    question = copy.deepcopy(questions[6])

    question['message'] = question['message'].format(action)

    answer = prompt(question)
    return int(answer['row_id'])

def get_details_to_modify():
    """
        Lets the user to enter the site details to be modified
        PARAMETERS
            None
        RETURNS
            The site information
    """
    print()

    question = copy.deepcopy(questions[3:6])

    question[0]['message'] = question[0]['message'].format('new ', '', 'no change')
    question[1]['message'] = question[1]['message'].format('new ', '', 'no change')
    question[2]['message'] = question[2]['message'].format('new ', ' (press enter if no change)')
    
    answer = prompt(question)
    return answer

questions = [
    {
        'type': 'password',
        'name': 'password',
        'message': 'Enter the passowrd for admin account'
    },
    {
        'type': 'list',
        'name': 'entrychoice',
        'message': 'What do you want to do?',
        'choices': [
            'Add',
            'Search',
            'Delete',
            'Modify',
            'Quit'
        ]
    },
    {
        'type': 'input',
        'name': 'site_name',
        'message': 'Enter the full URL or name of the website{}:'
    },
    {
        'type': 'input',
        'name': 'usrname',
        'message': 'Enter the {}user name{} (press enter if {}):'
    },
    {
        'type': 'input',
        'name': 'registered_mail',
        'message': 'Enter the {}email{} (press enter if {}):'
    },
    {
        'type': 'password',
        'name': 'password',
        'message': 'Enter the {}password{}:'
    },
    {
        'type': 'input',
        'name': 'row_id',
        'message': 'Enter the row id to be {} from the above result:'
    }
]