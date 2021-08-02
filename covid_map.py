import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import pycountry

class CovMap():
    
    def __init__(self):
        self.country_and_code_dict = {}
        self.list_of_countries = []
        self.list_of_dates = []
        self.world_map = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    def upload_covid_data(self):
        self.URL_DATASET = r'https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv'
        self.cov_19_data_frame = pd.read_csv(self.URL_DATASET)
        return self.cov_19_data_frame

    def make_list_of_countries(self):   
        self.list_of_countries = self.cov_19_data_frame['Country'].unique().tolist()
        return self.list_of_countries

    def get_ISO_3_from_pycountry(self):
        for country in self.list_of_countries:
            try:
                country_data = pycountry.countries.search_fuzzy(country)
                country_code = country_data[0].alpha_3
                self.country_and_code_dict.update({country : country_code})
            except:
                print('could not add ISO 3 code for:', country)
                self.country_and_code_dict.update({country : ' '})
        return self.country_and_code_dict
    
    def make_new_column_iso(self):
        for k, v in self.country_and_code_dict.items():
            self.cov_19_data_frame.loc[(self.cov_19_data_frame.Country == k), 'iso_a3'] = v
        return self.cov_19_data_frame

    def make_list_of_dates(self):
        self.list_of_dates = self.cov_19_data_frame['Date'].unique().tolist()
        return self.list_of_dates

    def get_newest_date(self):
        self.newest_date = self.list_of_dates[-1]
        return self.newest_date

    def get_only_last_day_from_covid_data(self):
        cov_filter = self.cov_19_data_frame['Date'].isin([self.newest_date])
        self.cov_19_filtered = self.cov_19_data_frame[cov_filter]
        return self.cov_19_filtered

    def merge_geodataframe_with_csv_dataframe(self):
        self.merged_dataframes = self.world_map.merge(self.cov_19_filtered, how='outer')
        return self.merged_dataframes

    def make_a_covid_world_map_plot(self, pick='Confirmed'):
        self.pick = pick
        plt.rcParams['figure.figsize'] = [50, 70] 
        variable = self.pick
        fig, ax = plt.subplots(1, figsize=(30,10))
        ax.axis('off')
        self.merged_dataframes.plot(
            column=variable,
            missing_kwds={'color': 'lightgrey', "label": "Missing values"},
            ax=ax,
            legend=True,
            legend_kwds={'label': f"{self.pick} by Country",'orientation': "horizontal"}) 
        plt.show()


class GuiCommunication():
    
    def gui_communication(self, gui_pick='Deaths'):
        self.gui_pick = gui_pick
        m = CovMap()
        m.upload_covid_data()
        m.make_list_of_countries()
        m.get_ISO_3_from_pycountry()
        m.make_new_column_iso()
        m.make_list_of_dates()
        m.get_newest_date()
        m.get_only_last_day_from_covid_data()
        m.merge_geodataframe_with_csv_dataframe()
        m.make_a_covid_world_map_plot(self.gui_pick)
        

class Make_Map(CovMap):

    def __init__(self):
        m = CovMap()
        m.upload_covid_data()
        m.make_list_of_countries()
        m.get_ISO_3_from_pycountry()
        m.make_new_column_iso()
        m.make_list_of_dates()
        m.get_newest_date()
        m.get_only_last_day_from_covid_data()
        m.merge_geodataframe_with_csv_dataframe()
        m.make_a_covid_world_map_plot()

if __name__ == "__main__":
    cov = Make_Map()
