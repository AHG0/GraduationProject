<template>
  <div>
    <el-row>
      <el-col :span="6">
        <el-input v-model="userId" placeholder="用户ID"></el-input>
      </el-col>
      <el-col :span="6">
        <el-input v-model="couponId" placeholder="优惠券ID"></el-input>
      </el-col>
    </el-row>
    <el-table :data="filteredCoupons" border style="width: 100%">
      <el-table-column prop="userid" label="使用用户id"></el-table-column>
      <el-table-column prop="coupon_id" label="描述优惠券id"></el-table-column>
      <el-table-column prop="useTime" label="使用时间"></el-table-column>
      <el-table-column prop="actions" label="操作">
        <template slot-scope="scope">
          <el-button type="danger" @click="removeCoupon(scope.$index)">移除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[10, 20, 30, 40]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="filteredCoupons.length">
    </el-pagination>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      usedCoupons: [], // 从后端获取的优惠券数据
      searchText: '',
      selected: true, // 标志位，表示当前显示已选择的优惠券还是全部优惠券
      currentPage: 1,
      pageSize: 10,
      userId: '',
      couponId: '',
    };
  },
  computed: {
    filteredCoupons() {
      let filtered = this.usedCoupons;
      if (this.userId) {
        filtered = filtered.filter(coupon => coupon.userid.toString().includes(this.userId));
      }
      if (this.couponId) {
        filtered = filtered.filter(coupon => coupon.coupon_id.toString().includes(this.couponId));
      }
      return filtered;
    }
  },
  methods: {
    // 从后端获取优惠券数据的方法
    fetchCoupons() {
      axios.get('/pay_api/getUsedCoupons')
          .then((resp) => {
            this.usedCoupons = resp.data
            console.log(resp.data)
          })
    },
    removeCoupon(index) {
      // 移除优惠券的方法，可以根据实际需求修改
      console.log(this.usedCoupons[index])
      this.$confirm('确定要移除该优惠券吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        axios.delete("/pay_api/delete_coupon/" + this.usedCoupons[index].id).then((resp) => {
          this.$message.success(resp.data);
          this.fetchCoupons();
        })
      }).catch(() => {
        this.$message.info('已取消移除');
      });
    },
    handleSizeChange(val) {
      this.pageSize = val;
    },
    handleCurrentChange(val) {
      this.currentPage = val;
    }
  },
  mounted() {
    this.fetchCoupons();
  }
};
</script>
