<template>
    <div>
        <base-header class="header pb-8 pt-5 pt-lg-8 d-flex align-items-center"
                     style="min-height: 600px; background-image: url(img/theme/profile-cover.jpg); background-size: cover; background-position: center top;">
            <!-- Mask -->
            <span class="mask bg-gradient-success opacity-8"></span>
            <!-- Header container -->
            <div class="container-fluid d-flex align-items-center">
                <!-- <div class="row"> -->
                <div class="col-lg-7 col-md-10">
                    <h1 class="display-2 text-white">Hi {{this.$session.get('user_name')}}, </h1>
                    <p class="text-white mt-0 mb-5">你可以在这里修改自己的个人信息</p>
                    <!-- <a href="#!" class="btn btn-info">Edit profile</a> -->
                </div>
                <!-- </div> -->
            </div>
        </base-header>

        <div class="container-fluid mt--7">
            <div class="row">
                <div class="col-xl-4 order-xl-2 mb-5 mb-xl-0">
                    <user-card-preview :avatar_url='model.avatar_url'
                                       :comment='model.comment'
                                       :gender='model.gender'
                                       :preview='true'
                                       :resident_city='model.resident_city_name'
                                       :user_name='model_user_name'
                    ></user-card-preview>
                </div>

                <div class="col-xl-8 order-xl-1">
                    <card shadow type="secondary">
                        <div class="bg-white border-0" slot="header">
                            <div class="row align-items-center">
                                <div class="col-8">
                                    <h3 class="mb-0">我的账户</h3>
                                </div>
                            </div>
                        </div>
                        <div class="row align-items-center">
                            <div class="col-8">
                                <h6 class="heading-small text-muted mb-4">个人信息</h6>
                            </div>
                            <div class="col-4 text-right">
                                <base-button @click='setUserInfo()' size='sm' type='primary'>保存</base-button>
                            </div>
                        </div>
                        <div class="pl-lg-4">
                            <div class='row'>
                                <div class="col-lg-12" v-show='message.personal_info.visible'>
                                    <base-alert v-bind:type='message.personal_info.type'>
                                        {{message.personal_info.message}}
                                    </base-alert>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-lg-6">
                                    <base-input alternative=""
                                                input-classes="form-control-alternative"
                                                label="姓"
                                                placeholder='请输入你的姓'
                                                v-model="model.last_name"
                                    />
                                </div>
                                <div class="col-lg-6">
                                    <base-input alternative=""
                                                input-classes="form-control-alternative"
                                                label="名"
                                                placeholder='请输入你的名'
                                                v-model="model.first_name"
                                    />
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-lg-6">
                                    <div class='form-group has-label'>
                                        <label class='form-control-label'> 性别 </label>
                                        <div class='row'>
                                            <div class="col-lg-6">
                                                <base-button @click="model.gender='男'" aria-pressed="true" block outline
                                                             type="primary"
                                                             v-bind:class="{active: model.gender=='男'}">男
                                                </base-button>
                                            </div>
                                            <div class="col-lg-6">
                                                <base-button @click="model.gender='女'" aria-pressed="true" block outline
                                                             type="primary"
                                                             v-bind:class="{active: model.gender=='女'}">女
                                                </base-button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-lg-6">
                                    <div class='form-group has-label'>
                                        <label class='form-control-label'> 常住地 </label>
                                        <base-city-search @search-success='search_success'
                                                          button_name='搜索'
                                                          input_placeholder='请输入你的常住地'
                                                          v-model='model.resident_city_name'
                                        />
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-lg-12">
                                    <base-input alternative=""
                                                input-classes="form-control-alternative"
                                                label="邮箱地址"
                                                placeholder='设置新的邮箱'
                                                v-model="model.email"
                                    />
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-lg-12">
                                    <base-input alternative=""
                                                label="关于我">
                                        <textarea class="form-control form-control-alternative" placeholder='让小伙伴更加了解你吧'
                                                  rows="4" v-model="model.comment"></textarea>
                                    </base-input>
                                </div>
                            </div>

                        </div>
                        <hr class="my-4"/>
                        <div class="row align-items-center">
                            <div class="col-8">
                                <h6 class="heading-small text-muted mb-4">安全信息</h6>
                            </div>
                            <div class="col-4 text-right">
                                <base-button @click='resetPassword()' size='sm' type='primary'>保存</base-button>
                            </div>
                        </div>
                        <div class='pl-lg-4'>
                            <div class='row'>
                                <div class="col-lg-12" v-show='message.password.visible'>
                                    <base-alert v-bind:type='message.password.type'>
                                        {{message.password.message}}
                                    </base-alert>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-lg-12">
                                    <base-input @focus="error.visible=false"
                                                input-classes="form-control-alternative"
                                                label='请输入旧密码'
                                                type="password"
                                                v-model="model.old_password">
                                    </base-input>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-lg-6">
                                    <base-input @focus="error.visible=false"
                                                input-classes="form-control-alternative"
                                                label='设置新的密码'
                                                type="password"
                                                v-model="model.new_password">
                                    </base-input>
                                </div>
                                <div class="col-lg-6">
                                    <base-input @focus="error.visible=false"
                                                input-classes="form-control-alternative"
                                                label='请再输一次新的密码'
                                                type="password"
                                                v-model="model.verify_password">
                                    </base-input>
                                </div>
                            </div>
                        </div>
                        <hr class="my-4"/>
                        <!-- Address -->
                        <!-- <h6 class="heading-small text-muted mb-4">Contact information</h6>
                        <div class="pl-lg-4">
                            <div class="row">
                                <div class="col-md-12">
                                    <base-input alternative=""
                                                label="Address"
                                                placeholder="Home Address"
                                                input-classes="form-control-alternative"
                                                v-model="model.address"
                                    />
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-lg-4">
                                    <base-input alternative=""
                                                label="City"
                                                placeholder="City"
                                                input-classes="form-control-alternative"
                                                v-model="model.city"
                                    />
                                </div>
                                <div class="col-lg-4">
                                    <base-input alternative=""
                                                label="Country"
                                                placeholder="Country"
                                                input-classes="form-control-alternative"
                                                v-model="model.country"
                                    />
                                </div>
                                <div class="col-lg-4">
                                    <base-input alternative=""
                                                label="Postal code"
                                                placeholder="Postal code"
                                                input-classes="form-control-alternative"
                                                v-model="model.zipCode"
                                    />
                                </div>
                            </div>
                        </div>
                        <hr class="my-4" /> -->
                        <!-- Description -->
                    </card>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    import {setTimeout} from 'timers';
    import UserCardPreview from './UserCardPreview';

    export default {
        name: 'settings',
        data() {
            return {
                model: {
                    email: '',
                    first_name: '',
                    last_name: '',
                    gender: '',
                    comment: '',
                    resident_city_id: '',
                    old_password: '',
                    new_password: '',
                    verify_password: '',
                    avatar_url: '',
                    resident_city_name: ''
                },
                error: {
                    visible: false,
                    message: ''
                },
                message: {
                    personal_info: {
                        visible: false,
                        message: '',
                        type: ''
                    },
                    password: {
                        visible: false,
                        message: '',
                        type: ''
                    },
                    comment: {
                        visible: false,
                        message: '',
                        type: ''
                    }
                }
            }
        },
        computed: {
            model_user_name: function () {
                if (typeof this.model.last_name === 'undefined' || typeof this.model.first_name === 'undefined') {
                    return '';
                } else {
                    return this.model.last_name + ' ' + this.model.first_name;
                }
            }
        },
        components: {
            'user-card-preview': UserCardPreview
        },
        mounted() {
            var that = this;

            function success(response) {
                let user_name = response.data.user_name;
                that.model.first_name = user_name.split(' ')[1];
                that.model.last_name = user_name.split(' ')[0];
                that.model.email = response.data.email;
                that.model.gender = that.$gender[response.data.gender];
                that.model.resident_city_id = response.data.resident_city.city_id;
                that.model.resident_city_name = response.data.resident_city.city_name;
                that.model.comment = response.data.comment;
                that.model.avatar_url = response.data.avatar_url;
                if (that.model.avatar_url == '') {
                    that.model.avatar_url = 'img/theme/team-4-800x800.jpg'
                }
            }

            function fail(response) {
                console.error('获取信息时发生未知错误', response.data);
            }

            this.$backend_conn('get_user_info', {}, that, success, fail);
        },
        methods: {
            setUserInfo() {
                var that = this;
                var data = {
                    user_name: this.model_user_name,
                    email: this.model.email,
                    gender: this.$gender_reverse[this.model.gender],
                    comment: this.model.comment,
                    resident_city_id: this.model.resident_city_id
                };

                function success(response) {
                    that.message.personal_info.visible = true;
                    that.message.personal_info.message = '个人信息成功保存, 即将刷新';
                    that.message.personal_info.type = 'success';
                    setTimeout(function () {
                        that.$session.set('user_name', that.model_user_name);
                        that.$router.go();
                    }, 2000);
                }

                function fail(response) {
                    console.error('获取信息时发生未知错误', response.data);
                }

                this.$backend_conn('set_user_info', data, that, success, fail);
            },
            resetPassword() {
                var that = this;
                var data = {
                    old_pswd_hash: this.$md5(this.model.old_password),
                    new_pswd_hash: this.$md5(this.model.new_password)
                };

                function success(response) {
                    that.message.password.visible = true;
                    that.message.password.message = '密码成功修改';
                    that.message.password.type = 'success';
                    that.model.old_password = '';
                    that.model.new_password = '';
                    that.model.verify_password = '';
                }

                function fail(response) {
                    if (response.body.status == that.$status['wrong_password']) {
                        that.message.password.visible = true;
                        that.message.password.message = '旧密码错误, 请重试';
                        that.message.password.type = 'danger';
                        that.model.old_password = '';
                        that.model.new_password = '';
                        that.model.verify_password = '';
                    } else {
                        console.error('获取信息时发生未知错误', response.body);
                    }
                }

                this.$backend_conn('reset_password', data, that, success, fail);
            },
            search_success(city_id, city_name) {
                this.model.resident_city_id = city_id;
                this.model.resident_city_name = city_name;
            }
        }
    };
</script>
<style></style>
