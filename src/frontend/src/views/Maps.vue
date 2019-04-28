<template>
  <div>
    <base-header type="gradient-success" class="pb-6 pb-8 pt-5 pt-md-8">
      <div class="row">
          <editable :travel="travel"></editable>
      </div>
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

var travel=[
    { loc: "张三", time: 18 },
    { loc: "张三", time: 19 },
    { loc: "张三", time: 20 },
    { loc: "张三", time: 21 }
]

export default {
    data(){
      return {
        travel: travel
      }
    },
    mounted(){
        var mymap = L.map('map-canvas').setView([39.9877, 116.3075], 6);
        // tile
        L.tileLayer(
            'https://api.mapbox.com/styles/v1/oymisaki/cjv0cnpx43bzn1gqjofoc98q8/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1Ijoib3ltaXNha2kiLCJhIjoiY2p0ZWEwZDRlMWcwcTQzbW9xcWd5MnpxbyJ9.Ri_EK6iwsLzeH-ZgxJg0ig', 
            {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
                subdomains: 'abcd',
                maxZoom: 19
            }).addTo(mymap);
        // set my marker

        L.marker([39.9877, 116.3075]).addTo(mymap)
        .bindPopup("<b>你好！</b><br />我在北京大学第三教学楼！").openPopup();
        var popup = L.popup();
        var lastLoc = [39.9877, 116.3075];
        function onMapClick(e) {
            // popup
            popup
                .setLatLng(e.latlng)
                .setContent("You arrived here: " + e.latlng.toString())
                .openOn(mymap);

            // marker
            L.marker(e.latlng).addTo(mymap);
            var latlngs = [
                lastLoc,
                e.latlng
            ]
            // line
            L.polyline(latlngs, { color: '#1e90ff' }).addTo(mymap);
            lastLoc = e.latlng;
        }
        mymap.on('click', onMapClick);
    }
}
</script>
<style>
</style>
