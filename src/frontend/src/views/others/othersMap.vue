
<template>
  <div>
    <base-header type="gradient-success" class="pb-6 pb-8 pt-5 pt-md-8"></base-header>

    <div class="container-fluid mt--7">
      <div class="row">
        <div class="col">
          <div class="card shadow border-0">
            <div class="show-panel">
              <button
                v-for="(travel_group, index) in travel_group_list"
                :key="index"
                @click="showTravel(travel_group_list[index])"
                slot="title"
                class="btn dropdown-toggle button-text"
                :style="{backgroundColor:travel_group_list[index].color.hex, opacity:travel_group_list[index].color.a}"
              >{{travel_group_list[index].name}}</button>
            </div>
            <div id="map-canvas" class="map-canvas" style="height: 600px;z-index: 10"></div>
          </div>
        </div>
      </div>
    </div>

    <modal :show.sync="show.modal">
      <template slot="header">
        <h5 class="modal-title" id="exampleModalLabel">查看行迹</h5>
      </template>
      <div>
        <small class="text-muted text-center">行迹名</small>
        <br>
        <div class="row">
          <div class="col-11 inline-div">
            <base-input placeholder="行迹名" v-model="showRow.name" ref="travel_group_name" readonly></base-input>
          </div>
          <div class="inline-div">
            <i
              :class="['ni', show.collapsed ? 'ni-bold-down': 'ni-bold-up', 'icon-expand']"
              @click="show.collapsed=!show.collapsed;"
            ></i>
          </div>
        </div>
        <div class="row">
          <div class="col-11">
            <div :class="[show.collapsed?'collapse': 'expand']">
              <draggablelist :travel="showRow.travel" :gid="showRow.travel_group_id"></draggablelist>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-11">
            <small class="text-muted text-center">行迹笔记</small>
            <br>
            <b-form-textarea v-model="showRow.travel_group_note" placeholder="去让TA说点什么吧~" readonly></b-form-textarea>
          </div>
        </div>
        <div class="row">
          <div class="col-11">
            <small class="text-muted text-center">行迹颜色</small>
            <br>
            <button
              slot="title"
              class="btn button-text"
              :style="{backgroundColor:showRow.color.hex, opacity:showRow.color.a}"
            ></button>
          </div>
        </div>
      </div>
      <template slot="footer">
        <base-button
          type="primary"
          @click="show.modal = false;"
        >退出</base-button>
      </template>
    </modal>
  </div>
</template>
<script>
// TODO: 从router获得参数，post接口参数调整

import L from "leaflet";

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
      var content = `
      <div class="card"">
        <div class="card-body">
          <h5 class="card-title">
          ${element.location}&nbsp;
          ${element.date_start}至
          ${element.date_end}
          </h5>
          <p class="card-text"><hr>${travel.travel_group_note}</p>
        </div>
      </div>
      `;
      marker.bindPopup(content);

      marker.addTo(map);
      markers.push(marker);
    });
    markersGroup.push(markers);
  });

  return markersGroup;
}

var show = {
  addMode: false,
  modal: false,
  collapsed: true
};

export default {
  data() {
    return {
      show: {
        modal: false,
        collapsed: true
      },
      showRow: this.newTravelGroup(),
      showIndex: null,
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
    var backend = this.$backend_conn;

    backend(
      "get_all_travel_group_details",
      post_data,
      vue,
      function(response) {
        var travel_group_list = response.data.travel_group_info_list;
        travel_group_list.forEach(travel_group => {
          var tmp_list = travel_group.travel_infos.travel_info_list;
          tmp_list.sort(vue.compare("date_start"));

          tmp_list.forEach(travel => {
            travel.vbool = travel.visibility == "F";
            travel.location = travel.city.city_name;
            travel.coordinate = [travel.city.latitude, travel.city.longitude];
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
            travel_group_note: travel_group.travel_group_note,
            color: { hex: travel_group.travel_group_color, a: 0.8 }
          });
        });
        vue.markersGroup = mountMap(vue.map, vue.travel_group_list);
      },
      function(response) {
        alert(response.data.error_message);
      },
      false
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
  methods: {
    showTravel: function(row) {
      this.showRow = this.copy(row);
      this.showIndex = this.indexOf(this.travel_group_list, row);
      this.show.modal = true;
    }
  }
};
</script>
<style scoped>
.show-panel {
  position: absolute;
  margin-top: 20px;
  margin-left: 20px;
  padding: 20px;
  /* width: 100px;
  height: 100px; */
  z-index: 999;
  background-color: rgba(255, 255, 255, 0.5);
}
.icon-expand {
  position: relative;
  margin-top: 10px;
  margin-left: 10px;
  font-size: 150%;
  transition: transform 0.2s;
}

.icon-expand:hover {
  transform: scale(1.2);
}
.collapse {
  display: none;
  overflow: hidden;
  background-color: #ffffff;
}

.expand {
  display: block;
  overflow: hidden;
  background-color: #ffffff;
}

/* Dropdown Content (Hidden by Default) */
.dropdown-content {
  display: none;
  position: absolute;
  z-index: 2;
}
</style>
