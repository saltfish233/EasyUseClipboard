from typing import Optional

x : Optional[str] = "aa"

dic = {"a":1}

try:
    x = dic["b"]
    print(x)
except:
    pass
finally:
    print(x)