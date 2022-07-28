<template>
  <div id="BOX_LOGIN"> <!--登录页面框-->
    <p id="PARA_WELCOME">欢迎来到Thide! 请登录</p>
    <el-form ref="Form" 
    :model="Form"
    :rules="rules" 
    label-width="80px" 
    status-icon>
    <!--表单内容与data中的Form对象绑定 / 验证规则与data中的rules对象绑定 / status-icon属性为显示输入内容是否符合验证规则-->
    
    <!--为了使验证器生效，每个表单元素中需指定prop-->
    <!--用户名表单元素-->
      <el-form-item label="用户名" prop="username">
        <el-input placeholder="请输入用户名" v-model="Form.username"></el-input>
      </el-form-item>

    <!--密码表单元素-->
      <el-form-item label="密码" prop="password">
        <el-input placeholder="请输入密码" v-model="Form.password" type="password" show-password></el-input>
        <!--show-password属性在右侧提供调整输入的密码内容隐藏与否的按钮-->
      </el-form-item>

    <!--提交按钮表单元素-->
      <el-form-item>
        <el-button id="BUTTON_SUBMIT" type="primary" @click="submitForm('Form')" round>登录</el-button>
        <!--round只是设置形状-->
      </el-form-item>
    </el-form>

    <!--底端引导至注册页面的内容-->
    <p>还没有注册？</p>
    <el-link href="/signUp">点此注册!</el-link>
    <!--href有待修改-->
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'indexPage',
  data() {
    //自定义用户名输入验证器
    let validateUsername = (rule, value, callback) => {
      if (!value) {
        return callback(new Error("用户名不能为空"))
      }
      else
      {
        let cur_input = this.Form.username;
        let cur_reg = new RegExp("^[a-zA-Z_]"); //匹配字母或下划线的正则表达式
        if (this.Form.username.length < 2) { //输入用户名长度小于2
          return callback(new Error("用户名长度至少应为2个字符"))
        }
        else if (this.Form.username.length > 16) { //输入用户名长度大于16
          return callback(new Error("用户名长度至多为16个字符"))
        }
        else if (!(cur_reg.test(cur_input))) //输入用户名不是字母开头或下划线
        {
          return callback(new Error('用户名的第一个字符应为字母'))
        }
        else
          callback();
      }
    };

    //自定义密码输入验证器
    let validatePassword = (rule, value, callback) => {
      if (!value) { //检查密码是否为空
        return callback(new Error("密码不能为空"))
      }
      else
      {
        callback();
      }
    };

    return {
      Form: { // 用户名、密码表单提交内容
        username: "", 
        password: ""
      },
      
      rules: { //给每个Form对象元素设置自定义的验证器函数
        username: [
          { validator: validateUsername, trigger: 'blur'}
        ],
        password: [
          { validator: validatePassword, trigger: 'blur'}
        ]
      }
    };
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid)
        {
          let currentForm = {
            username: this.username,
            password: this.password
          };
          let currentFormJson = JSON.stringify(currentForm);
          //验证通过，打包成JSON格式以POST至后端

          axios.post('/user/login', currentFormJson)
          .then((res) => {
            console.log(res.code);
            console.log(res.session); // todo: 处理code和session
          })
          .catch((err) => { 
            console.log(err); //todo: 处理error情况
          });
        }
        else 
        {
          alert("用户名或密码输入有误!"); //无法通过验证则弹窗
          //可以考虑改为更精美的弹窗
          return false;
        }
      });
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  /* 以上为默认设置 */

  box-sizing: border-box;
  width: 100%;
  height: 800px;

  background-color: white;
  background-image: url(@/assets/small_logo_bg.png);
}

#BOX_LOGIN { /* 包含登录表单的框 */
  width: 300px;
  height: 300px;

  padding-top: 20px;
  padding-left: 20px;
  padding-right: 20px;

  margin: auto; /* 左右居中 */
  position: relative;
  top: 20%; /* 再适当调整垂直位置 */

  background-color: rgb(234, 234, 234);

  border-radius: 10px;
  box-shadow: 1px 0 10px rgb(0 0 0 / 10%);
}

#PARA_WELCOME { /* 顶端welcome句 */
  font-weight: bold;
}

.el-form-item { /* 调整表单元素位置 */
  margin-top: 20px;
}

.el-form-item label { /* 调整表单元素label字面的位置 */
  justify-content: space-around
}

#BUTTON_SUBMIT { /* 调整提交按钮大小 */
  width: 100px;
}
</style>
