#include <math.h>

#include "agg.h"

int agg_hist_init(agg_hist *h, double lo, double hi, int32_t buckets)
{
    if (h == NULL || !(hi > lo) || buckets < 1 || buckets > AGG_MAX_BUCKETS)
        return AGG_ERR_ARG;
    h->lo = lo;
    h->hi = hi;
    h->buckets = buckets;
    h->pad = 0;
    h->total = 0;
    for (int i = 0; i < AGG_MAX_BUCKETS; i++)
        h->counts[i] = 0;
    return AGG_OK;
}

int agg_hist_push(agg_hist *h, double x)
{
    if (h == NULL || isnan(x))
        return AGG_ERR_ARG;
    int idx;
    if (x <= h->lo)
        idx = 0;
    else if (x >= h->hi)
        idx = h->buckets - 1;
    else
        idx = (int)((x - h->lo) / (h->hi - h->lo) * h->buckets);
    if (idx >= h->buckets)
        idx = h->buckets - 1;
    h->counts[idx]++;
    h->total++;
    return AGG_OK;
}

int agg_hist_percentile(const agg_hist *h, double p, double *out)
{
    if (h == NULL || out == NULL || p <= 0.0 || p > 100.0)
        return AGG_ERR_ARG;
    if (h->total == 0)
        return AGG_ERR_EMPTY;
    double target = p / 100.0 * (double)h->total;
    double width = (h->hi - h->lo) / h->buckets;
    int64_t seen = 0;
    for (int i = 0; i < h->buckets; i++) {
        seen += h->counts[i];
        if ((double)seen >= target) {
            *out = h->lo + width * (i + 1);
            return AGG_OK;
        }
    }
    *out = h->hi;
    return AGG_OK;
}
