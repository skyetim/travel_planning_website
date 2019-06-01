<template>
    <div class="row justify-content-center">
        <div class="col-lg-5 col-md-7">
            <div class="card bg-secondary shadow border-0">
                <!-- <div class="card-header bg-transparent pb-5">
                    <div class="text-muted text-center mt-2 mb-3">
                        <small>Sign up with</small>
                    </div>
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
                        <small>填写姓名, 邮箱, 密码以注册</small>
                    </div>
                    <form role="form">

                        <base-input class="input-group-alternative mb-3"
                                    placeholder="Name"
                                    addon-left-icon="ni ni-hat-3"
                                    v-model="model.user_name"
                                    @focus="login_error.visible=false">
                        </base-input>

                        <base-input class="input-group-alternative mb-3"
                                    placeholder="邮箱"
                                    addon-left-icon="ni ni-email-83"
                                    v-model="model.email"
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

                        <!-- <base-input class="input-group-alternative mb-3"
                                    placeholder="Resident city"
                                    addon-left-icon="ni ni-hat-3"
                                    v-model="model.resident_city">
                        </base-input> -->



                        <!-- <div class="text-muted font-italic">
                            <small>password strength: <span class="text-success font-weight-700">strong</span></small>
                        </div> -->

                        <!-- <div class="row my-4">
                            <div class="col-12">
                                <base-checkbox class="custom-control-alternative">
                                    <span class="text-muted">I agree with the <a href="#!">Privacy Policy</a></span>
                                </base-checkbox>
                            </div>
                        </div> -->
                        <div class="text-center">
                            <base-button type="primary" class="my-4" @click='register'>创建账户</base-button>
                        </div>
                    </form>
                </div>
            </div>
            <div class="row mt-3">
                <div class="col-6">
                    <a href="#" class="text-light">
                        <small> </small>
                    </a>
                </div>
                <div class="col-6 text-right">
                    <router-link to="/login" class="text-light">
                        <small>登录已有账户</small>
                    </router-link>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
  import {email} from 'vuelidate/lib/validators';
  import { setTimeout } from 'timers';
  export default {
    name: 'register',
    data() {
      return {
        model: {
          name: '',
          email: '',
          password: '',
          resident_city_id: 1, 
          gender: '男'
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
        register(){
            if (this.name=='' || this.email=='' || this.password=='' || this.resident_city_id=='' || this.gender==''){
                this.login_error.visible = true;
                this.login_error.message = '以上内容均为必填项, 请全部填写';
                return
            }
            this.$http.post('http://185.239.71.198:9000/api/register', {
                pswd_hash: this.$md5(this.model.password),
                email: this.model.email, 
                user_name: this.model.name, 
                gender: this.model.gender, 
                resident_city_id: this.model.resident_city_id
            }).then(function (response) {
                if (response.status === 200) {
                    if (response.body.status == this.$status['normal']){
                        this.login_error.visible = true;
                        this.login_error.message = '注册成功, 请登录';
                        // setTimeout(function(){}, 1500);
                        this.$router.push('/login');
                    } else if (response.body.status == this.$status['user_already_exists']){
                        this.login_error.visible = true;
                        this.login_error.message = '该邮箱已存在, 请尝试登录';
                    } else {
                        console.error('注册时发生未知错误', response.body)
                    }
                } else {
                    this.login_error.visible = true; 
                    this.login_error.message = '网络连接有问题, 请重试';
                    console.error(response.body);
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
