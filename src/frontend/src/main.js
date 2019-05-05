import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './registerServiceWorker'
import ArgonDashboard from './plugins/argon-dashboard'

Vue.config.productionTip = false

Vue.use(ArgonDashboard)

function getCookie(name) {
  var arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");
  if (arr = document.cookie.match(reg))
    return (arr[2]);
  else
    return null;
}
Vue.prototype.getCookie = getCookie;

new Vue({
  router,
  render: h => h(App), 
  created() {
    this.checkLogin();
  }, 
  methods: {
    checkLogin(){
      if (!this.getCookie('sessionid') && this.$route.name!='register') {
        this.$router.push('/login');
      } 
    }
  }, 
  watch:{
    '$route': 'checkLogin'
  }
}).$mount('#app')
