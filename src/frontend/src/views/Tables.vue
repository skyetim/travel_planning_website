<template>
  <div>
    <base-header type="gradient-success" class="pb-6 pb-8 pt-5 pt-md-8">
      <travel-stats :travel_group_list="travel_group_list"/>
    </base-header>

    <div class="container-fluid mt--7">
      <div class="row">
        <div class="col">
          <edit-projects-table
            title="我的行迹"
            :travel_group_list="travel_group_list"
            :friend_info_list="friend_info_list"
            @update="update_travel_group"
          ></edit-projects-table>
        </div>
      </div>

      <div class="row mt-5">
        <div class="col">
          <associate-travel-table
            title="关联行迹"
            :associate_travel_list="associate_travel_list"
            @update="update_associate_travel"
          ></associate-travel-table>
        </div>
      </div>
    </div>

    <!-- <div>{{JSON.stringify(travel_group_list)}}</div> -->
  </div>
</template>
<script>
import AssociateTravelTable from "./Tables/AssociateTravelTable.vue";

export default {
  data() {
    return {
      travel_group_list: [],
      friend_info_list: [],
      associate_travel_list: []
    };
  },
  components: {
    "associate-travel-table": AssociateTravelTable
  },
  created: function() {
    var vue = this;
    var backend = this.$backend_conn;

    backend(
      "get_all_travel_group_details",
      {},
      vue,
      function(response) {
        var travel_group_list = response.data.travel_group_info_list;
        travel_group_list.forEach(travel_group => {
          var tmp_list = travel_group.travel_infos.travel_info_list;
          tmp_list.sort(vue.compare("date_start"));

          tmp_list.forEach(travel => {
            backend(
              "get_travel_company_list",
              { travel_id: travel.travel_id },
              vue,
              function(response1) {
                var company_list = [];
                response1.data.company_list.forEach(user_id => {
                  backend(
                    "get_others_user_info",
                    { others_user_id: user_id },
                    vue,
                    function(response2) {
                      company_list.push({
                        user_id: user_id,
                        user_name: response2.data.user_name,
                        avatar_url: response2.data.avatar_url
                      });
                      travel.company_list = company_list;
                    },
                    function(response1) {
                      alert(response1.data.error_message);
                    }
                  );
                });
                travel.company_list = company_list;
              },
              function(response) {
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
            color: { hex: travel_group.travel_group_color, a: 0.8 }
          });
        });

      },
      function(response) {
        alert(response.data.error_message);
      }
    );

    backend(
      "get_friend_list",
      {},
      vue,
      function(response) {
        response.data.friend_list.forEach(user_id => {
          backend(
            "get_others_user_info",
            { others_user_id: user_id },
            vue,
            function(response1) {
              vue.friend_info_list.push({
                user_id: user_id,
                user_name: response1.data.user_name,
                avatar_url: response1.data.avatar_url
              });
            },
            function(response1) {
              alert(response1.data.error_message);
            }
          );
        });
      },
      function(response) {
        alert(response.data.error_message);
      }
    );
  },
  methods: {
    update_travel_group: function(data) {
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
    },

    update_associate_travel: function(data) {
      this.associate_travel_list = JSON.parse(JSON.stringify(data));
    }
  }
};
</script>
<style scoped>
</style>
