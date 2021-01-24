import Login from '../views/login'
import CommonLayout from '../layout'

import NormalForm from '../views/form'
import NormalTable from '../views/table'

import TrainFormStart from '../views/trainform/train_start'
import TrainFormAppend from '../views/trainform/train_receive'
import TrainInfo from '../views/trainform/train_info'

import ProjectFormStart from '../views/projectform/pro_start'
import ProjectFormReceive from '../views/projectform/pro_receive'

import PredictFormStart from '../views/predictform/pre_start'
import PredictFormAppend from '../views/predictform/pre_receive'
import PredictInfo from '../views/predictform/pre_info'

import TaskTable from '../views/tasktable/task_table'
import ApplyTable from '../views/applytable/apply_table'


const routes = [
  // Login View
  {
    path: '/login',
    component: Login,
    name: 'login',
    menu: false
  },
  // Normal View
  {
    path: '/test',
    // 异步载入组件
    component: function (resolve, reject) {
      require.ensure([], function (require) {
        let comm = require('../views/test/query')
        resolve(comm)
      })
    },
    name: 'testQuery',
    menu: false,  // 禁止在导航(navbar / levelbar)中显示
    meta: {
      auth: false // 无需登录校验
    }
  },
  // Table View
  {
    path: '/overall',
    icon: 'table',
    name: 'table',
    component: CommonLayout,
    redirect: '/overall/',
    meta: {
      label: '总览'
    },
    children: [
      {
        path: '/overall/',
        component: NormalTable,
        name: 'normalTable',
        meta: {
          label: '项目列表(禁用）'
        }
      },
      {
        path: '/overall/task',
        component: TaskTable,
        name: 'taskTable',
        meta: {
          label: '任务列表'
        }
      },
      {
        path: '/overall/apply',
        component: ApplyTable,
        name: 'applyTable',
        meta: {
          label: '申请列表'
        }
      }
    ]
  },
  // Form View
  {
    path: '/projectform',
    name: 'projectform',
    icon: 'bars',
    component: CommonLayout,
    redirect: '/project/',
    meta: {
      label: '项目管理'
    },
    children: [
      {
        path: '/project/start',
        component: ProjectFormStart,
        name: 'startproject',
        meta: {
          label: '发起项目（禁用）'
        }
      }
    ]
  },
  {
    path: '/trainform',
    name: 'trainform',
    icon: 'bars',
    component: CommonLayout,
    redirect: '/train/',
    meta: {
      label: '训练管理'
    },
    children: [
      {
        path: '/train/start',
        component: TrainFormStart,
        name: 'starttrain',
        meta: {
          label: '发起训练'
        }
      },
      {
        path: '/train/append',
        component: TrainFormAppend,
        name: 'appendtrain',
        meta: {
          label: '加入训练'
        }
      },
      {
        path: '/train/info',
        component: TrainInfo,
        name: 'trainInfo',
        meta: {
          label: '训练详情'
        }
      }
    ]
  },
  {
    path: '/predictform',
    name: 'predictform',
    icon: 'bars',
    component: CommonLayout,
    redirect: '/predict/',
    meta: {
      label: '预测管理'
    },
    children: [
      {
        path: '/predict/start',
        component: PredictFormStart,
        name: 'startpredict',
        meta: {
          label: '发起预测'
        }
      },
      {
        path: '/predict/append',
        component: PredictFormAppend,
        name: 'appendpredict',
        meta: {
          label: '加入预测'
        }
      },
      {
        path: '/predict/info',
        component: PredictInfo,
        name: 'predictinfo',
        meta: {
          label: '预测详情'
        }
      }
    ]
  },
  {
    path: '*',
    redirect: '/table/'
  }
]

export default routes
