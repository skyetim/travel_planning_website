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
                    <user-card-preview :user_name='model.model_user_name'
                                       :gender='model.gender'
                                       :resident_city='model.resident_city'
                                       :comment='model.comment'
                    ></user-card-preview>
                </div>

                <div class="col-xl-8 order-xl-1">
                    <card shadow type="secondary">
                        <div slot="header" class="bg-white border-0">
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
                                        <base-button type='primary' @click='setUserInfo()' size='sm'>保存</base-button>
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
                                                        label="姓"
                                                        input-classes="form-control-alternative"
                                                        placeholder='请输入你的姓'
                                                        v-model="model.last_name"
                                            />
                                        </div>
                                        <div class="col-lg-6">
                                            <base-input alternative=""
                                                        label="名"
                                                        input-classes="form-control-alternative"
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
                                                        <base-button block outline type="primary" aria-pressed="true" v-bind:class="{active: model.gender=='男'}" @click="model.gender='男'">男</base-button>
                                                    </div>
                                                    <div class="col-lg-6">
                                                        <base-button block outline type="primary" aria-pressed="true" v-bind:class="{active: model.gender=='女'}" @click="model.gender='女'">女</base-button>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="col-lg-6">
                                            <base-input alternative=""
                                                        label="常住地"
                                                        input-classes="form-control-alternative"
                                                        placeholder='请输入你的常住地'
                                                        v-model="model.resident_city"
                                            />
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="col-lg-12">
                                            <base-input alternative=""
                                                        label="邮箱地址"
                                                        input-classes="form-control-alternative"
                                                        placeholder='设置新的邮箱'
                                                        v-model="model.email"
                                            />
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="col-lg-12">
                                           <base-input alternative=""
                                                    label="关于我">
                                            <textarea rows="4" class="form-control form-control-alternative" placeholder='让小伙伴更加了解你吧' v-model="model.comment"></textarea>
                                        </base-input>
                                        </div>
                                    </div>
                                    
                                </div>    
                                <hr class="my-4" />
                                 <div class="row align-items-center">
                                    <div class="col-8">
                                        <h6 class="heading-small text-muted mb-4">安全信息</h6>
                                    </div>
                                    <div class="col-4 text-right">
                                        <base-button type='primary' @click='resetPassword()' size='sm'>保存</base-button>
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
                                            <base-input input-classes="form-control-alternative"
                                                        label='请输入旧密码'
                                                        type="password"
                                                        v-model="model.old_password"
                                                        @focus="error.visible=false">
                                            </base-input>
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="col-lg-6">
                                            <base-input input-classes="form-control-alternative"
                                                        label='设置新的密码'
                                                        type="password"
                                                        v-model="model.new_password"
                                                        @focus="error.visible=false">
                                            </base-input>
                                        </div>
                                        <div class="col-lg-6">
                                            <base-input input-classes="form-control-alternative"
                                                        label='请再输一次新的密码'
                                                        type="password"
                                                        v-model="model.verify_password"
                                                        @focus="error.visible=false">
                                            </base-input>
                                        </div>
                                    </div>
                                </div>
                                <hr class="my-4" />
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
import { setTimeout } from 'timers';
import UserCardPreview from './UserCardPreview';
  export default {
    name: 'settings',
    data() {
      return {
        model: {
          email: '',
          first_name: '',
          last_name: '',
          resident_city: '',
          gender: '', 
          comment: '', 
          resident_city_id: 1, 
          old_password: '', 
          new_password: '', 
          verify_password: ''
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
        model_user_name: function(){
            if (typeof this.model.last_name === 'undefined' || typeof this.model.first_name === 'undefined' ) {
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
        if (this.$session.exists()) {
            this.$http.post('http://185.239.71.198:9000/api/get_user_info', {
                user_id: this.$session.get('user_id'),
                session_id: this.$session.id().replace('sess:', '')
          }).then(function (response) {
              if (response.status === 200) {
                if (response.body.status == this.$status['normal']){
                  let user_name = response.body.user_name;
                  this.model.first_name = user_name.split(' ')[1];
                  this.model.last_name = user_name.split(' ')[0]
                  this.model.email = response.body.email;
                  this.model.gender = this.$gender[response.body.gender];
                  this.model.resident_city_id = response.body.resident_city_id;
                  this.model.comment = response.body.comment;
                } else if (response.body.status == this.$status['user_anthorization_error']) {
                  window.alert('用户登录信息有误, 请重新登录');
                  this.$session.destroy();
                  this.$router.push('/login');
                } else if (response.body.status == this.$status['user_session_timeout']){
                  window.alert('用户长时间未操作, 自动退出, 请重新登录');
                  this.$session.destroy();
                  this.$router.push('/login');
                } else {
                  console.error('获取信息时发生未知错误', response.body);
                }
              } else {
                console.error('网络连接有问题', response.body);
              }
          }, function (err) {
              console.error('err', err);
            }); 
          } else {
            window.alert('用户已退出, 请重新登录');
            this.$router.push('/login');
          }
    }, 
    methods: {
        setUserInfo() {
            if (this.$session.exists()) {
            this.$http.post('http://185.239.71.198:9000/api/set_user_info', {
                user_id: this.$session.get('user_id'),
                session_id: this.$session.id().replace('sess:', ''),
                user_name: this.model_user_name, 
                email: this.model.email, 
                gender: this.$gender_reverse[this.model.gender], 
                comment: this.model.comment, 
                resident_city_id: this.model.resident_city_id
          }).then(function (response) {
              if (response.status === 200) {
                if (response.body.status == this.$status['normal']){
                    this.message.personal_info.visible = true;
                    this.message.personal_info.message = '个人信息成功保存, 即将刷新';
                    this.message.personal_info.type = 'success';
                    var that = this;
                    setTimeout(function(){
                        that.$session.set('user_name', this.model_user_name);
                        that.$router.go();
                    }, 2000);
                } else if (response.body.status == this.$status['user_anthorization_error']) {
                  window.alert('用户登录信息有误, 请重新登录');
                  this.$session.destroy();
                  this.$router.push('/login');
                } else if (response.body.status == this.$status['user_session_timeout']){
                  window.alert('用户长时间未操作, 自动退出, 请重新登录');
                  this.$session.destroy();
                  this.$router.push('/login');
                } else {
                  console.error('获取信息时发生未知错误', response.body);
                }
              } else {
                console.error('网络连接有问题', response.body);
              }
          }, function (err) {
              console.error('err', err);
            }); 
          } else {
            window.alert('用户已退出, 请重新登录');
            this.$router.push('/login');
          }
        }, 
        resetPassword() {
            if (this.$session.exists()) {
            this.$http.post('http://185.239.71.198:9000/api/reset_password', {
                user_id: this.$session.get('user_id'),
                session_id: this.$session.id().replace('sess:', ''),
                old_pswd_hash: this.$md5(this.model.old_password),
                new_pswd_hash: this.$md5(this.model.new_password),
          }).then(function (response) {
              if (response.status === 200) {
                if (response.body.status == this.$status['normal']){
                    this.message.password.visible = true;
                    this.message.password.message = '密码成功修改';
                    this.message.password.type = 'success';
                    this.model.old_password = '';
                    this.model.new_password = '';
                    this.model.verify_password = '';
                } else if (response.body.status == this.$status['user_anthorization_error']) {
                  window.alert('用户登录信息有误, 请重新登录');
                  this.$session.destroy();
                  this.$router.push('/login');
                } else if (response.body.status == this.$status['user_session_timeout']){
                  window.alert('用户长时间未操作, 自动退出, 请重新登录');
                  this.$session.destroy();
                  this.$router.push('/login');
                } else if (response.body.status == this.$status['wrong_password']) {
                    this.message.password.visible = true;
                    this.message.password.message = '旧密码错误, 请重试';
                    this.message.password.type = 'danger';
                    this.model.old_password = '';
                    this.model.new_password = '';
                    this.model.verify_password = '';
                } else {
                  console.error('获取信息时发生未知错误', response.body);
                }
              } else {
                console.error('网络连接有问题', response.body);
              }
          }, function (err) {
              console.error('err', err);
            }); 
          } else {
            window.alert('用户已退出, 请重新登录');
            this.$router.push('/login');
          }
        }
    }
  };
</script>
<style></style>
