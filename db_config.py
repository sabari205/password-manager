from configparser import ConfigParser

def read_config(filename='config.ini', section='mysql'):
    """
        Reads the config file and returns the config object to
        connect to the database
        PARAMETERS
            filename: Name or path of the config file
            section: Section name from which the config has to be returned
        RETURNS
            The config object for connection establishment
    """

    parser = ConfigParser()
    parser.read(filename)

    ret_obj = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            ret_obj[item[0]] = item[1]
    else:
        raise Exception(f'{section} not in the config file {filename}')

    return ret_obj
