<template>
  <div>
    <base-header type="gradient-success" class="pb-6 pb-8 pt-5 pt-md-8">
      <travel-stats :travelGroup="travelGroup"/>
    </base-header>

    <div class="container-fluid mt--7 div-table">
      <div class="row">
        <div class="col">
          <edit-projects-table title="我的行迹" :tableData="travelGroup"></edit-projects-table>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
var travelGroup = [
  {
    name: "广州自驾游",
    travel_group_id: "",
    travel: [
      {
        location: "广州",
        coordinate: [23.16667, 113.23333],
        start: "2019-05-12",
        end: "2019-06-15"
      },
      {
        location: "深圳",
        coordinate: [22.61667, 114.06667],
        start: "2019-05-12",
        end: "2019-06-15"
      },
      {
        location: "海陵岛",
        coordinate: [21.85, 111.95],
        start: "2019-05-12",
        end: "2019-06-15"
      }
    ],
    dates: { start: "2019-05-01", end: "2019-07-19" },
    color: { hex: "#f5365c", a: 0.8 },
    status: 2
  },
  {
    name: "云南穷游",
    travel_group_id: "",
    travel: [
      {
        location: "丽江",
        coordinate: [26.86, 100.25],
        start: "2019-05-12",
        end: "2019-06-15"
      },
      {
        location: "昆明",
        coordinate: [25.04, 102.73],
        start: "2019-05-12",
        end: "2019-06-15"
      },
      {
        location: "普洱",
        coordinate: [23.07, 101.03],
        start: "2019-05-12",
        end: "2019-06-15"
      },
      {
        location: "大理",
        coordinate: [25.69, 100.19],
        start: "2019-05-12",
        end: "2019-06-15"
      }
    ],
    dates: { start: "2019-07-17", end: "2019-07-19" },
    color: { hex: "#172b4d", a: 0.8 },
    status: 2
  },
  {
    name: "江南之旅",
    travel_group_id: "",
    travel: [
      {
        location: "南京",
        coordinate: [32.05, 118.78333],
        start: "2019-05-12",
        end: "2019-06-15"
      },
      {
        location: "苏州",
        coordinate: [31.32, 120.62],
        start: "2019-05-12",
        end: "2019-06-15"
      },
      {
        location: "周庄",
        coordinate: [31.13, 120.9],
        start: "2019-05-12",
        end: "2019-06-15"
      },
      {
        location: "上海",
        coordinate: [31.22, 121.48],
        start: "2019-05-12",
        end: "2019-06-15"
      }
    ],
    dates: { start: "2018-07-17", end: "2018-07-19" },
    color: { hex: "#fb6340", a: 0.8 },
    status: 1
  },
  {
    name: "北方之旅",
    travel_group_id: "",
    travel: [
      {
        location: "北京",
        coordinate: [39.92, 116.46],
        start: "2019-05-12",
        end: "2019-06-15"
      },
      {
        location: "承德",
        coordinate: [40.97, 117.93],
        start: "2019-05-12",
        end: "2019-06-15"
      },
      {
        location: "赤峰",
        coordinate: [42.28, 118.87],
        start: "2019-05-12",
        end: "2019-06-15"
      }
    ],
    dates: { start: "2018-07-17", end: "2018-07-19" },
    color: { hex: "#2dce89", a: 0.8 },
    status: 0
  }
];
export default {
  data() {
    return {
      travelGroup: travelGroup,
      map: null,
      markers: []
    };
  },
  beforeCreate: function() {
    var post_data = new Object();
    post_data.user_id = this.$session.get("user_id");
    post_data.session_id = this.$session.id().replace("sess:", "");
    console.log(post_data);

    var vue = this;
    var backend = this.$backend;

    backend.get_travel_group_list(
      post_data,
      function(response) {
        var travel_group_list = response.data.travel_group_list;
        travel_group_list.forEach(travel_group => {
          var travel_list = [];
          travel_group.travel_list.forEach(travel => {
            travel_list.push({
              travel_id: travel.travel_id,
              location: travel.city_name,
              coordinate: [travel.latitude, travel.longtitude],
              start: travel.date_start,
              end: travel.data.date_end,
              citi_id: travel.city_id,
              status: travel.visibility
            });
          });
          vue.travelGroup.push({
            name: travel_group.travel_group_name,
            travel_group_id: travel_group.travel_group_id,
            travel: travel_list,
            dates: {
              start: "",
              end: ""
            },
            status: "",
            color: travel_group.travel_group_color
          });
        });
        alert("success");
      },
      function(response) {
        alert(response.data.error_message);
      }
    );
  }
};
</script>
<style scoped>
.div-table {
  overflow-y: hidden;
}
</style>
