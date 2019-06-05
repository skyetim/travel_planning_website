<template>
  <div>
    <base-header
      class="header pb-8 pt-5 pt-lg-8 d-flex align-items-center"
      style="min-height: 240px; background-size: cover; background-position: center top;"
    >
      <span class="mask bg-gradient-success opacity-8"></span>
    </base-header>
    <div class="card shadow">
      <div class="card-header border-0">
        <div class="row align-items-center">
          <div class="col">
            <h3 class="mb-0">Friends</h3>
          </div>
          <div class="col text-right">
            <base-button
              type="primary"
              size="sm"
              @click="add_travel_group(newTravelGroup());"
            >创建新的行程</base-button>
          </div>
        </div>
      </div>

      <div class="table-responsive">
        <base-table
          class="table align-items-center table-flush"
          :class="type === 'dark' ? 'table-dark': ''"
          :thead-classes="type === 'dark' ? 'thead-dark': 'thead-light'"
          tbody-classes="list"
          :data="tableData"
        >
          <template slot="columns">
            <th>Profile</th>
            <th>City</th>
            <th>Comment</th>
            <th>Note</th>
            <th></th>
          </template>
          <template slot-scope="{row}">
            <th scope="row">
              <div class="media align-items-center">
                <div class="avatar-group">
                  <a href="#" class="avatar avatar-sm rounded-circle" data-toggle="tooltip">
                    <img alt="Image placeholder" :src="row.avatar_url">
                  </a>
                </div>
                <div class="media-body">
                  <span
                    class="name mb-0 text-sm"
                  >&nbsp;{{row.user_name}}&nbsp;&nbsp;#&nbsp;{{row.user_id}}&nbsp;&nbsp;&nbsp;&nbsp;</span>
                  <img
                    alt="Image placeholder"
                    style="width:20px;height:20px;background-color:aqua"
                    :src="row.gender"
                  >
                </div>
              </div>
            </th>
            <td>
              <badge class="badge-dot mr-4" :type="row.statusType">
                <span
                  class="status"
                >{{row.resident_city.country_name}}.&nbsp;{{row.resident_city.city_name}}</span>
              </badge>
            </td>
            <td>
              <badge class="badge-dot mr-4" :type="row.statusType">
                <span class="status">{{row.comment}}</span>
              </badge>
            </td>
            <td>
              <badge class="badge-dot mr-4" :type="row.statusType">
                <span class="status">{{row.friend_note}}</span>
              </badge>
            </td>
            <td>
              <base-button size="sm" type="success" class="mr-4">Edit</base-button>
              <base-button size="sm" type="success" class="mr-4">Remove</base-button>
            </td>
          </template>
        </base-table>
      </div>
      <div
        class="card-footer d-flex justify-content-end"
        :class="type === 'dark' ? 'bg-transparent': ''"
      ></div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import qs from "qs";

axios.defaults.headers["Content-Type"] =
  "application/x-www-form-urlencoded; charset=UTF-8";

var profile_data = {
  user_info: {
    user_name: "",
    user_id: "",
    session_id: "",
    email: "",
    gender: "",
    resident_city: "",
    comment: "",
    avatar_url: "",
    friend_count: ""
  },

  tableData: []
};

export default {
  name: "user-profile",
  components: {},
  props: {
    type: {
      type: String
    },
    title: String
  },
  data() {
    return profile_data;
  },
  mounted() {
    login();
  },
  method: {
    removeFriend: function(friend_user_id) {
      var remove_friend_url = "http://139.162.123.242:9000/api/set_friend_note";
      var remove_friend_data = {
        user_id: profile_data.user_info.user_id,
        session_id: profile_data.user_info.session_id,
        friend_user_id: friend_user_id
      };
      axios
        .post(remove_friend_url, qs.stringify(remove_friend_data))
        .then(response => {
          alert("Deleted");
          login();
        })
        .catch(error => {
          alert(error);
        });
    }
  }
};

function login() {
  var login_url = "http://139.162.123.242:9000/api/login";
  var login_data = {
    email: "carol7u@pku.edu.cn",
    pswd_hash: "12344321123443211234432112344321"
  };
  axios
    .post(login_url, qs.stringify(login_data))
    .then(response => {
      profile_data.user_info.user_id = response.data.user_id.toString();
      profile_data.user_info.session_id = response.data.session_id.toString();
      getUserInfo();
    })
    .catch(error => {
      alert(error);
    });
}

function getUserInfo() {
  var get_user_info_url = "http://139.162.123.242:9000/api/get_user_info";
  var get_user_info_data = {
    user_id: profile_data.user_info.user_id,
    session_id: profile_data.user_info.session_id
  };
  axios
    .post(get_user_info_url, qs.stringify(get_user_info_data))
    .then(response => {
      profile_data.user_info.user_name = response.data.user_name;
      profile_data.user_info.gender = response.data.gender;
      profile_data.user_info.email = response.data.email;
      profile_data.user_info.resident_city =
        response.data.resident_city.city_name;
      profile_data.user_info.comment = response.data.comment;

      if (response.data.avatar_url == "")
        response.data.avatar_url = "img/theme/team-4-800x800.jpg";
      profile_data.user_info.avatar_url = response.data.avatar_url;

      getFriendList();
    })
    .catch(error => {
      alert(error);
    });
}

function getFriendList() {
  var get_friend_list_url = "http://139.162.123.242:9000/api/get_friend_list";
  var get_friend_list_data = {
    user_id: profile_data.user_info.user_id,
    session_id: profile_data.user_info.session_id
  };
  axios
    .post(get_friend_list_url, qs.stringify(get_friend_list_data))
    .then(response => {
      profile_data.user_info.friend_count = response.data.count;
      for (var i = 0; i < response.data.count; i++) {
        getFriendUserInfo(response.data.friend_list[i]);
      }
    })
    .catch(error => {
      alert(error);
    });
}

function getFriendUserInfo(friend_user_id) {
  var get_friend_info_url = "http://139.162.123.242:9000/api/get_friend_info";
  var get_friend_info_data = {
    user_id: profile_data.user_info.user_id,
    session_id: profile_data.user_info.session_id,
    friend_user_id: friend_user_id
  };
  axios
    .post(get_friend_info_url, qs.stringify(get_friend_info_data))
    .then(response => {
      if (response.data.avatar_url == "")
        response.data.avatar_url = "img/theme/team-1-800x800.jpg";

      if (response.data.gender == "F")
        response.data.gender = "img/theme/gender_f.jpg";
      else response.data.gender = "img/theme/gender_m.jpg";
      profile_data.tableData.push(response.data);
    })
    .catch(error => {
      alert(error);
    });
}

//function setFriendNote(user_id,friend_note) {
//    var set_friend_note_url = 'http://139.162.123.242:9000/api/set_friend_note';
//    var set_friend_note_data = {
//        'user_id': profile_data.user_info.user_id,
//        'session_id': profile_data.user_info.session_id,
//        'friend_user_id': user_id,
//        'friend_note': friend_note,
//    };
//    axios.post(set_friend_note_url, qs.stringify(set_friend_note_data))
//        .then((response) => {
//            login();
//        })
//        .catch((error) => { alert(error); });
//}
</script>
<style></style>
