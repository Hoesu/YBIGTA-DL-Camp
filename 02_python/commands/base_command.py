# commands/base_command.py
import os
from typing import List

"""
TODO 3-1: The BaseCommand class has a show_usage method implemented, but the execute method is not 
implemented and is passed on to the child class. Think about why this difference is made.

Answer: BaseCommand 클래스는 'ls','mv','cp','pwd','grep' 커맨드 클래스들의 부모 클래스입니다.
show_usage 같이 자식들이 모두 공통적으로 가져야할 메소드들은 여기서 구현하면 되지만, execute
메소드는 자식 클래스가 수행하고자 하는 역할에 따라 다르게 구현되어야 합니다. 따라서 여기선
execute를 구현해야 한다는 리마인더 느낌으로 메소드의 틀만 제공해놓고, 자식 클래스에서 각자
목적에 맞게 부모 클래스의 메소드를 오버라이딩 시키면 효율적인 OOP 구조가 완성됩니다.


TODO 3-2: The update_current_path method of the BaseCommand class is slightly different from other methods. 
It has a @classmethod decorator and takes a cls argument instead of self. In Python, this is called a 
class method, and think about why it was implemented as a class method instead of a normal method.

Answer: update_current_path를 클래스 메소드로 정의해서 사용하는 이유는 클래스 변수로 선언된
current_path를 클래스의 인스턴스 생성 없이 엑세스해서 변경할 수 있게 하기 위함입니다.
이렇게 하면 BaseCommand의 하위 클래스들은 모두 같은 current_path를 가지게 되고,
BaseCommand.update_current_path 선언을 하면 current_path를 한번에 업데이트하고 공유할 수 있습니다.
JAVA에서 static method, variable이 하는 역할과 비슷합니다.

"""
class BaseCommand:
    """
    Base class for all commands. Each command should inherit from this class and 
    override the execute() method.
    
    For example, the MoveCommand class overrides the execute() method to implement 
    the mv command.

    Attributes:
        current_path (str): The current path. Usefull for commands like ls, cd, etc.
    """

    current_path = os.getcwd()

    @classmethod
    def update_current_path(cls, new_path: str):
        """
        Update the current path.
        You need to understand how class methods work.

        Args:
            new_path (str): The new path. (Must be an relative path)
        """
        BaseCommand.current_path = os.path.join(BaseCommand.current_path, new_path)

    def __init__(self, options: List[str], args: List[str]) -> None:
        """
        Initialize a new instance of BaseCommand.

        Args:
            options (List[str]): The command options (e.g. -v, -i, etc.)
            args (List[str]): The command arguments (e.g. file names, directory names, etc.)
        """
        self.options = options
        self.args = args
        self.description = 'Helpful description of the command'
        self.usage = 'Usage: command [options] [arguments]'

    def show_usage(self) -> None:
        """
        Show the command usage.
        """
        print(self.description)
        print(self.usage)

    def execute(self) -> None:
        """
        Execute the command. This method should be overridden by each subclass.
        """
        raise NotImplementedError