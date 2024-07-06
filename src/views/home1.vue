<template>
  <el-container>
    <el-container>
      <el-menu class="el-menu-vertical-demo">
        <div style="text-align: center">
          <el-button style="width: 90%" @click="show=false; input=''; disabled=false"> New Question</el-button>
        </div>
        <el-table :data="tableData" style="width: 100%">
          <el-table-column width="180" label="历史记录" prop="date" show-overflow-tooltip>
            <template v-slot="scope">
              <el-link @click="selectData(scope.row.input); show = true;" :underline="false">
                {{ scope.row.input }}
              </el-link>
            </template>
          </el-table-column>
          <el-table-column>
            <template v-slot="scope">
              <el-button
                  @click="deleteRow(scope.row.input)"
                  type="text">
                移除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-menu>
      <el-main style="height: 584px">
        <div style="text-align: center">
          <el-input type="textarea" style="box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1); width: 1166px" id="input"
                    :disabled="disabled"
                    :rows="6" v-model="input"
                    placeholder="please enter the question" clearable>
          </el-input>
        </div>
        <div style="text-align: center; line-height: 80px">
          <el-button type="primary" @click="submit(input);" style="height: 45px">提交</el-button>
        </div>

        <div style="display: flex">
          <transition name="el-fade-in-linear">
            <div v-show="show" style="position: center; margin: auto;height: 30px">
              <div class="transition-span">纠纷性质</div>
              <div class="transition-box"
                   style="text-align:center; justify-content: center; align-items: center; text-indent: 0;line-height: 260px">
                {{ classify_result }}
              </div>
            </div>
          </transition>

          <transition name="el-fade-in-linear">
            <div v-show="show" style="position: center; margin: auto;height: 30px">
              <div class="transition-span">相似纠纷检索</div>
              <div class="transition-box1" style="text-indent: 0">
                <div>
                  <span id="title_one_span">第一条相似纠纷</span><span> :</span>
                </div>
                <el-link @click="show_method_one()" :underline="false"
                         style="word-break: break-word; text-indent: 2em">
                  {{ similar_result_one }}
                </el-link>

                <div>
                  <span id="title_two_span">第二条相似纠纷</span><span> :</span>
                </div>

                <el-link @click="show_method_two()" :underline="false" style="word-break: break-word; text-indent: 2em">
                  {{ similar_result_two }}
                </el-link>

                <div>
                  <span id="title_three_span">第三条相似纠纷</span><span> :</span>
                </div>
                <el-link class="display" @click="show_method_three()" :underline="false"
                         style="word-break: break-word; text-indent: 2em">
                  {{ similar_result_three }}
                </el-link>
              </div>
            </div>
          </transition>
        </div>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>

import {GetRequest} from "@/unity/api";
import i from "@/Home";

export default {
  data() {
    return {
      tableData: [],
      other: '',
      input: '',
      classify_result: "",
      similar_result_one: "",
      similar_result_two: "",
      similar_result_three: "",
      title: "第一条相似纠纷",
      show: false,
      show_: false,
      loading: true,
      err: "系统错误",
      disabled: false,
    }
  },
  created() {
    this.selectInput();
  },

  methods: {

    deleteRow(input) {
      GetRequest("http://localhost:8080/api/deleteClassify", input).then((res) => {
        if (res) {
          this.$message.success("删除成功")
          this.selectInput()
        }
      })
    },

    selectInput() {
      this.$axios.get('http://localhost:8080/api/selectClassify').then((res) => {
        console.log(res.data)
        this.tableData = res.data.reverse()
      })
    },
    selectData(input) {
      this.disabled = true;
      GetRequest('http://localhost:8080/api/selectClassifyData', input).then((resp) => {
        this.$message.success("查询成功")
        this.input = resp.data.input;
        this.jsonData = resp.data.rsl1;
        this.classify_result = resp.data.clas;
        this.similar_result_one = resp.data.simiOne;
        this.similar_result_two = resp.data.simiTwo;
        this.similar_result_three = resp.data.simiThree;
      })
    },
    submit(input) {
      if (input === '') {
        this.$message.warning("请输入")
      } else {
        let arr = []
        for (let a of this.tableData) {
          arr.push(a.input)
        }
        if (arr.includes(input)) {
          this.$message.error("数据重复，无法提交")
        } else {
          console.log(this.input)
          this.disabled = true;
          this.$message.success("提交成功")
          GetRequest('/api/Classify', this.input).then((resp) => {
            this.show = true;
            if (JSON.stringify(resp.data) !== null) {
              this.show_ = true;
              this.classify_result = resp.data.classify_result;
              this.other = resp.data.other;
              this.similar_result_one = resp.data.similar_result.similar_result_one;
              this.similar_result_two = resp.data.similar_result.similar_result_two;
              this.similar_result_three = resp.data.similar_result.similar_result_three;
              this.selectInput();
              this.$message.success(i.data().item_1 + "数据处理完成");
            } else {
              this.classify_result = this.err;
              this.other = this.err;
              this.similar_result_one = this.err;
              this.similar_result_two = this.err;
              this.similar_result_three = this.err;
            }
          })
        }
      }
    },
    consultation() {
      this.$router.push('/Consultation')
    },
    show_method_one() {
      this.show_ = true;
      this.title = document.getElementById("title_one_span").innerText
      this.other = "缴纳满一年的是可以办理报销的。" +
          "生育保险待遇由用人单位在职工产后或手术后18个月内，向社会保险经办机构申请办理，申办时应填报《职工生育待遇申领表》，并提供以下资料：" +
          "计划生育行政部门核发的生育证明；" +
          "生育医疗证明、门诊病历、出院小结、计划生育手术记录等原始材料；" +
          "婴儿出生证。" +
          "社会保险经办机构应当自受理申请之日起 15 个工作日内对用人单位提供的资料进行审核，审核完成后将生育保险费用拨付给职工所在用人单位，并由用人单位按照本办法规定的生育保险待遇项目和标准发给职工。"
    },
    show_method_two() {
      this.show_ = true;
      this.title = document.getElementById("title_two_span").innerText
      this.other = "向劳动向劳动部门投诉解决。\n" +
          "根据《中华人民共和国劳动合同法》第八十五条第一项的规定，用人单位未按照劳动合同的约定或者国家规定及时足额支付劳动者劳动报酬的，由劳动行政部门责令限期支付劳动报酬，逾期不支付的，责令用人单位按应付金额百分之五十以上百分之一百以下的标准向劳动者加付赔偿金。\n" +
          "投诉的解决的优点是，一旦用人单位是接到劳动行政部门的处理通知的，如果没有特别的原因，用人单位在劳动行政部门的压力下就可能会及时支付劳动者的工资，这样劳动者可能用最短的时间，最低的成本解决拖欠的工资问题。因此，这种方式在处理拖欠工资时，一般情况下可以首先选择。但是，如果劳动者的请求复杂的，如涉及经济补偿、赔偿金等，需要具体认定的，则可能劳动行政部门也无法解决，需要进行劳动仲裁程序。"
    },
    show_method_three() {
      this.show_ = true;
      this.title = document.getElementById("title_three_span").innerText
      this.other = "孕期被公司辞退有赔偿，除非是过失性辞退。孕期被辞退属于违法辞退，按经济补偿标准的二倍向劳动者支付赔偿金。经济补偿按劳动者在本" +
          "单位工作的年限，每满一年支付一个月工资的标准向劳动者支付。法律依据：《中华人民共和国劳动合同法》第四十二条 第四项劳动者有下列情形之一" +
          "的，用人单位不得依照本法第四十条、第四十一条的规定解除劳动合同：(四)女职工在孕期、产期、哺乳期的；第八十七条用人单位违反本法规定解除或" +
          "者终止劳动合同的，应当依照本法第四十七条规定的经济补偿标准的二倍向劳动者支付赔偿金。"
    }
  }
}
;
</script>

<style scoped>
.el-header {
  background-color: #0e4479;
  color: #303133;
  line-height: 60px;
  align-content: center;
}

.transition-span {
  background-color: #0e4479;
  width: 550px;
  height: 40px;
  line-height: 40px;
  text-align: center;
  color: #f4f4f5;
  border-radius: 7px;
  position: relative;
}

.transition-box {
  line-height: 30px;
  text-indent: 2em;
  background-color: #fff;
  border-radius: 7px;
  width: 550px;
  height: 260px;
  word-break: break-word;
  overflow-y: auto;
}

.transition-box1 {
  line-height: 36px;
  text-indent: 2em;
  background-color: #fff;
  border-radius: 7px;
  width: 550px;
  height: 260px;
  word-break: break-word;
  overflow-y: auto;
}

.transition-box2 {
  line-height: 30px;
  text-indent: 2em;
  background-color: #fff;
  border-radius: 7px;
  width: 400px;
  height: 260px;
  word-break: break-word;
  overflow-y: auto;
}

body {
  margin: 0;
  padding: 0;
}

</style>

