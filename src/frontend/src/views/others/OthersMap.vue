<template>
    <div>
        <base-header class="pb-6 pb-8 pt-5 pt-md-8" type="gradient-success"></base-header>

        <div class="container-fluid mt--7">
            <div class="row">
                <div class="col">
                    <div class="card shadow border-0">
                        <div class="show-panel">
                            <button
                                    :key="index"
                                    :style="{backgroundColor:travel_group_list[index].color.hex, opacity:travel_group_list[index].color.a}"
                                    class="btn dropdown-toggle button-text"
                                    slot="title"
                                    v-for="(travel_group, index) in travel_group_list"
                            >{{travel_group_list[index].name}}
                            </button>
                        </div>
                        <div class="map-canvas" id="map-canvas" style="height: 600px;z-index: 10"></div>
                    </div>
                </div>
            </div>
        </div>
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

    export default {
        'name': "others-map",
        data() {
            return {
                map: null,
                markersGroup: []
            };
        },
        props: {
            travel_group_list: Array
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
                    minZoom: 4
                }
            ).addTo(this.map);
            this.markersGroup = mountMap(this.map, this.travel_group_list);
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
</style>
