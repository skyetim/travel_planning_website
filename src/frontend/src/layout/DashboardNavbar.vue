<template>
    <base-nav :show-toggle-button="false"
              class="navbar-top navbar-dark"
              expand
              id="navbar-main">
        <form class="navbar-search navbar-search-dark form-inline mr-3 d-none d-md-flex ml-lg-auto">
            <!-- <div class="form-group mb-0">
                <base-input placeholder="Search"
                            class="input-group-alternative"
                            alternative=""
                            addon-right-icon="fas fa-search">
                </base-input>
            </div> -->
        </form>
        <ul class="navbar-nav align-items-center d-none d-md-flex">
            <li class="nav-item dropdown">
                <base-dropdown class="nav-link pr-0">
                    <div class="media align-items-center" slot="title">
                <span class="avatar avatar-sm rounded-circle">
                  <img :src="avatar_url" alt="Image placeholder">
                </span>
                        <div class="media-body ml-2 d-none d-lg-block">
                            <span :key="this.$session.get('user_name')" class="mb-0 text-sm  font-weight-bold">{{this.user_name}}</span>
                        </div>
                    </div>

                    <template>
                        <div class=" dropdown-header noti-title">
                            <h6 class="text-overflow m-0">系统设置</h6>
                        </div>
                        <router-link class="dropdown-item" to="/message">
                            <i class="ni ni-notification-70"></i>
                            <span>信息</span>
                        </router-link>
                        <router-link class="dropdown-item" to="/settings">
                            <i class="ni ni-settings-gear-65"></i>
                            <span>设置</span>
                        </router-link>
                        <!-- <router-link to="/profile" class="dropdown-item">
                            <i class="ni ni-calendar-grid-58"></i>
                            <span>Activity</span>
                        </router-link>
                        <router-link to="/profile" class="dropdown-item">
                            <i class="ni ni-support-16"></i>
                            <span>Support</span>
                        </router-link> -->
                        <div class="dropdown-divider"></div>
                        <router-link class="dropdown-item" to='/login' v-on:click.native='logout'>
                            <i class="ni ni-user-run"></i>
                            <span>注销</span>
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
                searchQuery: '',
                user_name: '',
                avatar_url: ''
            };
        },
        mounted() {
            if (this.$session.has('user_name') && this.$session.has('avatar_url')) {
                this.user_name = this.$session.get('user_name');
                this.avatar_url = this.$session.get('avatar_url');
            } else {
                var that = this;

                function success(response) {
                    that.$session.set('user_name', response.data.user_name);
                    that.user_name = response.data.user_name;
                    that.avatar_url = response.data.avatar_url;
                    if (that.avatar_url == '') {
                        function avatar_success(response) {
                            that.avatar_url = 'img/theme/team-4-800x800.jpg';
                        }
                        function avatar_fail(response) {
                            console.error('获取信息时发生未知错误', response.data);
                        }
                        that.$backend_conn('set_user_avatar_url', {avatar_url: 'img/theme/team-4-800x800.jpg'}, that, avatar_success, avatar_fail);
                    }
                }
                function fail(response) {
                    console.error('获取信息时发生未知错误', response.data);
                }
                this.$backend_conn('get_user_info', {}, that, success, fail);
            }
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
            logout() {
                var that = this;

                function success(response) {
                    that.$session.destroy();
                    that.$router.push('/login');
                }
                function fail(response) {
                    console.error('获取信息时发生未知错误', response.data);
                }
                this.$backend_conn('logout', {}, that, success, fail);
            },
        },
        set_user_avatar_url() {

        }
    };
</script>
