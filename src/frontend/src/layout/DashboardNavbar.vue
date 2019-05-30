<template>
    <base-nav class="navbar-top navbar-dark"
              id="navbar-main"
              :show-toggle-button="false"
              expand>
        <form class="navbar-search navbar-search-dark form-inline mr-3 d-none d-md-flex ml-lg-auto">
            <div class="form-group mb-0">
                <base-input placeholder="Search"
                            class="input-group-alternative"
                            alternative=""
                            addon-right-icon="fas fa-search">
                </base-input>
            </div>
        </form>
        <ul class="navbar-nav align-items-center d-none d-md-flex">
            <li class="nav-item dropdown">
                <base-dropdown class="nav-link pr-0">
                    <div class="media align-items-center" slot="title">
                <span class="avatar avatar-sm rounded-circle">
                  <img alt="Image placeholder" src="img/theme/team-4-800x800.jpg">
                </span>
                        <div class="media-body ml-2 d-none d-lg-block">
                            <span class="mb-0 text-sm  font-weight-bold">Tim Wang</span>
                        </div>
                    </div>

                    <template>
                        <div class=" dropdown-header noti-title">
                            <h6 class="text-overflow m-0">Welcome!</h6>
                        </div>
                        <router-link to="/profile" class="dropdown-item">
                            <i class="ni ni-single-02"></i>
                            <span>My profile</span>
                        </router-link>
                        <router-link to="/profile" class="dropdown-item">
                            <i class="ni ni-settings-gear-65"></i>
                            <span>Settings</span>
                        </router-link>
                        <router-link to="/profile" class="dropdown-item">
                            <i class="ni ni-calendar-grid-58"></i>
                            <span>Activity</span>
                        </router-link>
                        <router-link to="/profile" class="dropdown-item">
                            <i class="ni ni-support-16"></i>
                            <span>Support</span>
                        </router-link>
                        <div class="dropdown-divider"></div>
                        <router-link v-on:click.native='logout' to='/login' class="dropdown-item">
                            <i class="ni ni-user-run"></i>
                            <span>Logout</span>
                        </router-link>
                    </template>
                </base-dropdown>
            </li>
        </ul>
    </base-nav>
</template>
<script>
  export default {
    data() {
      return {
        activeNotifications: false,
        showMenu: false,
        searchQuery: ''
      };
    },
    methods: {
      toggleSidebar() {
        this.$sidebar.displaySidebar(!this.$sidebar.showSidebar);
      },
      hideSidebar() {
        this.$sidebar.displaySidebar(false);
      },
      toggleMenu() {
        this.showMenu = !this.showMenu;
      },
      logout(){
        if (this.$session.exists()) {
          this.$http.post('http://185.239.71.198:9000/api/logout', {
                user_id: this.$session.get('user_id'),
                session_id: this.$session.id().replace('sess:', '')
          }).then(function (response) {
              if (response.status === 200) {
                if (response.body.status == this.$status['normal']){
                  this.$session.destroy();
                  this.$router.push('/login');
                } else if (response.body.status == this.$status['user_anthorization_error']) {
                  window.alert('用户登录信息有误, 请重新登录');
                  this.$session.destroy();
                  this.$router.push('/login');
                } else if (response.body.status == this.$status['user_session_timeout']){
                  window.alert('用户长时间未操作, 自动退出, 请重新登录');
                  this.$session.destroy();
                  this.$router.push('/login');
                } else {
                  console.error('退出时发生未知错误', response.body);
                }
              } else {
                console.error('网络连接有问题');
              }
          }, function (err) {
              console.error('err', err);
            })
        } else {
          window.alert('用户已退出, 请重新登录');
          this.$router.push('/login');
        }
      }
    }
  };
</script>
