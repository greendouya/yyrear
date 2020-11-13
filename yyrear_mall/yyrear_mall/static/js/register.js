let vm = new Vue({
    el: '#app', // 通过id选择器找到绑定的html内容
    // 修改Vue读取变量的语法
    delimiters: ['[[', ']]'],
    data: { // 数据对象
        // v-model
        username: '',
        password: '',
        password2: '',
        mobile: '',
        allow: '',

        // v-show
        error_name: false,
        error_password: false,
        error_password2: false,
        error_mobile: false,
        error_allow: false,

        // error_message
        error_name_message: '',
        error_mobile_message: ''
    },
    methods: {   // 定义和实现事件方法
        // 校验用户名
        check_username() {
            let re = /^[a-zA-Z0-9_-]{5,20}$/
            if (re.test(this.username)) {
                this.error_name = false
            } else {
                this.error_name_message = '请输入5-20个字符的用户名'
                this.error_name = true
            }

            // 判断用户名是否重复注册
            if (this.error_name == false) { // 只有当用户输入的用户名满足条件时才回去判断
                let url = '/usernames/' + this.username + '/count/'
                axios.get(url, {
                    responseType: 'json'
                }).then(response => {
                    if (response.data.count == 1){
                        // 用户名已存在
                        this.error_name_message = '用户名已存在'
                        this.error_name = true
                    } else {
                        // 用户名不存在
                        this.error_name = false
                    }

                }).catch(error => {
                    console.log(error.response)
                })
            }
        },
        // 校验密码
        check_password() {
            let re = /^[0-9A-Za-z]{8,20}$/
            if (re.test(this.password)) {
                this.error_password = false
            } else {
                this.error_password = true
            }
        },
        // 校验确认密码
        check_password2() {
            if (this.password != this.password2) {
                this.error_password2 = true;
            } else {
                this.error_password2 = false;
            }
        },
        // 校验手机号
        check_mobile() {
            let re = /^1[3-9]\d{9}$/;
            if(re.test(this.mobile)) {
                this.error_mobile = false;
            } else {
                this.error_mobile_message = '您输入的手机号格式不正确';
                this.error_mobile = true;
            }
        },
        // 校验是否候选协议
        check_allow() {
            if(!this.allow) {
                this.error_allow = true;
            } else {
                this.error_allow = false;
            }
        },
        // 监听表单提交事件
        on_submit() {
            this.check_username();
            this.check_password();
            this.check_password2();
            this.check_mobile();
            this.check_allow();

            if(this.error_name == true || this.error_password == true || this.error_password2 == true
            || this.error_mobile == true || this.error_allow == true) {
                // 禁用表单的提交
                Event.returnValue = false;
            }
        },
    }
});