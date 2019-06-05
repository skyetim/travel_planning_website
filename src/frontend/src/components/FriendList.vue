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
          </div>
          {{travel_id}}
        </div>
        <div class="col-2 text-right">
          <base-button
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
var dummy = [
  {
    user_name: "Alice",
    user_id: 1,
    avatar_url: "img/theme/team-1-800x800.jpg"
  },
  {
    user_name: "Bob",
    user_id: 2,
    avatar_url: "img/theme/team-2-800x800.jpg"
  },
  {
    user_name: "Carol",
    user_id: 3,
    avatar_url: "img/theme/team-3-800x800.jpg"
  }
];

var friend_info_list = [
  {
    user_name: "Alice",
    user_id: 1,
    avatar_url: "img/theme/team-1-800x800.jpg"
  },
  {
    user_name: "Bob",
    user_id: 2,
    avatar_url: "img/theme/team-2-800x800.jpg"
  },
  {
    user_name: "Carol",
    user_id: 3,
    avatar_url: "img/theme/team-3-800x800.jpg"
  },
  {
    user_name: "David",
    user_id: 4,
    avatar_url: "img/theme/team-4-800x800.jpg"
  }
];
export default {
  name: "friend-list",
  props: {
    travel_id: Number
    // friend_info_list: Array
  },
  data() {
    return {
      travel_company: dummy,
      showList: false,
      friend_info_list: friend_info_list,
      success: false
    };
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

    del(friend) {
      var vue = this;
      for (var i = 0; i < vue.travel_company.length; ++i) {
        if (vue.travel_company[i].user_id == friend.user_id) {
          vue.travel_company.splice(i, 1);
        }
      }
      //   this.$backend_conn(
      //     "remove_travel_company",
      //     {
      //       travel_id: vue.travel_id,
      //       friend_user_id: friend.user_id
      //     },
      //     vue,
      //     function(response) {
      //       for (var i = 0; i < vue.travel_company.length; ++i) {
      //         if (vue.travel_company[i].user_id == friend.user_id) {
      //           vue.travel_company.splice(i, 1);
      //         }
      //       }
      //       console.log(response);
      //     },
      //     function(response) {
      //       alert(response.data.error_message);
      //     }
      //   );
    },

    invite(friend) {
      var vue = this;
      vue.success = true;
      setTimeout(function() {
        vue.success = false;
      }, 3000);
      //   this.$backend_conn(
      //     "invite_travel_company",
      //     {
      //       travel_id: vue.travel_id,
      //       friend_user_id: friend.user_id
      //     },
      //     function(response) {
      //       vue.success = true;
      //       setTimeout(function() {
      //         vue.success = false;
      //       }, 1000);
      //       console.log(response);
      //     },
      //     function(response) {
      //       alert(response.data.error_message);
      //     }
      //   );
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

