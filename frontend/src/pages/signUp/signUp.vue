<template>
  <div id="BOX_SIGNUP"> <!--注册页面框-->
    <p id="PARA_WELCOME">欢迎来到Thide! 请注册你的账号</p>

    <el-form 
    ref="Form" 
    :model="Form" 
    :rules="rules" 
    label-width="80px" 
    status-icon>
    <!--
      设置ref，方便获取DOM元素 / 表单内容与data中的Form对象绑定 / 验证规则与data中的rules对象绑定 / 
      tatus-icon属性为显示输入内容是否符合验证规则
    -->

    <!--用户名输入-->
      <el-form-item label="用户名" prop="username">
        <el-input placeholder="请输入用户名" v-model="Form.username"></el-input>
      </el-form-item>

    <!--密码输入-->
      <el-form-item label="密码" prop="password">
        <el-input placeholder="请输入密码" v-model="Form.password" type="password" show-password></el-input>
      </el-form-item>

    <!--二次密码输入-->
      <el-form-item label="确认密码" prop="passwordCheck">
        <el-input placeholder="请再次输入密码" v-model="Form.passwordCheck" type="password" show-password></el-input>
      </el-form-item>

      <!--按钮区-->
      <el-form-item>
        <el-button class="BUTTON_SUBMIT" type="primary" @click="submitForm('Form')" round>注册</el-button>
        <!--注册按钮，验证表单内容并调用发送函数-->
        <el-button class="BUTTON_SUBMIT" type="primary" @click="resetForm('Form')" round>重置</el-button>
        <!--重置按钮，将表单内容和目前的验证结果重置为空-->
      </el-form-item>
    </el-form>

    <p>已有账号?</p>
    <el-link href="/index">点此登录!</el-link>
    <!--href有待修改-->
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'signUp',
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
    }

    //自定义密码输入验证器
    let validatePassword = (rule, value, callback) => {
      if (!value) {
        return callback(new Error("密码不能为空"))
      }
      else
      {
        if (this.Form.passwordCheck !== '') 
        {
          this.$refs.Form.validateField('passwordCheck'); //去做二次密码输入的检查
        }
        callback();
      }
    };

    //自定义二次密码输入验证器
    let validatePasswordCheck = (rule, value, callback) => {
      if (value === '')
      {
        callback(new Error('请再次输入密码'));
      }
      else if (value !== this.Form.password) //与已输入密码不一致
      {
        callback(new Error('两次输入密码不一致!'));
      }
      else 
      {
        callback();
      }
    };

    return {
      Form: { /* 用户名、密码表单提交内容 */
        username: "", 
        password: "",
        passwordCheck: ""
      },
      
      rules: { //给每个Form对象元素设置自定义的验证器函数
        username: [
          { validator: validateUsername, trigger: 'blur' }
        ],
        password: [
          { validator: validatePassword, trigger: 'blur'  }
        ],
        passwordCheck: [
          { validator: validatePasswordCheck, trigger: 'blur' }
        ]
      }
    };
  },
  methods: {
    submitForm(formName) { //点击注册按钮，验证表单并提交
      this.$refs[formName].validate((valid) => {
        if (valid) //验证通过
        {
          let currentForm = { //提取用户名、密码
            username: this.username,
            password: this.password
          }
          let currentFormJson = JSON.stringify(currentForm)
          //验证通过，打包成JSON格式以POST至后端

          axios.post('/user/register', currentFormJson)
          .then((res) => {
            console.log(res.code);
            console.log(res.session); // todo: 处理code和session
          })
          .catch((err) => { 
            console.log(err); //todo: 处理error
          });
        }
        else 
        {
          alert("输入有误！"); //无法通过验证则弹窗警告
          //可以考虑改成更精美的弹窗警告
          return false;
        }
      });
    },
    resetForm(formName) { //点击重置按钮，重置表单内容
      this.$refs[formName].resetFields();
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

#BOX_SIGNUP { /* 包含登录表单的框 */
  width: 300px;
  height: 350px;

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

.BUTTON_SUBMIT {
  width: 100px;
  
  
}
</style>
