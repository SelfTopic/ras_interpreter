# ras_types.py

class string:
    def __init__(self, value: str):
        self.value = value

    def __repr__(self): # для удобной отладки
        return f"String({self.value})"

class integer:
    def __init__(self, value: int):
        self.value = value

    def __repr__(self):
        return f"Integer({self.value})"

class empty:
    def __init__(self):
        self.value = None

    def __repr__(self):
        return "Empty"

class float_: # Избегаем конфликта с ключевым словом float
    def __init__(self, value: float):
        self.value = value

    def __repr__(self):
        return f"Float({self.value})"

class list_: # Избегаем конфликта с ключевым словом list
    def __init__(self, value: list):
        self.value = value

    def __repr__(self):
        return f"List({self.value})"

class tuple_: # Избегаем конфликта с ключевым словом tuple
    def __init__(self, value: tuple):
        self.value = value
    def __repr__(self):
        return f"Tuple({self.value})"

class dict_: # Избегаем конфликта с ключевым словом dict
    def __init__(self, value: dict):
        self.value = value
    def __repr__(self):
        return f"Dict({self.value})"