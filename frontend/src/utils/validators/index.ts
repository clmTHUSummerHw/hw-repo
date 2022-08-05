//自定义用户名输入验证器
export const validateUsername = (_rule: any, value: string, callback: (arg0?: any) => any) =>
{
    if (!value)
    {
        return callback(new Error("用户名不能为空"))
    }
    else
    {
        const cur_reg = new RegExp("^[a-zA-Z_]"); //匹配字母或下划线的正则表达式
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
export const validatePassword = (_rule: any, value: string, callback: (arg0?: any) => any) =>
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

//自定义二次密码输入验证器
export const validatePasswordCheck = (form: { username: string; password: string; passwordCheck: string; }) =>
{
    return (_rule: any, value: string, callback: (arg0?: any) => any) =>
    {
        if (value === '')
        {
            callback(new Error('请再次输入密码'));
        }
        else if (value !== form.password) //与已输入密码不一致
        {
            callback(new Error('两次输入密码不一致!'));
        }
        else
        {
            callback();
        }
    };
}