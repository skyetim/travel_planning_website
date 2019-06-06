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
                        <small>安全信息</small>
                    </div>
                    <form role="form">
                        <div class='row'>
                            <div class='col-lg-6'>
                                <base-input class="input-group-alternative mb-3"
                                            placeholder="姓"
                                            addon-left-icon="ni ni-hat-3"
                                            v-model="model.last_name"
                                            @focus="login_error.visible=false">
                                </base-input>
                            </div>
                            <div class='col-lg-6'>
                                <base-input class="input-group-alternative mb-3"
                                            placeholder="名"
                                            addon-left-icon="ni ni-hat-3"
                                            v-model="model.first_name"
                                            @focus="login_error.visible=false">
                                </base-input>
                            </div>       
                        </div>

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

                        <hr>

                        <div class="text-center text-muted mb-4">
                            <small>个人信息</small>
                        </div>

                        <div class='input-group-alternative has-label'>
                            <label class='form-control-label'> 常住地 </label>
                            <base-city-search input_placeholder='请输入你的常住地'
                                            button_name='搜索'
                                            v-model='model.resident_city_name'
                                            @search-success='search_success'
                            />
                        </div>

                        <div class='input-group-alternative has-label container'>
                            <div class='row'>
                                <label class='form-control-label'> 性别 </label>
                            </div>
                            <div class='row'>
                                <div class="col-lg-6">
                                    <base-button block outline type="primary" aria-pressed="true" v-bind:class="{active: model.gender=='男', 'btn-sm': true}" @click="model.gender='男'">男</base-button>
                                </div>
                                <div class="col-lg-6">
                                    <base-button block outline type="primary" aria-pressed="true" v-bind:class="{active: model.gender=='女', 'btn-sm': true}" @click="model.gender='女'">女</base-button>
                                </div>
                            </div>
                        </div>

                        <hr>
                        

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
          first_name: '',
          last_name: '',
          email: '',
          password: '',
          resident_city_id: 1, 
          gender: '未设置'
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
            this.$http.post('http://139.162.123.242:9000/api/register', {
                pswd_hash: this.$md5(this.model.password),
                email: this.model.email, 
                user_name: this.model.last_name+' '+this.model.first_name, 
                gender: this.$gender_reverse[this.model.gender], 
                resident_city_id: this.model.resident_city_id
            }).then(function (response) {
                if (response.status === 200) {
                    if (response.body.status == this.$status['normal']){
                        this.login_error.visible = true;
                        this.login_error.message = '注册成功, 请登录';
                        var that = this;
                        setTimeout(function(){
                            that.$router.push('/login');
                        }, 1000);
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


        },
        search_success(city_id, city_name){
            this.model.resident_city_id = city_id;
            this.model.resident_city_name = city_name;
        } 
    }
  }
</script>
<style>
</style>