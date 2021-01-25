<template>
  <section class="history-list">
    <div class="search-bar">
      <div class="search-item">
        <div class="form-item">
          <label for="">任&nbsp;务&nbsp;I&nbsp;D：</label>
          <n3-input v-model="searchKey.taskId" @change="searchChange" readonly></n3-input>
        </div>
        <div class="form-item">
          <label for="">查询状态：</label>
          <n3-select v-model="searchKey.taskState" @change="searchChange" width="150px" readonly>
            <n3-option value="">不限</n3-option>
            <n3-option value="1">可训练</n3-option>
            <n3-option value="0">训练中</n3-option>
          </n3-select>
        </div>
      </div>
<!--      <div class="search-item">-->
<!--        <div class="form-item">-->
<!--          <label for="">开始时间： </label>-->
<!--          <n3-datepicker-->
<!--            :rules="[{type:'required'}]"-->
<!--            v-model="searchKey.startDate"-->
<!--            format="yyyy-MM-dd"-->
<!--            @change="searchChange"-->
<!--          >-->
<!--          </n3-datepicker>-->
<!--        </div>-->
<!--        <div class="form-item">-->
<!--          <label for="">结束时间：</label>-->
<!--          <n3-datepicker-->
<!--            :rules="[{type:'required'}]"-->
<!--            v-model="searchKey.endDate"-->
<!--            format="yyyy-MM-dd"-->
<!--            @change="searchChange"-->
<!--          >-->
<!--          </n3-datepicker>-->
<!--        </div>-->
<!--      </div>-->
      <div class="search-submit">
        <n3-button type="primary" block @click.native="searchRecord">搜索</n3-button>
      </div>
    </div>
    <n3-data-table
      :selection="selection"
      :source="source"
      :columns="columns"
      :filter="false"
      :search="false"
      :page="false"
      :select-col="false"
      :loading="loading"
      responsive
    >
    </n3-data-table>
    <n3-page
      :total="pagination.total"
      :pagesize="pagination.pagesize"
      :show-total="true"
      v-model="pagination.current"
      @change="pageChange"
    >
    </n3-page>
  </section>
</template>
<script>
  import API from '../../api'
  import qs from 'qs'
  import { dateFormat } from '../../utils'

  export default {
    data () {
      return {
        loading: false,
        searchChanged: false,
        searchKey: {
          taskId: '',
          taskState: '',
          startDate: '',
          endDate: ''
        },
        selection: {
          checkRows: [],
          onSelect (record, checked, checkRows) {},
          onSelectAll (checked, checkRows, changeRows) {},
          getCheckboxProps (record) {
            return {
              checked: false,
              disabled: true
            }
          }
        },
        pagination: {
          current: 1,
          total: 0,
          pagesize: 10
        },
        columns: [
          {
            title: 'ID',
            dataIndex: 'taskID',
            width: '50px',
            render: text => text || '无'
          },
          {
            title: '任务名',
            dataIndex: 'taskName',
            width: '200px',
            render: text => text || '无'
          },
          {
            title: '合作方',
            dataIndex: 'partner',
            width: '120px',
            render: text => text || '无'
          },
          {
            title: '最后操作时间',
            dataIndex: 'lastModifyTime',
            width: '160px',
            render: (text, record, index) => {
              return `<div>{{'${text}'}}</div>`
            }
          }, {
            title: '算法类型',
            dataIndex: 'learningType',
            width: '120px',
            render: (text) => {
              if (text === 'VLR') {
                return `纵向逻辑回归`
              }
              if (text === 'VSB') {
                return '纵向SecureBoost'
              }
              return '未知'
            }
          },
          {
            title: '任务状态',
            dataIndex: 'taskState',
            width: '120px',
            render: (text) => {
              if (text === '训练中' || text === '预测中') {
                return `<span style="color: #ff0000;">{{'${text}'}}</span>`
              }
              return `<span style="color: green;">{{'${text}'}}</span>`
            }
          },
          {
            title: '操作',
            dataIndex: 'taskState_ID',
            width: '120px',
            render: (text) => {
              let state = text.split('__')[0]
              let id = text.split('__')[1]
              if (state === '预测完成' || state === '预测中') {
                return `<button style="cursor: hand;background-color: transparent; border: 0;"
                            @click = "toPredictInfo('${id}')">
                          <n3-label type="primary">查看详情</n3-label>
                       </button>`
              }
              if (state === '训练中' || state === '训练完成') {
                return `<button style="cursor: hand;background-color: transparent; border: 0;"
                            @click = "toTrainInfo('${id}')">
                          <n3-label type="primary">查看详情</n3-label>
                       </button>`
              }
              return '无'
            }
          }
        ],
        source: []
      }
    },
    methods: {
      toPredictInfo (param) {
        console.log('ppp:', param)
        this.pa = {id: parseInt(param)}
        this.$router.push({name: 'predictinfo', params: this.pa})
      },
      toPredictStart (param) {
        console.log('ppp:', param)
        this.pa = {id: parseInt(param)}
        this.$router.push({name: 'startpredict', params: this.pa})
      },
      toTrainInfo (param) {
        console.log('ppp:', param)
        this.pa = {id: parseInt(param)}
        this.$router.push({name: 'trainInfo', params: this.pa})
      },
      pageChange(page) {
        this.pagination.current = page
        this.searchRecord()
      },
      searchChange () {
        this.searchChanged = true
      },
      searchRecord () {
        if (this.searchChanged) {
          this.pagination.current = 1
          this.searchChanged = false
        }
        let params = Object.assign({}, this.searchKey, {
          page: this.pagination.current
        })
        if (params.queryResult === 1) {
          params.queryResult = true
        }
        if (params.queryResult === 0) {
          params.queryResult = false
        }
        Object.keys(params).forEach(key => {
          let item = params[key]
          if (item === '' || typeof item === 'undefined') {
            delete params[key]
          }
        })
        let url = API.RECORD_LIST
        if (Object.keys(params).length < 2) {
          url = API.QUERY_LIST
        }
        url = 'http://127.0.0.1:5000/tasklist'
        console.log(Object.keys(params))
        this.loading = true
        console.log(params)
        this.$http.get(url, {
          params
        }).then(data => {
          console.log(data)
          this.source = data.result.data || []
          console.log(this.source)
          this.pagination.total = data.result.total || 0
          console.log(this.pagination.total)
          this.loading = false
        }).catch(error => {
          this.loading = false
          this.n3Alert({
            content: error || '加载失败，请刷新试试~',
            type: 'danger',
            placement: 'top-right',
            duration: 2000,
            width: '240px' // 内容不确定，建议设置width
          })
        })
      },
      reload () {
        this.pagination.current = 1
        this.searchRecord()
      }
    },
    watch: {
      '$route' () {
        if (this.$route.name === 'taskTable') {
          this.reload()
        }
      }
    },
    created () {
      this.reload()
    }
  }
</script>

<style lang="less">
  @import "../../style/define.less";
  .history-list {
    td a {
      color: @primaryColor;
    }
  }
</style>

