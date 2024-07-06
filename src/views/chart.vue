<template>
  <div>
    <div class="Echarts" style="width: 100%; height: 700px; margin: 0;padding: 0">
      <div id="main" style="width: 100%; height: 700px; margin: 0;padding: 0"></div>
    </div>
  </div>
</template>


<script>
export default {
  data() {
    return {
      myChart: {},
      option: {},
    };
  },
  methods: {

    makeRandomData() {
      this.num = Math.random() * 70;
      return this.num;
    },

    updateEcharts() {
      // 指定图表的配置项和数据
      let myTimer = setInterval(() => {
        this.myChart.setOption({
          series: [
            {
              name: "数据关系",
              radius: 70,
              animation: true,	// 是否开启动画；默认是开启
              emphasis: {},	// 可以设置被选中的元素突出显示的特殊样式

              itemStyle: {
                label: {
                  fontSize: 14,
                  color: 'yellow'
                }
              },
              type: 'graph',
              layout: 'force',//图表类型

              symbolSize: 15,
              roam: true,
              force: { //力引导图基本配置
                initLayout: true,//力引导的初始化布局，默认使用xy轴的标点
                repulsion: 800,//节点之间的斥力因子。支持数组表达斥力范围，值越大斥力越大。
                gravity: 0,//节点受到的向中心的引力因子。该值越大节点越往中心点靠拢。
                edgeLength: this.makeRandomData(),//边的两个节点之间的距离，这个距离也会受 repulsion。[10, 50] 。值越小则长度越长
                layoutAnimation: true
                //因为力引导布局会在多次迭代后才会稳定，这个参数决定是否显示布局的迭代动画，在浏览器端节点数据较多（>100）的时候不建议关闭，布局过程会造成浏览器假死。
              },

              label: {
                show: true,
                position: 'right',
              },
              // edgeSymbol: ['circle', 'arrow'],//线的样式 无剑头，有箭头
              edgeSymbolSize: [2, 10],
              edgeLabel: {
                textStyle: {
                  fontSize: 20
                }
              },
              lineStyle: {
                showAllSymbol: true,
                opacity: 0.9,
                width: 1,
                color: '#333333',
              },
              data: [
                // 列出所有项，不能有重复元素，参数不能和参数值相同。
                //每个对象都需要category：n（图例里data的索引值），如果没有，点击图例，对应项不会消失
                {name: '默特萨克', symbol: 'circle', category: 1, ignore: true, flag: true},
                {name: '拜仁慕尼黑', symbol: 'circle', ignore: true, category: 1, flag: true},
                {name: '厄齐尔', symbol: 'circle', ignore: true, category: 1, flag: true},
                {name: '波多尔斯基', symbol: 'circle', ignore: true, category: 1, flag: true},
                {name: '诺伊尔', symbol: 'circle', ignore: true, category: 0, flag: true},
                {name: '博阿滕', symbol: 'circle', ignore: true, category: 0, flag: true},
                {name: '施魏因施泰格', ignore: true, category: 0, flag: true},
                {name: '拉姆', symbol: 'circle', ignore: true, category: 0, flag: true},
                {name: '克罗斯', symbol: 'circle', ignore: true, category: 0, flag: true},
                {name: '穆勒', symbol: 'circle', ignore: true, category: 0, flag: true},
                {name: '格策', symbol: 'circle', ignore: true, category: 0, flag: true},
                {name: '胡梅尔斯', symbol: 'circle', ignore: true, category: 1, flag: true},
                {name: '魏登费勒', symbol: 'circle', ignore: true, category: 1, flag: true},
                {name: '杜尔姆', symbol: 'circle', ignore: true, category: 1, flag: true},
                {name: '格罗斯克罗伊茨', symbol: 'circle', ignore: true, category: 1, flag: true}
              ],
              focusNodeAdjacency: true,
              categories: [ //symbol name：用于和 legend 对应以及格式化 tooltip 的内容。 label有效
                {
                  name: '数据项',
                  symbol: 'circle'
                },
                {
                  name: '目录',
                  symbol: 'circle'
                }],
              links: [// 1、用data中的name列出对应关系。2、节点元素在data属性中的索引来建立节点之间的联系。
                {source: 0, target: 1},
                {source: '拉姆', target: '厄齐尔'},
                {source: '拉姆', target: '波多尔斯基'},
                {source: '拜仁慕尼黑', target: '诺伊尔'},
                {source: '拜仁慕尼黑', target: '博阿滕'},
                {source: '拜仁慕尼黑', target: '施魏因施泰格'},
                {source: '拜仁慕尼黑', target: '拉姆'},
                {source: '拜仁慕尼黑', target: '克罗斯'},
                {source: '拜仁慕尼黑', target: '穆勒'},
                {source: '拜仁慕尼黑', target: '格策'},
                {source: '格策', target: '胡梅尔斯'},
                {source: '格策', target: '魏登费勒'},
                {source: '格策', target: '杜尔姆'},
                {source: '格策', target: '格罗斯克罗伊茨'}
              ]
            }
          ]
        });
      }, 1000);
      this.myChart.on('mouseover', function (param) {
        if (param.dataType === 'node') {
          console.log('111')
          clearInterval(myTimer);
        }
      })

      this.option = {
        animation: true,
        title: {
          text: '数据图谱'
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} : {b}'// 如果用索引关联关系，悬浮窗会写索引。
        },
        legend: { //圖表控件
          show: true,
          data: [
            {
              name: '数据项',
              icon: 'circle'
            }, {
              name: '目录',
              icon: 'circle'
            }]
        },
      }

      // 使用刚指定的配置项和数据显示图表。
      this.myChart.setOption(this.option)
    },

    mounted() {
      this.myChart = this.$echarts.init(document.getElementById("main"));

      this.myChart.on('click', function (param) {
        if (param.dataType === 'node') {
          console.log('点击了节点', param.data.name, param.data)
        } else {
          console.log('点击了边', param)
        }
      });
      this.updateEcharts()
    },
  }
}
</script>
