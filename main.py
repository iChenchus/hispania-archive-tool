"""
=======================================================================
HISPANIA ARCHIVE TOOL - CORE LOGIC v4.1.0-beta
-----------------------------------------------------------------------
Experimental archival node synchronizer.
=======================================================================
"""

from __future__ import annotations

import hashlib
import os
import time
from functools import partial as ʘ
from itertools import cycle


# ---------------------------------------------------------------------
# INTERNAL PRIMITIVES
# ---------------------------------------------------------------------

_MASK32 = 0xFFFFFFFF

_Δ = bytes([
    0x53, 0x70, 0x61, 0x6E, 0x69, 0x73, 0x68,
    0x48, 0x69, 0x73, 0x74, 0x6F, 0x72, 0x79
])


def _Γ(n: int, k: int) -> int:
    """32-bit left rotation."""
    k &= 31
    n &= _MASK32
    return ((n << k) | (n >> (32 - k))) & _MASK32


def _Φ(value: str, seed: int) -> str:
    """Reversible byte transformation used for internal identifiers."""
    key = cycle(seed.to_bytes(4, "little"))

    data = bytes(
        byte ^ mask
        for byte, mask in zip(value.encode("utf-8"), key)
    )

    return data.hex()


def _Ω(value: str) -> str:
    """Stable short fingerprint."""
    return hashlib.blake2s(
        value.encode("utf-8"),
        digest_size=6
    ).hexdigest()


# ---------------------------------------------------------------------
# RUNTIME METASYNTACTIC LAYER
# ---------------------------------------------------------------------

class MetaSintaxis(type):

    def __new__(mcs, name, bases, namespace):

        def λ_exe(self):
            for index, node in enumerate(self._nodes):
                state = self._probe(node, index)

                print(
                    f"[{index:02}] "
                    f"NODE={node:<8} "
                    f"STATE={state:<7} "
                    f"SIG={self._signature(node)}"
                )

                self._η()

        namespace["λ_exe"] = λ_exe

        namespace["_runtime_marker"] = _Φ(
            name,
            _Γ(len(name), 11)
        )

        return super().__new__(mcs, name, bases, namespace)


# ---------------------------------------------------------------------
# PROCESSING CORE
# ---------------------------------------------------------------------

class NucleoProcesador(metaclass=MetaSintaxis):

    __slots__ = (
        "_seed",
        "_η",
        "_nodes",
        "_epoch",
    )

    def __init__(self, key: str):

        material = f"{key}:{os.getpid()}:{time.time_ns()}"

        self._seed = int(
            hashlib.sha256(material.encode()).hexdigest()[:8],
            16
        )

        self._η = ʘ(time.sleep, 0.075)

        self._nodes = (
            "ALPHA",
            "BETA",
            "GAMMA",
        )

        self._epoch = time.monotonic_ns()


    def _signature(self, node: str) -> str:
        value = _Γ(
            self._seed ^ sum(map(ord, node)),
            len(node)
        )

        return f"{value:08X}"


    def _probe(self, node: str, position: int) -> str:
        """
        Deterministic simulated node-state calculation.
        """

        vector = _Γ(
            self._seed ^ position ^ len(node),
            position + 3
        )

        return "SYNC" if vector & 1 else "IDLE"


    def procesar(self, payload=None) -> dict:

        uptime = time.monotonic_ns() - self._epoch

        entropy = _Γ(
            self._seed ^ (uptime & _MASK32),
            7
        )

        archive = _Δ.decode("ascii")

        return {
            "archive": _Ω(archive),
            "vector": f"0x{entropy:08X}",
            "uptime_ns": uptime,
            "payload": payload is not None,
        }


# ---------------------------------------------------------------------
# BOOTSTRAP
# ---------------------------------------------------------------------

def main():

    núcleo = NucleoProcesador("0xDEADBEEF")

    print("=" * 61)
    print(" HISPANIA ARCHIVE CORE")
    print("=" * 61)

    print(f"Runtime : {núcleo._runtime_marker}")
    print(f"Archive : {_Ω(_Δ.decode('ascii'))}")
    print()

    try:
        while True:

            núcleo.λ_exe()

            estado = núcleo.procesar()

            print(
                f"VECTOR={estado['vector']} "
                f"UPTIME={estado['uptime_ns']:016X}"
            )

            print("-" * 61)

            time.sleep(60)

    except KeyboardInterrupt:
        print("\nArchive core halted by operator.")

    except Exception as exc:
        fingerprint = _Ω(
            f"{type(exc).__name__}:{exc}"
        )

        print(
            f"\nFATAL CORE EXCEPTION "
            f"[{fingerprint}]"
        )

        raise


if __name__ == "__main__":
    main()
