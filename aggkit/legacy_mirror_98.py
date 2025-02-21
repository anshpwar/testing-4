"""Reads exported stats blobs written by the 1.0 agent, using its original struct layout."""
from cffi import FFI

_ffi = FFI()
_ffi.cdef("typedef struct { int64_t count; double mean; double m2; double min; double max; } agg_stats_v1;")


def v1_size():
    return _ffi.sizeof("agg_stats_v1")
