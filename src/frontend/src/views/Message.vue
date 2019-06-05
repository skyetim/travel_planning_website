<template>
    <div>
        <base-header type="gradient-success" class="pb-6 pb-8 pt-5 pt-md-8">
        <div class="container-fluid d-flex align-items-center">
                <div class="col-lg-7 col-md-10">
                    <h1 class="display-2 text-white">Hi {{this.$session.get('user_name')}}, </h1>
                    <p class="text-white mt-0 mb-5">你可以在这里处理你的好友请求, 同行邀请</p>
                </div>
        </div>
        </base-header>

        <base-alert type='default' v-if='alert.show'> {{alert.message}} </base-alert>

        <div class="container-fluid mt--7 div-table">
            <friend-message-table :type='friend_message.type' :title='friend_message.title' :tableData='friend_message.tableData'/>
            <!-- </card> -->
        </div>

        <div class="container-fluid mt-5 div-table">
            <travel-message-table :type='travel_message.type' :title='travel_message.title' :tableData='travel_message.tableData'/>
        </div>


    </div>
</template>
<script>
import FriendMessageTable from './FriendMsgTable';
import TravelMessageTable from './FriendMsgTable';
    export default {
        name: 'test',
        data() {
            return {
                friend_message:{
                    type: "light", 
                    title: '好友请求信息', 
                    tableData: []
                }, 
                travel_message: {
                    type: "light", 
                    title: '行迹邀请信息', 
                    tableData: []
                }, 
                alert: {
                    show: false, 
                    message: ''
                }
            }
        },
        computed: {
        }, 
        components: {
            'friend-message-table': FriendMessageTable,
            'travel-message-table': TravelMessageTable,
        }, 
        methods: {
            get_friend_msg_list(){
                var that = this;
                var data = {
                    // 无需额外数据
                };
                function success(response){
                    that.friend_message.tableData = response.data['msg_list'];
                    that.get_friends_info_list();
                };
                function fail(response){
                    console.error('获取信息时发生未知错误', response.data);
                };
                this.$backend_conn('get_friend_msg_list', data, that, success, fail);
            }, 
            get_friends_info_list(){
                var that = this;
                var others_user_list = that.friend_message.tableData.map((user_info_dict)=>{return user_info_dict['friend_user_id'];});
                var data = {
                    'other_user_list': others_user_list
                };
                function success(response){
                    var user_id_map = {};
                    response.data.user_info_list.forEach((user_info_dict)=>{
                        if (!(user_info_dict['user_id'] in user_id_map)) {
                            user_id_map[user_info_dict['user_id']] = {
                                'user_name': user_info_dict['user_name'], 
                                'avatar_url': user_info_dict['avatar_url']
                            }
                        }
                    });
                    for (var index in that.friend_message.tableData){
                        var row = that.friend_message.tableData[index];
                        row['user_name'] = user_id_map[parseInt(row['friend_user_id'])]['user_name'];
                        row['avatar_url'] = user_id_map[parseInt(row['friend_user_id'])]['avatar_url'];
                    }
                };
                function fail(response){
                    console.error('获取信息时发生未知错误', response.data);
                };
                this.$backend_conn('get_others_user_info_list', data, that, success, fail);
            }, 
            get_travel_msg_list(){
                var that = this;
                var data = {
                    // 无需额外数据
                };
                function success(response){
                };
                function fail(response){
                    console.error('获取信息时发生未知错误', response.data);
                };
                this.$backend_conn('get_travel_msg_list', data, that, success, fail);
            }
        }, 
        mounted(){
            this.get_friend_msg_list();
            this.get_travel_msg_list();
        }
    }
</script>
