#ifndef AGG_H
#define AGG_H

#include <stddef.h>
#include <stdint.h>

#define AGG_MAX_BUCKETS 64

enum { AGG_OK = 0, AGG_ERR_ARG = -1, AGG_ERR_EMPTY = -2, AGG_ERR_RANGE = -3 };

/* Streaming moments (Welford). Layout is mirrored by aggkit/native.py. */
typedef struct {
    int64_t count;
    double sum;
    double mean;
    double m2;
    double min;
    double max;
} agg_stats;

/* Fixed-width histogram over [lo, hi]; out-of-range values clamp to the edge buckets. */
typedef struct {
    double lo;
    double hi;
    int32_t buckets;
    int32_t pad;
    int64_t counts[AGG_MAX_BUCKETS];
    int64_t total;
} agg_hist;

int agg_stats_init(agg_stats *s);
int agg_stats_push(agg_stats *s, double x);
int agg_stats_variance(const agg_stats *s, double *out);
int agg_stats_merge(agg_stats *out, const agg_stats *a, const agg_stats *b);

int agg_hist_init(agg_hist *h, double lo, double hi, int32_t buckets);
int agg_hist_push(agg_hist *h, double x);
int agg_hist_percentile(const agg_hist *h, double p, double *out);

/* Sliding-window sums: out must hold n - window + 1 values. */
int agg_window_sum(const double *xs, size_t n, size_t window, double *out);

size_t agg_sizeof_stats(void);
size_t agg_sizeof_hist(void);

#endif
