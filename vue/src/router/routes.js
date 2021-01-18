import Login from '../views/login'
import CommonLayout from '../layout'

import NormalForm from '../views/form'
import TrainForm from '../views/trainform'
import NormalTable from '../views/table'
import ProjectForm from '../views/projectform'

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
    path: '/table',
    icon: 'table',
    name: 'table',
    component: CommonLayout,
    redirect: '/table/',
    meta: {
      label: '总览'
    },
    children: [
      {
        path: '/table/',
        component: NormalTable,
        name: 'normalTable',
        meta: {
          label: '项目管理'
        }
      },
      {
        path: '/table/',
        component: NormalTable,
        name: 'normalTable',
        meta: {
          label: '任务管理'
        }
      },
      {
        path: '/table/',
        component: NormalTable,
        name: 'normalTable',
        meta: {
          label: '申请管理'
        }
      }
    ]
  },
  // Form View
  {
    path: '/projectform',
    name: 'form',
    icon: 'bars',
    component: CommonLayout,
    redirect: '/project/',
    meta: {
      label: '项目管理'
    },
    children: [
      {
        path: '/project/info',
        component: ProjectForm,
        name: 'projectForm',
        meta: {
          label: '项目详情'
        }
      }
    ]
  },
  {
    path: '/trainform',
    name: 'form',
    icon: 'bars',
    component: CommonLayout,
    redirect: '/train/',
    meta: {
      label: '训练管理'
    },
    children: [
      {
        path: '/train/start',
        component: TrainForm,
        name: 'trainForm',
        meta: {
          label: '发起训练'
        }
      },
      {
        path: '/train/info',
        component: TrainForm,
        name: 'trainForm',
        meta: {
          label: '训练详情'
        }
      }
    ]
  },
  {
    path: '/form',
    name: 'form',
    icon: 'bars',
    component: CommonLayout,
    redirect: '/predict/',
    meta: {
      label: '预测管理'
    },
    children: [
      {
        path: '/predict/start',
        component: NormalForm,
        name: 'normalForm',
        meta: {
          label: '预测详情'
        }
      },
      {
        path: '/predict/info',
        component: NormalForm,
        name: 'normalForm',
        meta: {
          label: '发起预测'
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
