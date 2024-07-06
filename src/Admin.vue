<template>
  <el-container>
    <el-container>
      <el-header style="text-align: left; font-size: 12px; height: 60px; display: flex; padding: 0">
        <div style="text-align: center; font-size: 25px; color: #f4f4f4; width: 220px;">管理员页面</div>
        <div style="padding: 0 20px 0">
          <el-dropdown @command="handleCommand">
            <em class="el-icon-setting" style="margin-right: 15px"></em>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item>返回登录</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
          <el-tag type="info">{{ get_username }}</el-tag>
        </div>

      </el-header>
      <el-container>
        <el-row style="width: 220px;background-color: #f3f3f3">
          <el-col style="width: 220px">
            <el-menu default-active="1">
              <el-submenu index="1">
                <template slot="title">
                  <em class="el-icon-menu"></em>
                  <span>站点统计</span>
                </template>
                <el-menu-item-group>
                  <template slot="title" style="padding: 0"></template>
                  <el-menu-item @click="visit" index="1-1">查看</el-menu-item>
                  <el-menu-item index="1-2">修改</el-menu-item>
                </el-menu-item-group>
              </el-submenu>
              <el-submenu index="2">
                <template slot="title">
                  <em class="el-icon-menu"></em>
                  <span>用户管理</span>
                </template>
                <el-menu-item-group>
                  <template slot="title" style="padding: 0"></template>
                  <el-menu-item @click="user_select" index="2-1">查找</el-menu-item>
                  <el-menu-item @click="user" index="2-2">修改</el-menu-item>
                </el-menu-item-group>
              </el-submenu>
              <el-submenu index="3">
                <template slot="title">
                  <em class="el-icon-menu"></em>
                  <span>通知管理</span>
                </template>
                <el-menu-item-group>
                  <template slot="title" style="padding: 0"></template>
                  <el-menu-item @click="check_notify" index="3-1">查看</el-menu-item>
                  <el-menu-item @click="publish_notify" index="3-2">发布</el-menu-item>
                </el-menu-item-group>
              </el-submenu>
              <el-submenu index="4">
                <template slot="title">
                  <em class="el-icon-menu"></em>
                  <span>优惠券管理</span>
                </template>
                <el-menu-item-group>
                  <template slot="title" style="padding: 0"></template>
                  <el-menu-item @click="discount" index="4-1">查看优惠券</el-menu-item>
                  <el-menu-item @click="used_coupons" index="4-2">已使用优惠券</el-menu-item>
                </el-menu-item-group>
              </el-submenu>
              <el-submenu index="5">
                <template slot="title">
                  <em class="el-icon-menu"></em>
                  <span>反馈管理</span>
                </template>
                <el-menu-item-group>
                  <template slot="title" style="padding: 0"></template>
                  <el-menu-item @click="check_feedback" index="5-1">查看</el-menu-item>
                  <el-menu-item index="5-2">修改</el-menu-item>
                </el-menu-item-group>
              </el-submenu>
              <el-submenu index="6">
                <template slot="title">
                  <em class="el-icon-menu"></em>
                  <span>个人信息</span>
                </template>
                <el-menu-item-group>
                  <template slot="title" style="padding: 0"></template>
                  <el-menu-item index="6-1">查看</el-menu-item>
                  <el-menu-item index="6-2">修改</el-menu-item>
                </el-menu-item-group>
              </el-submenu>
            </el-menu>
          </el-col>
        </el-row>

        <el-main style="padding: 0; height: 648px">
          <router-view/>
        </el-main>
      </el-container>
    </el-container>
  </el-container>
</template>

<script>


export default {
  name: "Admin",
  data() {
    return {
      get_username: "",
    }
  },

  created() {
    this.get_username = this.$cookie.get("username")
    this.$router.push("/visit")
  },

  methods: {
    handleCommand() {
      this.$router.push('/');
    },
    user() {
      this.$router.push('/user_test3')
    },
    user_select() {
      this.$router.push('/user_select')
    },
    visit(){
      this.$router.push('/visit')
    },
    check_notify(){
      this.$router.push('/check_notify')
    },
    publish_notify(){
      this.$router.push('/publish_notify')
    },
    discount(){
      this.$router.push('/discount')
    },
    used_coupons(){
      this.$router.push('/used_coupons')
    },
    check_feedback(){
      this.$router.push('/check_feedback')
    }
  }
};
</script>

<style scoped>
.main {
  width: 100%;
  border: hidden;
  overflow: hidden;
}

.el-header {
  background-color: #B3C0D1;
  color: #333;
  line-height: 55px;
}
</style>