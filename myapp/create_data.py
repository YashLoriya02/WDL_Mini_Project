URL_DATA = {
    'Display Type': "display_tech",
    'Features': 'with',
    'Brands': 'brand',
    'Screen Size': 'display',
    'Screen Resolution': 'display_res',
    'ROM': 'memory',
    'Battery Size': 'battery_size',
    'RAM': 'ram',
    'CPU': 'cpu',
    'Front Camera': 'front_cam',
    'Rear Camera': 'camera',
}


class CreateData:
    def __init__(self, request) -> None:
        self.request = request

    def get_unique_category(self, category: list) -> list:
        return list(set(category))

    def create_data_dict(self, category_values: list, category: list) -> dict:
        return {i: {category[i]: category_values[i]} for i in range(len(category))}

    def get_filters(self, data_dict: dict) -> dict:
        filters = {}
        for key, value in data_dict.items():
            filter_type = next(iter(value.keys()))
            filter_value = next(iter(value.values()))
            if filter_type not in filters:
                filters[filter_type] = []
            filters[filter_type].append(filter_value)
        return filters

    def format_filters(self, filters: dict) -> dict:
        for filter_type, values in filters.items():
            filters[filter_type] = '-'.join(values)
        return filters

    def build_url(self, fomated_filters: dict) -> str:
        base_url = "https://www.smartprix.com/mobiles/"
        filter_string = '/'.join(
            f"{value}-{URL_DATA[key]}" for key, value in fomated_filters.items())
        final_url = base_url + filter_string + '/'
        return final_url

    def process_url(self, unique_dict: dict, data_dict: dict) -> str:

        filters = self.get_filters(data_dict=data_dict)

        fomated_filters = self.format_filters(filters=filters)

        final_url = self.build_url(fomated_filters=fomated_filters)

        return final_url

    def get_category_and_category_values(self):
        return self.request.get('id'), self.request.get('category')

    def process(self):
        category_values, category = self.get_category_and_category_values()
        unique_category = self.get_unique_category(category=category)
        data_dict = self.create_data_dict(
            category_values=category_values,
            category=category
        )
        processed_url = self.process_url(
            unique_dict=unique_category,
            data_dict=data_dict
        )

        return processed_url
