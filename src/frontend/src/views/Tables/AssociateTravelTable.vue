<template>
    <div class="card shadow">
        <div class="card-header border-0">
            <div class="row align-items-center">
                <div class="col">
                    <h3 class="mb-0">{{title}}</h3>
                </div>
                <div class="col text-right">
                    <small>{{hasAssociate()?"": "还没有关联行程哦~快去寻找伙伴吧"}}</small>
                </div>
            </div>
        </div>
        <div class="table-responsive">
            <editable
                    :data="associate_travel_list"
                    :thead-classes="thead-light"
                    class="table align-items-center table-flush"
                    ref="editable"
                    tbody-classes="list"
                    v-show="hasAssociate()"
            >
                <template slot="columns">
                    <th></th>
                    <th>城市</th>
                    <th>开始</th>
                    <th>结束</th>
                    <th>行程</th>
                    <th>行程创建者</th>
                </template>

                <template slot-scope="{row}">
                    <th scope="row">
                        <base-button @click="leave_travel(row)" size="sm" type="primary">取消同行</base-button>
                    </th>

                    <td>
                        <div>
                            <div>{{row.city.city_name}}</div>
                        </div>
                    </td>

                    <td>
                        <div>{{row.date_start}}</div>
                    </td>

                    <td>
                        <div>{{row.date_end}}</div>
                    </td>

                    <td>
                        <div>{{displayStatus({start: row.date_start, end:row.date_end})}}</div>
                    </td>
                    <td>
                        <div class="avatar-group">
                            <a
                                    :data-original-title="row.owner_user_name"
                                    class="avatar avatar-sm rounded-circle"
                                    data-toggle="tooltip"
                                    href="#"
                            >
                                <img :src="row.owner_avatar_url" alt="Image placeholder">
                            </a>
                        </div>
                    </td>
                </template>
            </editable>
        </div>
    </div>
</template>

<script>
    import "@/assets/vendor/nucleo/css/nucleo.css";
    import "@/assets/vendor/@fortawesome/fontawesome-free/css/all.min.css";
    import "@/assets/scss/argon.scss";
    import moment from "moment";

    export default {
        name: "associate-travel-table",
        data() {
            return {};
        },
        props: {
            type: {
                type: String
            },
            title: String,
            associate_travel_list: Array
        },
        methods: {
            hasAssociate: function () {
                return this.associate_travel_list.length != 0;
            },
            displayStatus: function (dates) {
                if (!dates.start || !dates.end) {
                    return "";
                }

                var begin = moment(dates.start);
                var end = moment(dates.end);
                var today = moment(Date());

                if (begin.isBefore(today) && today.isBefore(end)) {
                    return "行程中";
                } else if (end.isBefore(today)) {
                    return "";
                } else {
                    return "距离行程开始" + begin.diff(today, "days").toString() + "天";
                }
            },

            // ajax
            leave_travel: function (row) {
                var vue = this;
                var backend = this.$backend_conn;

                backend(
                    "leave_friends_travel",
                    {
                        friend_user_id: row.owner_user_id,
                        friend_travel_id: row.travel_id
                    },
                    vue,
                    function (response) {
                        vue.associate_travel_list.splice(
                            vue.indexOf(vue.associate_travel_list, row),
                            1
                        );
                        vue.$emit("update", vue.associate_travel_list);
                        console.log(response);
                    },
                    function (response) {
                        alert(response.data.error_message);
                    }
                );
            }
        }
    };
</script>

<style scoped>


</style>
