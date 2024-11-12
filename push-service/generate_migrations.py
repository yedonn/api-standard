import datetime
import os
import subprocess
import sys

def main():
    try:
        # Change the working directory to the location of your alembic.ini file
        # Adjust the path if necessary
        # os.chdir('./')

        # Format timestamp for a file-friendly name
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        migration_message = f'Auto-generated migration {timestamp}'

        # Run alembic revision to auto-generate migration scripts
        result = subprocess.run(
            ['alembic', 'revision', '--autogenerate', '-m', migration_message],
            check=True,
            capture_output=True,
            text=True
        )

        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
    
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}", file=sys.stderr)

if __name__ == '__main__':
    main()
