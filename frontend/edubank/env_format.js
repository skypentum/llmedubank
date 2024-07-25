// 환경 변수 정의
var local_env = {
    apiUrl: "Your LOCALHOST API URL"
};

var ops_env = {
    apiUrl: "Your Remote API URL"
};

var env = {}

// 환경 변수를 외부에서 사용할 수 있도록 export
if(window.location.hostname == 'localhost' || window.location.hostname == '127.0.0.1')
    env = local_env;
else
    env = ops_env;

module.exports = env;