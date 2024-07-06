module.exports = {
    // publicPath: "/", //根路径  Vue CLI 3.3 前使用 baseUrl
    outputDir: "dist1", //构建输出目录
    assetsDir: "assets", //静态资源目录
    lintOnSave: false, //是否开启eslint保存检测
    runtimeCompiler: true,
    publicPath: "/", // 设置打包文件相对路径
    devServer: {
        open: true, //配置自动启动浏览器
        https: false,
        hotOnly: false, //热更新
        port: 8080,
        // 配置跨域-请求后端的接口
        proxy: {
            '/api': {
                target: 'http://localhost:8088', //对应自己的接口
                changeOrigin: true,
                async: false,
                headers: {
                    crossDomain: true,
                    // 'Content-Type': 'application/x-www-form-urlencoded'
                },
                pathRewrite: {
                    '^/api': ''
                }
            },
            '/file_api': {
                target: 'http://localhost:8089', //对应文件实体抽取的接口
                changeOrigin: true,
                async: false,
                headers: {
                    crossDomain: true,
                    'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryNOwrfQfAncKahlbj'
                },
                pathRewrite: {
                    '^/file_api': ''
                }
            },
            '/file_c_api': {
                target: 'http://localhost:8090', //对应文件分类的接口
                changeOrigin: true,
                async: false,
                headers: {
                    crossDomain: true,
                    'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryNOwrfQfAncKahlbj'
                },
                pathRewrite: {
                    '^/file_c_api': ''
                }
            },
            '/login_api': {
                target: 'http://localhost:8093', //对应login接口
                changeOrigin: true,
                async: false,
                headers: {
                    crossDomain: true,
                },
                pathRewrite: {
                    '^/login_api': ''
                }
            },
            '/pay_api': {
                target: 'http://localhost:8091', //对应pay接口
                changeOrigin: true,
                async: false,
                headers: {
                    crossDomain: true,
                },
                pathRewrite: {
                    '^/pay_api': ''
                }
            },
            '/user_api': {
                target: 'http://localhost:8093/', //对应UserStart接口
                changeOrigin: true,
                async: false,
                headers:
                    {
                        crossDomain: true,
                        'Content-Type':
                            'application/x-www-form-urlencoded'
                    },
                pathRewrite: {
                    '^/user_api': '/'
                }
            },
            '/notify_api': {
                target: 'http://localhost:8092/', //对应notify接口
                changeOrigin: true,
                async: false,
                headers:
                    {
                        crossDomain: true,
                        'Content-Type':
                            'application/x-www-form-urlencoded'
                    },
                pathRewrite: {
                    '^/notify_api': '/'
                }
            },
            '/socket_api': {
                target: 'http://localhost:8094/', //对应socket接口
                changeOrigin: true,
                async: false,
                headers:
                    {
                        crossDomain: true,
                        'Content-Type':
                            'application/x-www-form-urlencoded'
                    },
                pathRewrite: {
                    '^/socket_api': '/'
                }
            },
            '/coupon_api': {
                target: 'http://localhost:8095/', //对应coupon接口
                changeOrigin: true,
                async: false,
                headers:
                    {
                        crossDomain: true,
                        'Content-Type': 'application/json'

                    },
                pathRewrite: {
                    '^/coupon_api': '/'
                }
            },
            '/feedback_api': {
                target: 'http://localhost:8096/', //对应feedback接口
                changeOrigin: true,
                async: false,
                headers:
                    {
                        crossDomain: true,

                    },
                pathRewrite: {
                    '^/feedback_api': '/'
                }
            },
        },
    }
}