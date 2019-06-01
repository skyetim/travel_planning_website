<template>
        <div class="row justify-content-center">
            <div class="col-lg-5 col-md-7">
                <div class="card bg-secondary shadow border-0">
                    <!-- <div class="card-header bg-transparent pb-5">
                        <div class="text-muted text-center mt-2 mb-3"><small>Sign in with</small></div>
                        <div class="btn-wrapper text-center">
                            <a href="#" class="btn btn-neutral btn-icon">
                                <span class="btn-inner--icon"><img src="img/icons/common/github.svg"></span>
                                <span class="btn-inner--text">Github</span>
                            </a>
                            <a href="#" class="btn btn-neutral btn-icon">
                                <span class="btn-inner--icon"><img src="img/icons/common/google.svg"></span>
                                <span class="btn-inner--text">Google</span>
                            </a>
                        </div>
                    </div> -->
                    <div class="card-body px-lg-5 py-lg-5">
                        <div class="text-center text-muted mb-4">
                            <small>输入注册邮箱与密码登录行迹</small>
                        </div>
                        <form role="form">
                            <base-input class="input-group-alternative mb-3"
                                        placeholder="邮箱"
                                        addon-left-icon="ni ni-email-83"
                                        v-model="model.email"
                                        type='email'
                                        @focus="login_error.visible=false">
                            </base-input>
                            <div v-if="!$v.model.email.email">
                                <base-alert type='primary'>
                                    请输入正确的邮箱地址
                                </base-alert>
                            </div>
                            <base-input class="input-group-alternative"
                                        placeholder="密码"
                                        type="password"
                                        addon-left-icon="ni ni-lock-circle-open"
                                        v-model="model.password"
                                        @focus="login_error.visible=false">
                            </base-input>
                            <div v-show="login_error.visible">
                                <base-alert type='primary'>
                                    {{this.login_error.message}}
                                </base-alert>
                            </div>
                            <base-checkbox class="custom-control-alternative">
                                <span class="text-muted">7天内无需重复登录</span>
                            </base-checkbox>
                            <div class="text-center">
                                <base-button type="primary" class="my-4" @click='login'>登录</base-button>
                            </div>
                        </form>
                    </div>
                </div>
                <div class="row mt-3">
                    <div class="col-6">
                        <a href="#" class="text-light"><small> </small></a>
                    </div>
                    <div class="col-6 text-right">
                        <router-link to="/register" class="text-light"><small>创建新的账户</small></router-link>
                    </div>
                </div>
            </div>
        </div>
</template>
<script>
  import {email} from 'vuelidate/lib/validators';
  export default {
    name: 'login',
    data() {
      return {
        model: {
          email: '',
          password: ''
        }, 
        login_error: {
            visible: false, 
            message: ''
        }
      }
    },
    validations: {
        model: {
            email:{
                email
            }
        }
    }, 
    methods: {
        login() {
            if(this.model.email=='' || this.model.password==''){
                this.login_error.visible = true;
                this.login_error.message = '邮箱地址与密码未填充完全';
                return
            }
            // TODO: POST
            this.$http.post('http://185.239.71.198:9000/api/login', {
                pswd_hash: this.$md5(this.model.password),
                email: this.model.email
            }).then(function (response) {
                if (response.status === 200) {
                    if (response.body.status == this.$status['normal']){
                        this.$session.start();
                        this.$session.renew(response.body.session_id);
                        this.$session.set('user_id', response.body.user_id);
                        this.$router.push('/');
                    } else if (response.body.status == this.$status['user_does_not_exist']){
                        this.login_error.visible = true;
                        this.login_error.message = '用户不存在';
                    } else if (response.body.status == this.$status['wrong_password']) {
                        this.login_error.visible = true;
                        this.login_error.message = '密码错误';
                    } else {
                        console.error('登录时发生未知错误', response.body)
                    }
                } else {
                    this.login_error.visible = true; 
                    this.login_error.message = '网络连接有问题, 请重试';
                }
            }, function (err) {
                console.error('err', err)
            })

        }
    }
  }
</script>
<style>
</style>
