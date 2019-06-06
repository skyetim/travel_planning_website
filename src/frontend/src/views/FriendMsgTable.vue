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
                    <td :ref='row.msg_id' v-if="row.msg_type=='A'">
                        <base-button @click='agree(row.friend_user_id, row.msg_id)' size='sm' type='primary'>同意
                        </base-button>
                        <base-button @click='ignore(row.friend_user_id, row.msg_id)' size='sm' type='secondary'>忽略
                        </base-button>
                    </td>
                    <td :ref='row.msg_id' v-else-if="row.msg_type=='D'">
                        <base-button @click='read(row.friend_user_id, row.msg_id)' size='sm' type='primary'>已读
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
            agree(friend_user_id, msg_id) {
                this.add_friend(friend_user_id);
                this.del_friend_msg(msg_id, '已添加');
            },
            ignore(friend_user_id, msg_id) {
                this.del_friend_msg(msg_id, '已忽略');
            },
            read(friend_user_id, msg_id) {
                this.del_friend_msg(msg_id, '已读');
            },
            add_friend(friend_user_id) {
                var that = this;
                var data = {
                    friend_user_id: friend_user_id,
                    friend_note: ''
                };

                function success(response) {
                    // 无需处理
                }
                function fail(response) {
                    if (response.data.status == that.$status['friend_already_exists']) {
                        return;
                    }
                    console.error('获取信息时发生未知错误', response.data);
                }
                this.$backend_conn('add_friend', data, that, success, fail);
            },
            del_friend_msg(msg_id, msg) {
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
                this.$backend_conn('del_friend_msg', data, that, success, fail);
            }
        }
    }
</script>
<style>
</style>
