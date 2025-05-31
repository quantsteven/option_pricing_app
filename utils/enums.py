from enum import Enum
from typing import Any, List, Literal

Case = Literal["orig", "upper", "lower"]


class BaseEnum(Enum):

    @classmethod
    def to_list(cls, *, case: Case = "orig") -> List[Any]:
        """
        返回成员 value 列表
        case: "orig"  原样   (默认)
              "upper" 转成大写
              "lower" 转成小写
        """
        if case == "orig":
            return [m.value for m in cls]

        if case == "upper":
            return [str(m.value).upper() for m in cls]

        if case == "lower":
            return [str(m.value).lower() for m in cls]

        raise ValueError(f"Unsupported case: {case!r}")

    def upper(self):
        return self.value.upper()

    def lower(self):
        return self.value.lower()

    def capitalize(self):
        return self.value.capitalize()

    def __getitem__(self, idx):
        return self.value[idx]


class EuropeanOptionType(BaseEnum):
    CALL = "call"
    PUT = "put"


class SingleTouchOptionType(BaseEnum):
    OTU = "otu"
    OTD = "otd"
    NTU = "ntu"
    NTD = "ntd"


class DoubleTouchOptionType(BaseEnum):
    DOT = "dot"
    DNT = "dnt"
    OTUNTD = "otuntd"
    OTDNTU = "otdntu"


class SingleBarrierOptionType(BaseEnum):
    UOC = "uoc"
    UIC = "uic"
    UOP = "uop"
    UIP = "uip"
    DOC = "doc"
    DIC = "dic"
    DOP = "dop"
    DIP = "dip"


class DoubleBarrierOptionType(BaseEnum):
    DKOC = "dkoc"
    DKIC = "dkic"
    DKOP = "dkop"
    DKIP = "dkip"

