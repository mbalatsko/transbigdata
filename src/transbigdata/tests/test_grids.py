import transbigdata as tbd
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon

class TestGrids:
    def setup_method(self):
        self.bounds = [113.6,22.4,113.605,22.405]
        self.params = (113.6, 22.4, 0.004863669213934598, 0.004496605206422906)

    def test_rect_grids(self):
        result = tbd.rect_grids(self.bounds,accuracy = 500)
        res1 = result[0]['geometry'].to_wkt().iloc[0]
        res2 = result[1]
        assert res1=='POLYGON ((113.597568165393 22.39775169739679, 113.602431834607 22.39775169739679, 113.602431834607 22.40224830260321, 113.597568165393 22.40224830260321, 113.597568165393 22.39775169739679))'
        truth = (113.6, 22.4, 0.004863669213934598, 0.004496605206422906)
        assert np.allclose(res2,truth)

    def test_grid_params(self):
        result = tbd.grid_params(self.bounds,accuracy = 500)
        truth = (113.6, 22.4, 0.004863669213934598, 0.004496605206422906)
        assert np.allclose(result,truth)

    def test_GPS_to_grids(self):
        result = tbd.GPS_to_grids(113.7,22.7,self.params)
        truth = (21, 67)
        assert np.allclose(result,truth)

    def test_grids_centre(self):
        result = tbd.grids_centre(21, 67,self.params)
        truth = (113.70213705349262, 22.70127254883033)
        assert np.allclose(result,truth)

    def test_gridid_to_polygon(self):
        result = tbd.gridid_to_polygon(pd.Series(21), pd.Series(67),self.params)[0].wkt
        truth = 'POLYGON ((113.6997052188857 22.69902424622712, 113.7045688880996 22.69902424622712, 113.7045688880996 22.70352085143355, 113.6997052188857 22.70352085143355, 113.6997052188857 22.69902424622712))'
        assert result==truth
    
    def test_hexagon_grids(self):
        result = tbd.hexagon_grids(self.bounds,accuracy = 500)['geometry'].iloc[0].wkt
        truth = 'POLYGON ((113.5955084235794 22.4, 113.5977542117897 22.40359627046783, 113.6022457882103 22.40359627046783, 113.6044915764206 22.4, 113.6022457882103 22.39640363649211, 113.5977542117897 22.39640363649211, 113.5955084235794 22.4))'
        assert result==truth
    
    def test_gridid_sjoin_shape(self):
        data = pd.DataFrame([[1, 1], [10, 10], [100, 100]],
                    columns=['LONCOL', 'LATCOL'])
        shape = gpd.GeoDataFrame([Polygon([[1, 1], [10, 10], [100, 100]]),
                                Polygon(
                                    [[113.6, 22.4], [113.61, 22.41], [113.6, 22.42]])
                                ], columns=['geometry'])
        result = tbd.gridid_sjoin_shape(data, shape, self.params, col=['LONCOL', 'LATCOL'])['geometry'].iloc[0].wkt
        truth = 'POLYGON ((113.602431834607 22.40224830260321, 113.6072955038209 22.40224830260321, 113.6072955038209 22.40674490780964, 113.602431834607 22.40674490780964, 113.602431834607 22.40224830260321))'
        assert result==truth

    def test_grid_params_gini(self):
        data = pd.DataFrame([[113.6, 22.4], [113.61, 22.41], [113.6, 22.42]],
                    columns=['lon', 'lat'])
        result = tbd.grid_params_gini(data,col = ['lon','lat'],accuracy = 500,gini = 'max',gap = 2,sample = 10000)
        truth = [113.60333333333331, 22.41, 0.004863931711621178, 0.004496605206422906]
        assert np.allclose(result,truth)