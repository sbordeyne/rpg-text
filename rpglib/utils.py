import sys
import time
import math
import os
import random
import re


def display(text, delay=0.05):
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(delay)


class Vector2:
    def __init__(self, *args):
        if len(args) == 2:
            self.x = args[0]
            self.y = args[1]
        elif len(args) == 1:
            if isinstance(args[0], Vector2):
                self.x, self.y = args[0].x, args[0].y
            else:
                self.x, self.y = args[0]
        else:
            raise ValueError

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise IndexError

    def __iter__(self):
        return iter(self.tuple)

    def __add__(self, other):
        other = Vector2(other)
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        other = Vector2(other)
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector2(other * self.x, other * self.y)
        else:
            raise ValueError

    def __str__(self):
        return f"Vector2({self.x}, {self.y})"

    def __div__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector2(self.x / other, self.y / other)
        else:
            raise ValueError

    def __bool__(self):
        return self.x and self.y

    def __eq__(self, other):
        other = Vector2(other)
        return other.x == self.x and other.y == self.y

    def __abs__(self):
        return Vector2(abs(self.x), abs(self.y))

    @property
    def magnitude(self):
        return math.sqrt(self.magnitudesq)

    @property
    def magnitudesq(self):
        return self.x * self.x + self.y * self.y

    @property
    def str_values(self):
        return f"({self.x}, {self.y})"

    def dot(self, other):
        other = Vector2(other)
        return self.x * other.x + self.y * other.y

    @property
    def tuple(self):
        return self.x, self.y

    def angle_to(self, other):
        other = Vector2(other)
        return math.acos(self.dot(other)/(self.magnitude*other.magnitude))

    def distance(self, other):
        return math.sqrt(self.distancesq(other))

    def distancesq(self, other):
        other = Vector2(other)
        return (self.x - other.x) * (self.x - other.x) + (self.y - other.y) * (self.y - other.y)

    def clamp(self, minimum=(0, 0), maximum=None):
        if maximum is None:
            raise ValueError
        if isinstance(minimum, tuple):
            minimum = Vector2(minimum)
        if isinstance(maximum, tuple):
            maximum = Vector2(maximum)
        rvx = self.x
        rvy = self.y
        if self.x >= maximum.x:
            rvx = maximum.x
        if self.x <= minimum.x:
            rvx = minimum.x
        if self.y >= maximum.y:
            rvy = maximum.y
        if self.y <= minimum.y:
            rvy = minimum.y
        self.x, self.y = rvx, rvy


class InvalidInputError(Exception):
    pass


class RetryCountExceededError(Exception):
    pass


def sanitized_input(message="", cast_obj=None, n_retries=-1, error_msg="", valid_input=[]):
    """
         Function sanitized_input :
         @args
             message: string to show the user (default: "")
             cast_obj: an object to cast the string into. Object must have an __init__
                       method that can take a string as the first positionnal argument.
                       object should raise a ValueError exception if a string can't be cast into
                       that object (default: str)
             n_retries: number of retries. No limit if n_retries < 0 (default: -1)
             error_msg: message to show the user before asking the input again in
                        case an error occurs (default: repr of the exception)
             valid_input: an iterable to check if the result is allowed.
        @returns
           rv : string literal casted into the cast_obj as per that object's rules.
           raises : RetryCountExceededError if the retry count has exceeded the n_retries limit.
    """
    raw = ""
    retry_cnt = 0
    cast_obj = cast_obj if cast_obj is not None else str
    if not hasattr(valid_input, '__iter__'):
        valid_input = (valid_input, )
    while (retry_cnt < n_retries) or n_retries < 0:
        try:
            raw = input(message)
            rv = cast_obj(raw)
            if not valid_input or rv in valid_input:
                return rv
            else:
                raise InvalidInputError(f"InvalidInputError: input invalid in function 'sanitized_input' of {__name__}")
        except ValueError as e:
            if error_msg:
                print(error_msg)
            else:
                print(repr(e))
            retry_cnt += 1
            continue
        except InvalidInputError as e:
            if error_msg:
                print(error_msg)
            else:
                print(repr(e))
            retry_cnt += 1
            continue
    raise RetryCountExceededError(f"RetryCountExceededError : count exceeded in function 'sanitized_input' of {__name__}")


def clear_screen():
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')


class MaxLenList:
    def __init__(self, maxlen, iterable=None):
        if iterable is None:
            iterable = [None] * maxlen
        self.maxlen = maxlen
        self.items = iterable
        self.index = 0

    def __iter__(self):
        return self.items

    def __getitem__(self, item):
        if not isinstance(item, int):
            raise IndexError

        if item > self.maxlen:
            raise IndexError

        return self.items[item]

    def __contains__(self, item):
        return item in self.items

    def append(self, item):
        if self.index < len(self.items):
            self.items[self.index] = item
            self.index += 1
            return
        else:
            self.items.append(item)
            return self.items.pop(0)

    def pop(self, index=None):
        if index is None:
            index = self.index
        item = self.items[index]
        self.items[index] = None
        self.index -= 1
        return item


def parse_dice_format(dice_format):
    dice_format = dice_format.replace(" ", "")
    n_dice, rest = dice_format.split("d")
    n_dice = int(n_dice) if n_dice else 1
    n_faces, mod = rest.split("+")
    n_faces = int(n_faces)
    mod = int(mod)
    return sum([random.randint(1, n_faces) for i in range(n_dice)]) + mod


def interpolate_brackets(string, **data):
    for key, value in data.items():
        pattern = '[' + key + ']'
        re.sub(pattern, string)
    return string
