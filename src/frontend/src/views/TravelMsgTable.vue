<template>
    <div :class="type === 'dark' ? 'bg-default': ''"
         class="card shadow">
        <div :class="type === 'dark' ? 'bg-transparent': ''"
             class="card-header border-0">
            <div class="row align-items-center">
                <div class="col">
                    <h3 :class="type === 'dark' ? 'text-white': ''" class="mb-0">
                        {{title}}
                    </h3>
                </div>
                <!-- <div class="col text-right">
                  <base-button type="primary" size="sm">See all</base-button>
                </div> -->
            </div>
        </div>

        <div class='col-md-6 center'>
            <base-alert :type='alert.type' v-if='alert.show'>{{alert.message}}</base-alert>
        </div>

        <div class="table-responsive">
            <base-table :class="type === 'dark' ? 'table-dark': ''"
                        :columns='tableColumn'
                        :data="tableData"
                        :thead-classes="type === 'dark' ? 'thead-dark': 'thead-light'"
                        class="table align-items-center table-flush"
                        tbody-classes="list">

                <template slot-scope="{row}">
                    <th scope="row">
                        <div class="media align-items-center">
                            <a class="avatar rounded-circle mr-3" href="#">
                                <img :src="row.avatar_url" alt="Image placeholder">
                            </a>
                            <div class="media-body">
                                <span class="name mb-0 text-sm">{{row.user_name}}</span>
                            </div>
                        </div>
                    </th>
                    <td class="budget">
                        {{row.msg_content}}
                    </td>
                    <td :ref='row.msg_id' v-if="row.msg_type=='I'">
                        <base-button @click='agree(row.friend_user_id, row.msg_id, row.travel_id)' size='sm'
                                     type='primary'>同意
                        </base-button>
                        <base-button @click='ignore(row.friend_user_id, row.msg_id, row.travel_id)' size='sm'
                                     type='secondary'>忽略
                        </base-button>
                    </td>

                    <td :ref='row.msg_id' v-else>
                        <base-button @click='read(row.friend_user_id, row.msg_id, row.travel_id)' size='sm'
                                     type='primary'>已读
                        </base-button>
                    </td>

                </template>

            </base-table>
        </div>


        <!-- <div class="card-footer d-flex justify-content-end"
             :class="type === 'dark' ? 'bg-transparent': ''">
          <base-pagination total="30"></base-pagination>
        </div> -->

    </div>
</template>
<script>
    export default {
        name: 'friend-msg-table',
        props: {
            type: {
                type: String,
                default: 'light'
            },
            title: String,
            tableData: {
                type: Array,
                default: () => [],
                description: 'Table data'
            }
        },
        data() {
            return {
                tableColumn: [
                    '用户名', '申请信息', '操作'
                ],
                modals: {
                    addFriendShow: false
                },
                request: {
                    others_user_id: '',
                    request_note: ''
                },
                alert: {
                    show: false,
                    message: '',
                    type: 'success'
                }
            }
        },
        methods: {
            agree(friend_user_id, msg_id, friend_travel_id) {
                this.join_friends_travel(friend_user_id, friend_travel_id);
                this.del_travel_msg(msg_id, '已加入');
            },
            ignore(friend_user_id, msg_id, friend_travel_id) {
                this.del_travel_msg(msg_id, '已忽略');
            },
            read(friend_user_id, msg_id, friend_travel_id) {
                this.del_travel_msg(msg_id, '已读');
            },
            join_friends_travel(friend_user_id, friend_travel_id) {
                var that = this;
                var data = {
                    friend_user_id: friend_user_id,
                    friend_travel_id: friend_travel_id
                };

                function success(response) {
                    // 无需处理
                }
                function fail(response) {
                    console.error('获取信息时发生未知错误', response.data);
                }
                this.$backend_conn('join_friends_travel', data, that, success, fail);
            },
            del_travel_msg(msg_id, msg) {
                var that = this;
                var data = {
                    msg_id: msg_id
                };

                function success(response) {
                    that.$refs[msg_id].innerHTML = msg;
                }
                function fail(response) {
                    console.error('获取信息时发生未知错误', response.data);
                }
                this.$backend_conn('del_travel_msg', data, that, success, fail);
            }
        }
    }
</script>
<style>
</style>
