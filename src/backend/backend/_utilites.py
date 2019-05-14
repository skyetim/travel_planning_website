import json
import os
from urllib import parse
import googlemaps
import urllib3


urllib3.disable_warnings()


class GeoCoder(object):
    def __init__(self, api_file):
        api_cfg = {}
        with open(api_file) as api_file:
            api_cfg.update(json.load(api_file))
        self.__API_Key = api_cfg['API_Key']
        self.__gmaps = googlemaps.Client(key=self.__API_Key)
        self.__http = urllib3.PoolManager()

    # Version = 1 使用 googlemaps 库
    # Version = 2 直接使用 HTTPS 请求
    def geocode(self, address, version=1):
        """
        Return a list of Geocoding results.
            :param address: arbitary address string, can be approximate;
            :param version: decide using 'googlemaps' package (version=1, default) or Google Maps Web API (version=2)
            :returns: returns a list of Geocoding results(see Doc)
        """
        if address == '':
            return []
        if version == 1:
            return self._geocode_1(address)
        return self._geocode_2(address)

    def _geocode_1(self, address):
        res = self.__gmaps.geocode(address, language='zh-CN')
        return res  # 返回的是一个 list

    def _geocode_2(self, address):
        url = f'https://maps.googleapis.com/maps/api/geocode/json?' \
            f'address={parse.quote(address)}' \
            f'&key={self.__API_Key}' \
            f'&language=zh-CN'
        temp = self.__http.request('GET', url)
        # 读出来的 json 的结构为 {results, status}，只取 list
        return json.loads(temp.data.decode('utf-8'))['results']

    def rev_geocode(self, latlng, version=1):
        if version == 1:
            return self._rev_geocode_1(latlng)
        return self._rev_geocode_2(latlng)

    def _rev_geocode_1(self, latlng):
        res = self.__gmaps.reverse_geocode(latlng,
                                           language='zh-CN',
                                           result_type='locality')
        return res

    def _rev_geocode_2(self, latlng):
        lat, lng = latlng
        url = f'https://maps.googleapis.com/maps/api/geocode/json?' \
            f'latlng={lat},{lng}' \
            f'&key={self.__API_Key}' \
            f'&language=zh-CN' \
            f'&result_type=locality'
        temp = self.__http.request('GET', url)
        return json.loads(temp.data.decode('utf-8'))

    def address_to_gps(self, address, version=1):
        res = self.geocode(address, version=version)
        if not res:
            return ()
        loc = res[0]['geometry']['location']
        return loc['lat'], loc['lng']

    @staticmethod
    def __geores_to_city(res):
        if not res:
            return dict()
        add_com = res[0]['address_components']
        res = {'country': '', 'admin_area_1': '', 'locality': ''}
        for x in add_com:
            if 'country' in x['types']:
                res['country'] = x['long_name']
            if 'administrative_area_level_1' in x['types']:
                res['admin_area_1'] = x['long_name']
            if 'locality' in x['types']:
                res['locality'] = x['long_name']

        if res['admin_area_1'] == '':
            res['admin_area_1'] = res['country']
        if res['locality'] == '':
            res['locality'] = res['admin_area_1']

        return res

    def address_to_city(self, address, version=1):
        res = self.geocode(address, version=version)
        return self.__geores_to_city(res)

    def gps_to_city(self, latlng, version=1):
        res = self.rev_geocode(latlng, version=version)
        return self.__geores_to_city(res)


if __name__ == '__main__':
    api_file = os.path.join(os.path.dirname(__file__), 'yang.gapi')
    gc = GeoCoder(api_file=api_file)
    print(f'Address to City: 北京大学物理学院->{gc.address_to_city("北京大学物理学院")}')
    print(f'Address to GPS: 洛杉矶->{gc.address_to_gps("洛杉矶")}')
    latlng = (32.05549011970849, 118.7776112197085)
    print(f'GPS to city: {latlng}->{gc.gps_to_city(latlng, version=1)}')
