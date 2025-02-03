#include <math.h>
#include <stddef.h>

#include "agg.h"
#include "check.h"

static void test_init_validation(void)
{
    agg_hist h;
    CHECK_EQ(agg_hist_init(&h, 0, 10, 10), AGG_OK);
    CHECK_EQ(agg_hist_init(&h, 5, 5, 10), AGG_ERR_ARG);
    CHECK_EQ(agg_hist_init(&h, 0, 10, 0), AGG_ERR_ARG);
    CHECK_EQ(agg_hist_init(&h, 0, 10, AGG_MAX_BUCKETS + 1), AGG_ERR_ARG);
    CHECK_EQ(agg_hist_init(NULL, 0, 10, 5), AGG_ERR_ARG);
}

static void test_bucketing_and_clamping(void)
{
    agg_hist h;
    agg_hist_init(&h, 0, 100, 10);
    agg_hist_push(&h, 5);
    agg_hist_push(&h, 15);
    agg_hist_push(&h, 99.9);
    agg_hist_push(&h, -50);
    agg_hist_push(&h, 500);
    CHECK_EQ(h.total, 5);
    CHECK_EQ(h.counts[0], 2);
    CHECK_EQ(h.counts[1], 1);
    CHECK_EQ(h.counts[9], 2);
    CHECK_EQ(agg_hist_push(&h, NAN), AGG_ERR_ARG);
}

static void test_percentiles(void)
{
    agg_hist h;
    double p;
    agg_hist_init(&h, 0, 100, 10);
    CHECK_EQ(agg_hist_percentile(&h, 50, &p), AGG_ERR_EMPTY);
    for (int i = 0; i < 100; i++)
        agg_hist_push(&h, i + 0.5);
    CHECK_EQ(agg_hist_percentile(&h, 50, &p), AGG_OK);
    CHECK(fabs(p - 50.0) < 1e-9);
    CHECK_EQ(agg_hist_percentile(&h, 99, &p), AGG_OK);
    CHECK(fabs(p - 100.0) < 1e-9);
    CHECK_EQ(agg_hist_percentile(&h, 0, &p), AGG_ERR_ARG);
    CHECK_EQ(agg_hist_percentile(&h, 100.5, &p), AGG_ERR_ARG);
}

static void test_layout(void)
{
    CHECK_EQ(agg_sizeof_hist(), sizeof(agg_hist));
    CHECK_EQ(offsetof(agg_hist, counts), 24);
}

int main(void)
{
    test_init_validation();
    test_bucketing_and_clamping();
    test_percentiles();
    test_layout();
    CHECK_DONE();
}
