<template>
  <div>
    <base-header type="gradient-success" class="pb-6 pb-8 pt-5 pt-md-8">
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

var travel = [
  {
    name: "balabala之旅",
    travel: [{location: "广州", coordinate: [23.16667, 113.23333]},
            {location: "深圳", coordinate: [22.61667, 114.06667]},
            {location: "北京", coordinate: [39.95, 116.3]},
            {location: "上海", coordinate: [31.23, 121.47]},
            {location: "南京", coordinate: [32.05, 118.78333]}],
    dates: { start: "2019-05-01", end: "2019-07-19" },
    status: 2,
  },
  {
    name: "开心之旅",
    travel: [{location: "广州", coordinate: [23.16667, 113.23333]},
            {location: "深圳", coordinate: [22.61667, 114.06667]},
            {location: "北京", coordinate: [39.95, 116.3]},
            {location: "上海", coordinate: [31.23, 121.47]},
            {location: "南京", coordinate: [32.05, 118.78333]}],
    dates: { start: "2019-07-17", end: "2019-07-19" },
    status: 0
  },
  {
    name: "LOL之旅",
    travel: [{location: "广州", coordinate: [23.16667, 113.23333]},
            {location: "深圳", coordinate: [22.61667, 114.06667]},
            {location: "北京", coordinate: [39.95, 116.3]},
            {location: "上海", coordinate: [31.23, 121.47]},
            {location: "南京", coordinate: [32.05, 118.78333]}],
    dates: { start: "2018-07-17", end: "2018-07-19" },
    status: 3
  },
  {
    name: "有意思的行程",
    travel: [{location: "广州", coordinate: [23.16667, 113.23333]},
            {location: "深圳", coordinate: [22.61667, 114.06667]},
            {location: "北京", coordinate: [39.95, 116.3]},
            {location: "上海", coordinate: [31.23, 121.47]},
            {location: "南京", coordinate: [32.05, 118.78333]}],
    dates: { start: "2018-07-17", end: "2018-07-19" },
    status: 1
  },
  {
    name: "Go to Hell!",
    travel: [{location: "广州", coordinate: [23.16667, 113.23333]},
            {location: "深圳", coordinate: [22.61667, 114.06667]},
            {location: "北京", coordinate: [39.95, 116.3]},
            {location: "上海", coordinate: [31.23, 121.47]},
            {location: "南京", coordinate: [32.05, 118.78333]}],
    dates: { start: "2018-07-17", end: "2018-07-19" },
    status: 0  
  }
];
      
function mountMap(map, travel){
  var markers = [];

  travel.forEach(element => {
    var nowLoc = element.coordinate;
    var marker = L.marker(nowLoc)
                  .bindPopup("你在"+element.dates.range.replace('to', '至')+"来过这里")
                  .addTo(map);
    markers.push(marker);
  });

  return markers;
}

export default {
    data(){
      return {
        travel: travel,
        map: null,
        markers: []
      }
    },
    mounted(){
      this.map =  L.map('map-canvas').setView([39.9877, 116.3075], 4);

      // tile
      L.tileLayer(
        'https://api.mapbox.com/styles/v1/oymisaki/cjv1qcq5g0rvu1fjmh365xxs1/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1Ijoib3ltaXNha2kiLCJhIjoiY2p0ZWEwZDRlMWcwcTQzbW9xcWd5MnpxbyJ9.Ri_EK6iwsLzeH-ZgxJg0ig',

        {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
            subdomains: 'abcd',
            maxZoom: 21
        }).addTo(this.map);
      this.markers = mountMap(this.map, this.travel);
    },
    methods:{
      // 保存
      save: function(){
        // 提交表单到数据库
        for(var i = 0; i < this.markers.length; i++){
            this.map.removeLayer(this.markers[i]);
        }
        this.markers = mountMap(this.map, this.travel);
      }
    }
}
</script>
<style>
</style>
