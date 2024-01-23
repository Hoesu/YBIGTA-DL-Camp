from .base_command import BaseCommand
import os
import shutil
from typing import List

class CopyCommand(BaseCommand):
    def __init__(self, options: List[str], args: List[str]) -> None:
        """
        Initialize the CopyCommand object.

        Args:
            options (List[str]): List of command options.
            args (List[str]): List of command arguments.
        """
        super().__init__(options, args)

        # Override the attributes inherited from BaseCommand
        self.description = 'Copy a file or directory to another location'
        self.usage = 'Usage: cp [source] [destination]'

        # TODO 6-1: Initialize any additional attributes you may need.
        # Refer to list_command.py, grep_command.py to implement this.
        self.name = 'cp'
        self.options = options
        self.source_dir = self.args[0]
        self.destination_dir = self.args[1]

    def execute(self) -> None:
        """
        Execute the copy command.
        Supported options:
            -i: Prompt the user before overwriting an existing file.
            -v: Enable verbose mode (print detailed information)
        
        TODO 6-2: Implement the functionality to copy a file or directory to another location.
        You may need to handle exceptions and print relevant error messages.
        You may use the file_exists() method to check if the destination file already exists.
        """
        try:
            # if -v is given, print the file transition process.
            # It does not matter whether the transition was successful.
            if '-v' in self.options:
                print("%s: copying '%s' to '%s'" 
                      %(self.name, self.source_dir, self.destination_dir))
            
            # Check if the file exists in the source directory.
            if not self.file_exists(self.current_path, self.source_dir):
                raise FileNotFoundError()
            
            origin = os.path.join(self.current_path, self.source_dir)
            target = os.path.join(self.current_path, self.destination_dir)
            
            # If -i is given and the file already exists in the destination directory,
            # provide the overwrite option (y/n).
            if '-i' in self.options:
                if self.file_exists(self.destination_dir, self.source_dir):
                    print("%s: overwrite '%s/%s'? (y/n)"
                          %(self.name, self.destination_dir, self.source_dir))
                    
                    answer = input(">> ")
                    if answer == "y":
                        shutil.copy(origin, target)
                    else:
                        pass
                else:
                    shutil.copy(origin, target)
            else:
                shutil.copy(origin, target)

        except FileNotFoundError as e:
            print("%s: '%s' does not exist."
                  %(self.name, self.source_dir))
        

    def file_exists(self, directory: str, file_name: str) -> bool:
        """
        Check if a file exists in a directory.
        Feel free to use this method in your execute() method.

        Args:
            directory (str): The directory to check.
            file_name (str): The name of the file.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        file_path = os.path.join(directory, file_name)
        return os.path.exists(file_path)
