from .base_command import BaseCommand
import os
import shutil
from typing import List

class MoveCommand(BaseCommand):
    def __init__(self, options: List[str], args: List[str]) -> None:
        """
        Initialize the MoveCommand object.

        Args:
            options (List[str]): List of command options.
            args (List[str]): List of command arguments.
        """
        super().__init__(options, args)

        # Override the attributes inherited from BaseCommand
        self.description = 'Move a file or directory to another location'
        self.usage = 'Usage: mv [source] [destination]'
        self.name = 'mv'
        self.options = options
        self.source_dir = self.args[0]
        self.destination_dir = self.args[1]

    def execute(self) -> None:
        """
        Execute the move command.
        Supported options:
            -i: Prompt the user before overwriting an existing file.
            -v: Enable verbose mode (print detailed information)
        """
        try:
            # if -v is given, print the file transition process.
            # It does not matter whether the transition was successful.
            if '-v' in self.options:
                print("%s: moving '%s' to '%s'" 
                      %(self.name, self.source_dir, self.destination_dir))
            
            # Check if the file exists in the source directory.
            if not self.file_exists(self.current_path, self.source_dir):
                raise FileNotFoundError()
            
            origin = os.path.join(self.current_path, self.source_dir)
            target = os.path.join(self.current_path, self.destination_dir)
            copy = os.path.join(self.current_path, self.destination_dir, self.source_dir)
            
            # If -i is given and the file already exists in the destination directory,
            # provide the overwrite option (y/n).
            if '-i' in self.options:
                if self.file_exists(self.destination_dir, self.source_dir):
                    print("%s: overwrite '%s'? (y/n)"
                          %(self.name, self.source_dir))
                
                    answer = input(">> ")
                    if answer == "y":
                        os.remove(copy)
                        shutil.move(origin, target)
                    else:
                        pass
                else:
                    shutil.move(origin, target)
            else:
                if self.file_exists(self.destination_dir, self.source_dir):
                    raise FileExistsError()
                else:
                    shutil.move(origin, target)

        except FileNotFoundError as e:
            print("%s: '%s' does not exist."
                  %(self.name, self.source_dir))
        except FileExistsError as e:
            print("%s: cannot move '%s' to '%s': Destination path '%s' already exists."
                  %(self.name, self.source_dir, self.destination_dir,
                    os.path.join(self.destination_dir, self.source_dir)
            ))
    
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
