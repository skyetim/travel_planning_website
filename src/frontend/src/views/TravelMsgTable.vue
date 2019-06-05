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
      <base-alert :type='alert.type' v-if='alert.show'>{{alert.message}}</base-alert>
    </div>

    <div class="table-responsive">
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
                <img alt="Image placeholder" :src="row.avatar_url">
              </a>
              <div class="media-body">
                <span class="name mb-0 text-sm">{{row.user_name}}</span>
              </div>
            </div>
          </th>
          <td class="budget">
            {{row.msg_content}}
          </td>
          <td v-if="row.msg_type=='I'" :ref='row.msg_id'>
            <base-button size='sm' type='primary' @click='agree(row.friend_user_id, row.msg_id, row.travel_id)'>同意</base-button>
            <base-button size='sm' type='secondary' @click='ignore(row.friend_user_id, row.msg_id, row.travel_id)'>忽略</base-button>
          </td>

          <td v-else :ref='row.msg_id'>
            <base-button size='sm' type='primary' @click='read(row.friend_user_id, row.msg_id, row.travel_id)'>已读</base-button>            
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
      agree(friend_user_id, msg_id, friend_travel_id){
        this.join_friends_travel(friend_user_id, friend_travel_id);
        this.del_travel_msg(msg_id, '已加入');
      }, 
      ignore(friend_user_id, msg_id, friend_travel_id){
        this.del_travel_msg(msg_id, '已忽略');
      },
      read(friend_user_id, msg_id, friend_travel_id){
        this.del_travel_msg(msg_id, '已读');
      },
      join_friends_travel(friend_user_id, friend_travel_id){
        var that = this;
        var data = {
          friend_user_id: friend_user_id, 
          friend_travel_id: friend_travel_id
        };
        function success(response){
          // 无需处理
        };
        function fail(response){
            console.error('获取信息时发生未知错误', response.data);
        };
        this.$backend_conn('join_friends_travel', data, that, success, fail);
      }, 
      del_travel_msg(msg_id, msg){
        var that = this;
        var data = {
          msg_id: msg_id
        };
        function success(response){
          that.$refs[msg_id].innerHTML = msg;          
        };
        function fail(response){
            console.error('获取信息时发生未知错误', response.data);
        };
        this.$backend_conn('del_travel_msg', data, that, success, fail);
      }
    }
  }
</script>
<style>
</style>
  