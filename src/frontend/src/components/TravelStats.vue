<template>
  <div>
    <!-- Card stats -->
    <div class="row">
      <div class="col-xl-3 col-lg-6">
        <stats-card
          title="我的足迹遍布"
          type="gradient-red"
          :sub-title="getTotal"
          icon="ni ni-active-40"
          class="mb-4 mb-xl-0"
        >
          <template slot="footer">
            <span class="text-nowrap">从{{getEarlist}}起</span>
            <br/>
            <span class="text-success mr-2">
              <i class="fa fa-arrow-up"></i>
              平均每年去{{getAverage}}个城市
            </span>
          </template>
        </stats-card>
      </div>
      <!-- <div class="col-xl-3 col-lg-6">
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
      </div> -->
    </div>
  </div>
</template>
<script>
import StatsCard from "./StatsCard.vue";

export default {
  name: "travel-stats",
  props: {
    travelGroup: Array
  },
  components: {
    "stats-card": StatsCard
  },
  computed: {
    getTotal: function() {
      var cities = new Set();
      this.travelGroup.forEach(travel => {
        travel.travel.forEach(element => {
          cities.add(element.location);
        });
      });
      return cities.size + "个城市";
    },
    getAverage: function() {
      return 1;
    },
    getEarlist: function() {
      return "2009-01-01";
    }
  }
};
</script>
<style scoped>
</style>
