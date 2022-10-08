from sql_operations import *
from cli import *
import bcrypt
import pyperclip

def authenticate_user(pwd, max_try):
    while max_try:
        password = get_password().encode('utf-8')
        if bcrypt.checkpw(password, pwd):
            return True
        else:
            max_try -= 1
            print(f'\n{max_try} tries left')
    else:
        print('\nMaximum tries ended, please try again later')
        return False

max_try = 3

if __name__ == '__main__':
    db = connect_to_db()
    cursor = db.cursor()

    pwd = fetch_password(cursor).encode('utf-8')

    # Checking whether the password entered by the user matches with the admin password
    if not authenticate_user(pwd, max_try):
        cursor.close()
        db.close()
        exit()

    while True:
        option = get_entry_choice()

        if option == 'Add':
            site_info = get_website_info()
            status = insert_site(cursor, site_info)
            if status:
                print('\nInserted successfully')
                db.commit()
            else:
                print('\nTry again')

        elif option == 'Search':
            site_name = get_website_name(' to search')
            row_ids = fetch_site_info(cursor, site_name)

            row_id = get_row_id(' copied')

            while row_id not in row_ids and row_id > -1:
                print('\nRow id doesn\'t match. Please try again (-1 to quit)')
                row_id = get_row_id(' copied')

            pwd = fetch_password(cursor).encode('utf-8')

            if row_id != -1 and authenticate_user(pwd, 1):
                pyperclip.copy(fetch_password(cursor, False, row_id))
                print("\npassword copied to clipboard")
            else:
                print("\nExiting search")

        elif option == 'Delete':
            site_info = get_website_info_to_delete()
            rowcount, row_ids = get_no_of_sites(cursor, site_info)
            status = False

            if rowcount <= -1:
                print('\nAtleast one value should be provided')

            elif rowcount > 1:
                row_id = get_row_id(' delete')

                while row_id not in row_ids and row_id > -1:
                    print('\nRow id doesn\'t match. Please try again (-1 to quit)')
                    row_id = get_row_id(' delete')

                if row_id != -1:
                    status = delete_site_info(cursor, row_id, choice=False)
                else:
                    status = False
                    print("\nExiting delete")

            elif rowcount == 1:
                status = delete_site_info(cursor, site_info, choice=True)

            if status:
                print('\nDeleted successfully')
                db.commit()
            else:
                print('\nTry again')

        elif option == 'Modify':
            site_name = get_website_name(' to modify')
            row_ids = fetch_site_info(cursor, site_name)

            row_id = get_row_id(' modify')

            while row_id not in row_ids and row_id > -1:
                print('\nRow id doesn\'t match. Please try again (-1 to quit)')
                row_id = get_row_id(' modify')

            if row_id != -1:
                new_site_info = get_details_to_modify()
                status = modify_site_info(cursor, new_site_info, row_id)
            else:
                status = False
                print("\nExiting modify")

            if status:
                print('\nSuccessfully modified')
                db.commit()
            else:
                print('\nTry again')

        elif option == 'Quit':
            break

    cursor.close()
    db.close()