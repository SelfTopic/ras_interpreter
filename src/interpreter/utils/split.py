# спиздил с чатгпт, не проверял, чекнешь
# params("param1 :integer: ++ param2 :string++integer: << 12345++param3:bool ++ integer:") ->
# -> ["param1 :integer:", "param2 :string++integer: << 12345", "param3:bool ++ integer:"]

import re

example_string = "param1 :integer: ++ param2 :string++integer: << 12345++param3:bool ++ integer:"

def params(s):
  parts = re.split(r"\s*\+\+\s*", s)
  result = []
  current = ""
  in_colon = False
  for part in parts:
    if ":" in part:
      # Проверяем, сколько раз открывается и закрывается двоеточие в текущей части
      open_colons = part.count(":") % 2 != 0
      if not in_colon:
        current = part
        in_colon = open_colons
      else:
        current += "++" + part
        in_colon = open_colons  #Обновляем статус, если внутри текущего фрагмента были парные двоеточия
      if not in_colon:
          result.append(current)
          current = ""
    else:
      if in_colon:
        current += "++" + part
      else:
        result.append(part)

  if current: #Добавляем остаток, если остались не обработанные части
    result.append(current)

  return [part.strip() for part in result if part.strip()]