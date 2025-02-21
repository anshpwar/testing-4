"""cffi ABI-mode binding for build/libagg.{dylib,so}. The cdef mirrors c/include/agg.h."""
import pathlib
import subprocess
import sys

from cffi import FFI

ROOT = pathlib.Path(__file__).resolve().parent.parent
_EXT = "dylib" if sys.platform == "darwin" else "so"
LIB_PATH = ROOT / "build" / f"libagg.{_EXT}"

CDEF = """
typedef struct {
    int64_t count;
    double sum;
    double mean;
    double m2;
    double min;
    double max;
} agg_stats;

typedef struct {
    double lo;
    double hi;
    int32_t buckets;
    int32_t pad;
    int64_t counts[64];
    int64_t total;
} agg_hist;

int agg_stats_init(agg_stats *s);
int agg_stats_push(agg_stats *s, double x);
int agg_stats_variance(const agg_stats *s, double *out);
int agg_stats_merge(agg_stats *out, const agg_stats *a, const agg_stats *b);

int agg_hist_init(agg_hist *h, double lo, double hi, int32_t buckets);
int agg_hist_push(agg_hist *h, double x);
int agg_hist_percentile(const agg_hist *h, double p, double *out);

int agg_window_sum(const double *xs, size_t n, size_t window, double *out);

size_t agg_sizeof_stats(void);
size_t agg_sizeof_hist(void);
"""

ERRORS = {-1: "invalid argument", -2: "not enough data", -3: "range error"}

ffi = FFI()
ffi.cdef(CDEF)
if not LIB_PATH.exists():
    subprocess.run(["make", "-C", str(ROOT), "-s", "build"], check=True, capture_output=True)
lib = ffi.dlopen(str(LIB_PATH))


class NativeError(Exception):
    def __init__(self, code, what=""):
        self.code = code
        super().__init__(f"{what}: {ERRORS.get(code, code)}" if what else ERRORS.get(code, str(code)))


def check(rc, what=""):
    if rc < 0:
        raise NativeError(rc, what)
    return rc
