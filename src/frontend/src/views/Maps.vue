<template>
  <div>
    <base-header type="gradient-success" class="pb-6 pb-8 pt-5 pt-md-8">
      <travel-stats :travelGroup="travel_group_list"/>
    </base-header>

    <div class="container-fluid mt--7">
      <div class="row">
        <div class="col">
          <div class="card shadow border-0">
            <div class="color-picker">
              <base-dropdown v-for="(travel_group, index) in travel_group_list" :key="index">
                <button
                  slot="title"
                  class="btn dropdown-toggle button-text"
                  :style="{backgroundColor:travel_group.color.hex, opacity:travel_group.color.a}"
                >{{travel_group.name}}</button>
                <div>
                  <swatches v-model="travel_group.color"></swatches>
                </div>
              </base-dropdown>
            </div>
            <div id="map-canvas" class="map-canvas" style="height: 600px;"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import L from "leaflet";
import swatches from "vue-color/src/components/Swatches.vue";

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

function mountMap(map, travel_group_list) {
  var markersGroup = [];

  travel_group_list.forEach(travel => {
    var markers = [];
    var myCustomColour = travel.color.hex;
    const markerHtmlStyles = makeColorStyle(myCustomColour);
    const myicon = L.divIcon({
      iconUrl: "",
      className: "",
      iconAnchor: [0, 24],
      labelAnchor: [-6, 0],
      popupAnchor: [1, -12],
      html: `<span style="${markerHtmlStyles}" />`
    });
    travel.travel.forEach(element => {
      var marker = L.marker(element.coordinate, {
        icon: myicon
      });
      marker.bindPopup(
        "你在" +
          travel.dates.start +
          "至" +
          travel.dates.end +
          "来过" +
          element.location
      );

      marker.addTo(map);
      markers.push(marker);
    });
    markersGroup.push(markers);
  });

  return markersGroup;
}

export default {
  components: {
    swatches
  },
  data() {
    return {
      travel_group_list: [],
      map: null,
      markersGroup: []
    };
  },
  created: function() {
    var post_data = new Object();
    post_data.user_id = this.$session.get("user_id");
    post_data.session_id = this.$session.id().replace("sess:", "");

    var vue = this;
    var backend = this.$backend;

    backend.get_all_travel_group_details(
      post_data,
      function(response) {
        var travel_group_list = response.data.travel_group_info_list;
        travel_group_list.forEach(travel_group => {
          var tmp_list = travel_group.travel_infos.travel_info_list;
          tmp_list.sort(vue.compare("date_start"));

          tmp_list.forEach(travel => {
            backend.city_id_to_city(
              { city_id: travel.city_id },
              function(response1) {
                travel.location = response1.data.city_name;
                travel.coordinate = [
                  response1.data.latitude,
                  response1.data.longitude
                ];
                try {
                  vue.markersGroup = mountMap(vue.map, vue.travel_group_list);
                } catch (err) {
                  console.log(err);
                }
              },
              function() {
                alert(response.data.error_message);
              }
            );
          });

          var start = tmp_list.length > 0 ? tmp_list[0].date_start : "";
          var end =
            tmp_list.length > 0 ? tmp_list[tmp_list.length - 1].date_end : "";

          vue.travel_group_list.push({
            name: travel_group.travel_group_name,
            travel_group_id: travel_group.travel_group_id,
            travel: tmp_list,
            dates: {
              start: start,
              end: end
            },
            color: { hex: travel_group.travel_group_color, a: 0.8 }
          });
        });
      },
      function(response) {
        alert(response.data.error_message);
      }
    );
  },
  mounted: function() {
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
  },
  watch: {
    travel_group_list: {
      handler: function() {
        try {
          this.changeColor();
        } catch (err) {
          console.log(err);
        }
      },
      deep: true
    }
  },
  methods: {
    changeColor: function() {
      // 提交表单到数据库
      for (var i = 0; i < this.markersGroup.length; i++) {
        for (var j = 0; j < this.markersGroup[i].length; j++) {
          this.map.removeLayer(this.markersGroup[i][j]);
        }
      }
      this.markersGroup = mountMap(this.map, this.travel_group_list);
    }
  }
};
</script>
<style scoped>
.color-picker {
  position: absolute;
  margin-top: 20px;
  margin-left: 20px;
  padding: 20px;
  /* width: 100px;
  height: 100px; */
  z-index: 9999;
  background-color: rgba(255, 255, 255, 0.5);
}

.button-text {
  font-weight: 550;
  padding: 8px;
  color: rgba(255, 255, 255);
}
</style>
