<template>
  <div>
    <div style="text-align: center">
      <h1>优惠券管理</h1>
      <el-button type="primary" @click="addCoupon">添加优惠券</el-button>
    </div>
    <el-dialog
        :title="title"
        :visible.sync="showAddCouponDialog"
        width="30%">
      <el-form :model="newCoupon" :rules="couponRules" ref="couponForm" label-width="100px">
        <el-form-item label="优惠券名称" prop="name">
          <el-input v-model="newCoupon.name"></el-input>
        </el-form-item>
        <el-form-item label="优惠券描述" prop="description">
          <el-input v-model="newCoupon.description"></el-input>
        </el-form-item>
        <el-form-item label="折扣额度" prop="discount">
          <el-input v-model="newCoupon.discount" type="number"></el-input>
        </el-form-item>
        <el-form-item label="过期时间" prop="validity">
          <el-date-picker value-format="yyyy-MM-dd" type="date" placeholder="选择日期" v-model="newCoupon.validity"
                          style="width: 100%;"></el-date-picker>
        </el-form-item>
        <el-form-item label="适用范围" prop="category">
          <el-select style="width: 100%;" v-model="newCoupon.category" placeholder="请选择适用范围">
            <el-option label="月付" value="月付"></el-option>
            <el-option label="季付" value="季付"></el-option>
            <el-option label="年付" value="年付"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="优惠类别" prop="type">
          <el-select style="width: 100%;" v-model="newCoupon.type" placeholder="请选择优惠类别">
            <el-option label="满减" value="满减"></el-option>
            <el-option label="折扣" value="折扣"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="showAddCouponDialog=false;editingCoupon=null">取消</el-button>
        <el-button type="primary" @click="addOrUpdateCoupon">{{
            editingCoupon ? '保存' : '添加'
          }}</el-button>
      </span>
    </el-dialog>
    <div style="margin: 0 20px 20px">
      <el-table :data="coupons" style="width: 100%">
        <el-table-column prop="id" label="优惠券ID"></el-table-column>
        <el-table-column prop="name" label="优惠券名称"></el-table-column>
        <el-table-column prop="description" label="优惠券描述"></el-table-column>
        <el-table-column prop="discount" label="折扣额度"></el-table-column>
        <el-table-column prop="validity" label="过期时间"></el-table-column>
        <el-table-column prop="category" label="适用范围" width="100px"></el-table-column>
        <el-table-column prop="type" label="类别" width="100px"></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button @click="editCoupon(scope.row)">编辑</el-button>
            <el-button type="danger" @click="deleteCoupon(scope.$index)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'coupon',
  data() {
    return {
      showAddCouponDialog: false,
      newCoupon: {
        category: '',
        description: '',
        discount: '',
        id: '',
        name: '',
        selected: '',
        type: '',
        validity: '',
      },
      couponRules: {
        name: [{required: true, message: '请输入优惠券名称', trigger: 'blur'}],
        description: [{required: true, message: '请输入优惠券描述', trigger: 'blur'}],
        discount: [{required: true, message: '请输入折扣额度', trigger: 'blur'}],
        category: [{required: true, message: '请输入优惠券适用范围', trigger: 'blur'}],
        type: [{required: true, message: '请输入优惠券类别', trigger: 'blur'}],
        validity: [{required: true, message: '请选择优惠券过期时间', trigger: 'blur'}],
      },
      coupons: [],
      editingCoupon: null,
      title: '',
      add: false,
      edit: false,
    };
  },
  mounted() {
    // 获取优惠券列表
    this.selectCoupons();
  },
  methods: {
    selectCoupons() {
      // 发送请求获取优惠券列表
      axios.get('/coupon_api/get_coupon')
          .then(response => {
            this.coupons = response.data;
            console.log(this.coupons)
          })
          .catch(error => {
            console.error('Error fetching coupons:', error);
          });
    },
    addCoupon() {
      this.showAddCouponDialog = true;
      this.add = true;
      this.edit = false;
      this.title = '添加优惠券';
      this.newCoupon = {
        category: '',
        description: '',
        discount: '',
        id: '',
        name: '',
        selected: '',
        type: '',
        validity: '',
      }
    },
    addOrUpdateCoupon() {
      this.$refs.couponForm.validate((valid) => {
        if (valid) {
          if (this.edit) {
            // 编辑优惠券
            axios.put(`/coupon_api/update_coupon/${this.editingCoupon.id}`, this.newCoupon)
                .then(response => {
                  const index = this.coupons.findIndex(coupon => coupon.id === response.data.id);
                  this.coupons.splice(index, 1, response.data);
                  this.showAddCouponDialog = false;
                  this.$refs.couponForm.resetFields();
                  this.editingCoupon = null;
                  this.selectCoupons()
                })
                .catch(error => {
                  console.error('Error updating coupon:', error);
                });
          } else {
            // 添加优惠券
            var data = this.newCoupon
            axios.get("/coupon_api/add_coupon", {params: data})
                .then(response => {
                  if (response.data === 1) {
                    this.coupons.push(data);
                    this.showAddCouponDialog = false;
                    this.$refs.couponForm.resetFields();
                    this.selectCoupons()
                  }
                })
                .catch(error => {
                  console.error('Error adding coupon:', error);
                });
          }
        }
      });
    },
    editCoupon(coupon) {
      this.edit = true;
      this.add = false;
      this.title = '修改优惠券'
      this.showAddCouponDialog = true;
      this.editingCoupon = coupon;
      this.newCoupon = {...coupon}; // 将当前优惠券信息复制到表单中进行编辑
      this.selectCoupons()
    },
    deleteCoupon(index) {
      const coupon = this.coupons[index];
      axios.get(`/pay_api/is_exist_coupon/${coupon.id}`)
          .then((resp) => {
            if (resp.data === 1) {
              this.$message.error(`ID为${coupon.id}的优惠券存在关联用户`)
            } else {
              // 删除优惠券
              axios.delete(`/coupon_api/delete_coupon/${coupon.id}`)
                  .then((resp) => {
                    if (resp.data === "删除成功") {
                      this.$message.success(resp.data)
                      this.coupons.splice(index, 1);
                    } else {
                      this.$message.error(resp.data)
                    }
                  })
            }
          })
    },
  }
}
</script>
<style scoped>

</style>