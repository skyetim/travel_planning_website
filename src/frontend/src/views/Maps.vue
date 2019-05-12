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

var color_picker = ["#f5365c", "#172b4d", "#fb6340", "#11cdef", "#2dce89"];

var travelGroup = [
  {
    name: "balabala之旅",
    travel: [
      { location: "广州", coordinate: [23.16667, 113.23333] },
      { location: "深圳", coordinate: [22.61667, 114.06667] }
    ],
    dates: { start: "2019-05-01", end: "2019-07-19" },
    status: 2
  },
  {
    name: "开心之旅",
    travel: [
      { location: "北京", coordinate: [39.95, 116.3] },
      { location: "上海", coordinate: [31.23, 121.47] }
    ],
    dates: { start: "2019-07-17", end: "2019-07-19" },
    status: 0
  },
  {
    name: "LOL之旅",
    travel: [{ location: "南京", coordinate: [32.05, 118.78333] }],
    dates: { start: "2018-07-17", end: "2018-07-19" },
    status: 3
  }
];

function mountMap(map, travelGroup) {
  var markersGroup = [];

  travelGroup.forEach(travel => {
    var markers = [];
    var myCustomColour = color_picker[travel.status];
    const markerHtmlStyles = `
      background-color: ${myCustomColour};
      opacity: 0.8;
      width: 2.5rem;
      height: 2.5rem;
      display: block;
      left: -1.5rem;
      top: -1.5rem;
      position: relative;
      border-radius: 3rem 3rem 0;
      transform: rotate(45deg);
      border: 1px solid #FFFFFF;`;
    const myicon = L.divIcon({
      className: "my-custom-pin",
      iconAnchor: [0, 24],
      labelAnchor: [-6, 0],
      popupAnchor: [0, -36],
      html: `<span style="${markerHtmlStyles}" />`
    });
    travel.travel.forEach(element => {
      var marker = L.marker(element.coordinate, {
        icon: myicon
      })
        .bindPopup(
          "你在" +
            travel.dates.start +
            "至" +
            travel.dates.end +
            "来过" +
            element.location
        )
        .addTo(map);
      markers.push(marker);
    });
    markersGroup.push(markers);
  });

  return markersGroup;
}

export default {
  data() {
    return {
      travelGroup: travelGroup,
      map: null,
      markersGroup: []
    };
  },
  mounted() {
    this.map = L.map("map-canvas").setView([39.9877, 116.3075], 4);

    // tile
    L.tileLayer(
      "https://api.mapbox.com/styles/v1/oymisaki/cjv1qcq5g0rvu1fjmh365xxs1/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1Ijoib3ltaXNha2kiLCJhIjoiY2p0ZWEwZDRlMWcwcTQzbW9xcWd5MnpxbyJ9.Ri_EK6iwsLzeH-ZgxJg0ig",

      {
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: "abcd",
        maxZoom: 21
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
.my-div-icon {
  color: "#172b4d";
}
</style>
