"""
Frame class to manage function frame information in code generation.
"""

from typing import List
from .error import IllegalRuntimeException


class Frame:
    """
    Frame class to manage function frame information in code generation.
    
    Attributes:
        name (str): Name of the function
        return_type: Return type of the function
        current_label (int): Current label
        curr_op_stack_size (int): Current size of operand stack
        max_op_stack_size (int): Maximum size of operand stack
        curr_index (int): Current index of local variable
        max_index (int): Maximum index used
        start_label (List[int]): Stack containing start labels of scopes
        end_label (List[int]): Stack containing end labels of scopes
        index_local (List[int]): Stack containing local indices of scopes
        con_label (List[int]): Stack containing continue labels of loops
        brk_label (List[int]): Stack containing break labels of loops
    """
    
    def __init__(self, name: str, return_type):
        """
        Initialize Frame.
        
        Args:
            name: Name of the function
            return_type: Return type of the function
        """
        self.name = name
        self.return_type = return_type
        self.current_label = 0
        self.curr_op_stack_size = 0
        self.max_op_stack_size = 0
        self.curr_index = 0
        self.max_index = 0
        self.start_label: List[int] = []
        self.end_label: List[int] = []
        self.index_local: List[int] = []
        self.con_label: List[int] = []
        self.brk_label: List[int] = []

    def get_curr_index(self) -> int:
        """Return current index."""
        return self.curr_index

    def set_curr_index(self, index: int) -> None:
        """Set current index."""
        self.curr_index = index

    def get_new_label(self) -> int:
        """Return a new label in the function."""
        tmp = self.current_label
        self.current_label = self.current_label + 1
        return tmp

    def push(self) -> None:
        """Simulate an instruction that pushes a value onto operand stack."""
        self.curr_op_stack_size = self.curr_op_stack_size + 1
        if self.max_op_stack_size < self.curr_op_stack_size:
            self.max_op_stack_size = self.curr_op_stack_size

    def pop(self) -> None:
        """
        Simulate an instruction that pops a value out of operand stack.
        
        Raises:
            IllegalRuntimeException: When stack is empty
        """
        self.curr_op_stack_size = self.curr_op_stack_size - 1
        if self.curr_op_stack_size < 0:
            raise IllegalRuntimeException("Pop empty stack")

    def get_stack_size(self) -> int:
        """Return current stack size."""
        return self.curr_op_stack_size

    def get_max_op_stack_size(self) -> int:
        """Return the maximum size of the operand stack."""
        return self.max_op_stack_size

    def check_op_stack(self) -> None:
        """Check if the operand stack is empty."""
        if self.curr_op_stack_size != 0:
            raise IllegalRuntimeException("Stack not empty")

    def enter_scope(self, is_proc: bool) -> None:
        """
        Invoked when parsing into a new scope inside a function.
        
        Args:
            is_proc: Boolean indicating whether this is a procedure (function)
        """
        start = self.get_new_label()
        end = self.get_new_label()
        self.start_label.append(start)
        self.end_label.append(end)
        self.index_local.append(self.curr_index)
        if is_proc:
            self.max_op_stack_size = 0
            self.max_index = 0

    def exit_scope(self) -> None:
        """
        Invoked when parsing out of a scope in a function.
        
        Raises:
            IllegalRuntimeException: When there is an error exiting scope
        """
        if not self.start_label or not self.end_label or not self.index_local:
            raise IllegalRuntimeException("Error when exit scope")
        self.start_label.pop()
        self.end_label.pop()
        self.curr_index = self.index_local.pop()

    def get_start_label(self) -> int:
        """Return the starting label of the current scope."""
        if not self.start_label:
            raise IllegalRuntimeException("None start label")
        return self.start_label[-1]

    def get_end_label(self) -> int:
        """Return the ending label of the current scope."""
        if not self.end_label:
            raise IllegalRuntimeException("None end label")
        return self.end_label[-1]

    def get_new_index(self) -> int:
        """Return a new index for a local variable declared in a scope."""
        tmp = self.curr_index
        self.curr_index = self.curr_index + 1
        if self.curr_index > self.max_index:
            self.max_index = self.curr_index
        return tmp

    def get_max_index(self) -> int:
        """Return the maximum index used in generating code for the current function."""
        return self.max_index

    def enter_loop(self) -> None:
        """Invoked when parsing into a loop statement."""
        con = self.get_new_label()
        brk = self.get_new_label()
        self.con_label.append(con)
        self.brk_label.append(brk)

    def exit_loop(self) -> None:
        """
        Invoked when parsing out of a loop statement.
        
        Raises:
            IllegalRuntimeException: When there is an error exiting loop
        """
        if not self.con_label or not self.brk_label:
            raise IllegalRuntimeException("Error when exit loop")
        self.con_label.pop()
        self.brk_label.pop()

    def get_continue_label(self) -> int:
        """Return the label of the innermost enclosing loop to which continue would jump."""
        if not self.con_label:
            raise IllegalRuntimeException("None continue label")
        return self.con_label[-1]

    def get_break_label(self) -> int:
        """Return the label of the innermost enclosing loop to which break would jump."""
        if not self.brk_label:
            raise IllegalRuntimeException("None break label")
        return self.brk_label[-1]
