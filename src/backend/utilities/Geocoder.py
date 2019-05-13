# -*- coding: UTF-8 -*-

import googlemaps
from urllib import parse
import urllib3
import json

urllib3.disable_warnings()


class Geocoder():
    def __init__(self, API_file):
        with open(API_file) as f:
            temp = json.load(f)
        self.__API_Key = temp["API_Key"]
        self.__gmaps = googlemaps.Client(key=self.__API_Key)
        self.__http = urllib3.PoolManager()

    # Version=1使用googlemaps库
    # Version=2直接使用HTTPS请求
    def geocode(self, address, version=1):
        '''
        Return a list of Geocoding results.
            :param address: arbitary address string, can be approximate;
            :param version: decide using 'googlemaps' package (version=1, default) or Google Maps Web API (version=2)
            :returns: returns a list of Geocoding results(see Doc)
        '''
        if address == "":
            return []
        if version == 1:
            return self._geocode_1(address)
        return self._geocode_2(address)

    def _geocode_1(self, address):
        res = self.__gmaps.geocode(address, language="zh-CN")
        return res  # 返回的是一个list

    def _geocode_2(self, address):
        url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + \
            parse.quote(address)+"&key="+self.__API_Key+"&language=zh-CN"
        temp = self.__http.request('GET', url)
        # 读出来的json的结构为{results,status}，只取list
        return json.loads(temp.data.decode("utf-8"))["results"]

    def rev_geocode(self, latlng, version=1):
        if version == 1:
            return self._rev_geocode_1(latlng)
        return self._rev_geocode_2(latlng)

    def _rev_geocode_1(self, latlng):
        res = self.__gmaps.reverse_geocode(
            latlng, language="zh-CN", result_type="locality")
        return res

    def _rev_geocode_2(self, latlng):
        url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+str(latlng[0])+","+str(latlng[1]) + \
            "&key="+self.__API_Key+"&language=zh-CN"+"&result_type=locality"
        temp = self.__http.request('GET', url)
        return json.loads(temp.data.decode("utf-8"))

    def address_to_gps(self, address, version=1):
        res = self.geocode(address, version=version)
        if res == []:
            return ()
        loc = res[0]["geometry"]["location"]
        return loc["lat"], loc["lng"]

    @staticmethod
    def __geores_to_city(res):
        if res == []:
            return dict()
        add_com = res[0]["address_components"]
        res = {"country": "", "admin_area_1": "", "locality": ""}
        for x in add_com:
            if "country" in x["types"]:
                res["country"] = x["long_name"]
            if "administrative_area_level_1" in x["types"]:
                res["admin_area_1"] = x["long_name"]
            if "locality" in x["types"]:
                res["locality"] = x["long_name"]

        if res["admin_area_1"] == "":
            res["admin_area_1"] = res["country"]
        if res["locality"] == "":
            res["locality"] = res["admin_area_1"]

        return res

    def address_to_city(self, address, version=1):
        res = self.geocode(address, version=version)
        return self.__geores_to_city(res)

    def gps_to_city(self, latlng, version=1):
        res = self.rev_geocode(latlng, version=version)
        return self.__geores_to_city(res)


if __name__ == "__main__":
    g = Geocoder("yang.gapi")
    print("Address to City: 北京大学物理学院->"+str(g.address_to_city("北京大学物理学院")))
    print("Address to GPS: 洛杉矶->"+str(g.address_to_gps("洛杉矶")))
    print("GPS to city: (32.05549011970849, 118.7776112197085)->"+str(g.gps_to_city((32.05549011970849, 118.7776112197085), version=1)))

    # # print(g.geocode("南京"))
    # # print(g.rev_geocode((32.05549011970849, 118.7776112197085), version=1))
    # print(g.gps_to_city((32.05549011970849, 118.7776112197085), version=1))
