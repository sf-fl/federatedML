<template>
  <div>
    <el-row :gutter="15">
      <el-form ref="elForm" :model="formData" :rules="rules" size="medium" label-width="100px">
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
          <el-form-item label="文件地址" prop="fileloc">
            <el-input v-model="formData.fileloc" placeholder="文件地址" readonly :style="{width: '100%'}">
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="数据库地址" prop="dbloc">
            <el-input v-model="formData.dbloc" placeholder="数据库地址" readonly :style="{width: '100%'}">
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="19">
          <el-form-item label="下拉选择" prop="feature">
            <el-select v-model="formData.feature" placeholder="请选择下拉选择" filterable clearable
                       :style="{width: '100%'}">
              <el-option v-for="(item, index) in featureOptions" :key="index" :label="item.label"
                         :value="item.value" :disabled="item.disabled"></el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="24">
          <el-form-item size="large">
            <el-button placeholder="formData.feature" type="primary" @click="submitForm">{{formData.feature}}</el-button>
            <el-button @click="resetForm">返回</el-button>
          </el-form-item>
        </el-col>
      </el-form>
    </el-row>
  </div>
</template>
<script>
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
        partnerIPPort: '',
        datainfo: '',
        trainratio: '',
        fileloc: '',
        dbloc: '',
        feature: ''
      },
      rules: {
        taskID: [{
          pattern: /^1(3|4|5|7|8|9)\d{9}$/,
          message: '手机号格式错误',
          trigger: 'blur'
        }],
        taskname: [{
          pattern: /^1(3|4|5|7|8|9)\d{9}$/,
          message: '手机号格式错误',
          trigger: 'blur'
        }],
        projectname: [{
          pattern: /^1(3|4|5|7|8|9)\d{9}$/,
          message: '手机号格式错误',
          trigger: 'blur'
        }],
        modelname: [{
          pattern: /^1(3|4|5|7|8|9)\d{9}$/,
          message: '手机号格式错误',
          trigger: 'blur'
        }],
        MLA: [{
          pattern: /^1(3|4|5|7|8|9)\d{9}$/,
          message: '手机号格式错误',
          trigger: 'blur'
        }],
        alianfeature: [{
          pattern: /^1(3|4|5|7|8|9)\d{9}$/,
          message: '手机号格式错误',
          trigger: 'blur'
        }],
        createtime: [{
          pattern: /^1(3|4|5|7|8|9)\d{9}$/,
          message: '手机号格式错误',
          trigger: 'blur'
        }],
        lastmodify: [{
          pattern: /^1(3|4|5|7|8|9)\d{9}$/,
          message: '手机号格式错误',
          trigger: 'blur'
        }],
        userIPPort: [{
          pattern: /^1(3|4|5|7|8|9)\d{9}$/,
          message: '手机号格式错误',
          trigger: 'blur'
        }],
        partnerIPPort: [{
          pattern: /^1(3|4|5|7|8|9)\d{9}$/,
          message: '手机号格式错误',
          trigger: 'blur'
        }],
        datainfo: [{
          pattern: /^1(3|4|5|7|8|9)\d{9}$/,
          message: '手机号格式错误',
          trigger: 'blur'
        }],
        trainratio: [{
          pattern: /^1(3|4|5|7|8|9)\d{9}$/,
          message: '手机号格式错误',
          trigger: 'blur'
        }],
        fileloc: [{
          pattern: /^1(3|4|5|7|8|9)\d{9}$/,
          message: '手机号格式错误',
          trigger: 'blur'
        }],
        dbloc: [{
          pattern: /^1(3|4|5|7|8|9)\d{9}$/,
          message: '手机号格式错误',
          trigger: 'blur'
        }],
        feature: [{
          required: true,
          message: '请选择下拉选择',
          trigger: 'change'
        }]
      },
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
    }
  },
  computed: {},
  watch: {},
  created () {},
  mounted () {},
  methods: {
    submitForm () {
      this.$refs['elForm'].validate(valid => {
        if (!valid) return
        // TODO 提交表单
      })
    },
    resetForm () {
      this.$refs['elForm'].resetFields()
    },
  }
}

</script>
<style>
</style>
