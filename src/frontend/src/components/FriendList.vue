<template>
  <div>
    <div class="row">
      <div class="col">
        <base-alert type="success" v-show="success">
          <span class="alert-inner--icon" margin-right="10px">
            <i class="ni ni-bell-55"></i>
          </span>
          <span class="alert-inner--text">
            <strong>已成功邀请!</strong> 请等待好友同意!
          </span>
          <button
            @click="success=false;"
            type="button"
            class="close"
            data-dismiss="alert"
            aria-label="Close"
          >
            <span aria-hidden="true">&times;</span>
          </button>
        </base-alert>
      </div>
    </div>
    <div class="friend-list">
      <div class="row align-items-center">
        <div class="col-10">
          <div class="avatar-group">
            <a
              v-for="(friend, index) in travel_company"
              :key="index"
              href="#"
              class="avatar avatar-sm rounded-circle"
              data-toggle="tooltip"
              :data-original-title="friend.user_name"
            >
              <img alt="Image placeholder" :src="friend.avatar_url">
            </a>
            <small>{{hasCompany()?"":"还没有同伴哦，快快邀请吧！"}}</small>
          </div>
        </div>
        <div class="col-2 text-right">
          <base-button
            v-show="hasFriend()"
            type="primary"
            size="sm"
            @click="showList = !showList;"
          >{{showList?"完成": "管理同行"}}</base-button>
        </div>
      </div>

      <div
        v-show="showList"
        class="row align-items-center"
        v-for="(friend,index) in friend_info_list"
        :key="index"
      >
        <div class="col-1">
          <a
            href="#"
            class="avatar avatar-sm rounded-circle"
            data-toggle="tooltip"
            :data-original-title="friend.user_name"
          >
            <img alt="Image placeholder" :src="friend.avatar_url">
          </a>
        </div>
        <div class="col-9 text-left">{{friend.user_name}}</div>
        <div class="col-2 text-right">
          <base-button
            type="primary"
            size="sm"
            @click="isCompany(friend)?del(friend):invite(friend)"
          >{{isCompany(friend)?"移除":"邀请"}}</base-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "friend-list",
  props: {
    travel_id: Number,
    friend_info_list: Array
  },
  data() {
    return {
      travel_company: [],
      showList: false,
      success: false
    };
  },
  created: function() {
    var vue = this;
    if (typeof this.travel_id != "undefined") {
      this.$backend_conn(
        "get_travel_company_list",
        { travel_id: this.travel_id },
        vue,
        function(response) {
          response.data.company_list.forEach(user_id => {
            vue.friend_info_list.forEach(friend => {
              if (friend.user_id == user_id) {
                vue.travel_company.push({
                  user_id: user_id,
                  user_name: friend.user_name,
                  avatar_url: friend.avatar_url
                });
              }
            });
          });
          vue.friend_info_list.forEach;
          console.log(response);
        },
        function(response) {
          alert(response.data.error_message);
        }
      );
    }
  },
  methods: {
    isCompany: function(friend) {
      var start = false;
      this.travel_company.forEach(company => {
        if (company.user_id == friend.user_id) {
          start = true;
        }
      });
      return start;
    },
    hasCompany: function() {
      return this.travel_company.length != 0;
    },
    hasFriend: function() {
      return this.friend_info_list.length != 0;
    },
    del(friend) {
      var vue = this;
      this.$backend_conn(
        "remove_travel_company",
        {
          travel_id: vue.travel_id,
          friend_user_id: friend.user_id
        },
        vue,
        function(response) {
          for (var i = 0; i < vue.travel_company.length; ++i) {
            if (vue.travel_company[i].user_id == friend.user_id) {
              vue.travel_company.splice(i, 1);
            }
          }
          console.log(response);
        },
        function(response) {
          alert(response.data.error_message);
        }
      );
    },

    invite(friend) {
      var vue = this;

      this.$backend_conn(
        "invite_travel_company",
        {
          travel_id: vue.travel_id,
          friend_user_id: friend.user_id
        },
        vue,
        function(response) {
          vue.success = true;
          setTimeout(function() {
            vue.success = false;
          }, 2000);
          console.log(response);
        },
        function(response) {
          alert(response.data.error_message);
        }
      );
    }
  }
};
</script>
<style scoped>
.friend-list {
  max-height: 200px;
  overflow-y: auto;
  overflow-x: hidden;
}
</style>

