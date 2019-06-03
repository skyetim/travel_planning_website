<template>
  <div>
    <base-header type="gradient-success" class="pb-6 pb-8 pt-5 pt-md-8"></base-header>

    <div class="container-fluid mt--7">
      <div class="row">
        <div class="col">
          <div class="card shadow border-0">
            <div class="color-picker">
              <button
                v-for="(travel_group, index) in travel_group_list"
                :key="index"
                @click="editTravel(travel_group_list[index])"
                slot="title"
                class="btn dropdown-toggle button-text"
                :style="{backgroundColor:travel_group_list[index].color.hex, opacity:travel_group_list[index].color.a}"
              >{{travel_group_list[index].name}}</button>
              <base-button
                type="primary"
                @click="edit.addMode = true;edit.modal = true;editRow=newTravelGroup();"
              >添加新的行程</base-button>
            </div>
            <div id="map-canvas" class="map-canvas" style="height: 600px;"></div>
          </div>
        </div>
      </div>
    </div>

    <modal :show.sync="edit.modal">
      <template slot="header">
        <h5 class="modal-title" id="exampleModalLabel">{{edit.addMode? "新建行迹" : "修改行迹"}}</h5>
      </template>
      <div>
        <small class="text-muted text-center">行迹名</small>
        <br>
        <div class="row">
          <div class="col-11 inline-div">
            <base-input placeholder="行迹名" v-model="editRow.name" ref="travel_group_name"></base-input>
          </div>
          <div class="inline-div">
            <i
              :class="['ni', edit.collapsed ? 'ni-bold-down': 'ni-bold-up', 'icon-expand']"
              @click="edit.collapsed=!edit.collapsed;"
            ></i>
          </div>
        </div>
        <div class="row">
          <div class="col-11">
            <div :class="[edit.collapsed?'collapse': 'expand']">
              <draggablelist :travel="editRow.travel" :gid="editRow.travel_group_id"></draggablelist>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-11">
            <base-dropdown>
              <button
                slot="title"
                class="btn dropdown-toggle button-text"
                :style="{backgroundColor:editRow.color.hex, opacity:editRow.color.a}"
              >行迹颜色</button>
              <div>
                <swatches v-model="editRow.color"></swatches>
              </div>
            </base-dropdown>
          </div>
        </div>
      </div>
      <template slot="footer">
        <base-button
          type="primary"
          @click="edit.addMode?add_travel_group(editRow):set_travel_group(editRow, row);edit.modal = false;"
        >Save changes</base-button>
      </template>
    </modal>
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

var edit = {
  addMode: false,
  modal: false,
  collapsed: true
};

export default {
  components: {
    swatches
  },
  data() {
    return {
      edit: {
        addMode: false,
        modal: false,
        collapsed: true
      },
      editRow: this.newTravelGroup(),
      editIndex: null,
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
        // try {
        //   this.reMount();
        // } catch (err) {
        //   console.log(err);
        // }
        this.reMount();
      },
      deep: true
    }
  },
  methods: {
    reMount: function() {
      // 提交表单到数据库
      for (var i = 0; i < this.markersGroup.length; i++) {
        for (var j = 0; j < this.markersGroup[i].length; j++) {
          this.map.removeLayer(this.markersGroup[i][j]);
        }
      }
      this.markersGroup = mountMap(this.map, this.travel_group_list);
    },
    editTravel: function(row) {
      this.editRow = this.copy(row);
      this.editIndex = this.indexOf(this.travel_group_list, row);
      this.edit.addMode = false;
      this.edit.modal = true;
    },
    del: function(row) {
      for (var i = 0; i < this.travel_group_list.length; ++i) {
        if (row == this.travel_group_list[i]) {
          this.$backend.remove_travel_group(
            {
              user_id: this.$session.get("user_id"),
              session_id: this.$session.id().replace("sess:", ""),
              travel_group_id: row.travel_group_id
            },
            function(response) {
              this.travel_group_list.splice(i, 1);
              console.log(response);
            },
            function(response) {
              alert(response.data.error_message);
            }
          );
          break;
        }
      }
    },
    // ajax
    add_travel_group: function(row) {
      var vue = this;
      var backend = this.$backend;
      var session = this.$session;

      backend.add_travel_group(
        {
          user_id: session.get("user_id"),
          session_id: session.id().replace("sess:", ""),
          travel_group_name: row.name,
          travel_group_note: "hello",
          travel_group_color: row.color.hex
        },
        function(response) {
          row.travel.forEach(travel => {
            backend.add_travel(
              {
                user_id: session.get("user_id"),
                session_id: session.id().replace("sess:", ""),
                city_id: travel.city_id,
                date_start: travel.date_start,
                date_end: travel.date_end,
                visibility: travel.visibility,
                travel_note: ""
              },
              function(response) {
                travel.travel_id = response.data.travel_id;
                console.log(response);
              },
              function(response) {
                alert(response.data.error_message);
              }
            );
          });
          row.travel_group_id = response.data.travel_group_id;
          vue.travel_group_list.push(row);
          vue.$set(vue.travel_group_list, vue.editIndex, editRow);
          vue.reMount();
          console.log(response);
        },
        function(response) {
          alert(response.data.error_message);
        }
      );
    },

    set_travel_group: function(editRow) {
      var vue = this;
      var backend = this.$backend;
      var session = this.$session;

      backend.set_travel_group_info(
        {
          user_id: session.get("user_id"),
          session_id: session.id().replace("sess:", ""),
          travel_group_id: editRow.travel_group_id,
          travel_group_name: editRow.name,
          travel_group_note: "hello",
          travel_group_color: editRow.color.hex
        },
        function(response) {
          editRow.travel.forEach(travel => {
            backend.set_travel_info(
              {
                user_id: session.get("user_id"),
                session_id: session.id().replace("sess:", ""),
                travel_id: travel.travel_id,
                city_id: travel.city_id,
                date_start: travel.date_start,
                date_end: travel.date_end,
                visibility: travel.visibility,
                travel_note: ""
              },
              function(response) {
                console.log(response);
              },
              function(response) {
                alert(response.data.error_message);
              }
            );
          });

          vue.travel_group_list[vue.editIndex] = editRow;
          vue.$set(vue.travel_group_list, vue.editIndex, editRow);
          vue.reMount();
          console.log(response);
        },
        function(response) {
          alert(response.data.error_message);
        }
      );
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
