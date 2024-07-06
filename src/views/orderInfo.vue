<template>
  <el-container style="width: 100%">
    <el-main style="margin: 5px 10px 0;">
<!--      <div style="text-align: center; margin: 0 0 20px">-->
<!--        <el-button @click="selectOrderById()">刷新</el-button>-->
<!--      </div>-->
      <div>
        <el-table
            :data="tableData.slice((currentPage-1)*PageSize,currentPage*PageSize)"
            style="width: 100%">
          <el-table-column prop="out_trade_no" label="订单号"></el-table-column>
          <el-table-column prop="subject" label="订单名称"></el-table-column>
          <el-table-column prop="total_amount" label="付款金额"></el-table-column>
          <el-table-column prop="trade_status" label="订单状态"></el-table-column>
          <el-table-column prop="pay_channel" label="订单支付渠道"></el-table-column>
          <el-table-column prop="create_time" label="订单创建时间"></el-table-column>
          <el-table-column prop="pay_time" label="付款时间"></el-table-column>
          <el-table-column prop="discount_amount" label="折扣金额"></el-table-column>
        </el-table>
      </div>

      <div class="page">
        <!-- 分页控件 -->
        <el-pagination
            :background="true"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page.sync="currentPage"
            :page-sizes="pageSizes"
            :page-size="PageSize"
            :total="totalCount"
            layout="total, sizes, prev, pager, next, jumper">
        </el-pagination>
      </div>
    </el-main>
  </el-container>
</template>

<script>
import {GetRequestByUserId} from "@/unity/api";

export default {
  name: "orderInfo",
  created() {
    this.selectOrderById()
  },
  data() {
    return {
      // 总数据
      tableData: [],

      userid: this.$cookie.get("userid"),

      // 默认显示第几页
      currentPage: 1,
      // 总条数，根据接口获取数据长度(注意：这里不能为空)
      totalCount: 0,
      // 个数选择器（可修改）
      pageSizes: [1, 5, 10],
      // 默认每页显示的条数（可修改）
      PageSize: 5,
    }
  },
  methods: {
    selectOrderById() {
      GetRequestByUserId("http://localhost:8080/pay_api/selectAllOrder", this.userid).then((res) => {
        this.tableData = res.data.reverse()
        this.totalCount = this.tableData.length
      })
    },

    // 分页
    // 每页显示的条数
    handleSizeChange(val) {
      // 改变每页显示的条数
      this.PageSize = val
      // 注意：在改变每页显示的条数时，要将页码显示到第一页
      this.currentPage = 1
    },
    // 显示第几页
    handleCurrentChange(val) {
      // 改变默认的页数
      this.currentPage = val
    },
  }
}
</script>

<style scoped>
.page {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0;
  padding: 0;
}
</style>