<template>
  <div>
    <base-header type="gradient-success" class="pb-6 pb-8 pt-5 pt-md-8">
      <div class="row">
          <editable     
        columns="[
          {
            label: 'Name',
            field: 'name',
          },
          {
            label: 'Position',
            field: 'position',
          },
          {
            label: 'Office',
            field: 'office',
          },
          {
            label: 'Age',
            field: 'age',
          },
          {
            label: 'Start date',
            field: 'date',
            sort: 'asc'
          },
          {
            label: 'Salary',
            field: 'salary',
          }
        ]" 
        rows=" [
          {
            name: 'Tiger Nixon',
            position: 'System Architect',
            office: 'Edinburgh',
            age: '61',
            date: '2011/04/25',
            salary: '$320'
          },
          {
            name: 'Garrett Winters',
            position: 'Accountant',
            office: 'Tokyo',
            age: '63',
            date: '2011/07/25',
            salary: '$170'
          },
          {
            name: 'Ashton Cox',
            position: 'Junior Technical Author',
            office: 'San Francisco',
            age: '66',
            date: '2009/01/12',
            salary: '$86'
          },
          {
            name: 'Cedric Kelly',
            position: 'Senior Javascript Developer',
            office: 'Edinburgh',
            age: '22',
            date: '2012/03/29',
            salary: '$433'
          }
        ]"></editable>
      </div>
      <!-- Card stats -->
      <div class="row">
        <div class="col-xl-3 col-lg-6">
          <stats-card
            title="Total traffic"
            type="gradient-red"
            sub-title="350,897"
            icon="ni ni-active-40"
            class="mb-4 mb-xl-0"
          >
            <template slot="footer">
              <span class="text-success mr-2">
                <i class="fa fa-arrow-up"></i> 3.48%
              </span>
              <span class="text-nowrap">Since last month</span>
            </template>
          </stats-card>
        </div>
        <div class="col-xl-3 col-lg-6">
          <stats-card
            title="Total traffic"
            type="gradient-orange"
            sub-title="2,356"
            icon="ni ni-chart-pie-35"
            class="mb-4 mb-xl-0"
          >
            <template slot="footer">
              <span class="text-success mr-2">
                <i class="fa fa-arrow-up"></i> 12.18%
              </span>
              <span class="text-nowrap">Since last month</span>
            </template>
          </stats-card>
        </div>
        <div class="col-xl-3 col-lg-6">
          <stats-card
            title="Sales"
            type="gradient-green"
            sub-title="924"
            icon="ni ni-money-coins"
            class="mb-4 mb-xl-0"
          >
            <template slot="footer">
              <span class="text-danger mr-2">
                <i class="fa fa-arrow-down"></i> 5.72%
              </span>
              <span class="text-nowrap">Since last month</span>
            </template>
          </stats-card>
        </div>
        <div class="col-xl-3 col-lg-6">
          <stats-card
            title="Performance"
            type="gradient-info"
            sub-title="49,65%"
            icon="ni ni-chart-bar-32"
            class="mb-4 mb-xl-0"
          >
            <template slot="footer">
              <span class="text-success mr-2">
                <i class="fa fa-arrow-up"></i> 54.8%
              </span>
              <span class="text-nowrap">Since last month</span>
            </template>
          </stats-card>
        </div>
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

export default {
    mounted(){
        var mymap = L.map('map-canvas').setView([39.9877, 116.3075], 6);
        // tile
        L.tileLayer(
            'http://{s}.tile.osm.org/{z}/{x}/{y}.png', 
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
            var polyline = L.polyline(latlngs, { color: '#98986f', opacity: 0.5 }).addTo(mymap);
            lastLoc = e.latlng;
        }
        mymap.on('click', onMapClick);
    }
}
</script>
<style>
</style>
