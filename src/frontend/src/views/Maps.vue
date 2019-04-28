<template>
  <div>
    <base-header type="gradient-success" class="pb-6 pb-8 pt-5 pt-md-8">
      <div class="row">
          <editable :travel="travel" :headers="headers"></editable>
      </div>
    <button class="btn btn-primary btn-sm addBox" @click="save()">保存</button>
    </base-header>

    <div class="container-fluid mt--7">
      <div class="row">
        <div class="col">
          <div class="card shadow border-0">
            <div id="map-canvas" class="map-canvas" style="height: 600px;">
                
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import L from 'leaflet';

var headers = ["行迹", "时间", "经度", "纬度"];
var travel = [
    ["北京", "2019", "116.30", "39.95"],
    ["上海", "2019", "121.47", "31.23"]
]
export default {
    data(){
      return {
        travel: travel,
        headers: headers,
        mymap: null
      }
    },
    mounted(){
      this.mymap =  L.map('map-canvas').setView([39.9877, 116.3075], 4);

      // tile
      L.tileLayer(
        'https://api.mapbox.com/styles/v1/oymisaki/cjv0cnpx43bzn1gqjofoc98q8/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1Ijoib3ltaXNha2kiLCJhIjoiY2p0ZWEwZDRlMWcwcTQzbW9xcWd5MnpxbyJ9.Ri_EK6iwsLzeH-ZgxJg0ig', 
        {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
            subdomains: 'abcd',
            maxZoom: 19
        }).addTo(this.mymap);
      var lastLoc = [parseFloat(travel[0][3]), parseFloat(travel[0][2])];
      travel.forEach(element => {
        var nowLoc = [parseFloat(element[3]), parseFloat(element[2])];
        L.marker(nowLoc).addTo(this.mymap).bindPopup("你在"+element[1]+"来过这里").openPopup();
        var latlngs = [
              lastLoc,
              nowLoc
          ];
        L.polyline(latlngs, { color: '#1e90ff' }).addTo(this.mymap);
        lastLoc = nowLoc;
      });
    },
    methods:{
      // 保存
      save: function(){
        // 提交表单到数据库
        var lastLoc = [parseFloat(travel[0][3]), parseFloat(travel[0][2])];
        travel.forEach(element => {
          var nowLoc = [parseFloat(element[3]), parseFloat(element[2])];
          L.marker(nowLoc).addTo(this.mymap).bindPopup("你在"+element[1]+"来过这里").openPopup();
          var latlngs = [
                lastLoc,
                nowLoc
            ];
          L.polyline(latlngs, { color: '#1e90ff' }).addTo(this.mymap);
          lastLoc = nowLoc;
        });
      }
    }
}
</script>
<style>
</style>
