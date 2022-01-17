
from collections import namedtuple
from typing import List
import main

_allowed_chars = [char for char in "0123456789.()UIui "]

class _StackFrame:
    def __init__(self, operand: main.Propability, op: str) -> None:
        self.operand = operand
        self.op = op
        pass

def _empty_frame() -> _StackFrame:
    return _StackFrame(None, None)

def _validate_text_chars(text: str) -> None:
    for c in text:
        if c not in _allowed_chars:
            pos = text.partition(c)
            raise Exception("Unidentified char {} at {}_{}_{}".format(c, *pos))
    open_count = text.count('(')
    close_count = text.count(')')
    if open_count != close_count:
        raise Exception("Illformatted query: brackets not valid")

def _get_tokens(text: str) -> str:
    word = ''
    for char in text:
        char = char.capitalize()
        if char == ' ':
            if word:
                yield word
                word = ''
            continue
        elif char in ['U', 'I', ')', '(']:
            if word:
                yield word
            word = ''
            yield char
            continue
        else:
            word += char
    if word:
        yield word

def _evaluate(op1: main.Propability, op2: main.Propability, op: str) -> main.Propability:
    if op == 'U':
        return main.Union(op1, op2)
    elif op == 'I':
        return main.Intersection(op1, op2)
    else:
        raise Exception("Invalid operation {}".format(op))

def _evaluate_text(text: str) -> main.Propability:

    stack: List[_StackFrame] = []
    current_frame = _empty_frame()

    def handle_new_operand(operand: main.Propability, current_frame: _StackFrame) -> _StackFrame:
        if current_frame.operand:
            lhs = current_frame.operand
            rhs = operand
            new_operand = _evaluate(lhs, rhs, current_frame.op)
            return _StackFrame(new_operand, None) 
        else:
            return _StackFrame(operand, None)

    for token in _get_tokens(text):
        if token in ['U', 'I']:
            current_frame.op = token
        elif token == '(':
            stack.append(current_frame)
            current_frame = _empty_frame()
        elif token == ')':
            last_frame = current_frame
            current_frame = stack.pop()
            current_frame = handle_new_operand(last_frame.operand, current_frame)
        else:
            prop = float(token) / 100
            operand = main.Single(prop)
            current_frame = handle_new_operand(operand, current_frame)
    
    return current_frame.operand
    

def process_text(text: str) -> main.Propability:
    text = ' '.join(text.split()).strip()
    _validate_text_chars(text)
    return _evaluate_text(text)