<template>
    <div id="index-view">
        <div class="login">
            <!--登录页面框-->
            <p class="welcome">欢迎来到Thide! 请登录</p>
            <el-form ref="form" :model="form" :rules="rules" label-width="80px" status-icon>
                <!--表单内容与data中的Form对象绑定 / 验证规则与data中的rules对象绑定 / status-icon属性为显示输入内容是否符合验证规则-->

                <!--为了使验证器生效，每个表单元素中需指定prop-->
                <!--用户名表单元素-->
                <el-form-item label="用户名" prop="username">
                    <el-input placeholder="请输入用户名" v-model="form.username"></el-input>
                </el-form-item>

                <!--密码表单元素-->
                <el-form-item label="密码" prop="password">
                    <el-input placeholder="请输入密码" v-model="form.password" type="password" show-password></el-input>
                    <!--show-password属性在右侧提供调整输入的密码内容隐藏与否的按钮-->
                </el-form-item>

                <!--提交按钮表单元素-->
                <el-form-item>
                    <el-button class="submit" type="primary" @click="submitForm('Form')" round>登录</el-button>
                    <!--round只是设置形状-->
                </el-form-item>
            </el-form>

            <!--底端引导至注册页面的内容-->
            <p>还没有注册？</p>
            <router-link to="/sign-up">点此注册！</router-link>
            <!--href有待修改-->
        </div>
    </div>
</template>

<script lang="ts">
import axios from 'axios';
import { FormInstance } from 'element-plus';
import { defineComponent, ref } from 'vue';
import LoginResult from '@/utils/post-util/LoginResult';

export default defineComponent({
    name: 'indexPage',
    data()
    {
        //自定义用户名输入验证器
        const validateUsername = (_rule: any, value: string, callback: (arg0?: any) => any) =>
        {
            if (!value)
            {
                return callback(new Error("用户名不能为空"))
            }
            else
            {
                let cur_reg = new RegExp("^[a-zA-Z_]"); //匹配字母或下划线的正则表达式
                if (value.length < 2)
                { //输入用户名长度小于2
                    return callback(new Error("用户名长度至少应为2个字符"));
                }
                else if (value.length > 16)
                { //输入用户名长度大于16
                    return callback(new Error("用户名长度至多为16个字符"));
                }
                else if (!(cur_reg.test(value))) //输入用户名不是字母开头或下划线
                {
                    return callback(new Error('用户名的第一个字符应为字母'));
                }
                else
                    callback();
            }
        };

        //自定义密码输入验证器
        const validatePassword = (_rule: any, value: string, callback: (arg0?: any) => any) =>
        {
            if (!value)
            { //检查密码是否为空
                return callback(new Error("密码不能为空"))
            }
            else
            {
                callback();
            }
        };

        return {
            form: { // 用户名、密码表单提交内容
                username: "",
                password: ""
            },

            rules: { //给每个Form对象元素设置自定义的验证器函数
                username: [
                    { validator: validateUsername, trigger: 'blur' }
                ],
                password: [
                    { validator: validatePassword, trigger: 'blur' }
                ]
            }
        };
    },
    methods: {
        async submitForm(formName: string)
        {
            let form: FormInstance = this.$refs['form'] as FormInstance;
            let valid = await form.validate();

            if (!valid)
            {
                alert('用户名或密码输入有误!'); //无法通过验证则弹窗
                //TODO: 可以考虑改为更精美的弹窗
                return;
            }

            try
            {
                let result = await axios.post('/user/login', JSON.stringify(this.form));
                if (LoginResult.validate(result))
                {
                    console.log(JSON.stringify(result)); //TODO: 处理请求结果
                }
                else
                {
                    console.log(JSON.stringify(result)); //TODO: 处理特殊异常（一般应该不会出现，可简单处理）
                }
            }
            catch (e)
            {
                console.log(e); //TODO: 处理error情况
                return;
            }
        }
    }
})
</script>

<style lang="scss">
#index-view
{
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

    .login
    {
        /* 包含登录表单的框 */
        width: 300px;
        height: 300px;

        padding-top: 20px;
        padding-left: 20px;
        padding-right: 20px;

        margin: auto;
        /* 左右居中 */
        position: relative;
        top: 20%;
        /* 再适当调整垂直位置 */

        background-color: rgb(234, 234, 234);

        border-radius: 10px;
        box-shadow: 1px 0 10px rgb(0 0 0 / 10%);
    }

    .welcome
    {
        /* 顶端welcome句 */
        font-weight: bold;
    }

    .submit
    {
        /* 调整提交按钮大小 */
        width: 100px;
    }

    .el-form-item
    {
        /* 调整表单元素位置 */
        margin-top: 20px;

        label
        {
            /* 调整表单元素label字面的位置 */
            justify-content: space-around;
        }
    }
}
</style>