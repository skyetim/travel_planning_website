<template>
    <div>
        <base-header class="pb-6 pb-8 pt-5 pt-md-8" type="gradient-success">
            <travel-stats :travel_group_list="travel_group_list"/>
        </base-header>

        <div class="container-fluid mt--7">
            <div class="row">
                <div class="col">
                    <div class="card shadow border-0">
                        <div class="edit-panel">
                            <button
                                    :key="index"
                                    :style="{backgroundColor:travel_group_list[index].color.hex, opacity:travel_group_list[index].color.a}"
                                    @click="editTravel(travel_group_list[index])"
                                    class="btn dropdown-toggle button-text"
                                    slot="title"
                                    v-for="(travel_group, index) in travel_group_list"
                            >{{travel_group_list[index].name}}
                            </button>
                            <base-button @click="add_travel_group(newTravelGroup())" type="primary">创建新的行程
                            </base-button>
                        </div>
                        <div class="map-canvas" id="map-canvas" style="height: 600px;z-index: 10"></div>
                    </div>
                </div>
            </div>
        </div>

        <modal :show.sync="edit.modal">
            <template slot="header">
                <h5 class="modal-title" id="exampleModalLabel">编辑行迹</h5>
            </template>
            <div>
                <small class="text-muted text-center">行迹名</small>
                <br>
                <div class="row">
                    <div class="col-11 inline-div">
                        <base-input placeholder="行迹名" ref="travel_group_name" v-model="editRow.name"></base-input>
                    </div>
                    <div class="inline-div">
                        <i
                                :class="['ni', edit.collapsed ? 'ni-bold-down': 'ni-bold-up', 'icon-expand']"
                                @click="edit.collapsed=!edit.collapsed"
                        ></i>
                    </div>
                </div>
                <div class="row">
                    <div class="col-11">
                        <div :class="[edit.collapsed?'collapse': 'expand']">
                            <draggablelist
                                    :friend_info_list="friend_info_list"
                                    :gid="editRow.travel_group_id"
                                    :travel="editRow.travel"
                            ></draggablelist>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-11">
                        <small class="text-muted text-center">行迹笔记</small>
                        <br>
                        <b-form-textarea placeholder="说点什么吧~" v-model="editRow.travel_group_note"></b-form-textarea>
                    </div>
                </div>
                <div class="row">
                    <div class="col-11">
                        <small class="text-muted text-center">标记颜色</small>
                        <br>
                        <base-dropdown>
                            <button
                                    :style="{backgroundColor:editRow.color.hex, opacity:editRow.color.a}"
                                    class="btn button-text"
                                    slot="title"
                            ></button>
                            <div>
                                <swatches v-model="editRow.color"></swatches>
                            </div>
                        </base-dropdown>
                    </div>
                </div>
            </div>
            <template slot="footer">
                <base-button @click="del(editIndex)edit.modal = false;" type="primary">删除</base-button>
                <base-button @click="set_travel_group(editRow, row)edit.modal = false;" type="primary">保存</base-button>
            </template>
        </modal>
    </div>
</template>
<script>
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

    export default {
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
                friend_info_list: [],
                map: null,
                markersGroup: []
            };
        },
        created: function () {
            var vue = this;
            var backend = this.$backend_conn;

            backend(
                "get_all_travel_group_details",
                {},
                vue,
                function (response) {
                    var travel_group_list = response.data.travel_group_info_list;
                    travel_group_list.forEach(travel_group => {
                        var tmp_list = travel_group.travel_infos.travel_info_list;
                        tmp_list.sort(vue.compare("date_start"));

                        tmp_list.forEach(travel => {
                            backend(
                                "get_travel_company_list",
                                {travel_id: travel.travel_id},
                                vue,
                                function (response1) {
                                    var company_list = [];
                                    response1.data.company_list.forEach(user_id => {
                                        backend(
                                            "get_others_user_info",
                                            {others_user_id: user_id},
                                            vue,
                                            function (response2) {
                                                company_list.push({
                                                    user_id: user_id,
                                                    user_name: response2.data.user_name,
                                                    avatar_url: response2.data.avatar_url
                                                });
                                                travel.company_list = company_list;
                                            },
                                            function (response1) {
                                                alert(response1.data.error_message);
                                            }
                                        );
                                    });
                                    travel.company_list = company_list;
                                },
                                function (response) {
                                    alert(response.data.error_message);
                                }
                            );
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
                            color: {hex: travel_group.travel_group_color, a: 0.8}
                        });
                    });
                    vue.markersGroup = mountMap(vue.map, vue.travel_group_list);
                },
                function (response) {
                    alert(response.data.error_message);
                }
            );

            backend(
                "get_friend_list",
                {},
                vue,
                function (response) {
                    response.data.friend_list.forEach(user_id => {
                        backend(
                            "get_others_user_info",
                            {others_user_id: user_id},
                            vue,
                            function (response1) {
                                vue.friend_info_list.push({
                                    user_id: user_id,
                                    user_name: response1.data.user_name,
                                    avatar_url: response1.data.avatar_url
                                });
                            },
                            function (response1) {
                                alert(response1.data.error_message);
                            }
                        );
                    });
                },
                function (response) {
                    alert(response.data.error_message);
                }
            );
        },
        mounted: function () {
            this.map = L.map("map-canvas").setView([37.51, 105.18], 4);

            // tile
            L.tileLayer(
                "https://api.mapbox.com/styles/v1/oymisaki/cjvkxybdi2dt91cqiktdeozp9/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1Ijoib3ltaXNha2kiLCJhIjoiY2p0ZWEwZDRlMWcwcTQzbW9xcWd5MnpxbyJ9.Ri_EK6iwsLzeH-ZgxJg0ig",
                {
                    attribution:
                        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
                    subdomains: "abcd",
                    maxZoom: 6,
                    minZoom: 2
                }
            ).addTo(this.map);
        },
        methods: {
            reMount: function () {
                // 提交表单到数据库
                for (var i = 0; i < this.markersGroup.length; i++) {
                    for (var j = 0; j < this.markersGroup[i].length; j++) {
                        this.map.removeLayer(this.markersGroup[i][j]);
                    }
                }
                this.markersGroup = mountMap(this.map, this.travel_group_list);
            },
            editTravel: function (row) {
                this.editRow = this.copy(row);
                this.editIndex = this.indexOf(this.travel_group_list, row);
                this.edit.addMode = false;
                this.edit.modal = true;
            },
            del: function (index) {
                var vue = this;
                this.$backend_conn(
                    "remove_travel_group",
                    {
                        travel_group_id: this.travel_group_list[index].travel_group_id
                    },
                    vue,
                    function (response) {
                        vue.travel_group_list.splice(index, 1);
                        vue.edit.modal = false;
                    },
                    function (response) {
                        alert(response.data.error_message);
                    }
                );
            },
            // ajax
            add_travel_group: function (row) {
                var vue = this;
                var backend = this.$backend_conn;
                backend(
                    "add_travel_group",
                    {
                        travel_group_name: row.name,
                        travel_group_note: row.travel_group_note,
                        travel_group_color: row.color.hex
                    },
                    vue,
                    function (response) {
                        row.travel_group_id = response.data.travel_group_id;
                        vue.travel_group_list.push(vue.copy(row));
                        vue.$set(
                            vue.travel_group_list,
                            vue.travel_group_list.length - 1,
                            vue.copy(row)
                        );
                        vue.editTravel(
                            vue.travel_group_list[vue.travel_group_list.length - 1]
                        );
                        vue.reMount();
                    },
                    function (response) {
                        alert(response.data.error_message);
                    }
                );
            },

            set_travel_group: function (editRow) {
                var vue = this;
                var backend = this.$backend_conn;

                backend(
                    "set_travel_group_info",
                    {
                        travel_group_id: editRow.travel_group_id,
                        travel_group_name: editRow.name,
                        travel_group_note: editRow.travel_group_note,
                        travel_group_color: editRow.color.hex
                    },
                    vue,
                    function (response) {
                        editRow.travel.forEach(travel => {
                            backend(
                                "set_travel_info",
                                {
                                    travel_id: travel.travel_id,
                                    city_id: travel.city_id,
                                    date_start: travel.date_start,
                                    date_end: travel.date_end,
                                    visibility: travel.visibility,
                                    travel_note: ""
                                },
                                vue,
                                function (response) {
                                },
                                function (response) {
                                    alert(response.data.error_message);
                                }
                            );
                        });

                        vue.travel_group_list[vue.editIndex] = editRow;
                        vue.$set(vue.travel_group_list, vue.editIndex, editRow);
                        vue.reMount();
                    },
                    function (response) {
                        alert(response.data.error_message);
                    }
                );
            }
        }
    };
</script>
<style scoped>
    .edit-panel {
        position: absolute;
        margin-top: 20px;
        margin-left: 20px;
        padding: 20px;
        /* width: 100px;
        height: 100px; */
        z-index: 11;
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
