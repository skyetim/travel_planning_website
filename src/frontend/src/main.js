import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './registerServiceWorker'
import ArgonDashboard from './plugins/argon-dashboard'
import { Icon } from "leaflet";
import 'leaflet/dist/leaflet.css';

delete Icon.Default.prototype._getIconUrl;

Icon.Default.mergeOptions({
  iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
  iconUrl: require("leaflet/dist/images/marker-icon.png"),
  shadowUrl: require("leaflet/dist/images/marker-shadow.png")
});

Vue.config.productionTip = false

Vue.use(ArgonDashboard)

Vue.prototype.getCookie = (name) => {
  var reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");
  var result_array = document.cookie.match(reg);
  if (result_array) {
    return (result_array[2]);
  }
  else
    return null;
}

Vue.prototype.setCookie = (c_name, value, expiredays) => {
  var expire_time = new Date();　　
  expire_time.setTime(expire_time.getTime() + expiredays);
  document.cookie = c_name + "=" + escape(value) + ((expiredays == null) ? "" : ";expires=" + expire_time.toUTCString());
}

new Vue({
  router,
  render: h => h(App), 
  created() {
    this.checkLogin();
  }, 
  methods: {
    checkLogin(){
      if (!this.getCookie('session') && this.$route.name!='register') { // 如果没有login且不在register页自动跳转
        this.$router.push('/login');
      } else if (this.getCookie('session') && (this.$route.name=='login' || this.$route.name=='register')){ // 如果已经login进入login页自动跳转
        this.$router.push('/');
      }
    }
  }, 
  watch:{
    '$route': 'checkLogin'
  }
}).$mount('#app')
