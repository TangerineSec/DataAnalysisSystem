<template>
<!--  头部颜色更改-->
  <div class="header" style="position: relative;background: linear-gradient(to right, #90cdf4, #a7f3d0);">
    <!-- 折叠按钮 -->
    <div class="collapse-btn" @click="collapseChage" v-if="$route.name!=='Home'" >
      <i v-if="!collapse" class="el-icon-s-fold"></i>
      <i v-else class="el-icon-s-unfold"></i>
    </div>

    <div class="logo" style="position: absolute; left: 50%; transform: translate(-50%); text-align: center">{{headerName}}</div>
<!--    <div class="header-right">-->
<!--      <div class="header-user-con">-->

        <!-- 消息中心 -->
        <!--                <div class="btn-bell">-->
        <!--                    <el-tooltip effect="dark" :content="message?`有${message}条未读消息`:`消息中心`" placement="bottom">-->
        <!--                        <router-link to="/tabs">-->
        <!--                            <i class="el-icon-bell"></i>-->
        <!--                        </router-link>-->
        <!--                    </el-tooltip>-->
        <!--                    <span class="btn-bell-badge" v-if="message"></span>-->
        <!--                </div>-->
        <!-- 用户头像 -->
        <!--                <div class="user-avator">-->
        <!--                    <img src="../assets/img/img.jpg" />-->
        <!--                </div>-->
        <!-- 用户名下拉菜单 -->

<!--        <el-dropdown class="user-name" trigger="click">-->
<!--                    <span class="el-dropdown-link">-->
<!--                        {{ name }}-->
<!--                        <i class="el-icon-caret-bottom"></i>-->
<!--                    </span>-->
<!--          <template #dropdown>-->
<!--            <el-dropdown-menu>-->
<!--              &lt;!&ndash;                            <a href="https://github.com/lin-xin/vue-manage-system" target="_blank">&ndash;&gt;-->
<!--              &lt;!&ndash;                                <el-dropdown-item>项目仓库</el-dropdown-item>&ndash;&gt;-->
<!--              &lt;!&ndash;                            </a>&ndash;&gt;-->
<!--              &lt;!&ndash;                            <el-dropdown-item command="user">个人中心</el-dropdown-item>&ndash;&gt;-->
<!--              <el-dropdown-item divided @click="loginout">退出登录</el-dropdown-item>-->
<!--            </el-dropdown-menu>-->
<!--          </template>-->
<!--        </el-dropdown>-->
<!--      </div>-->
<!--    </div>-->
  </div>
</template>
<script>
import {cleanToken} from "@/utils/authUtils";


export default {
  props: {headerName: String},
  data() {
    return {
      name: '',
      intervalTask: []
    }
  },
  methods: {
    loginout() {
      cleanToken()
      this.$router.push("/login")
    },
    collapseChage() {
      this.$store.commit("handleCollapse", !this.collapse);
    },
    // checkLogin() {
    //   getLoginStatusApi().then(res => {
    //     setToken(res)
    //   })
    // }
  },
  computed: {
    collapse() {
      return this.$store.state.collapse;
    }
  },
  mounted() {
    // if (document.body.clientWidth < 1500) {
    //   this.collapseChage();
    // }
    // const {token, name} = getUserInfo()
    // this.name = name;
    // let task  = setInterval(() => {
    //   this.checkLogin()
    // }, 10 * 1000)
    // this.intervalTask.push(task)
  },
  beforeUnmount() {
    console.log('beforeUnmount');

    for (let task of this.intervalTask) {
      window.clearInterval(task);
    }
    this.intervalTask = []
  }
  // setup() {
  //       // const username = localStorage.getItem("ms_username");
  //       // const token = localStorage.getItem("token");
  //       // const message = 2;
  //
  //       const store = useStore();
  //       // 侧边栏折叠
  //       const collapseChage = () => {
  //           store.commit("handleCollapse", !collapse.value);
  //       };
  //       // 用户名下拉菜单选择事件
  //       const router = useRouter();
  //       const handleCommand = (command) => {
  //           if (command == "loginout") {
  //               localStorage.removeItem("ms_username");
  //               router.push("/login");
  //           } else if (command == "user") {
  //               router.push("/user");
  //           }
  //       };
  //
  //       return {
  //           username,
  //           message,
  //           collapse,
  //           collapseChage,
  //           handleCommand,
  //       };
  //   },
};
</script>
<style scoped>
.header {
  position: relative;
  box-sizing: border-box;
  width: 100%;
  height: 70px;
  font-size: 220px;
  color: #c5213d;
}

.collapse-btn {
  float: left;
  padding: 0 21px;
  cursor: pointer;
  line-height: 70px;
  color: black;
}

.header .logo {
  float: left;
  width: 250px;
  line-height: 70px;
}

.header-right {
  float: right;
  padding-right: 50px;
}

.header-user-con {
  display: flex;
  height: 70px;
  align-items: center;
}

.btn-fullscreen {
  transform: rotate(45deg);
  margin-right: 5px;
  font-size: 24px;
}

.btn-bell,
.btn-fullscreen {
  position: relative;
  width: 30px;
  height: 30px;
  text-align: center;
  border-radius: 15px;
  cursor: pointer;
}

.btn-bell-badge {
  position: absolute;
  right: 0;
  top: -2px;
  width: 8px;
  height: 8px;
  border-radius: 4px;
  background: #f56c6c;
  color: #fff;
}

.btn-bell .el-icon-bell {
  color: #fff;
}

.user-name {
  margin-left: 10px;
}

.user-avator {
  margin-left: 20px;
}

.user-avator img {
  display: block;
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.el-dropdown-link {
  color: #fff;
  cursor: pointer;
}

.el-dropdown-menu__item {
  text-align: center;
}
</style>
