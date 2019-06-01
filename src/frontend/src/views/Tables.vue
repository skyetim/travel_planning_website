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
  }
};
</script>
<style scoped>
.div-table {
  overflow-y: hidden;
}
</style>
