from __future__ import annotations

import random
from string import ascii_lowercase
from typing import ClassVar


class UniqueNames:
    _names: ClassVar[dict[str, bool]] = {}

    vowels: str = "eyuioa"
    consonants: str = "".join(list(set(ascii_lowercase).difference(set(vowels))))

    @classmethod
    def generate(cls) -> str:
        while cls._names.get(name := "".join(
            "".join((
                *random.choices(cls.consonants, k=random.randint(2, 2)),   # noqa: S311
                random.choice(cls.vowels),   # noqa: S311
            )) for _ in range(random.randint(2, 4))   # noqa: S311
        )):
            pass
        cls._names[name] = True
        return name


if __name__ == "__main__":
    print(UniqueNames.generate())
