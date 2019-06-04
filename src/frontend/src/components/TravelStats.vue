<template>
  <div>
    <!-- Card stats -->
    <div class="row">
      <div class="col-xl-3 col-lg-6">
        <stats-card
          title="足迹遍布"
          type="gradient-red"
          :sub-title="getTotal"
          icon="ni ni-planet"
          class="mb-4 mb-xl-0"
        >
          <template slot="footer">
            <span class="text-success mr-2"><i class="ni ni-calendar-grid-58 font"></i>从{{getEarlist}}起</span>
          </template>
        </stats-card>
      </div>

      <!-- <div class="col-xl-3 col-lg-6">
        <stats-card
          title="时间最长"
          type="gradient-red"
          :sub-title="getLongestCity.city"
          icon="ni ni-building"
          class="mb-4 mb-xl-0"
        >
          <template slot="footer">
            <span class="text-success mr-2"><i class="ni ni-calendar-grid-58 font"></i>一共待了{{getLongestCity.days}}天</span>
          </template>
        </stats-card>
      </div>-->

      <div class="col-xl-3 col-lg-6">
        <stats-card
          title="最长城市"
          type="gradient-red"
          :sub-title="getLongestCity.city"
          icon="ni ni-building"
          class="mb-4 mb-xl-0"
        >
          <template slot="footer">
            <span class="text-success mr-2"><i class="ni ni-calendar-grid-58 font"></i>一共待了{{getLongestCity.days}}天</span>
          </template>
        </stats-card>
      </div>

      <div class="col-xl-6 col-lg-6">
        <stats-card
          title="最长行迹"
          type="gradient-red"
          :sub-title="getLongestTravelGroup.name"
          icon="ni ni-istanbul"
          class="mb-4 mb-xl-0"
        >
          <template slot="footer">
            <span class="text-success mr-2"><i class="ni ni-calendar-grid-58 font"></i>一共待了{{getLongestTravelGroup.days}}天</span>
          </template>
        </stats-card>
      </div>
    </div>
  </div>
</template>
<script>
import StatsCard from "./StatsCard.vue";
import moment from "moment";

export default {
  name: "travel-stats",
  props: {
    travel_group_list: Array
  },
  components: {
    "stats-card": StatsCard
  },
  computed: {
    today: function() {
      return moment(Date()).format("YYYY-MM-DD");
    },
    getTotal: function() {
      var vue = this;
      var cities = new Set();
      this.travel_group_list.forEach(travel_group => {
        travel_group.travel.forEach(element => {
          if (element.date_start < vue.today) {
            cities.add(element.location);
          }
        });
      });
      return cities.size + "个城市";
    },
    getYearsAverage: function() {
      var average =
        this.getTotal /
        moment(this.getEarlist)
          .diff(moment(this.today), "years")
          .toString();
      return isNaN(average) ? 0 : average;
    },
    getEarlist: function() {
      var vue = this;
      if (this.travel_group_list.length == 0) {
        return "";
      } else {
        var earlist = vue.today;
        this.travel_group_list.forEach(travel_group => {
          earlist =
            earlist < travel_group.dates.start
              ? earlist
              : travel_group.dates.start;
        });
        return earlist;
      }
    },
    getLongestCity: function() {
      var vue = this;
      var obj = {
        days: 0,
        city: ""
      };
      this.travel_group_list.forEach(travel_group => {
        travel_group.travel.forEach(element => {
          if (element.date_end < vue.today) {
            var days = moment(element.date_end).diff(
              moment(element.date_start),
              "days"
            );

            if (obj.days < days) {
              obj.days = days;
              obj.city = element.location;
            }
          }
        });
      });

      return obj;
    },
    getLongestTravelGroup: function() {
      var vue = this;
      var obj = {
        days: 0,
        name: ""
      };
      this.travel_group_list.forEach(travel_group => {
        if (travel_group.dates.start < vue.today) {
          var days = moment(travel_group.dates.end).diff(
            moment(travel_group.dates.start),
            "days"
          );

          if (obj.days < days) {
            obj.days = days;
            obj.name = travel_group.name;
          }
        }
      });

      return obj;
    }
  }
};
</script>
<style scoped>
.font{
  font-size: 90%;
  margin-right: 5px;
}
</style>
