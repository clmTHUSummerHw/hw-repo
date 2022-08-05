export default class LoginResult
{
    code = -1
    session = ""

    static validate(obj: any): obj is LoginResult
    {
        if(typeof obj.code != "number")
            return false;
        if(typeof obj.session != "string")
            return false;
        return true;
    }
}