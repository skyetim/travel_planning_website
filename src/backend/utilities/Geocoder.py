# -*- coding: UTF-8 -*-

import googlemaps
from urllib import parse
import urllib3
import json

urllib3.disable_warnings()


class Geocoder(object):
    def __init__(self, API_file):
        with open(API_file) as f:
            temp = json.load(f)
        self.API_Key = temp["API_Key"]
        self.gmaps = googlemaps.Client(key=self.API_Key)
        self.http = urllib3.PoolManager()

    # Version=1使用googlemaps库
    # Version=2直接使用HTTPS请求
    def geocode(self, address, version=1):
        if version == 1:
            return self.geocode_1(address)
        else:
            return self.geocode_2(address)

    def geocode_1(self, address):
        res = self.gmaps.geocode(address, language="zh-CN")
        return res  # 返回的是一个list

    def geocode_2(self, address):
        url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + \
            parse.quote(address)+"&key="+self.API_Key+"&language=zh-CN"
        temp = self.http.request('GET', url)
        # 读出来的json的结构为{results,status}，只取list
        return json.loads(temp.data.decode("utf-8"))["results"]

    def rev_geocode(self, latlng, version=1):
        if version == 1:
            return self.rev_geocode_1(latlng)
        else:
            return self.rev_geocode_2(latlng)

    def rev_geocode_1(self, latlng):
        res = self.gmaps.reverse_geocode(
            latlng, language="zh-CN", result_type="locality")
        return res

    def rev_geocode_2(self, latlng):
        url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+str(latlng[0])+","+str(latlng[1]) + \
            "&key="+self.API_Key+"&language=zh-CN"+"&result_type=locality"
        temp = self.http.request('GET', url)
        return json.loads(temp.data.decode("utf-8"))


if __name__ == "__main__":
    g = Geocoder("yang.gapi")
    print(g.geocode("南京大学"))
    # print(g.geocode_2("南京大学"))
    print(g.rev_geocode((32.05549011970849, 118.7776112197085), version=1))
