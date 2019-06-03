<template>
  <div>
    <base-header type="gradient-success" class="pb-6 pb-8 pt-5 pt-md-8">
      <travel-stats :travelGroup="travel_group_list"/>
    </base-header>

    <div class="container-fluid mt--7">
      <div class="row">
        <div class="col">
          <edit-projects-table title="我的行迹" :travel_group_list="travel_group_list" @update="update"></edit-projects-table>
        </div>
      </div>

      <div class="row mt-5">
        <div class="col"></div>
      </div>
    </div>

    <!-- <div>{{JSON.stringify(travel_group_list)}}</div> -->
  </div>
</template>
<script>
export default {
  data() {
    return {
      travel_group_list: []
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
                travel.vbool = (travel.visibility == 'F');
                travel.location = response1.data.city_name;
                travel.coordinate = [
                  response1.data.latitude,
                  response1.data.longitude
                ];
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
        console.log(travel_group_list);
      },
      function(response) {
        alert(response.data.error_message);
      }
    );
  },

  methods: {
    update: function(data) {
      var vue = this;
      this.travel_group_list = JSON.parse(JSON.stringify(data));
      this.travel_group_list.forEach(travel_group => {
        travel_group.travel.sort(vue.compare("date_start"));
        travel_group.dates.start =
          travel_group.travel.length > 0
            ? travel_group.travel[0].date_start
            : "";
        travel_group.dates.end =
          travel_group.travel.length > 0
            ? travel_group.travel[travel_group.travel.length - 1].date_end
            : "";
      });
    }
  }
};
</script>
<style scoped>
</style>
