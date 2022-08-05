<template>
    <div id="sign-up-view">
        <div class="sign-up">
            <!--注册页面框-->
            <p id="welcome">欢迎来到Thide! 请注册你的账号</p>

            <el-form ref="form" :model="form" :rules="rules" label-width="80px" status-icon>
                <!--
                    设置ref，方便获取DOM元素 / 表单内容与data中的form对象绑定 / 验证规则与data中的rules对象绑定 /
                    tatus-icon属性为显示输入内容是否符合验证规则
                -->

                <!--用户名输入-->
                <el-form-item label="用户名" prop="username">
                    <el-input placeholder="请输入用户名" v-model="form.username"></el-input>
                </el-form-item>

                <!--密码输入-->
                <el-form-item label="密码" prop="password">
                    <el-input placeholder="请输入密码" v-model="form.password" type="password" show-password></el-input>
                </el-form-item>

                <!--二次密码输入-->
                <el-form-item label="确认密码" prop="passwordCheck">
                    <el-input placeholder="请再次输入密码" v-model="form.passwordCheck" type="password" show-password>
                    </el-input>
                </el-form-item>

                <!--按钮区-->
                <el-form-item>
                    <el-button class="submit" type="primary" @click="submitForm" round>注册</el-button>
                    <!--注册按钮，验证表单内容并调用发送函数-->
                    <el-button class="submit" type="primary" @click="resetForm" round>重置</el-button>
                    <!--重置按钮，将表单内容和目前的验证结果重置为空-->
                </el-form-item>
            </el-form>

            <p>已有账号?</p>
            <el-link href="/index">点此登录!</el-link>
            <!--href有待修改-->
        </div>
    </div>
</template>

<script lang="ts">
import axios from 'axios';
import { defineComponent } from 'vue';
import { validateUsername, validatePassword, validatePasswordCheck } from '@/utils/validators';
import { FormInstance } from 'element-plus';
import RegisterResult from '@/utils/post-util/RegisterResult';

export default defineComponent({
    name: 'signUp',
    data()
    {
        return {
            form: { /* 用户名、密码表单提交内容 */
                username: "",
                password: "",
                passwordCheck: ""
            },
        };
    },

    computed:
    {
        rules() //给每个Form对象元素设置自定义的验证器函数
        {
            return {
                username: [
                    { validator: validateUsername, trigger: 'blur' }
                ],
                password: [
                    { validator: validatePassword, trigger: 'blur' }
                ],
                passwordCheck: [
                    { validator: validatePasswordCheck(this.form), trigger: 'blur' }
                ]
            }
        }
    },

    methods:
    {
        //点击注册按钮，验证表单并提交
        async submitForm()
        {
            let form = this.$refs['form'] as FormInstance;
            let valid = await form.validate();

            if (!valid)
            {
                alert("输入有误！"); //无法通过验证则弹窗警告
                //TODO: 可以考虑改成更精美的弹窗警告
                return;
            }

            try
            {
                let result = await axios.post('/user/register', JSON.stringify(this.form)) as RegisterResult;
                //TODO: 处理请求结果
                return;
            }
            catch (e)
            {
                console.log(e); //TODO: 处理error
                return;
            }
        },

        //点击重置按钮，重置表单内容
        resetForm()
        {
            let form = this.$refs['form'] as FormInstance;
            form.resetFields();
        }
    }
})
</script>

<style lang="scss">
#sign-up-view
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

    .sign-up
    {
        /* 包含登录表单的框 */
        width: 300px;
        height: 350px;

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

    .el-form-item
    {
        /* 调整表单元素位置 */
        margin-top: 20px;
    }

    .submit
    {
        width: 100px;
    }
}
</style>