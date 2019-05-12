<template>
  <div>
    <div class="container-fluid mt--7">
      <div class="row">
        <div class="col">
          <div class="card shadow border-0">
            <div id="map-canvas" class="map-canvas" style="height: 600px;"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import L from "leaflet";
import { swatches } from 'vue-color';

var color_picker = ["#f5365c", "#172b4d", "#fb6340", "#11cdef", "#2dce89"];

var travelGroup = [
  {
    name: "广州自驾游",
    travel: [
      { location: "广州", coordinate: [23.16667, 113.23333] },
      { location: "深圳", coordinate: [22.61667, 114.06667] },
      { location: "海陵岛", coordinate: [21.85, 111.95] }
    ],
    dates: { start: "2019-05-01", end: "2019-07-19" },
    status: 0
  },
  {
    name: "云南穷游",
    travel: [
      { location: "丽江", coordinate: [26.86, 100.25] },
      { location: "昆明", coordinate: [25.04, 102.73] },
      { location: "普洱", coordinate: [23.07, 101.03] },
      { location: "大理", coordinate: [25.69, 100.19] }
    ],
    dates: { start: "2019-07-17", end: "2019-07-19" },
    status: 1
  },
  {
    name: "江南之旅",
    travel: [
      { location: "南京", coordinate: [32.05, 118.78333] },
      { location: "苏州", coordinate: [31.32, 120.62] },
      { location: "周庄", coordinate: [31.13, 120.9] },
      { location: "上海", coordinate: [31.22, 121.48] }
    ],
    dates: { start: "2018-07-17", end: "2018-07-19" },
    status: 2
  },
  {
    name: "北方之旅",
    travel: [
      { location: "北京", coordinate: [39.92, 116.46] },
      { location: "承德", coordinate: [40.97, 117.93] },
      { location: "赤峰", coordinate: [42.28, 118.87] }
    ],
    dates: { start: "2018-07-17", end: "2018-07-19" },
    status: 3
  }
];

function makeColorStyle(color) {
  return `
      background-color: ${color};
      opacity: 0.8;
      width: 2.0rem;
      height: 2.0rem;
      display: block;
      left: -0.82rem;
      top: -0.65rem;
      position: relative;
      border-radius: 3rem 3rem 0;
      transform: rotate(45deg);
      border: 1px solid #FFFFFF;`;
}

function mountMap(map, travelGroup) {
  var markersGroup = [];

  travelGroup.forEach(travel => {
    var markers = [];
    var myCustomColour = color_picker[travel.status];
    const markerHtmlStyles = makeColorStyle(myCustomColour);
    const myicon = L.divIcon({
      iconUrl: "",
      className: "",
      iconAnchor: [0, 24],
      labelAnchor: [-6, 0],
      popupAnchor: [12, 12],
      html: `<span style="${markerHtmlStyles}" />`
    });
    travel.travel.forEach(element => {
      var marker = L.marker(element.coordinate, {
        icon: myicon
      });

      marker.on("mouseover", function(e) {
        //open popup;
        var popup = L.popup()
          .setLatLng(e.latlng)
          .setContent(
            "你在" +
              travel.dates.start +
              "至" +
              travel.dates.end +
              "来过" +
              element.location +
              " " +
              "点击编辑..."
          );
        popup.openOn(map);
        marker.on("mouseout", function() {
          map.closePopup(popup);
        });
      });

      var template =
        ' <div class="color-picker">\
          <swatches-picker v-model="colors"></swatches-picker>\
          <h2>Swatches</h2>\
        </div>';
      marker.on("click", function(e) {
        var popup = L.popup()
          .setLatLng(e.latlng)
          .setContent(template);
        popup.openOn(map);
      });
      marker.addTo(map);
      markers.push(marker);
    });
    markersGroup.push(markers);
  });

  return markersGroup;
}

var colors = {
  hex: "#194d33e6",
  hsl: {
    h: 150,
    s: 0.5,
    l: 0.2,
    a: 0.9
  },
  hsv: {
    h: 150,
    s: 0.66,
    v: 0.3,
    a: 0.9
  },
  rgba: {
    r: 25,
    g: 77,
    b: 51,
    a: 0.9
  },
  a: 0.9
};
export default {
  components:{
    'swatches-picker': swatches
  },
  data() {
    return {
      travelGroup: travelGroup,
      map: null,
      markersGroup: [],
      colors: colors
    };
  },
  mounted() {
    this.map = L.map("map-canvas").setView([37.51, 105.18], 4);

    // tile
    L.tileLayer(
      "https://api.mapbox.com/styles/v1/oymisaki/cjvkxybdi2dt91cqiktdeozp9/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1Ijoib3ltaXNha2kiLCJhIjoiY2p0ZWEwZDRlMWcwcTQzbW9xcWd5MnpxbyJ9.Ri_EK6iwsLzeH-ZgxJg0ig",
      {
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: "abcd",
        maxZoom: 6,
        minZoom: 4
      }
    ).addTo(this.map);
    this.markersGroup = mountMap(this.map, this.travelGroup);
  },
  methods: {
    // 保存
    save: function() {
      // 提交表单到数据库
      for (var i = 0; i < this.markersGroup.length; i++) {
        this.map.removeLayer(this.markers[i]);
      }
      this.markersGroup = mountMap(this.map, this.travel);
    }
  }
};
</script>
<style>
.color-picker {
  position: relative;
  margin-bottom: 10px;
  margin: 0 10px 0 10px;
  z-index: 2;
}
</style>
