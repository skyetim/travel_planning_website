<template>
    <div class="card card-profile shadow">
        <change-avatar :field="field"
                                    @crop-success="cropSuccess"
                                    @crop-upload-success="cropUploadSuccess"
                                    @crop-upload-fail="cropUploadFail"
                                    v-model="show"
                                    :width="300"
                                    :height="300"
                                    :url="url"
                                    langType='zh'
                                    img-format="png"
                                    :withCredentials='true'>
        </change-avatar>
        <div class="row justify-content-center">
            <div class="col-lg-3 order-lg-2">
                <div class="card-profile-image">
                    <a v-b-tooltip.hover.top title="点击以更改头像" @click="toggleShow()" >
                        <img :src="avatar_url" class="rounded-circle">
                    </a>
                </div>
            </div>
        </div>
        <div class="card-header text-center border-0 pt-8 pt-md-4 pb-0 pb-md-4">
            <div class="d-flex justify-content-between">
                <span class='description'>预览</span>
                <!-- <base-button size="sm" type="info" class="mr-4">Connect</base-button> -->
                <!-- <base-button size="sm" type="default" class="float-right">Message</base-button> -->
            </div>
        </div>
        <div class="card-body pt-0 pt-md-4">
            <div class="row">
                <div class="col">
                    <div class="card-profile-stats d-flex justify-content-center mt-md-5">
                        <div>
                            <span class="heading">{{friends_num}}</span>
                            <span class="description">朋友</span>
                        </div>
                        <div>
                            <span class="heading">{{travel_groups_num}}</span>
                            <span class="description">行迹</span>
                        </div>
                        <!-- <div>
                            <span class="heading">89</span>
                            <span class="description">Comments</span>
                        </div> -->
                    </div>
                </div>
            </div>
            <div class="text-center">
                <h3>
                    {{user_name}}<span class="font-weight-light">, {{gender}}</span>
                </h3>
                <div class="h5 font-weight-300">
                    <i class="ni location_pin mr-2"></i>{{resident_city}}
                </div>
                <!-- <div class="h5 mt-4">
                    <i class="ni business_briefcase-24 mr-2"></i>Solution Manager - Creative Tim Officer
                </div>
                <div>
                    <i class="ni education_hat mr-2"></i>University of Computer Science
                </div> -->
                <hr class="my-4" />
                <p>{{comment}}</p>
            </div>
        </div>
    </div>
</template>
<script>
    // import 'babel-polyfill'; // es6 shim
    import Upload from '@/plugins/vue-image-crop-upload/upload.vue';
    import BTooltipDirective from 'bootstrap-vue/es/directives/tooltip'
    export default {
        name: 'user_card_preview',
        props: {
            user_name: {
                'default': '未设置'
            }, 
            gender: {
                'default': '未设置'
            }, 
            resident_city: {
                'default': '未设置'
            }, 
            comment: {
                'default': '未设置'
            }, 
            avatar_url: {
                'dafault': 'img/theme/team-4-800x800.jpg'
            }
        }, 
        directives: {
            'b-tooltip': BTooltipDirective
        },
        data() {
            return {
                show: false,
                field:'smfile',
                url: 'https://sm.ms/api/upload', 
                params: {
                },
                headers: {
                },
                friends_num: 0, 
                travel_groups_num: 0, 
            }
        },
        components: {
            'change-avatar': Upload
        },
        methods: {
            toggleShow() {
                this.show = !this.show;
            },
            /**
             * crop success
             *
             * [param] avatar_url
             * [param] field
             */
            cropSuccess(avatar_url, field){
                console.log('-------- crop success --------');
                this.avatar_url = avatar_url;
            },
            /**
             * upload success
             *
             * [param] jsonData  server api return data, already json encode
             * [param] field
             */
            cropUploadSuccess(jsonData, field){
                console.log('-------- upload success --------');
                if (this.$session.exists()) {
                    this.$http.post('http://139.162.123.242:9000/api/set_user_avatar_url', {
                        user_id: this.$session.get('user_id'),
                        session_id: this.$session.id().replace('sess:', ''), 
                        avatar_url: jsonData.url
                }).then(function (response) {
                    if (response.status === 200) {
                        if (response.body.status == this.$status['normal']){
                            this.avatar_url = jsonData.url;
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
            /**
             * upload fail
             *
             * [param] status    server api return error status, like 500
             * [param] field
             */
            cropUploadFail(status, field){
                console.log('-------- upload fail --------');
                console.log(status);
                console.log('field: ' + field);
            }
        }
    }
</script>
