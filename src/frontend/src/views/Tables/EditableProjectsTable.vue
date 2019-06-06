<template>
    <div class="card shadow">
        <div class="card-header border-0">
            <div class="row align-items-center">
                <div class="col">
                    <h3 class="mb-0">{{title}}</h3>
                </div>
                <div class="col text-right">
                    <base-button @click="add_travel_group(newTravelGroup())" size="sm" type="primary">创建新的行程
                    </base-button>
                </div>
            </div>
        </div>
        <div class="table-responsive">
            <editable
                    :data="travel_group_list"
                    :thead-classes="thead-light"
                    class="table align-items-center table-flush"
                    ref="editable"
                    tbody-classes="list"
            >
                <template slot="columns">
                    <th></th>
                    <th>行迹</th>
                    <th>开始</th>
                    <th>结束</th>
                    <th>行程</th>
                </template>

                <template slot-scope="{row}">
                    <th scope="row">
                        <i @click="editTravel(row)" class="ni ni-settings-gear-65 icon-edit"></i>
                    </th>

                    <td>
                        <div>
                            <div>{{row.name}}</div>
                        </div>
                    </td>

                    <td>
                        <div>{{row.dates.start}}</div>
                    </td>

                    <td>
                        <div>{{row.dates.end}}</div>
                    </td>

                    <td>
                        <div>{{displayStatus(row.dates)}}</div>
                    </td>
                </template>
            </editable>
        </div>

        <modal :show.sync="edit.modal">
            <template slot="header">
                <h5 class="modal-title" id="exampleModalLabel">编辑行迹</h5>
            </template>
            <div>
                <small class="text-muted text-center">行迹名</small>
                <br>
                <div class="row">
                    <div class="col-11 inline-div">
                        <base-input placeholder="行迹名" ref="travel_group_name" v-model="editRow.name"></base-input>
                    </div>
                    <div class="inline-div">
                        <i
                                :class="['ni', edit.collapsed ? 'ni-bold-down': 'ni-bold-up', 'icon-expand']"
                                @click="edit.collapsed=!edit.collapsed"
                        ></i>
                    </div>
                </div>
                <div class="row">
                    <div class="col-11">
                        <div :class="[edit.collapsed?'collapse': 'expand']">
                            <draggablelist :friend_info_list="friend_info_list" :gid="editRow.travel_group_id"
                                           :travel="editRow.travel"></draggablelist>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-11">
                        <small class="text-muted text-center">行迹笔记</small>
                        <br>
                        <b-form-textarea placeholder="说点什么吧~" v-model="editRow.travel_group_note"></b-form-textarea>
                    </div>
                </div>
                <div class="row">
                    <div class="col-11">
                        <small class="text-muted text-center">标记颜色</small>
                        <br>
                        <base-dropdown>
                            <button
                                    :style="{backgroundColor:editRow.color.hex, opacity:editRow.color.a}"
                                    class="btn button-text"
                                    slot="title"
                            ></button>
                            <div>
                                <swatches v-model="editRow.color"></swatches>
                            </div>
                        </base-dropdown>
                    </div>
                </div>
            </div>
            <template slot="footer">
                <base-button @click="del(editIndex)edit.modal = false;" type="primary">删除</base-button>
                <base-button @click="set_travel_group(editRow, row)edit.modal = false;" type="primary">保存</base-button>
            </template>
        </modal>
    </div>
</template>

<script>
    import "@/assets/vendor/nucleo/css/nucleo.css";
    import "@/assets/vendor/@fortawesome/fontawesome-free/css/all.min.css";
    import "@/assets/scss/argon.scss";
    import moment from "moment";

    var edit = {
        modal: false,
        collapsed: true
    };

    export default {
        name: "edit-projects-table",
        data() {
            return {
                edit: edit,
                editRow: this.newTravelGroup(),
                editIndex: null
            };
        },
        props: {
            type: {
                type: String
            },
            title: String,
            location: String,
            travel_group_list: Array,
            friend_info_list: Array
        },
        methods: {
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
            editTravel: function (row) {
                this.editRow = this.copy(row);
                // this.editRow = row;
                this.editIndex = this.indexOf(this.travel_group_list, row);
                this.edit.modal = true;
            },
            del: function (index) {
                var vue = this;
                this.$backend_conn(
                    "remove_travel_group",
                    {
                        travel_group_id: this.travel_group_list[index].travel_group_id
                    },
                    vue,
                    function (response) {
                        vue.travel_group_list.splice(index, 1);
                        vue.edit.modal = false;
                        console.log(response);
                    },
                    function (response) {
                        alert(response.data.error_message);
                    }
                );
            },

            // ajax
            add_travel_group: function (row) {
                var vue = this;
                var backend = this.$backend_conn;

                backend(
                    "add_travel_group",
                    {
                        travel_group_name: row.name,
                        travel_group_note: row.travel_group_note,
                        travel_group_color: row.color.hex
                    },
                    vue,
                    function (response) {
                        row.travel_group_id = response.data.travel_group_id;
                        vue.travel_group_list.push(vue.copy(row));
                        vue.$emit("update", vue.travel_group_list);
                        vue.editTravel(vue.travel_group_list[vue.travel_group_list.length - 1]);
                        console.log(response);
                    },
                    function (response) {
                        alert(response.data.error_message);
                    }
                );
            },

            set_travel_group: function (editRow) {
                var vue = this;
                var backend = this.$backend_conn;

                backend(
                    "set_travel_group_info",
                    {
                        travel_group_id: editRow.travel_group_id,
                        travel_group_name: editRow.name,
                        travel_group_note: editRow.travel_group_note,
                        travel_group_color: editRow.color.hex
                    },
                    vue,
                    function (response) {
                        editRow.travel.forEach(travel => {
                            backend(
                                "set_travel_info",
                                {
                                    travel_id: travel.travel_id,
                                    city_id: travel.city_id,
                                    date_start: travel.date_start,
                                    date_end: travel.date_end,
                                    visibility: travel.visibility,
                                    travel_note: ""
                                },
                                vue,
                                function (response) {
                                    console.log(response);
                                },
                                function (response) {
                                    alert(response.data.error_message);
                                }
                            );
                        });

                        vue.travel_group_list[vue.editIndex] = editRow;
                        vue.$emit("update", vue.travel_group_list);
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
    /* icons */

    .icon-expand {
        position: relative;
        margin-top: 10px;
        margin-left: 10px;
        font-size: 150%;
        transition: transform 0.2s;
    }

    .icon-expand:hover {
        transform: scale(1.2);
    }

    .icon-edit {
        font-size: 120%;
        transition: transform 0.2s;
    }

    .icon-edit:hover {
        transform: scale(1.2);
    }

    /* collapse and expand */
    .collapse {
        display: none;
        overflow: hidden;
        background-color: #ffffff;
    }

    .expand {
        display: block;
        overflow: hidden;
        background-color: #ffffff;
    }

    /* Dropdown Content (Hidden by Default) */
    .dropdown-content {
        display: none;
        position: absolute;
        z-index: 2;
    }

    /* modal input*/
    .inline-div {
        display: inline-block;
    }
</style>
