from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import pytest
import pytz
import timely_beliefs as tb

from bvp.data.models.assets import Asset, Power
from bvp.data.queries.utils import multiply_dataframe_with_deterministic_beliefs


@pytest.mark.parametrize(
    "query_start, query_end, num_values",
    [
        (
            datetime(2015, 1, 1, tzinfo=pytz.utc),
            datetime(2015, 1, 2, tzinfo=pytz.utc),
            96,
        ),
        (datetime(2015, 1, 1, tzinfo=pytz.utc), None, 96),
        (None, datetime(2015, 1, 2, tzinfo=pytz.utc), 96),
        (None, None, 96),
        (
            datetime(2015, 1, 1, tzinfo=pytz.utc),
            datetime(2015, 1, 1, 12, tzinfo=pytz.utc),
            48,
        ),
        (None, datetime(2015, 1, 1, 12, tzinfo=pytz.utc), 48),
        (
            datetime(1957, 1, 1, tzinfo=pytz.utc),
            datetime(1957, 1, 2, tzinfo=pytz.utc),
            0,
        ),
    ],
)
def test_collect_power(db, app, query_start, query_end, num_values):
    wind_device_1 = Asset.query.filter_by(name="wind-asset-1").one_or_none()
    data = Power.query.filter(Power.asset_id == wind_device_1.id).all()
    print(data)
    bdf: tb.BeliefsDataFrame = Power.collect(
        wind_device_1.name, (query_start, query_end)
    )
    print(bdf)
    assert (
        bdf.index.names[0] == "event_start"
    )  # first index level of collect function should be event_start, so that df.loc[] refers to event_start
    assert pd.api.types.is_timedelta64_dtype(
        bdf.index.get_level_values("belief_horizon")
    )  # dtype of belief_horizon is timedelta64[ns], so the minimum horizon on an empty BeliefsDataFrame is NaT instead of NaN
    assert len(bdf) == num_values
    for v1, v2 in zip(bdf.values, data):
        assert abs(v1[0] - v2.value) < 10 ** -6


@pytest.mark.parametrize(
    "query_start, query_end, resolution, num_values",
    [
        (
            datetime(2015, 1, 1, tzinfo=pytz.utc),
            datetime(2015, 1, 2, tzinfo=pytz.utc),
            timedelta(minutes=15),
            96,
        ),
        (
            datetime(2015, 1, 1, tzinfo=pytz.utc),
            datetime(2015, 1, 2, tzinfo=pytz.utc),
            timedelta(minutes=30),
            48,
        ),
        (
            datetime(2015, 1, 1, tzinfo=pytz.utc),
            datetime(2015, 1, 2, tzinfo=pytz.utc),
            "30min",
            48,
        ),
        (
            datetime(2015, 1, 1, tzinfo=pytz.utc),
            datetime(2015, 1, 2, tzinfo=pytz.utc),
            "PT45M",
            32,
        ),
    ],
)
def test_collect_power_resampled(
    db, app, query_start, query_end, resolution, num_values
):
    wind_device_1 = Asset.query.filter_by(name="wind-asset-1").one_or_none()
    bdf: tb.BeliefsDataFrame = Power.collect(
        wind_device_1.name, (query_start, query_end), resolution=resolution
    )
    print(bdf)
    assert len(bdf) == num_values


def test_multiplication():
    df1 = pd.DataFrame(
        [[30.0, timedelta(hours=3)]],
        index=pd.date_range(
            "2000-01-01 10:00", "2000-01-01 15:00", freq="1h", closed="left"
        ),
        columns=["event_value", "belief_horizon"],
    )
    df2 = pd.DataFrame(
        [[10.0, timedelta(hours=1)]],
        index=pd.date_range(
            "2000-01-01 13:00", "2000-01-01 18:00", freq="1h", closed="left"
        ),
        columns=["event_value", "belief_horizon"],
    )
    df = multiply_dataframe_with_deterministic_beliefs(df1, df2)
    df_compare = pd.concat(
        [
            pd.DataFrame(
                [[np.nan, timedelta(hours=3)]],
                index=pd.date_range(
                    "2000-01-01 10:00", "2000-01-01 13:00", freq="1h", closed="left"
                ),
                columns=["event_value", "belief_horizon"],
            ),
            pd.DataFrame(
                [[300.0, timedelta(hours=1)]],
                index=pd.date_range(
                    "2000-01-01 13:00", "2000-01-01 15:00", freq="1h", closed="left"
                ),
                columns=["event_value", "belief_horizon"],
            ),
            pd.DataFrame(
                [[np.nan, timedelta(hours=1)]],
                index=pd.date_range(
                    "2000-01-01 15:00", "2000-01-01 18:00", freq="1h", closed="left"
                ),
                columns=["event_value", "belief_horizon"],
            ),
        ],
        axis=0,
    )
    pd.testing.assert_frame_equal(df, df_compare)
