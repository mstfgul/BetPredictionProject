from get_raw_data import get_links, get_csv_files
from mergedata import merge_data
from data_fitting_model import main_process
from model_training import main




url = 'https://www.football-data.co.uk/belgiumm.php'
string_to_find = 'Jupiler League'

if __name__ == '__main__':
    list_of_links = get_links(url, string_to_find)
    get_csv_files(list_of_links[:24])
    merge_data()
    main_process()
    main()
