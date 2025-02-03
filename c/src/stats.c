#include <float.h>
#include <math.h>

#include "agg.h"

int agg_stats_init(agg_stats *s)
{
    if (s == NULL)
        return AGG_ERR_ARG;
    s->count = 0;
    s->mean = 0.0;
    s->m2 = 0.0;
    s->min = DBL_MAX;
    s->max = -DBL_MAX;
    return AGG_OK;
}

int agg_stats_push(agg_stats *s, double x)
{
    if (s == NULL || isnan(x))
        return AGG_ERR_ARG;
    s->count++;
    double delta = x - s->mean;
    s->mean += delta / (double)s->count;
    s->m2 += delta * (x - s->mean);
    if (x < s->min)
        s->min = x;
    if (x > s->max)
        s->max = x;
    return AGG_OK;
}

int agg_stats_variance(const agg_stats *s, double *out)
{
    if (s == NULL || out == NULL)
        return AGG_ERR_ARG;
    if (s->count < 2)
        return AGG_ERR_EMPTY;
    *out = s->m2 / (double)(s->count - 1);
    return AGG_OK;
}

int agg_stats_merge(agg_stats *out, const agg_stats *a, const agg_stats *b)
{
    if (out == NULL || a == NULL || b == NULL)
        return AGG_ERR_ARG;
    agg_stats r;
    if (a->count == 0) {
        r = *b;
    } else if (b->count == 0) {
        r = *a;
    } else {
        int64_t n = a->count + b->count;
        double delta = b->mean - a->mean;
        r.count = n;
        r.mean = a->mean + delta * (double)b->count / (double)n;
        r.m2 = a->m2 + b->m2 + delta * delta * (double)a->count * (double)b->count / (double)n;
        r.min = a->min < b->min ? a->min : b->min;
        r.max = a->max > b->max ? a->max : b->max;
    }
    *out = r;
    return AGG_OK;
}

int agg_window_sum(const double *xs, size_t n, size_t window, double *out)
{
    if (xs == NULL || out == NULL || window == 0)
        return AGG_ERR_ARG;
    if (window > n)
        return AGG_ERR_RANGE;
    double acc = 0.0;
    for (size_t i = 0; i < window; i++)
        acc += xs[i];
    out[0] = acc;
    for (size_t i = window; i < n; i++) {
        acc += xs[i] - xs[i - window];
        out[i - window + 1] = acc;
    }
    return AGG_OK;
}

size_t agg_sizeof_stats(void) { return sizeof(agg_stats); }
size_t agg_sizeof_hist(void) { return sizeof(agg_hist); }
