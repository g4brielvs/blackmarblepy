import datetime
from pathlib import Path
from typing import List, Optional

import geopandas
import numpy as np
import pandas as pd
from rasterstats import zonal_stats

from .raster import VARIABLE_DEFAULT, bm_raster, transform
from .types import Product


def bm_extract(
    gdf: geopandas.GeoDataFrame,
    product_id: Product,
    date_range: datetime.date | List[datetime.date],
    bearer: str,
    aggfunc: str | List[str] = ["mean"],
    variable: Optional[str] = None,
    drop_values_by_quality_flag: List[int] = [],
    check_all_tiles_exist: bool = True,
    file_directory: Optional[Path] = None,
    file_prefix: Optional[str] = None,
    file_skip_if_exists: bool = True,
):
    """Extract and aggregate nighttime lights zonal statistics from `NASA Black Marble <https://blackmarble.gsfc.nasa.gov>`_.

    Parameters
    ----------
    gdf: geopandas.GeoDataFrame
        Region of interest

    product_id: Product
        NASA Black Marble product suite (VNP46) identifier. The available products are shown in following list:

        - ``VNP46A1``: Daily (raw)
        - ``VNP46A2``: Daily (corrected)
        - ``VNP46A3``: Monthly
        - ``VNP46A4``: Annual

    date_range: datetime.date | List[datetime.date]
        Date range (single date or list of dates) for which to retrieve NASA Black Marble data.

    bearer: str
        NASA Earthdata Bearer token. Please refer to the `documentation <https://worldbank.github.io/blackmarblepy/examples/blackmarblepy.html#nasa-earthdata-bearer-token>`_.

    aggfunc: str | List[str], default=["mean"]
        Which statistics to calculate for each zone. All possible choices are listed in `rasterstats.utils.VALID_STATS <https://pythonhosted.org/rasterstats/rasterstats.html?highlight=zonal_stats#rasterstats.gen>`_.

    variable: str, default = None
        Variable to create GeoTIFF raster. Further information, please see the `NASA Black Marble User Guide <https://ladsweb.modaps.eosdis.nasa.gov/api/v2/content/archives/Document%20Archive/Science%20Data%20Product%20Documentation/VIIRS_Black_Marble_UG_v1.2_April_2021.pdf>`_ for `VNP46A1`, see Table 3; for `VNP46A2` see Table 6; for `VNP46A3` and `VNP46A4`, see Table 9. By default, it uses the following default variables:

        - For ``VNP46A1``, uses ``DNB_At_Sensor_Radiance_500m``
        - For ``VNP46A2``, uses ``Gap_Filled_DNB_BRDF-Corrected_NTL``
        - For ``VNP46A3``, uses ``NearNadir_Composite_Snow_Free``.
        - For ``VNP46A4``, uses ``NearNadir_Composite_Snow_Free``.

    drop_values_by_quality_flag: List[int], optional
        List of the quality flag values for which to drop data values. Each pixel has a quality flag value, where low quality values can be removed. Values are set to ``NA`` for each value in the list.

        For ``VNP46A1`` and ``VNP46A2`` (daily data):

        - ``0``: High-quality, Persistent nighttime lights
        - ``1``: High-quality, Ephemeral nighttime Lights
        - ``2``: Poor-quality, Outlier, potential cloud contamination, or other issues
        - ``255``: No retrieval, Fill value (masked out on ingestion)

        For ``VNP46A3`` and ``VNP46A4`` (monthly and annual data):

        - ``0``: Good-quality, The number of observations used for the composite is larger than 3
        - ``1``: Poor-quality, The number of observations used for the composite is less than or equal to 3
        - ``2``: Gap filled NTL based on historical data
        - ``255``: Fill value

    check_all_tiles_exist: bool, default=True
        Check whether all Black Marble nighttime light tiles exist for the region of interest. Sometimes not all tiles are available, so the full region of interest may not be covered. By default (True), it skips cases where not all tiles are available.

    file_directory: pathlib.Path, optional
        Where to produce output. By default, the output will be produced onto a temporary directory.

    file_directory_prefix: str, optional
        Prefix

    file_skip_if_exists: bool, default=True
        Whether to skip downloading or extracting data if the data file for that date already exists.

     bearer
    Returns
    -------
    pandas.DataFrame
        Zonal statistics dataframe
    """
    if variable is None:
        variable = VARIABLE_DEFAULT.get(Product(product_id))

    dataset = bm_raster(
        gdf,
        product_id,
        date_range,
        bearer,
        variable,
        drop_values_by_quality_flag,
        check_all_tiles_exist,
        file_directory,
        file_prefix,
        file_skip_if_exists,
    )

    results = []
    for time in dataset["time"]:
        da = dataset[variable].sel(time=time)

        # Perform zonal statistics
        zonal_statistics = zonal_stats(
            gdf,
            da.values,
            nodata=np.nan,
            affine=transform(da),
            stats=aggfunc,
        )
        # Convert the statistics to a DataFrame and add the prefix 'ntl_'
        zonal_statistics_df = pd.DataFrame(zonal_statistics).add_prefix("ntl_")

        # Concatenate the GeoDataFrame with the zonal statistics
        zonal_statistics_df = pd.concat([gdf, zonal_statistics_df], axis=1)
        zonal_statistics_df["date"] = time.values

        results.append(zonal_statistics_df)

    return pd.concat(results)
