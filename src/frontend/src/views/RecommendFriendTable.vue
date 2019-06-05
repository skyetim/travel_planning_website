<template>
  <div class="card shadow"
       :class="type === 'dark' ? 'bg-default': ''">
    <div class="card-header border-0"
         :class="type === 'dark' ? 'bg-transparent': ''">
      <div class="row align-items-center">
        <div class="col">
          <h3 class="mb-0" :class="type === 'dark' ? 'text-white': ''">
            {{title}}
          </h3>
        </div>
        <!-- <div class="col text-right">
          <base-button type="primary" size="sm">See all</base-button>
        </div> -->
      </div>
    </div>

    <div class='col-md-6 center'>
      <base-alert :type='alert.type' v-if='alert.show' :dismissible='true'>{{alert.message}}</base-alert>
    </div>

    <div class="table-responsive table-fixed-height">
      <base-table class="table align-items-center table-flush"
                  :class="type === 'dark' ? 'table-dark': ''"
                  :thead-classes="type === 'dark' ? 'thead-dark': 'thead-light'"
                  tbody-classes="list"
                  :data="tableData"
                  :columns='tableColumn'>

        <template slot-scope="{row}">
          <th scope="row">
            <div class="media align-items-center">
              <a href="#" class="avatar rounded-circle mr-3">
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

          <td>
            <base-button size='sm' type='secondary' @click='display_note_edit(row.user_id)' v-if='!row.is_friend'>添加好友</base-button>
            <span v-if='row.is_friend' :ref='row.user_id'>已经是好友</span>
          </td>

        </template>

      </base-table>
    </div>

    <modal :show.sync="modals.addFriendShow"
               body-classes="p-0"
               modal-classes="modal-dialog-centered modal-sm">
            <card type="secondary" shadow
                  header-classes="bg-white pb-5"
                  body-classes="px-lg-5 py-lg-5"
                  class="border-0">
                <template>
                    <div class="text-center text-muted mb-4">
                        <small>给用户留言可以增加通过率哦</small>
                    </div>
                    <form role="form">
                        <base-input alternative
                                    class="mb-3"
                                    placeholder="申请备注"
                                    addon-left-icon="ni ni-email-83"
                                    v-model='request.request_note'>
                        </base-input>
                        <div class="text-center">
                            <base-button type="primary" class="my-4" @click='send_friend_request()'>发送好友请求</base-button>
                        </div>
                    </form>
                </template>
            </card>
        </modal>


    <!-- <div class="card-footer d-flex justify-content-end"
         :class="type === 'dark' ? 'bg-transparent': ''">
      <base-pagination total="30"></base-pagination>
    </div> -->

  </div>
</template>
<script>
  export default {
    name: 'recommend-friend-table',
    data() {
      return {
        title: '潜在好友推荐', 
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
      display_note_edit(user_id){
        this.request.others_user_id = user_id;
        this.modals.addFriendShow = true;
      },
      send_friend_request(){
        var that = this;
        function success(response){
          that.modals.addFriendShow = false;
          that.alert.show = true;
          that.alert.message = '好友请求发送成功';
          that.alert.type = 'success';
          // row.is_friend = true;
          // that.$refs[row.user_id] = '已发送好友请求';
        };
        function fail(response){
          if (response.data.status = that.$status['friend_already_exists']){
            that.modals.addFriendShow = false;
            that.alert.show = true;
            that.alert.message = '他已经是您的好友';
            that.alert.type = 'warning';
          } else {
            console.error('获取信息时发生未知错误', response.data);
          }
        };
        this.$backend_conn('send_friend_request', this.request, that, success, fail);
      }, 
      get_friends_info_list(user_list){
        var that = this;
        var data = {
            'other_user_list': user_list
        };
        function success(response){
            that.tableData = response.data.user_info_list.map((user_info_dict)=>{
                user_info_dict['gender'] = that.$gender[user_info_dict['gender']];
                user_info_dict['city_name'] = user_info_dict['resident_city']['city_name'];
                return user_info_dict;
            });
        };
        function fail(response){
            console.error('获取信息时发生未知错误', response.data);
        };
        this.$backend_conn('get_others_user_info_list', data, that, success, fail);
      }, 
    }, 
    created() {
      var that = this;
      var data = {
        // 无需额外数据
      };
      function success(response){
        if (response.data.count==0){
          return;
        }
        that.get_friends_info_list(response.data.user_list);
      };
      function fail(response){
          console.error('获取信息时发生未知错误', response.data);
      };
      this.$backend_conn('recommend_friend_list', data, that, success, fail);
    }
  }
</script>
<style>
.table-fixed-height{
  overflow-y: auto;
  max-height: 400px;
}
</style>
  