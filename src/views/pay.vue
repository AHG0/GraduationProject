<template>
  <div style="display: flex">
    <div style="margin: 40px auto 0">
      <div style="margin: 40px auto;">
        <el-row :gutter="20">
          <el-col :span="8" v-for="(item, index) in typeTableData" :key="index">
            <el-card style="margin-bottom: 20px;">
              <div style="text-align: center">
                <h3 slot="header">{{ item.usertype }}</h3>
              </div>
              <div style="height: 200px; width: 200px; text-align: center">
                <div v-for="(segment, segIndex) in item.description.split('，')" :key="segIndex">
                  <p>{{ segment }}</p>
                </div>
              </div>
              <div v-if="usertypeNum < item.usertypeNum" style="text-align: center; margin-top: 10px;">
                <el-button size="mini" type="primary" @click="setChoose(index)">立刻升级</el-button>
              </div>
              <div v-else style="text-align: center; margin-top: 10px;">
                <el-button disabled size="mini">您已拥有</el-button>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <el-dialog :visible.sync="dialog">
        <div class="card-header">你选择升级为{{ chooseUserType }}，请选择支付套餐</div>
        <div class="payment-options">
          <el-card class="payment-option" v-for="(item, index) in showPayData" :key="index">
            <div class="payment-option-title">{{ item.payType }}</div>
            <!--            未选择优惠券-->
            <div class="payment-option-description" v-if="selectedCoupon==='0'">
              <div>
                {{ item.total_amount }}
              </div>
              <div></div>
            </div>
            <!--            选择非通用优惠券-->
            <div class="payment-option-description" v-if="selectedCoupon!=='0' && selectedCoupon.category!=='通用'">
              <div v-if="item.payType===selectedCoupon.category">
                <div style="text-decoration: line-through;">
                  优惠前：{{ item.total_amount }}
                </div>
                <div>
                  优惠后：{{ finalPay(item.total_amount) }}
                </div>
              </div>
              <div v-if="item.payType!==selectedCoupon.category">
                <div>
                  {{ item.total_amount }}
                </div>
                <div></div>
              </div>
              <div class="payment-option-description" v-if="selectedCoupon==='0'">
                <div>
                  {{ item.total_amount }}
                </div>
                <div></div>
              </div>
            </div>
            <!--            选择通用优惠券-->
            <div class="payment-option-description" v-if="selectedCoupon!=='0'&&selectedCoupon.category==='通用'">
              <div>
                <div style="text-decoration: line-through">
                  优惠前：{{ item.total_amount }}
                </div>
                <div>
                  优惠后：{{ finalPay(item.total_amount) }}
                </div>
              </div>
            </div>
            <div style="text-align: center">
              <el-button
                  type="primary"
                  size="mini"
                  @click="submitForm(index, item.total_amount)">去支付
              </el-button>
            </div>
          </el-card>
        </div>
        <div style="text-align: center">
          <el-link @click="showCouponDialog">
            {{ selectedCoupon === '0' ? '点击选择优惠券' : '重新选择优惠券' }}
          </el-link>
        </div>
        <div style="text-align: center" v-if="selectedCoupon!=='0'">
          已选择【{{ selectedCoupon.category + selectedCoupon.name }}】
        </div>
      </el-dialog>
      <!-- 优惠券选择对话框 -->
      <el-dialog :visible.sync="couponDialogVisible">
        <div class="scrollable-dialog">
          <div class="coupon-selection">
            <el-row>
              <el-col :span="6">
                <el-input v-model="searchKeyword" placeholder="搜索优惠券" clearable @clear="clearSearch"
                          @input="searchCoupons"></el-input>
              </el-col>
              <el-col :span="18" class="filter-section">
                <span class="filter-label">筛选：</span>
                <el-select v-model="selectedCategory" placeholder="选择分类" clearable @change="filterCoupons">
                  <el-option v-for="category in categories" :key="category.id" :label="category.name"
                             :value="category.name"></el-option>
                </el-select>
                <el-select v-model="selectedType" placeholder="选择类型" clearable @change="filterCoupons">
                  <el-option v-for="type in types" :key="type.id" :label="type.name" :value="type.name"></el-option>
                </el-select>
              </el-col>
            </el-row>
            <el-row style="margin-top: 20px">
              <el-col :span="24">
                <el-card class="coupon-card" v-for="coupon in filteredCoupons" :key="coupon.id"
                         :body-style="{ padding: '10px' }"
                         :class="{ 'expired-coupon': isCouponExpired(coupon)||isCouponUsed(coupon), 'selected-coupon': selectedCoupon === coupon}"
                         @click.native="isCouponUsed(coupon) ? null : selectCoupon(coupon)">
                  <div class="coupon-content">
                    <div>
                      <h2>{{ coupon.name }}</h2>
                      <p>{{ coupon.description }}</p>
                      <span v-if="isCouponUsed(coupon)" class="used">已使用</span>
                      <span v-else-if="isCouponExpired(coupon)" class="expired">已过期</span>
                      <div style="text-align: right">
                        <span v-if="coupon.category === '通用'" class="coupon-category general">通用</span>
                        <span v-else-if="coupon.category === '月付'" class="coupon-category monthly">月付</span>
                        <span v-else-if="coupon.category === '季付'" class="coupon-category quarterly">季付</span>
                        <span v-else-if="coupon.category === '年付'" class="coupon-category yearly">年付</span>
                        <p class="coupon-validity">有效期至 {{ coupon.validity }}</p>
                      </div>
                    </div>
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </div>
        </div>
        <span slot="footer" class="dialog-footer">
          <el-button @click="couponDialogVisible=false;selectedCoupon='0'">取消使用</el-button>
          <el-button type="primary" @click="applyCoupon">使用优惠券</el-button>
        </span>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import qs from 'qs'
import axios from "axios";

export default {
  name: "pay",
  data() {
    return {
      subject: '', // 商品名称
      description: '1',
      sub_period: -1,//订阅周期
      userid: this.$cookie.get("userid"),
      usertypeNum: this.$cookie.get("usertypeNum"),
      chooseUserTypeNum: -1, //存放选择的会员类别
      chooseUserType: '',
      finalAmount: 0,
      couponShow: false,
      couponDialogVisible: false, // 是否显示优惠券选择对话框
      selectedCoupon: '0', // 选中的优惠券

      typeTitle: ['普通会员', '中级会员', '高级会员'],
      typeTableData: [
        {
          usertype: "普通会员",
          usertypeNum: 0,
          description: '1文件/次，10文件/天，10字/文件',
        }, {
          usertype: "中级会员",
          usertypeNum: 1,
          description: '10文件/次，100文件/天，100字/文件',
        }, {
          usertype: "高级会员",
          usertypeNum: 2,
          description: '100文件/次，1000文件/天，1000字/文件',
        }
      ],
      typeList: [
        {title: '商品描述', label: 'description'},
        {title: 'button', label: 'button'}
      ],

      payList: [
        {title: 'total_amount', label: 'total_amount'},
        {title: 'discount', label: 'discount'},
        {title: 'button', label: 'button'},
      ],
      payTitle: ['月付', '季付', '年付'],

      showPayData: [],

      payData: [[{
        payType: '月付',
        payTypeNum: 1,
        total_amount: '9',
      }, {
        payType: '季付',
        payTypeNum: 2,
        total_amount: '18',
      }, {
        payType: '年付',
        payTypeNum: 3,
        total_amount: '36',
      }], [{
        payType: '月付',
        payTypeNum: 1,
        total_amount: '12',
      }, {
        payType: '季付',
        payTypeNum: 2,
        total_amount: '24',
      }, {
        payType: '年付',
        payTypeNum: 3,
        total_amount: '48',
      }], [{
        payType: '月付',
        payTypeNum: 1,
        total_amount: '15',
      }, {
        payType: '季付',
        payTypeNum: 2,
        total_amount: '30',
      }, {
        payType: '年付',
        payTypeNum: 3,
        total_amount: '60',
      }],],
      dialog: false,
      searchKeyword: '',
      selectedCategory: '',
      selectedType: '',
      categories: [
        {id: 1, name: '月付'},
        {id: 2, name: '季付'},
        {id: 3, name: '年付'},
        {id: 4, name: '通用'},
      ],
      types: [
        {id: 1, name: '满减'},
        {id: 2, name: '折扣'}
      ],
      coupons: [],
      usedCoupons: [],
    }
  },
  computed: {
    filteredCoupons() {
      let filtered = this.coupons.filter(coupon => !this.isCouponUsed(coupon) && !this.isCouponExpired(coupon));
      // 过滤过期和被使用的
      const expiredCoupons = this.coupons.filter(coupon => this.isCouponExpired(coupon));
      const usedCoupons = this.coupons.filter(coupon => this.isCouponUsed(coupon));
      // 拼接
      filtered = filtered.concat(usedCoupons, expiredCoupons);
      // 搜索
      if (this.searchKeyword) {
        filtered = filtered.filter(coupon => coupon.name.toLowerCase().includes(this.searchKeyword.toLowerCase()));
      }
      if (this.selectedCategory) {
        filtered = filtered.filter(coupon => coupon.category === this.selectedCategory);
      }
      if (this.selectedType) {
        filtered = filtered.filter(coupon => coupon.type === this.selectedType);
      }
      return filtered;
    },
    isCouponExpired() {
      return coupon => {
        const currentDate = new Date();
        const expiryDate = new Date(coupon.validity);
        return expiryDate < currentDate; // 如果过期返回 true，否则返回 false
      };
    },
  },
  watch: {
    dialog(newName) {
      if (newName === false) {
        this.selectedCoupon = '0'
      }
    }
  },
  methods: {
    submitForm(index, total_amount) {
      this.subject = this.payTitle[index] + this.chooseUserType
      var discount = this.selectedCoupon !== '0' && this.selectedCoupon.category !== '通用' && this.selectedCoupon.category === this.payTitle[index] ? this.selectedCoupon.name : '0'
      var finalPay = this.selectedCoupon !== '0' && this.selectedCoupon.category !== '通用' && this.selectedCoupon.category === this.payTitle[index] ? this.finalAmount : total_amount
      var discount_id = this.selectedCoupon !== '0' && this.selectedCoupon.category !== '通用' && this.selectedCoupon.category === this.payTitle[index] ? this.selectedCoupon.id : '0'
      console.log("total_amount:" + finalPay)
      console.log("subject:" + this.subject)
      console.log("description:" + this.description)
      console.log("userid:" + this.userid)
      console.log("discount:" + discount)
      console.log("discount_id:" + discount_id)
      let postData = qs.stringify({
        total_amount: finalPay,
        subject: this.subject,
        description: this.description,
        userid: this.userid,
        discount: discount,
        discount_id: discount_id
      })
      this.$axios.post("http://localhost:8080/pay_api/AliPay", postData, {
        headers: {
          token: localStorage.getItem("token")
        }
      }).then((response) => {
        console.log(response);
        console.log("【支付宝返回】" + response.data);
        //这里是跳转新的页面
        document.querySelector('body').innerHTML = "正在前往支付页面......";
        const div = document.createElement('div');
        div.innerHTML = response.data;
        document.body.appendChild(div);
        // _blank -- 在新窗口中打开链接
        // _parent -- 在父窗体中打开链接
        // _self -- 在当前窗体打开链接,此为默认值
        // _top -- 在当前窗体打开链接，并替换当前的整个窗体(框架页)
        document.forms[0].setAttribute('target', '_top');// 新建窗口页面
        document.forms[0].submit();
        // GetRequestByUserId('http://localhost:8080/user_api/select_by_userid', this.userid).then((resp) => {
        //   this.$cookie.set('mail', resp.data.mail)
        //   this.$cookie.set('phone', resp.data.phone)
        //   this.$cookie.set('username', resp.data.username)
        //   this.$cookie.set('userid', resp.data.userid)
        //   this.$cookie.set('usertypeNum', resp.data.usertype)
        //   this.$cookie.set('permission', resp.data.permission)
        // })
      }).catch(function (error) {
        console.log(error)
      })
    },
    setChoose(index) {
      console.log(index)
      this.showPayData = this.payData[index]
      this.chooseUserTypeNum = this.typeTableData[index].usertypeNum
      this.chooseUserType = this.typeTableData[index].usertype
      this.description = this.typeTableData[index].description
      this.dialog = true
    },
    showCouponDialog() {
      // 请求获取可用优惠券列表
      this.couponShow = true
      axios.get('/pay_api/couponsUsedByUser/' + this.userid)
          .then((resp) => {
            this.usedCoupons = resp.data
            console.log(resp.data)
          })
      axios.get('/coupon_api/get_coupon')
          .then(response => {
            this.coupons = response.data;
            this.couponDialogVisible = true; // 显示优惠券选择对话框
          })
          .catch(error => {
            console.error('Error fetching available coupons:', error);
          });
    },
    applyCoupon() {
      this.couponDialogVisible = false;
    },
    finalPay(value) {
      if (this.selectedCoupon.type === '折扣') {
        this.finalAmount = value * this.selectedCoupon.discount
        return value * this.selectedCoupon.discount
      } else if (this.selectedCoupon.type === '满减') {
        this.finalAmount = value - this.selectedCoupon.discount
        return value - this.selectedCoupon.discount
      } else {
        this.finalAmount = value
        return value
      }

    },
    searchCoupons() {
      // 发送请求获取优惠券列表
      axios.get('/coupon_api/get_coupon')
          .then(response => {
            this.coupons = response.data;
          })
          .catch(error => {
            console.error('Error fetching coupons:', error);
          });
    },
    clearSearch() {
      this.searchKeyword = '';
    },
    // 判断优惠券是否已被使用
    isCouponUsed(coupon) {
      return this.usedCoupons.includes(coupon.id);
    },
    selectCoupon(selectedCoupon) {
      console.log(selectedCoupon)
      if (selectedCoupon && !this.isCouponExpired(selectedCoupon)) {
        this.selectedCoupon = selectedCoupon;
        this.coupons.forEach(coupon => {
          coupon.selected = (coupon === selectedCoupon);
        });
      } else if (selectedCoupon && this.isCouponExpired(selectedCoupon)) {
        // 过期
        console.log("Expired coupon cannot be selected.");
      } else {
        // 已使用或无效
        console.log("Invalid coupon selection.");
      }
    }
  }
}
</script>

<style scoped>
.demo-table-expand {
  font-size: 0;
}

.demo-table-expand label {
  width: 90px;
  color: #99a9bf;
}

.demo-table-expand .el-form-item {
  margin-right: 0;
  margin-bottom: 0;
  width: 50%;
}

.coupon-selection {
  padding: 20px;
}

.filter-section {
  text-align: right;
}

.filter-label {
  margin-right: 10px;
}

.coupon-card {
  cursor: pointer;
  margin-bottom: 20px;
  transition: border-color 0.3s;
}

.coupon-validity {
  font-size: 12px;
  color: #999;
}

.coupon-content {
  margin: 5px 10px 10px;
}

.selected-coupon {
  border: 2px solid #409EFF;
}

.expired-coupon {
  color: #999;
  background-color: #f2f2f2;
  cursor: default;
}

.payment-options {
  display: flex;
  justify-content: space-around;
}

.payment-option {
  margin: 20px;
  width: 300px;
  text-align: center;
}

.payment-option-title {
  font-weight: bold;
  font-size: 18px;
  margin-bottom: 10px;
}

.payment-option-description {
  margin-bottom: 20px;
  height: 100px;
}

.used {
  background-color: #67C23A; /* 绿色背景表示已使用 */
  color: white; /* 白色字体 */
  padding: 3px 6px; /* 适当的内边距 */
  border-radius: 4px; /* 圆角边框 */
  height: auto;
}

.expired {
  background-color: #F56C6C; /* 红色背景表示已过期 */
  color: white; /* 白色字体 */
  padding: 3px 6px; /* 适当的内边距 */
  border-radius: 4px; /* 圆角边框 */
  height: auto;
}

.coupon-category {
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 12px;
}

.general {
  background-color: #999;
  color: white;
}

.monthly {
  background-color: #409EFF;
  color: white;
}

.quarterly {
  background-color: #67C23A;
  color: white;
}

.yearly {
  background-color: #F56C6C;
  color: white;
}

.scrollable-dialog {
  max-height: 390px;
  overflow-y: auto;
}
</style>