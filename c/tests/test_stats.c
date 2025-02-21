#include <math.h>

#include "agg.h"
#include "check.h"

static int near(double a, double b) { return fabs(a - b) < 1e-9; }

static void test_moments(void)
{
    agg_stats s;
    double v;
    CHECK_EQ(agg_stats_init(&s), AGG_OK);
    CHECK_EQ(agg_stats_variance(&s, &v), AGG_ERR_EMPTY);
    double xs[] = {2, 4, 4, 4, 5, 5, 7, 9};
    for (int i = 0; i < 8; i++)
        CHECK_EQ(agg_stats_push(&s, xs[i]), AGG_OK);
    CHECK_EQ(s.count, 8);
    CHECK(near(s.mean, 5.0));
    CHECK_EQ(agg_stats_variance(&s, &v), AGG_OK);
    CHECK(near(v, 32.0 / 7.0));
    CHECK(near(s.min, 2.0));
    CHECK(near(s.max, 9.0));
}

static void test_rejects_nan_and_null(void)
{
    agg_stats s;
    agg_stats_init(&s);
    CHECK_EQ(agg_stats_push(&s, NAN), AGG_ERR_ARG);
    CHECK_EQ(agg_stats_push(NULL, 1.0), AGG_ERR_ARG);
    CHECK_EQ(s.count, 0);
}

static void test_merge_matches_single_pass(void)
{
    agg_stats a, b, m, whole;
    agg_stats_init(&a);
    agg_stats_init(&b);
    agg_stats_init(&whole);
    for (int i = 1; i <= 10; i++) {
        agg_stats_push(i <= 4 ? &a : &b, (double)i * 1.5);
        agg_stats_push(&whole, (double)i * 1.5);
    }
    CHECK_EQ(agg_stats_merge(&m, &a, &b), AGG_OK);
    CHECK_EQ(m.count, whole.count);
    CHECK(near(m.mean, whole.mean));
    CHECK(near(m.m2, whole.m2));
    CHECK(near(m.min, whole.min) && near(m.max, whole.max));
}

static void test_merge_with_empty(void)
{
    agg_stats a, e, m;
    agg_stats_init(&a);
    agg_stats_init(&e);
    agg_stats_push(&a, 3.0);
    CHECK_EQ(agg_stats_merge(&m, &a, &e), AGG_OK);
    CHECK_EQ(m.count, 1);
    CHECK_EQ(agg_stats_merge(&m, &e, &a), AGG_OK);
    CHECK(near(m.mean, 3.0));
}

static void test_window_sum(void)
{
    double xs[] = {1, 2, 3, 4, 5};
    double out[3];
    CHECK_EQ(agg_window_sum(xs, 5, 3, out), AGG_OK);
    CHECK(near(out[0], 6) && near(out[1], 9) && near(out[2], 12));
    CHECK_EQ(agg_window_sum(xs, 5, 6, out), AGG_ERR_RANGE);
    CHECK_EQ(agg_window_sum(xs, 5, 0, out), AGG_ERR_ARG);
}

static void test_layout(void)
{
    CHECK_EQ(agg_sizeof_stats(), sizeof(agg_stats));
    CHECK_EQ(sizeof(agg_stats), 48);
}

int main(void)
{
    test_moments();
    test_rejects_nan_and_null();
    test_merge_matches_single_pass();
    test_merge_with_empty();
    test_window_sum();
    test_layout();
    CHECK_DONE();
}
