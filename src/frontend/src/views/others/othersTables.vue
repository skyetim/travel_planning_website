<template>
  <div>
    <base-header type="gradient-success" class="pb-6 pb-8 pt-5 pt-md-8">
      <travel-stats :travelGroup="travel_group_list"/>
    </base-header>

    <div class="container-fluid mt--7">
      <div class="row">
        <div class="col">
          <my-projects-table title="他的行迹" :travel_group_list="travel_group_list" @update="update"></my-projects-table>
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
// TODO : 从router获取参数并请求
import myProjectsTable from './utils/myProjectsTable.vue';

export default {
  data() {
    return {
      travel_group_list: []
    };
  },
  components:{
      "my-projects-table": myProjectsTable
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
        console.log(travel_group_list);
      },
      function(response) {
        alert(response.data.error_message);
      },
      false
    );
  }
};
</script>
<style scoped>
</style>
