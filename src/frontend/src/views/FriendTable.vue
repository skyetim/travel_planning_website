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
            <base-alert :dismissible='true' :type='alert.type' v-if='alert.show'>{{alert.message}}</base-alert>
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
                                <img :src="row.avatar_url">
                            </a>
                            <div class="media-body">
                                <span class="name mb-0 text-sm">{{row.user_name}}</span>
                            </div>
                        </div>
                    </th>
                    <td class="budget">
                        {{row.gender}}
                    </td>
                    <td>
                        {{row.city_name}}
                    </td>

                    <!-- <td>
                      <base-dropdown class="dropdown"
                                     position="right">
                        <a slot="title" class="btn btn-sm btn-icon-only text-light" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                          <i class="fas fa-ellipsis-v"></i>
                        </a>

                        <template>
                          <a class="dropdown-item" @click='modals.addFriendShow=true' href="#">添加好友</a>
                        </template>
                      </base-dropdown>
                    </td> -->

                    <td :ref='row.user_id'>
                        <base-button @click='del_friend(row)' size='sm' type='secondary'>删除好友</base-button>
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
        name: 'friend-table',
        data() {
            return {
                title: '好友列表',
                type: 'light',
                tableData: [],
                tableColumn: [
                    '用户名', '性别', '常住地', '操作'
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
            del_friend(row) {
                var that = this;
                var data = {
                    'friend_user_id': row.user_id
                };

                function success(response) {
                    that.$refs[row.user_id].innerHTML = '删除成功';
                }
<<<<<<< HEAD
                function fail(response) {
                    console.error('获取信息时发生未知错误', response.data);
                }
=======

                function fail(response) {
                    console.error('获取信息时发生未知错误', response.data);
                }

>>>>>>> frontend
                this.$backend_conn('remove_friend', data, that, success, fail);
            },
            get_friends_info_list(user_list) {
                var that = this;
                var data = {
                    'other_user_list': user_list
                };

                function success(response) {
                    that.tableData = response.data.user_info_list.map((user_info_dict) => {
                        user_info_dict['gender'] = that.$gender[user_info_dict['gender']];
                        user_info_dict['city_name'] = user_info_dict['resident_city']['city_name'];
                        return user_info_dict;
                    });
                }
<<<<<<< HEAD
                function fail(response) {
                    console.error('获取信息时发生未知错误', response.data);
                }
=======

                function fail(response) {
                    console.error('获取信息时发生未知错误', response.data);
                }

>>>>>>> frontend
                this.$backend_conn('get_others_user_info_list', data, that, success, fail);
            },
        },
        created() {
            var that = this;
            var data = {
                // 无需额外数据
            };

            function success(response) {
                if (response.data.count == 0) {
                    return;
                }
                that.get_friends_info_list(response.data.friend_list);
            }
<<<<<<< HEAD
            function fail(response) {
                console.error('获取信息时发生未知错误', response.data);
            }
=======

            function fail(response) {
                console.error('获取信息时发生未知错误', response.data);
            }

>>>>>>> frontend
            this.$backend_conn('get_friend_list', data, that, success, fail);
        }
    }
</script>
<style>
</style>
