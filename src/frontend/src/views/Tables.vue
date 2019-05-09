<template>
  <div>
    <base-header type="gradient-success" class="pb-6 pb-8 pt-5 pt-md-8">
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

    <div class="container-fluid mt--7 div-table">
      <div class="row">
        <div class="col">
          <edit-projects-table title="我的行迹" :tableData="travelGroup"></edit-projects-table>
        </div>
      </div>
    </div>
    <button class="btn btn-primary btn-sm addBox" @click="save()">保存</button>
  </div>
</template>
<script>
var travelGroup = [
  {
    name: "balabala之旅",
    travel: [{location: "广州", coordinate: [23.16667, 113.23333]},
            {location: "深圳", coordinate: [22.61667, 114.06667]},
            {location: "北京", coordinate: [39.95, 116.3]},
            {location: "上海", coordinate: [31.23, 121.47]},
            {location: "南京", coordinate: [32.05, 118.78333]}],
    dates: { start: "2019-05-01" , end: "2019-07-19" },
    status: 2,
  },
  {
    name: "开心之旅",
    travel: [{location: "广州", coordinate: [23.16667, 113.23333]},
            {location: "深圳", coordinate: [22.61667, 114.06667]},
            {location: "北京", coordinate: [39.95, 116.3]},
            {location: "上海", coordinate: [31.23, 121.47]},
            {location: "南京", coordinate: [32.05, 118.78333]}],
    dates: { start: "2019-07-17", end: "2019-07-19" },
    status: 0
  },
  {
    name: "LOL之旅",
    travel: [{location: "广州", coordinate: [23.16667, 113.23333]},
            {location: "深圳", coordinate: [22.61667, 114.06667]},
            {location: "北京", coordinate: [39.95, 116.3]},
            {location: "上海", coordinate: [31.23, 121.47]},
            {location: "南京", coordinate: [32.05, 118.78333]}],
    dates: { start: "2018-07-17", end: "2018-07-19" },
    status: 3
  },
  {
    name: "有意思的行程",
    travel: [{location: "广州", coordinate: [23.16667, 113.23333]},
            {location: "深圳", coordinate: [22.61667, 114.06667]},
            {location: "北京", coordinate: [39.95, 116.3]},
            {location: "上海", coordinate: [31.23, 121.47]},
            {location: "南京", coordinate: [32.05, 118.78333]}],
    dates: { start: "2018-07-17", end: "2018-07-19" },
    status: 1
  },
  {
    name: "Go to Hell!",
    travel: [{location: "广州", coordinate: [23.16667, 113.23333]},
            {location: "深圳", coordinate: [22.61667, 114.06667]},
            {location: "北京", coordinate: [39.95, 116.3]},
            {location: "上海", coordinate: [31.23, 121.47]},
            {location: "南京", coordinate: [32.05, 118.78333]}],
    dates: { start: "2018-07-17", end: "2018-07-19" },
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
<style>
.div-table{
  overflow-y: hidden;
}
</style>
