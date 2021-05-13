<template>
  <div>
    <el-row :gutter="15">
      <el-form ref="elForm" :model="formData" :rules="rules" size="medium" label-width="100px" label-position="left">
        <el-col :span="10">
          <el-form-item label="任务ID" prop="taskID">
            <el-input v-model="formData.taskID" placeholder="任务ID" readonly :style="{width: '100%'}">
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="任务名称" prop="taskname">
            <el-input v-model="formData.taskname" placeholder="任务名称" readonly :style="{width: '100%'}">
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="项目名称" prop="projectname">
            <el-input v-model="formData.projectname" placeholder="项目名称" readonly :style="{width: '100%'}">
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="模型名称" prop="modelname">
            <el-input v-model="formData.modelname" placeholder="模型名称" readonly :style="{width: '100%'}">
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="机器学习算法" prop="MLA">
            <el-input v-model="formData.MLA" placeholder="机器学习算法" readonly :style="{width: '100%'}">
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="对齐字段" prop="alianfeature">
            <el-input v-model="formData.alianfeature" placeholder="对齐字段" readonly :style="{width: '100%'}">
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="创建时间" prop="createtime">
            <el-input v-model="formData.createtime" placeholder="创建时间" readonly :style="{width: '100%'}">
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="最后操作时间" prop="lastmodify">
            <el-input v-model="formData.lastmodify" placeholder="最后操作时间" readonly :style="{width: '100%'}">
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="我方IP:端口" prop="userIPPort">
            <el-input v-model="formData.userIPPort" placeholder="我方IP:端口" readonly :style="{width: '100%'}">
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="对方IP:端口" prop="partnerIPPort">
            <el-input v-model="formData.partnerIPPort" placeholder="对方IP:端口" readonly
                      :style="{width: '100%'}"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="数据集描述" prop="datainfo">
            <el-input v-model="formData.datainfo" placeholder="数据集描述" readonly :style="{width: '100%'}">
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="训练集比例" prop="trainratio">
            <el-input v-model="formData.trainratio" placeholder="训练集比例" readonly :style="{width: '100%'}">
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="KS" prop="ks">
            <el-input v-model="formData.ks" placeholder="KS" readonly :style="{width: '100%'}">
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="AUC" prop="auc">
            <el-input v-model="formData.auc" placeholder="AUC" readonly :style="{width: '100%'}">
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="文件结果地址" prop="fileloc">
            <el-input v-model="formData.fileloc" placeholder="文件结果地址" readonly :style="{width: '100%'}">
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="数据库地址" prop="dbloc">
            <el-input v-model="formData.dbloc" placeholder="数据库地址" readonly :style="{width: '100%'}">
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="20">
          <el-row type="flex" justify="left" align="middle">
            <el-form-item label="阶段进度"></el-form-item>
            <el-steps :active="milepostActive">
              <el-step v-for="(value, key) in milepost"
                       :class="milepostActive== key+1 ? stepActive: allstep "
                       :title="value.title"
                       :description="value.description">
              </el-step>
            </el-steps>
          </el-row>
        </el-col>
        <el-col :span="11">
          <el-form-item label="详细进度">
            <el-input v-model="info" type="textarea" placeholder="等待详细信息" autofocus="autofocus"
                      :autosize="{minRows: 10, maxRows:15}" :style="{width: '150%'}" ></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="20">
          <el-row type="flex" justify="center">
            <el-form-item size="large">
              <el-button type="primary" @click="toPredict">发起预测</el-button>
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
              <el-button @click="backToTable">返回列表</el-button>
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            </el-form-item>
          </el-row>
        </el-col>
      </el-form>
    </el-row>
  </div>
</template>

<script>
import API from '../../api'
import axios from 'axios'
import {dateFormat} from "../../utils";

export default {
  components: {},
  props: [],
  data () {
    return {
      formData: {
        taskID: '',
        taskname: '',
        projectname: '',
        modelname: '',
        MLA: '',
        alianfeature: '',
        createtime: '',
        lastmodify: '',
        userIPPort: '',
        partnerIP: '',
        partnerIPPort: '',
        partnerPort: '',
        datainfo: '',
        trainratio: '',
        fileloc: '',
        ks: '',
        auc: '',
        dbloc: '',
        feature: '',
        progress: 3
      },
      rules: {},
      featureOptions: [{
        'label': '选项一',
        'value': 1
      }, {
        'label': '选项二',
        'value': 2
      }, {
        'label': '',
        'value': ''
      }],
      info: '',
      // 数组对象
      milepost: [
        // eslint-disable-next-line no-useless-escape
        {title: '测试连接', description: '\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003'},
        {title: '对齐', description: '\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003'},
        {title: '预处理', description: '\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003'},
        {title: '训练', description: '\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003'},
        {title: '保存结果', description: '\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003'},
        {title: '验证', description: '\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003'},
        {title: '完成', description: '\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003\u2003'},
      ],
      // 默认步骤数
      milepostActive: 1,
      // 动态添加类名
      stepActive: 'stepActive',
      allstep: 'allStep'
    }
  },
  computed: {},
  methods: {
    reload () {
      this.id = this.$route.params.id
      console.log(this.id)
      if (this.id === undefined) {
        this.formData.taskID = '暂时无法支持直接输入ID'
        this.formData.taskname = '请从任务列表选择进入'
      }
      axios.post(API.TRAIN_INFO, this.id)
        .then(response => {
          console.log(response.data)
          this.formData = response.data
          return response
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    toPredict () {
      console.log('data =', this.formData)
      this.$router.push({name: 'startpredict',
        params: {model_name: this.formData.modelname,
          MLA: this.formData.MLA,
          ip: this.formData.partnerIP,
          port: this.formData.partnerPort,
          partnername: this.formData.partnername}})
    },
    resetForm () {
      this.$refs['elForm'].resetFields()
    },
    backToTable () {
      this.$router.push('/overall/task')
    },
    updateInfo () {
      console.log('data =', this.formData)
      // eslint-disable-next-line eqeqeq
      if (this.formData.taskID !== undefined) {
        axios.post(API.TRAIN_DETAIL, this.formData.taskID)
          .then(data => {
            console.log(data)
            this.milepostActive = data.data.step
            console.log(this.milepostActive)
            this.info = data.data.detail
            console.log(this.info)
          })
      }
    }
  },
  watch: {
    '$route' () {
      if (this.timer) { // 如果定时器还在运行 或者直接关闭，不用判断
        clearInterval(this.timer) // 关闭
      }
      if (['trainForm'].indexOf(this.$route.name) > -1) {
        this.reload()
        this.updateInfo()
      }
      if (this.$route.params.id !== this.formData.id) {
        this.reload()
        this.updateInfo()
        this.timer = setInterval(() => {
          this.updateInfo()
        }, 10000)
      }
    }
  },
  mounted () {
    // setInterval(() => {
    //     this.updateInfo()
    // }, 10000)
  },
  created () {
    this.reload()
    this.updateInfo()
    this.timer = setInterval(() => {
      this.updateInfo()
    }, 10000)
  }
}

</script>

<style lang="scss">
.el-step.is-horizontal.stepActive{

  .el-step__head.is-finish{
    .el-step__line{
      // 当前步骤数横线样式设置
      .el-step__line-inner{
        width: 100% !important;
        border-width: 0 !important;

      }
      background: transparent;
      border-top: 5px dotted;
    }
    // 当前步骤数圆圈样式设置
    .el-step__icon.is-text{
      background: #409eff;
      color:#fff;
    }
  }
}
.allStep{
  .el-step__head.is-finish{
    .el-step__line{
      // 当前步骤数横线样式设置
      .el-step__line-inner{
        width: 100% !important;
        border-width: 1px !important;
      }
    }
    // 当前步骤数圆圈样式设置
    .el-step__icon.is-text{
      background: #409eff;
      color:#fff;
    }
  }
}
</style>
