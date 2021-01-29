import requests
from dotenv import load_dotenv
from pathlib import Path
import os


class Spoonacular(object):
    '''
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)
    api_key = os.getenv('API_KEY')
    '''
    api_key = os.environ.get('API_KEY')

    def __init__(self, api_key=api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_key = api_key

    def get_recipe_with_ingredients(self, ingredients: str, no_of_res=10):
        params = {
            'ingredients': ingredients,
            'limitLicense': True,
            'number': no_of_res,
            'ranking': 1,
            'ignorePantry': True
        }
        return self.get_resource(params, 'recipes', 'findByIngredients')

    def get_resource(self, params, type_='recipes', search_='findByIngredients'):
        endpoint = f"https://api.spoonacular.com/{type_}/{search_}/?apiKey={self.api_key}"
        headers = {
        }
        r = requests.get(endpoint, params=params, headers=headers)
        return r.json()

    def to_flask_dict(self, dict_):
        ls_final = []
        for i in dict_:
            dc_tmp = {}
            dc_tmp['title'], dc_tmp['id'], dc_tmp['url_image'] = i['title'], i['id'], i['image']
            tmp_missed = []
            for item in i['missedIngredients']:
                tmp_missed.append(item['original'])
            dc_tmp['missedIngredients'] = tmp_missed
            tmp_unused = []
            for item in i['unusedIngredients']:
                tmp_unused.append(item['original'])
            dc_tmp['unusedIngredients'] = tmp_unused
            tmp_used = []
            for item in i['usedIngredients']:
                tmp_used.append(item['original'])
            dc_tmp['usedIngredients'] = tmp_used
            dc_tmp['allIngredients'] = tmp_used + tmp_missed
            ls_final.append(dc_tmp)

        tuple_of_tuples = ()
        for item in ls_final:
            tuple_of_tuples = (
                (item['url_image'], item['title'], ','.join(item['allIngredients'])),) + tuple_of_tuples

        return ls_final, tuple_of_tuples
