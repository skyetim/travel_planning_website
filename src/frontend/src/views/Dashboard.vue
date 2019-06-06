<template>
    <div>
        <base-header class="pb-6 pb-8 pt-5 pt-md-8" type="gradient-success">
            <!-- Card stats -->
            <travel-stats :travel_group_list="travel_group_list"/>
        </base-header>

        <!--Charts-->
        <div class="container-fluid mt--7">
            <div class="row">
                <div class="col-xl-8 mb-5 mb-xl-0">
                    <card header-classes="bg-transparent" type='transparent'>
                        <recommend-friend-table/>
                    </card>
                    <card header-classes="bg-transparent" type='transparent'>
                        <edit-projects-table
                                :friend_info_list="friend_info_list"
                                :travel_group_list="travel_group_list"
                                @update="update_travel_group"
                                title="行迹"
                        ></edit-projects-table>
                    </card>
                </div>

                <div class="col-xl-4">
                    <user-card-preview
                            :avatar_url="model.avatar_url"
                            :comment="model.comment"
                            :gender="model.gender"
                            :resident_city="model.resident_city_name"
                            :user_name="model_user_name"
                    ></user-card-preview>
                </div>
            </div>
            <!-- <div class="row">
              <div class="col">
                <edit-projects-table
                  title="行迹"
                  :travel_group_list="travel_group_list"
                  :friend_info_list="friend_info_list"
                  @update="update_travel_group"
                ></edit-projects-table>
              </div>
            </div> -->
        </div>
    </div>
</template>
<script>
    import UserCardPreview from "./UserCardPreview.vue";
    import RecommendFriendTable from "./RecommendFriendTable.vue";

    export default {
        components: {
            "user-card-preview": UserCardPreview,
            "recommend-friend-table": RecommendFriendTable
        },
        data() {
            return {
                friend_info_list: [],
                travel_group_list: [],
                model: {
                    email: "",
                    first_name: "",
                    last_name: "",
                    gender: "",
                    comment: "",
                    resident_city_id: "",
                    old_password: "",
                    new_password: "",
                    verify_password: "",
                    avatar_url: "",
                    resident_city_name: ""
                }
            };
        },
        computed: {
            model_user_name: function () {
                if (
                    typeof this.model.last_name === "undefined" ||
                    typeof this.model.first_name === "undefined"
                ) {
                    return "";
                } else {
                    return this.model.last_name + " " + this.model.first_name;
                }
            }
        },
        methods: {
            update_travel_group: function (data) {
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
        },
        mounted() {
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
                },
                function (response) {
                    alert(response.data.error_message);
                }
            );

            var that = this;

            function success(response) {
                let user_name = response.data.user_name;
                that.model.first_name = user_name.split(" ")[1];
                that.model.last_name = user_name.split(" ")[0];
                that.model.email = response.data.email;
                that.model.gender = that.$gender[response.data.gender];
                that.model.resident_city_id = response.data.resident_city.city_id;
                that.model.resident_city_name = response.data.resident_city.city_name;
                that.model.comment = response.data.comment;
                that.model.avatar_url = response.data.avatar_url;
                if (that.model.avatar_url == "") {
                    that.model.avatar_url = "img/theme/team-4-800x800.jpg";
                }
            }

            function fail(response) {
                console.error("获取信息时发生未知错误", response.data);
            }

            this.$backend_conn("get_user_info", {}, that, success, fail);

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
        }
    };
</script>
<style scoped>
    .set-margin {
        margin-top: 200px;
    }
</style>
